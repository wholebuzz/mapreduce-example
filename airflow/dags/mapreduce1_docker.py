from datetime import datetime
from json import loads

from airflow.operators.dummy import DummyOperator
from airflow import DAG

from helpers.mapreduce_docker_operator import mapreduce_docker_operator

with DAG(
    dag_id="mapreduce1_docker",
    schedule_interval=None,
    start_date=datetime(2021, 9, 30),
    tags=["ecs", "mapreduce"],
    catchup=False,
    user_defined_filters={'fromjson': lambda s: loads(s)},
) as dag:

    mapreduce_tasks = mapreduce_docker_operator(dag, num_workers=1)
    success = DummyOperator(task_id='mapreduce_success', trigger_rule='all_success')
    failure = DummyOperator(task_id='mapreduce_failure', trigger_rule='one_failed')

    mapreduce_tasks[-1] >> [success, failure]
