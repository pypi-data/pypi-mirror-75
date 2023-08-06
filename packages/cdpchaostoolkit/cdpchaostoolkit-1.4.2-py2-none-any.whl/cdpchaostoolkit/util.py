# -*- coding: utf-8 -*-

import subprocess
import os
import logzero
from logzero import logger

def change_working_directory(path: str = None):
    change_wd = subprocess.run(
        path, timeout=None, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=os.environ, shell=True)

    if change_wd.returncode > 1:
        logger.error(f'Cannot change the current working directory to {path}')
        return
