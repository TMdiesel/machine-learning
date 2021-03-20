# default package
import argparse
import inspect
import re
from abc import ABCMeta, abstractmethod
import pathlib
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
    """
    特徴量管理の基底クラス
    """
    def __init__(self,train=None,test=None,save_dir=None):
        self.name=self.__class__.__name__.lower()
        self.save_dir=save_dir
        self.train=train
        self.test=test
        self.ftrain = pd.DataFrame()
        self.ftest = pd.DataFrame()
        self.ftrain_path = pathlib.Path(self.save_dir) / f'{self.name}_ftrain.ftr'
        self.ftest_path = pathlib.Path(self.save_dir) / f'{self.name}_ftest.ftr'

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


class load_datasets(Feature):
    """
    特徴量を読み込む
    """
    def create_features(self):
        pass

    def load_datasets(self,feats):
        dfs = [pd.read_feather(self.save_dir/f"{feat}_ftrain.ftr") for feat in feats]
        X_train = pd.concat(dfs, axis=1)
        dfs = [pd.read_feather(self.save_dir/f"{feat}_ftest.ftr") for feat in feats]
        X_test = pd.concat(dfs, axis=1)
        return X_train, X_test


if __name__=="__main__":
    """
    for debug
    """
    feats = ['age',"embarked"]
    ld=load_datasets(save_dir=pathlib.Path("./data/feature"))
    X_train, X_test = ld.load_datasets(feats)