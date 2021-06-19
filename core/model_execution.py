import sys
import pandas as pd
import uuid
from pathlib import Path

sys.path.append("numerai/")
from src.trainer import Trainer


model_mapper = {
    1: "lr",
    2: "e_net",
    3: "lasso",
    4: "ridge",
    5: "xgboost",
    6: "lgboost",
    7: "catboost",
    8: "l_svr",
    9: "svr"
}


async def execute_model(message_params):
    task_id = message_params.get('task_id')
    model_id = message_params.get('model_id')
    # model_params = message_params.get('model_params')
    # action = message_params.get('action')

    dir_path = Path("./data")
    train_file = dir_path / "train.csv"
    test_file = dir_path / "test.csv"
    save_path = Path("./models")
    plot_eras = False

    model_name = model_id
    if model_id in model_mapper:
        model_name = model_mapper[model_id]

    submissions_path = Path("./upload")
    filename = f"upload/{uuid.uuid4().hex}.csv"

    trainer = Trainer(
        train_file,
        test_file,
        submissions_path,
        model_name,
        model_params,
        save_path,
        plot_eras
    )

    if action == 1:
        trainer.train()
    elif action == 2:
        trainer.find_hyperparameters()
    elif action == 3:
        trainer.evaluate()
        trainer.submission_df[["id", "prediction"]].to_csv(
            filename,
            index=False
        )
    else:
        trainer.evaluate_for_submition()
        trainer.submission_df[["id", "prediction"]].to_csv(
            filename,
            index=False
        )

    new_model_params = {}

    return filename, task_id, model_id, new_model_params
