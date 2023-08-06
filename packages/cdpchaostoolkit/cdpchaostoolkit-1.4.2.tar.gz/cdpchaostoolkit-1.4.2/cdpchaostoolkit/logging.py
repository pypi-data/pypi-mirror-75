# -*- coding: utf-8 -*-
import logging
import uuid
import logging.handlers
import logzero
import sys
from logzero import logger, LogFormatter, setup_default_logger
from pythonjsonlogger import jsonlogger
# from splunk_hec_handler import SplunkHecHandler
from cdpchaostoolkit import encoder

__all__ = ["configure_logger"]


class ChaosToolkitContextFilter(logging.Filter):
    def __init__(self, name: str = '', context_id: str = None):
        logging.Filter.__init__(self, name)
        self.context_id = context_id or str(uuid.uuid4())

    def filter(self, record: logging.LogRecord) -> bool:
        record.context_id = self.context_id
        return True


def configure_logger(verbose: bool = False, log_format: str = "string",
                     log_file: str = None, logger_name: str = "cdpchaos",
                     context_id: str = None):
    """
    Configure the cdpchaostoolkit logger.

    By default logs as strings to stdout and the given file. When `log_format`
    is `"json"`, records are set to the console as JSON strings but remain
    as strings in the log file. The rationale is that the log file is mostly
    for grepping purpose while records written to the console can be forwarded
    out of band to anywhere else.
    """
    log_level = logging.INFO
    splunk_log = True
    fmt = "%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s"
    if verbose:
        log_level = logging.DEBUG
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"

    formatter = LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    if log_format == 'json':
        fmt = "(process) (asctime) (levelname) (module) (lineno) (message)"
        if context_id:
            fmt = "(context_id) {}".format(fmt)
        formatter = jsonlogger.JsonFormatter(
            fmt, json_default=encoder, timestamp=True)

    # sadly, no other way to specify the name of the default logger publicly
    LOGZERO_DEFAULT_LOGGER = "cdpchaos"
    logger = setup_default_logger(level=log_level, formatter=formatter)
    if context_id:
        logger.addFilter(ChaosToolkitContextFilter(logger_name, context_id))

    # if splunk_log:
    #     #SplunkHandler
    #     token = '1ccffb85-2220-4875-99fb-18278491f341'
    #     hec_handler_host = "hwf2.splunk.aws.vz-connect.net"
    #     fmt = "[%(asctime)s : %(levelname)-5s: %(filename)s:%(lineno)s - %(name)8s:%(funcName)-12s] %(message)s"
    #     splunk_formatter = logging.Formatter(fmt)
    #     splunk_handler = SplunkHecHandler(hec_handler_host, token, index='ops_sbx_app', port=8088, proto='https', ssl_verify=False, source='cdpchaos')
    #     splunk_handler.setFormatter(splunk_formatter)
    #     splunk_handler.setLevel(logging.INFO)
    #     logger.addHandler(splunk_handler)

    if log_file:
        # always everything as strings in the log file
        logger.setLevel(logging.DEBUG)
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"
        formatter = LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
        logzero.logfile(log_file, formatter=formatter, mode='a',
                        loglevel=logging.DEBUG)
