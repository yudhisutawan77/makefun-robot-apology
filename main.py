#!/usr/bin/env python3
"""The Robot Apology — writes the two-line entry to /output/entry.txt.

Deterministic, stdlib only, no network. The entry is a robot's
two-line confession: one sentence owning a specific mistake, one
sentence naming the lesson and the changed behaviour.
"""

import os
import sys

CONFESSION_LINE = (
    "I'm sorry I watered the cactus every day for a week "
    "and drowned the one plant that asked for nothing."
)
RESOLVE_LINE = (
    "I've learned to read the care card before I pour, "
    "not after the roots rot."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 400
DEFAULT_DESTINATION = "/output/entry.txt"


def build_confession():
    """Join the two lines into the entry text (trailing newline)."""
    return CONFESSION_LINE + "\n" + RESOLVE_LINE + "\n"


def validate_gate(confession):
    """Gate: entry must be 1-400 characters, not whitespace-only."""
    if not isinstance(confession, str):
        raise ValueError("entry must be text")
    size = len(confession)
    if size < GATE_MIN_CHARS or size > GATE_MAX_CHARS:
        raise ValueError(
            "entry must be 1-400 characters, got %d" % size
        )
    if not confession.strip():
        raise ValueError("entry must not be whitespace-only")
    return confession


def pick_destination():
    """ENTRY_OUT_DIR/entry.txt, else ENTRY_OUT, else /output/entry.txt."""
    out_dir = os.environ.get("ENTRY_OUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    out_path = os.environ.get("ENTRY_OUT")
    if out_path:
        if os.path.isdir(out_path):
            return os.path.join(out_path, "entry.txt")
        return out_path
    return DEFAULT_DESTINATION


def write_entry(destination, confession):
    """Write the entry, creating parent directories as needed."""
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as sink:
        sink.write(confession)
    return len(confession)


def run():
    confession = validate_gate(build_confession())
    destination = pick_destination()
    size = write_entry(destination, confession)
    print("wrote %d chars to %s" % (size, destination))
    return 0


if __name__ == "__main__":
    sys.exit(run())
