import logging
import os.path as osp
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional
import openai

from .load_dataset import load_dataset, Sampler
from . import data_streams

logger = logging.getLogger(__name__)


@contextmanager
def scoped_log(message):
    tstart = time.time()
    print(f"▕▔ {message}")
    yield
    print(f"▕▁ Done in {time.time()-tstart:.2f} seconds")


@dataclass
class FinetuningHps:
    train_paths: list
    val_paths: list
    num_epochs: int = 1
    train_batch_size: int = 32
    val_batch_size: int = 50
    max_tokens: int = 2048
    update_scale: float = 1.0
    create_plan: bool = True
    plan_output_file: Optional[str] = None
    completions_every: int = 5
    num_completions: int = 1
    completion_tokens: int = 128
    completion_temperature: float = 0.4
    completion_prompt: str = ""
    snapshots_every: int = 100
    pack_timeaxis: bool = True
    pack_overlap: int = -1
    terminator: str = "<|endoftext|>"
    terminator_weight: float = 1.0


def train(planner, hps):
    enc = planner.make_encoding()
    stream_kwargs = dict(
        tokens_per_example=hps.max_tokens,
        enc=enc,
        pack_timeaxis=hps.pack_timeaxis,
        pack_overlap=hps.pack_overlap,
        terminator=hps.terminator,
        terminator_weight=hps.terminator_weight,
    )
    step_idx = 0
    for iepoch in range(hps.num_epochs):
        assert (
            step_idx > 0 or iepoch == 0
        ), "one full epoch over data produced no valid training steps, training is not running! Try decreasing the batch size"
        decayed_scale = hps.update_scale * (1 - iepoch / hps.num_epochs)
        train_it = data_streams.stream_from_files(
            hps.train_paths,
            **stream_kwargs,
            batch_size=hps.train_batch_size,
            seed=iepoch,
            pad=True,
        )
        val_it = (
            data_streams.stream_from_files(
                hps.val_paths,
                **stream_kwargs,
                batch_size=hps.val_batch_size,
                seed=iepoch,
                pad=False,
                forever=True,
            )
            if len(hps.val_paths) > 0
            else None
        )
        with scoped_log(f"Running epoch: {iepoch}"):
            # Post an extra validation batch at the beginning of the epoch
            # to tell logger that validation data is present (if it is present)
            post_val_batch(planner, val_it)
            for batch in train_it:
                if (
                    hps.completions_every > 0
                    and hps.num_completions > 0
                    and step_idx % hps.completions_every == 0
                ):
                    ### Sampling eval
                    planner.add(
                        "POST /v1/completions",
                        n=hps.num_completions,
                        max_tokens=hps.completion_tokens,
                        temperature=hps.completion_temperature,
                        prompt=hps.completion_prompt,
                        echo=True,
                    )

                if (
                    hps.snapshots_every > 0
                    and step_idx > 0
                    and step_idx % hps.snapshots_every == 0
                ):
                    planner.add(
                        "POST /v1/snapshots",
                        description=f"Step {step_idx} of openai-finetune",
                    )
                # Training batch
                # TODO in-epoch update_scale planner, probably cosine
                planner.add(
                    "POST /v1/updates",
                    example=batch["tokens"],
                    mask=batch["mask"],
                    scale=decayed_scale,
                )
                post_val_batch(planner, val_it)
                step_idx += 1
            planner.flush_to()
        planner.add(
            "POST /v1/snapshots",
            description=f"Step {step_idx} (last of the training run) of openai-finetune",
        )
        planner.flush_to()


def post_val_batch(planner, val_it):
    if val_it is not None:
        val_batch = next(val_it)
        planner.add(
            "POST /v1/completions",
            prompt=val_batch["tokens"],
            mask=val_batch["mask"],
            logprobs=0,
            max_tokens=0,
            echo=True,
        )


def save_snapshot(planner, epoch):
    planner.add("POST /v1/snapshots", description=f"Epoch {epoch} of openai-finetune")


def eval_step(planner, batch):
    planner.add(
        "POST /v1/completions",
        prompt=batch["tokens"],
        logprobs=0,
        max_tokens=0,
        echo=True,
    )


def train_epoch(planner, data_iterator, epnum, update_scale):
    toks_done = 0
    tokens = []

    last_update = None
    last_toks = None


def val_epoch(planner, data_iterator):
    for batch in data_iterator:
        eval_step(planner, batch)
