# default package
import re as re
import logging
import inspect
import pathlib

# third party package
import pandas as pd
import numpy as np
import hydra

# my package
from src.feature.base import Feature

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Pclass(Feature):
    def create_features(self):
        self.ftrain['Pclass'] = self.train['Pclass']
        self.ftest['Pclass'] = self.test['Pclass']


class Sex(Feature):
    def create_features(self):
        self.ftrain['Sex'] = self.train['Sex'].replace(['male', 'female'], [0, 1])
        self.ftest['Sex'] = self.test['Sex'].replace(['male', 'female'], [0, 1])


class FamilySize(Feature):
    def create_features(self):
        self.ftrain['FamilySize'] = self.train['Parch'] + self.train['SibSp'] + 1
        self.ftest['FamilySize'] = self.test['Parch'] + self.test['SibSp'] + 1


class Embarked(Feature):
    def create_features(self):
        self.ftrain['Embarked'] = self.train['Embarked'] \
            .fillna(('S')) \
            .map({'S': 0, 'C': 1, 'Q': 2}) \
            .astype(int)
        self.ftest['Embarked'] = self.test['Embarked'] \
            .fillna(('S')) \
            .map({'S': 0, 'C': 1, 'Q': 2}) \
            .astype(int)


class Fare(Feature):
    def create_features(self):
        data = self.train.append(self.test)
        fare_mean = data['Fare'].mean()
        self.ftrain['Fare'] = pd.qcut(
            self.train['Fare'].fillna(fare_mean),
            4,
            labels=False
        )
        self.ftest['Fare'] = pd.qcut(
            self.test['Fare'].fillna(fare_mean),
            4,
            labels=False
        )


class Age(Feature):
    def create_features(self):
        data = self.train.append(self.test)
        age_mean = data['Age'].mean()
        age_std = data['Age'].std()
        self.ftrain['Age'] = pd.qcut(
            self.train['Age'].fillna(
                np.random.randint(age_mean - age_std, age_mean + age_std)
            ),
            5,
            duplicates="drop",
            labels=False,
        )
        self.ftest['Age'] = pd.qcut(
            self.test['Age'].fillna(
                np.random.randint(age_mean - age_std, age_mean + age_std)
            ),
            5,
            duplicates="drop",
            labels=False
        )


class Title(Feature):
    def get_title(self,name):
        title_search = re.search(' ([A-Za-z]+)\.', name)
        if title_search:
            return title_search.group(1)
        return ""

    def create_features(self):
        title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}

        self.train['Title'] = self.train['Name'] \
            .apply(self.get_title) \
            .replace([
                'Lady',
                'Countess',
                'Capt',
                'Col',
                'Don',
                'Dr',
                'Major',
                'Rev',
                'Sir',
                'Jonkheer',
                'Dona'
            ], 'Rare') \
            .replace(['Mlle', 'Ms', 'Mme'], ['Miss', 'Miss', 'Mrs'])
        self.train['Title'] = self.train['Name'].map(title_mapping).fillna(0)
        self.test['Title'] = self.test['Name'] \
            .apply(self.get_title) \
            .replace([
                'Lady',
                'Countess',
                'Capt',
                'Col',
                'Don',
                'Dr',
                'Major',
                'Rev',
                'Sir',
                'Jonkheer',
                'Dona'
            ], 'Rare') \
            .replace(['Mlle', 'Ms', 'Mme'], ['Miss', 'Miss', 'Mrs'])
        self.test['Title'] = self.test['Title'].map(title_mapping).fillna(0)

        self.ftrain['Title'] = self.train['Title']
        self.ftest['Title'] = self.test['Title']


def get_features(namespace,kwargs):
    for _, v in namespace.items():
        if inspect.isclass(v) and issubclass(v, Feature) \
                and not inspect.isabstract(v):
            yield v(**kwargs)


def generate_features(namespace, overwrite, kwargs):
    for f in get_features(namespace,kwargs):
        if f.ftrain_path.exists() and f.ftest_path.exists() and not overwrite:
            logger.info(f"{f.name} was skipped")
        else:
            f.run().save()


@hydra.main(config_path="../../config/feature/",config_name="config.yaml")
def main(config):
    cwd=pathlib.Path(hydra.utils.get_original_cwd())

    train = pd.read_csv(cwd.joinpath(config.train_path))
    test =  pd.read_csv(cwd.joinpath(config.test_path))
    kwargs={
        "train":train,
        "test":test,
        "save_dir":cwd.joinpath(config.save_dir)
        }

    generate_features(globals(),False,kwargs)


if __name__ == '__main__':
    """
    for debug
    """
    main()
