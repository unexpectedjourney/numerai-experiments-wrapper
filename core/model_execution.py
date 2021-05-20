import pandas as pd
import uuid


async def execute_model(message_params):
    task_id = message_params.get('task_id')
    model_id = message_params.get('model_id')
    model_params = message_params.get('model_params')
    action = message_params.get('action')

    filename = f"{uuid.uuid4().hex}.csv"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(filename)

    return filename, task_id
