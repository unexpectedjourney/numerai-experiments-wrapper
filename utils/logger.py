import logging
FORMAT = ('[%(levelname)s]\t [%(asctime)s]\t '
          '[%(module)s:%(funcName)s:%(lineno)d]\t -\t %(message)s')


def setup_logger(name):
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    log = logging.getLogger(name)
    return log


