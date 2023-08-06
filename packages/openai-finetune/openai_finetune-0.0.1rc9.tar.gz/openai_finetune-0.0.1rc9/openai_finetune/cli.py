import argparse
import json
import logging
import os
import sys
import tempfile
from datetime import datetime

import openai
from . import train
from .planner import Planner, SyncPlanner
from openai import error

from .event_logger import log_event

# logger = logging.getLogger(__name__)
logger = logging.getLogger("openai_finetune.cli")
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)


def verify_files_exist(urls):
    # TODO
    pass


def finetune(args):
    train_paths = args.train.split(",")
    val_paths = args.val.split(",") if args.val else []
    verify_files_exist(train_paths + val_paths)

    hps = train.FinetuningHps(
        train_paths=train_paths,
        val_paths=val_paths,
        update_scale=args.scale,
        max_tokens=args.max_tokens,
        num_epochs=args.num_epochs,
        train_batch_size=args.batch_size,
        val_batch_size=args.val_batch_size,
        completions_every=args.completions_every,
        num_completions=args.num_completions,
        completion_temperature=args.completion_temperature,
        completion_tokens=args.completion_tokens,
        completion_prompt=args.completion_prompt,
        snapshots_every=args.snapshots_every,
        pack_timeaxis=args.pack_timeaxis,
        pack_overlap=args.pack_overlap,
        terminator=args.terminator,
        terminator_weight=args.terminator_weight,
    )

    if args.engine:
        finetune_sync(args, hps)
    else:
        raise NotImplementedError("Batch mode fine-tuning is not enabled yet")
        finetune_async(args, hps)


def finetune_sync(args, hps):
    logger.info(f"Preparing fine-tuning run on engine={args.engine} model={args.model}")
    planner = SyncPlanner(engine=args.engine, model=args.model, encoding=args.encoding)
    train.train(planner=planner, hps=hps)
    planner.close()


def finetune_async(args, hps):
    run = finetune_batch_job(
        hps,
        model=args.model,
        create_plan=args.plan,
        plan_output_file=args.output,
        plan_description=args.description,
        encoding=args.encoding,
    )
    if run is not None:
        if args.stream:
            logger.info(
                f"Waiting on progress. Resume any time: openai api events.list -r {run.id} -s"
            )
            # streaming back results with simple pretty-printing
            for event in openai.Event.list(run=run.id, stream=True):
                log_event(event, run)
        else:
            logger.info(
                f"You can monitor its progress: openai api events.list -r {run.id} -s"
            )


def finetune_batch_job(
    hps,
    *,
    model=None,
    create_plan=True,
    plan_output_file=None,
    plan_description=None,
    encoding="byte-pair-encoding-v0",
):
    create_run = create_plan and model

    if not create_plan and plan_output_file is None:
        logger.info(
            "Must save to a local path by passing -o <file> if you are not going to create a plan."
        )
        return

    logger.info(f"Fine-tuning model {model} with hps {hps}")
    planner = Planner(encoding=encoding, output=plan_output_file)
    if plan_output_file is None:
        logger.info(
            f"Building plan in tempfile: {planner.file.name} (pass -o <file> to save to disk)."
        )
    else:
        logger.info(
            f"Building plan in {planner.file.name} and will output to {plan_output_file}"
        )

    logger.info(
        f"Building fine-tuning plan. Each line will have at most {hps.max_tokens} tokens, "
        + f"each training batch will have {hps.train_batch_size} examples, "
        + f"and each validation batch will have at most {hps.val_batch_size} examples"
    )
    train.train(
        planner=planner, hps=hps,
    )

    try:
        if create_plan:
            logger.info(f"Uploading file to create plan object...")
            planner.file.seek(0)
            file = openai.File.create(purpose="plan", file=planner.file)
            plan = openai.Plan.create(
                description=plan_description or "Plan from openai fine-tune",
                file=file.id,
            )
            logger.info(f"Plan created: {plan}")
        else:
            plan = None
    finally:
        planner.close()
    if plan_output_file:
        logger.info(f"Plan contents are available in {plan_output_file}")

    if create_run:
        run = openai.Run.create(model=model, plan=plan.id)
        logger.info(f"Started run on {model}: {run}")
    elif create_plan:
        logger.info(
            f"You can now start any number of runs with your plan. For example, run this to fine-tune ada: openai api runs.create -p {plan.id} -s ada"
        )
    else:
        logger.info(
            f"You can now upload your file to create a plan, and then use that to create any number of runs. For example, run this to make a plan: openai api plans.create -f {plan_output_file}"
        )

    return run if create_run else None


