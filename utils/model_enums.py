from enum import IntEnum


class ModelName(IntEnum):
    LINEAR_REGRESSION = 1
    ELASTIC_NET = 2
    LASSO = 3
    RIDGE = 4


class ModelAction(IntEnum):
    TRAIN = 1
    TUNE_PARAMS = 2
    PREDICT_AND_SCORE = 3
    SUBMIT = 4
