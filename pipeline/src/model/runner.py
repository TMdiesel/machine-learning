# default package
import logging
import typing as t

# third party package
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold,cross_val_score
from sklearn.preprocessing import StandardScaler

# my pakcage

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Runner:

    def __init__(
        self, 
        run_name: str, 
        model, 
        ftrain: pd.DataFrame, 
        ftest: pd.DataFrame, 
        ytrain: np.array, 
        random_seed:int,
        client,
        run_id,
        n_fold=5,
        ):

        self.run_name = run_name
        self.model = model
        self.ftrain=ftrain
        self.ftest=ftest
        self.ytrain=ytrain
        self.n_fold = n_fold
        self.random_seed=random_seed
        self.client=client
        self.run_id=run_id

    def _normalize(self,x:np.array,flag_fit):
        if flag_fit:
            self.scaler=StandardScaler()
            self.scaler.fit(x)
        return self.scaler.transform(x)

    def run_cv(self):
        x_train=self._normalize(self.ftrain.values,flag_fit=True)

        # cross validation
        skf = StratifiedKFold(
            n_splits=self.n_fold,
            shuffle=True,
            random_state=self.random_seed,
            )
        score=cross_val_score(self.model,x_train,self.ytrain,
                                    cv=skf,scoring="accuracy")
        logger.info(f"cv_score:{score.mean()}")
        self.client.log_metric(self.run_id,"cv_score",score.mean())

        # train
        self.model.fit(x_train,self.ytrain)

    def predict(self):
        x_test=self._normalize(self.ftest.values,flag_fit=False)
        y_pred=self.model.predict(x_test)
        return y_pred


