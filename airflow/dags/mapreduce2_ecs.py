from datetime import datetime
from json import loads

from airflow.operators.dummy import DummyOperator
from airflow import DAG

from helpers.mapreduce import mapreduce_ecs_operator

with DAG(
    dag_id="mapreduce2_ecs",
    schedule_interval=None,
    start_date=datetime(2021, 9, 30),
    tags=["ecs", "mapreduce"],
    catchup=False,
    user_defined_filters={'fromjson': lambda s: loads(s)},
) as dag:

    mapreduce_tasks = mapreduce_ecs_operator(dag, num_workers=2)
    success = DummyOperator(task_id='mapreduce_success')
    failure = DummyOperator(task_id='mapreduce_failure')

    mapreduce_tasks[-1] >> [success, failure]
