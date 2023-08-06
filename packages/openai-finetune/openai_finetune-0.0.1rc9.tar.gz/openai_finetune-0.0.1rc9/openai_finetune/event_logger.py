import numpy as np
import time
from datetime import datetime


class EventLogger:
    def __init__(self, run=None):
        self.run = run
        self.updates_after_header = 0
        self.created = time.time()
        self.val_data_present = False
        self.update_data = None
        self.total_tokens = 0
        self.last_update_time = time.time()

    def log_event(self, data, params=None):
        params = params or {}
        if data["object"] == "headers":
            self.log_header(data)
        elif data["object"] == "text_completion":
            if data["choices"][0]["logprobs"] is None:
                self.log_completion(data)
            else:
                mask = params.get("mask")
                if mask is not None:
                    data["mask"] = mask
                self.log_val_batch(data)
        elif data["object"] == "snapshot":
            self.log_snapshot(data)
        elif data["object"] == "update":
            self.log_update_raw(data)
        else:
            raise ValueError(f"Unknown event type: {data['object']}")

    def log_header(self, data):
        print(
            f"{data['created_by']['run']} created from {data['created_by']['plan']} at {datetime.fromtimestamp(data['created'])}"
        )
        self.updates_after_header = 0
        self.total_tokens = 0
        self.created = data["created"]

    def log_completion(self, data):
        print("Completions:")
        for choice in data["choices"]:
            print(f"---\n{choice['text']}")
        self.updates_after_header = 0

    def log_val_batch(self, data):
        self.val_data_present = True
        if self.update_data is not None:
            update_data = self.update_data
            logprobs = [
                token
                for c in data["choices"]
                for token in c["logprobs"]["token_logprobs"][1:]
            ]
            logprobs = np.array(logprobs)
            if data["mask"] is not None:
                mask = np.array([m for masks in data["mask"] for m in masks[1:]])
                logprobs *= mask / mask.mean()
            update_data["val_loss"] = -logprobs.mean()
            update_data["val_data"] = data
            self.log_update(update_data)
        self.update_data = None

    def log_update_raw(self, data):
        data["elapsed"] = data["created"] - self.created
        self.total_tokens += data["tokens"]
        data["total_tokens"] = self.total_tokens
        data["tokens/s"] = data["tokens"] / (time.time() - self.last_update_time)
        self.last_update_time = time.time()
        if self.run is not None:
            # used as a run event reader (not in sync mode finetuning)
            data["plan_line"] = data["created_by"]["lineno"]
            data["completed"] = data["created_by"]["lineno"] / self.run.total_lines
        data["loss"] = -data["loss"]
        if not self.val_data_present:
            # if no val data, print log lines on update
            # otherwise, on val batch so that val loss
            # is measured after train loss
            self.log_update(data)
        self.update_data = data

    def log_update(self, data):
        keys = [
            "elapsed",
            "loss",
            "val_loss",
            "scale",
            "tokens",
            "total_tokens",
            "tokens/s",
        ]
        if "plan_line" in data:
            keys += [
                "plan_line",
                "completed",
            ]
        if self.updates_after_header % 10 == 0:
            print(f"\n{' | '.join([k.rjust(12) for k in keys])}")
        print(" | ".join(fixed_width(data.get(k)) for k in keys))
        self.updates_after_header += 1

    def log_snapshot(self, data):
        print(f"Created snapshot {data['id']}")
        self.updates_after_header = 0


def fixed_width(v, width=12):
    if isinstance(v, float):
        fmt = "{:" + str(width) + ".3g}"
        return fmt.format(v)
    else:
        return "".join([" "] * (width - len(str(v))) + [str(v)])


event_loggers = {}


def log_event(event, run=None, params=None):
    run_id = run.id if run is not None else None
    el = event_loggers.setdefault(run_id, EventLogger(run))
    el.log_event(event, params=params)


def add_update_callback(cb, run=None):
    add_callback("log_update", cb, run)


def add_completion_callback(cb, run=None):
    add_callback("log_completion", cb, run)


def add_callback(method, cb, run=None):
    assert method in ("log_update", "log_completion")
    run_id = run.id if run is not None else None
    el = event_loggers.setdefault(run_id, EventLogger(run))
    old_log_update = getattr(el, method)

    def new_log_update(data):
        old_log_update(data)
        cb(data)

    setattr(el, method, new_log_update)
