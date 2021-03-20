# default package
import argparse
import inspect
import re
from abc import ABCMeta, abstractmethod
from pathlib import Path
import time
from contextlib import contextmanager
import logging

# third party package
import pandas as pd

# my package
import src.utils.utils as utils

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Feature(metaclass=ABCMeta):
    def __init__(self,train,test,save_dir):
        self.name=self.__class__.__name__.lower()
        self.save_dir=save_dir
        self.train=train
        self.test=test
        self.ftrain = pd.DataFrame()
        self.ftest = pd.DataFrame()
        self.ftrain_path = Path(self.save_dir) / f'{self.name}_ftrain.feather'
        self.ftest_path = Path(self.save_dir) / f'{self.name}_ftest.feather'

    def run(self):
        with utils.timer(self.name):
            self.create_features()
        return self

    @abstractmethod
    def create_features(self):
        raise NotImplementedError

    def save(self):
        self.ftrain.to_feather(str(self.ftrain_path))
        self.ftest.to_feather(str(self.ftest_path))

    def load(self):
        self.ftrain = pd.read_feather(str(self.ftrain_path))
        self.ftest = pd.read_feather(str(self.ftest_path))