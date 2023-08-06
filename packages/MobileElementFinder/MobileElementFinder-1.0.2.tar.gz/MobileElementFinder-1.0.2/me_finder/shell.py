"""Functions for calling shell."""
import logging
import os
import pathlib
import shlex
import subprocess

import attr

from .errors import DependencyError, ExitCodeError

LOG = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ShellResult:
    """Container for shell command results."""

    cmd: str
    stdout: str
    stderr: str
    return_code: int


def _stringify_arg(arg):
    """Ensure that argument is a string."""
    if isinstance(arg, (str, int, float, pathlib.Path)):
        return str(arg)
    raise TypeError


def _get_executable_path(executable):
    """Get path to executable."""
    process = subprocess.run(['which', f'{executable}'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    path: str = process.stdout.rstrip()
    if not os.path.isfile(path):
        m = f'{executable} not found'
        logging.error(m)
        raise DependencyError(m)
    return path


def run_shell(*args, check=True):
    """Envoce shell commands.

    Keyword Arguments:
    args -- command line arguments
    """
    args = [_stringify_arg(arg) for arg in args]
    cmd = ' '.join([shlex.quote(arg) for arg in args])

    LOG.info(f'cmd: {cmd}')
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    if check:
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError as e:
            raise ExitCodeError(
                cmd=cmd,
                return_code=e.returncode,
                stderr=e.stderr.decode('utf-8'),
                stdout=e.stdout.decode('utf-8'))

    return ShellResult(
        cmd=cmd,
        stdout=proc.stdout.decode('utf-8'),
        stderr=proc.stderr.decode('utf-8'),
        return_code=proc.returncode)
