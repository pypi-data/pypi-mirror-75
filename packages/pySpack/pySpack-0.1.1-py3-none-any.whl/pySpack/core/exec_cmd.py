import subprocess
from typing import List


def exec_cmd(program: str, arguments: List) -> subprocess.CompletedProcess:
    return subprocess.run([program, *arguments], capture_output=True)