def add_finetuning_args(sub):
    sub.add_argument(
        "-t", "--train", help="Comma-separated list of files to train on", required=True
    )
    sub.add_argument("--val", help="Comma-separated list of files to evaluate on")
    sub.add_argument("--log-path", help="Directory to write logs to")
    sub.add_argument(
        "--num-epochs",
        default=1,
        type=int,
        help="The number of epochs to run over training set.",
    )
    sub.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="How many examples to have in each step.",
    )
    sub.add_argument(
        "--val-batch-size",
        type=int,
        default=50,
        help="How many examples to have in each val step.",
    )
    sub.add_argument(
        "-s",
        "--scale",
        type=float,
        help="How much to scale the update size by",
        default=1,
    )
    sub.add_argument(
        "--max-tokens",
        type=int,
        help="Set the max number of tokens in each training example",
        default=2048,
    )
    sub.add_argument(
        "--encoding",
        help="Set the encoding used in this plan",
        default="byte-pair-encoding-v0",
    )
    sub.add_argument(
        "--completions-every",
        help="Generate completions every COMPLETIONS_EVERY fine-tuning steps. Use -1 to not generate completions throughout training. Default: %(default)s",
        type=int,
        default=100,
    )
    sub.add_argument(
        "--num-completions",
        help="Generatate this many completions each time completions are generated. Default: %(default)s",
        type=int,
        default=5,
    )
    sub.add_argument(
        "--completion-tokens",
        help="Generatate this many tokens per completion. Default: %(default)s",
        type=int,
        default=128,
    )
    sub.add_argument(
        "--completion-temperature",
        help="Generatate this many tokens per completion. Default: %(default)s",
        type=float,
        default=0.4,
    )
    sub.add_argument(
        "--completion-prompt", help="Prompt for completions", type=str, default=""
    )
    sub.add_argument(
        "--snapshots-every",
        help="Save snapshots every SNAPSHOTS_EVERY fine-tuning steps. Default: %(default)s",
        type=int,
        default=100,
    )

    # API options
    sub.add_argument("--output", help="Save fine-tuning file to a local path")
    sub.add_argument("-d", "--description", help="A description for the Plan")
    sub.add_argument(
        "-P",
        "--no-plan",
        dest="plan",
        default=True,
        action="store_false",
        help="Do not upload the file and create a Plan object",
    )
    sub.add_argument("-m", "--model", help="What model to run with")
    sub.add_argument(
        "-e", "--engine", help="What engine to run with (will run synchronously)"
    )
    # sub.add_argument(
    #     "--no-stream",
    #     dest="stream",
    #     action="store_false",
    #     help="Whether to stream back results",
    # )
    sub.add_argument(
        "--no-pack-timeaxis",
        dest="pack_timeaxis",
        action="store_false",
        default=True,
        help="Disable packing multple samples into the time axis (enabled by default). "
        "Packing into timeaxis allows batch size to be roughly constant (which helps "
        "optimization, and makes use of hardware more efficiently). "
        "Disable only when you have a strong reason to.",
    )

    sub.add_argument(
        "--pack-overlap",
        default=-1,
        type=int,
        help="When packing timeaxis, this parameter determines what to do with the samples "
        "that did not fit into the context. When 0 or above, the next sample in the "
        "minibatch will start `overlap` prior to where previous sample ended. "
        "When negative, the cut-off part of the sample will be discarded (default). "
        "Positive values are useful when dealing with strings longer than max context size - "
        "these strings will be sliced with overlap.",
    )
    sub.add_argument(
        "--terminator",
        default="<|endoftext|>",
        help="Add this to the end of the sample. Needed when generating completions of varying length. "
        "Do not use for classification etc when completion has a fixed length, or when terminator tokens "
        " are explicitly present in the data. Set to '' to disable. Default: %(default)s",
    )

    sub.add_argument(
        "--terminator-weight",
        default=1.0,
        type=float,
        help="Loss weight of the terminator (see explanation for --terminator). Default: %(default)s",
    )
    sub.set_defaults(func=finetune)


def add_openai_args(parser):
    parser.add_argument("-b", "--api-base", help="What API base url to use.")
    parser.add_argument("-k", "--api-key", help="What API key to use.")
    parser.add_argument(
        "-o",
        "--organization",
        help="Which organization to run as (will use your default organization if not specified)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Set verbosity.",
    )


def configure_openai(args):
    if args.api_key is not None:
        openai.api_key = args.api_key
    if args.api_base is not None:
        openai.api_base = args.api_base
    if args.organization is not None:
        openai.organization = args.organization
    openai.max_network_retries = 5

    if args.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    logging.getLogger("openai_finetune").setLevel(
        min(logging.WARN, logger.getEffectiveLevel())
    )
    logging.getLogger("openai").setLevel(min(logging.WARN, logger.getEffectiveLevel()))


def main():
    parser = argparse.ArgumentParser()
    add_openai_args(parser)
    add_finetuning_args(parser)
    args = parser.parse_args()
    configure_openai(args)
    finetune(args)


if __name__ == "__main__":
    main()
