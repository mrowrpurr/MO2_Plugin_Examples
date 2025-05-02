#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from typing import List


def main(args: List[str]) -> int:
    exe_path = Path("mob") / "mob.exe"
    if not exe_path.exists():
        print(f"Error: {exe_path} does not exist.", file=sys.stderr)
        return 1

    # Run the exe from within its folder, forwarding all args
    result = subprocess.run(
        [str(exe_path)] + ["-d", "../build"] + args,
        cwd=exe_path.parent,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
