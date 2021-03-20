# default package
import logging
import pathlib
import time
from contextlib import contextmanager

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@contextmanager
def timer(name):
    t0 = time.time()
    logger.info(f'[{name}] start')
    yield
    logger.info(f'[{name}] done in {time.time() - t0:.0f} s')


def init_root_logger(
    outdir: pathlib.Path,
    filename_normal:str="normal.log",
    filename_error:str="error.log",
    ):

    outdir.mkdir(exist_ok=True)
    logging.getLogger().addHandler(
        _add_handler(outdir,logging.INFO,filename_normal))
    logging.getLogger().addHandler(
        _add_handler(outdir,logging.ERROR,filename_error))


def _add_handler(
    outdir:pathlib.Path,
    level,
    filename
    ):

    fh = logging.FileHandler(outdir/filename)
    fh.setLevel(level)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)
    return fh
