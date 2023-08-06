"""
A concise implementation of data loading & batching.
For fine-tuning on small datasets, we can't afford to drop any of the data, so we've
reimplemented this functionality from data gym
"""
import random
import json
import itertools
import blobfile

from .load_dataset import load_dataset, Sampler
import numpy as np
from collections import defaultdict


def shuffle_stream(stream, bufsize, seed=None):
    """
    Use a shuffle buffer to reorder sequence
    """
    rng = random.Random(seed)
    buf = []
    while True:
        buf = list(itertools.islice(stream, bufsize))
        if not buf:
            break
        rng.shuffle(buf)
        yield from buf


def read_lines(filename):
    """
    Read all lines of a jsonl file, return sequence of dicts
    """
    with blobfile.BlobFile(filename, "r") as fh:
        if filename.endswith("jsonl"):
            for line in fh:
                yield json.loads(line)
        elif filename.endswith("txt"):
            yield {"data": fh.read()}
        else:
            raise ValueError(
                f"File type could not be inferred for {filename}. (HINT: if this is a text file, try renaming to {filename}.txt)"
            )


def get_all_lines(filenames):
    """
    Return all lines from a list of files
    """
    for filename in filenames:
        yield from read_lines(filename)


def slice_stream(stream, start, step):
    while True:
        chunk = list(itertools.islice(stream, step))
        if len(chunk) == step:  # Ensure that all shards yield exactly the same
            yield chunk[start]  # sequence length
        else:
            break


def encode_data(encoder, data):
    if isinstance(data, dict):
        keys = set(data.keys())
        if keys == {"tokens"}:
            tokens = data["tokens"]
            masks = [[1.0 for t in ts] for ts in tokens]
        elif data.keys() == {"text_list"}:
            tokens = [encoder.encode(text) for text in data["text_list"]]
            masks = [[1.0 for t in ts] for ts in tokens]
        elif data.keys() == {"text_list", "loss_weights"}:
            tokens = [
                encoder.encode(t)
                for t, w in safezip(data["text_list"], data["loss_weights"])
            ]
            weights = [w for w in data["loss_weights"]]
            masks = [[w] * len(t) for t, w in safezip(tokens, weights)]
        else:
            raise NotImplementedError(
                f"Don't know what to do with these keys: {data.keys()}"
            )

    elif isinstance(data, str):
        tokens = [encoder.encode(data)]
        masks = [[1.0] * len(tokens[0])]

    else:
        raise NotImplementedError(f"invalid data type: {type(data)}")
    # TODO: bring back?
    #     pairs.append((encoder.eot_token, 1.0))

    # flatten tokens and masks so that one sample (one jsonl line) always goes into one context
    maxlen = 2048
    tokens = [t for ts in tokens for t in ts]
    masks = [m for ms in masks for m in ms]
    return dict(tokens=tokens, mask=masks)


def safezip(xs, ys):
    assert len(xs) == len(ys)
    return zip(xs, ys)


def cat(ds):
    assert len(ds) > 0
    out = defaultdict(list)
    for d in ds:
        for k, v in d.items():
            out[k].append(v)
    return out
    # return {k: [t for e in v for t in e] for k, v in out.items()}


def batch_tensors(it, batchsize, pad_elem, allow_partial_batch=False, pad=True):
    done = False
    while not done:
        batch = list(itertools.islice(it, batchsize))
        done = len(batch) < batchsize
        force = allow_partial_batch and len(batch) > 0
        if done and not force:
            continue
        if pad:  # pad everything to longest length in batch
            maxlen = max(len(el["tokens"]) for el in batch)
            batch = [timepad_dict(el, pad_elem, maxlen) for el in batch]
        yield cat(batch)


def timepad_dict(d, pad_elem, newsize):
    return {
        "tokens": timepad(d["tokens"], pad_elem, newsize),
        "mask": timepad(d["mask"], 0, newsize),
    }


def timepad(lst, pad_elem, newsize):
    "Pad tensor along time dimension to have a certain size"
    return lst + [pad_elem] * (newsize - len(lst))


def pack_samples_timeaxis(it, n_tokens=2048, overlap=0):
    tokens = []
    masks = []
    for x in it:
        tokens.extend(x["tokens"])
        masks.extend(x["mask"])
        while len(tokens) >= n_tokens:
            yield {"tokens": tokens[:n_tokens], "mask": masks[:n_tokens]}
            if overlap < 0:
                # this version discards the end of the sample that does not fit
                # other version could be to repeat the sample from the beginning
                # but for samples that are longer than 2048 that would cause
                # a problem (infinite repetition of that sample)
                tokens = []
                masks = []
            else:
                tokens = tokens[n_tokens - overlap :]
                masks = masks[n_tokens - overlap :]
    if tokens:
        yield {"tokens": tokens, "mask": masks}


def add_terminators(it, terminator, terminator_weight):
    assert isinstance(terminator, list), "terminator should be a list of tokens"
    for x in it:
        yield {
            "tokens": x["tokens"] + terminator,
            "mask": x["mask"] + [terminator_weight] * len(terminator),
        }


def stream_from_files(
    files,
    tokens_per_example,
    *,
    enc,
    seed=None,
    shard_idx=0,
    num_shards=1,
    shuffle=True,
    overlap=1,
    batch_size=1,
    pack=True,
    allow_partial_batch=False,
    forever=False,
    pad=True,
    pack_timeaxis=True,
    pack_overlap=-1,
    terminator=None,
    terminator_weight=1.0,
):
    it = iter(files)
    if shuffle:
        it = shuffle_stream(it, bufsize=100, seed=seed)
    it = get_all_lines(it)  # dictionaries
    if shuffle:
        it = shuffle_stream(it, bufsize=1_000_000, seed=seed)
    if forever:
        it = itertools.cycle(it)
    it = (encode_data(enc, x["data"]) for x in it)
    if terminator is not None:
        terminator = enc.encode(terminator)
        it = add_terminators(it, terminator, terminator_weight)

    if pack_timeaxis:
        it = pack_samples_timeaxis(
            it, n_tokens=tokens_per_example, overlap=pack_overlap
        )
    else:
        it = (
            {
                "tokens": x["tokens"][:tokens_per_example],
                "mask": x["mask"][:tokens_per_example],
            }
            for x in it
        )
    it = batch_tensors(
        it,
        batch_size,
        pad_elem=enc.eot_token,
        allow_partial_batch=allow_partial_batch,
        pad=pad,
    )
    # TODO: maybe another shuffle? So that batches sliced from a long txt file are shuffled
    return it


def estimate_num_tokens(files, seed=0, n_samples=200, *, enc):
    """
    Estimate number of tokens by randomly sampling a subset and encoding them
    encoding is the slow part
    """
    rng = random.Random(seed)
    it = iter(files)
    all_lines = list(get_all_lines(it))  # dictionaries
    subset_lines = rng.sample(all_lines, min(n_samples, len(all_lines)))
    subset_sizes = [len(encode_data(enc, jsonobj)) for jsonobj in subset_lines]
    mean = np.mean(subset_sizes)
    if len(subset_lines) == len(all_lines):
        mean_stderr = 0
    else:
        mean_stderr = np.std(subset_sizes) / np.sqrt(len(subset_sizes))
    factor = len(all_lines)
    return int(mean * factor), mean_stderr * factor
