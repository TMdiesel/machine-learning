# default package
import logging
import pathlib
import glob
import os

# third party package
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import hydra
import mlflow
from mlflow.tracking import MlflowClient

# my package
from src.model.runner import Runner
import src.feature.base as base
import src.utils.utils as utils 

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_model(model_name,params):
    model_dict={
        "LogisticRegression":LogisticRegression
    }
    return model_dict[model_name](**params)


@hydra.main(config_path="../../config/model",config_name="config.yaml")
def main(config):
    cwd=pathlib.Path(hydra.utils.get_original_cwd())

    # set mlflow
    client=MlflowClient(tracking_uri=str(cwd.joinpath(config.tracking_uri)))
    try:
        experiment_id = client.create_experiment(config.experiment_name)
    except mlflow.exceptions.MlflowException:
        experiment_id = client.get_experiment_by_name(config.experiment_name).experiment_id
    mlflow_tags={}
    mlflow_tags["mlflow.source.name"]=str(os.path.abspath(__file__)).replace("/",'\\')
    run = client.create_run(experiment_id,tags=mlflow_tags)
    run_id=run.info.run_id
    for key,val in config.items():
        client.log_param(run_id,key,val)

    # logger setting
    utils.init_root_logger(
        cwd.joinpath(config.log_dir),
        config.log_normal,
        config.log_error,
        )

    # read feature
    feats = config.feat_list
    ld=base.load_datasets(save_dir=cwd.joinpath(config.feature_dir))
    ftrain, ftest = ld.load_datasets(feats)
    ytrain=pd.read_csv(cwd.joinpath(config.train_path))["Survived"].values
    model=get_model(config.model_name,config.params)

    # train
    runner = Runner(
        run_name=config.run_name,
        model=model,
        ftrain=ftrain,
        ftest=ftest,
        ytrain=ytrain,
        random_seed=config.random_seed,
        client=client,
        run_id=run_id,
        n_fold=config.n_fold,
    )
    runner.run_cv()

    # save log&config to mlflow
    client.log_artifact(run_id, cwd.joinpath(config.log_dir)/config.log_normal)
    client.log_artifact(run_id, cwd.joinpath(config.log_dir)/config.log_error)
    for yamlfile in glob.glob(".hydra/*.yaml"):
        client.log_artifact(run_id,yamlfile)

if __name__ == '__main__':
    main()

