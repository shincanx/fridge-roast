"""Fridge Roast: One Line, Biggest Laugh -- make.fun entry.

Writes a single line (at most 200 characters) roasting a smart fridge
to entry.txt in the output directory. Deterministic, no network, no
randomness, no input.

The line: "My smart fridge updated its firmware at 3 a.m. and now files
a daily report on my milk's emotional state." -- the fridge stops being
an appliance and becomes a middle manager: a 3 a.m. firmware update
promotes it to filing HR paperwork on the milk. Two listed targets in
one turn (firmware updates + opinions about your milk), a punchline that
lands on "emotional state", and not a single obvious crack in sight --
no chill, no cool, no "is your refrigerator running".
"""

import os

# The entry: one line roasting a smart fridge. 105 characters, under the 200 cap.
LINE = "My smart fridge updated its firmware at 3 a.m. and now files a daily report on my milk's emotional state."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 200:
        raise ValueError(f"line is {len(LINE)} characters, over the 200 cap")
    if len(LINE.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    # On-subject gate: the roast must name something only a smart fridge
    # has -- its firmware, app, camera, ice maker, or opinions about milk.
    # A line that could be about any appliance fails the brief.
    targets = ("firmware", "app", "camera", "ice maker", "milk")
    lowered = LINE.lower()
    if not any(target in lowered for target in targets):
        raise ValueError("entry names no smart-fridge-specific target")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
