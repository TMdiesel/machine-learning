# default package
import logging
import pathlib

# third party package
import numpy as np
import pandas as pd
import mlflow
import hydra
from sklearn.linear_model import LogisticRegression

# my package
from src.model.runner import Runner
import src.feature.base as base
import src.utils.utils as utils 

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@hydra.main(config_path="../../config/model",config_name="config.yaml")
def main(config):
    cwd=pathlib.Path(hydra.utils.get_original_cwd())

    utils.init_root_logger(
        cwd.joinpath(config.log_dir),
        config.log_normal,
        config.log_error,
        )

    feats = config.feat_list
    ld=base.load_datasets(save_dir=cwd.joinpath(config.feature_dir))
    ftrain, ftest = ld.load_datasets(feats)
    ytrain=pd.read_csv(cwd.joinpath(config.train_path))["Survived"].values

    model=LogisticRegression()

    runner = Runner(
        run_name=config.run_name,
        model=model,
        ftrain=ftrain,
        ftest=ftest,
        ytrain=ytrain,
        random_seed=config.random_seed,
        n_fold=config.n_fold,
    )
    runner.run_cv()


if __name__ == '__main__':
    main()

