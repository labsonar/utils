import os
import typing
import subprocess

def run_process(
    comand: str,
    running_directory: str | None = None,
    on_output: typing.Callable[[str], None] = print,
):
    """ Run a command line in a subprocess, printing the progress

    Args:
        comand (str): command to execute
        running_directory (str, optional): directory where to execute the command.
            Defaults to None (current).
        on_output (Callable[[str], None], optional): callback called for each stdout line.
            Defaults to print.

    Raises:
        RuntimeError: Error detected in the process execution
    """

    process = subprocess.Popen(comand,
                               shell=True,
                               cwd=running_directory,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            on_output(output.strip())

    stderr_output = process.stderr.read()

    if process.returncode != 0:
        error_msg = stderr_output.strip() if stderr_output else "Unknown error"
        raise RuntimeError(f"subprocess failed (Code {process.returncode}): {error_msg}")
