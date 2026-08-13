# -*- coding: utf-8 -*-
"""Deployment credentials for the Hostinger VPS, read from the environment.

Nothing secret lives in this repo. Set the variables once per machine and the
deploy scripts pick them up:

    setx NEXTGEN_SSH_PASS "your-password"        (Windows, new shell after)
    export NEXTGEN_SSH_PASS='your-password'      (bash)

Prefer a key over a password — point NEXTGEN_SSH_KEY at a private key file and
the password is not consulted at all:

    setx NEXTGEN_SSH_KEY "%USERPROFILE%\\.ssh\\id_ed25519"

Host and user are not secrets, so they carry defaults and only need setting if
the server moves.
"""
import os

HOST = os.environ.get('NEXTGEN_SSH_HOST', 'srv1046530.hstgr.cloud')
USER = os.environ.get('NEXTGEN_SSH_USER', 'root')
PORT = int(os.environ.get('NEXTGEN_SSH_PORT', '22'))
KEY_FILE = os.environ.get('NEXTGEN_SSH_KEY') or None

FTP_HOST = os.environ.get('NEXTGEN_FTP_HOST', HOST)
FTP_USER = os.environ.get('NEXTGEN_FTP_USER', 'u324089851')

_MISSING = """
Missing {name}.

The deploy credentials are no longer stored in the code. Set the variable and
re-run:

    Windows : setx {name} "your-password"   (then open a new terminal)
    bash    : export {name}='your-password'

Better: set NEXTGEN_SSH_KEY to an SSH private key path and drop passwords
entirely.
"""


def _require(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(_MISSING.format(name=name))
    return value


def ssh_password():
    """The SSH password. Not needed — and not read — when a key is configured."""
    if KEY_FILE:
        return None
    return _require('NEXTGEN_SSH_PASS')


def ftp_password():
    return _require('NEXTGEN_FTP_PASS')


def ssh_connect_kwargs():
    """Keyword arguments for paramiko's SSHClient.connect()."""
    kwargs = {'hostname': HOST, 'port': PORT, 'username': USER, 'timeout': 15}
    if KEY_FILE:
        kwargs['key_filename'] = KEY_FILE
    else:
        kwargs['password'] = ssh_password()
    return kwargs
