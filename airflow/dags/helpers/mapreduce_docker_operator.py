from datetime import datetime
import time

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
from airflow import DAG


mapreduce_defaults = {
    'map': 'IdentityMapper',
    'reduce': 'IdentityReducer',
    'shuffle_directory': 's3://mapreduce-jobs/',
}


def conf_or_default_template(name, default):
    return '{{dag_run.conf.get("' + name + '") or "' + default + '"}}'


def mapreduce_docker_operator(dag, **kwargs):
    user = kwargs.get('user', 'mr-user')
    name = kwargs.get('name', 'mr-job')
    jobid = name + '-' + str(int(time.time()))
    config = conf_or_default_template('config', '')
    mapper = conf_or_default_template('map', kwargs.get('map', mapreduce_defaults['map']))
    reducer = conf_or_default_template('reduce', kwargs.get('reduce', mapreduce_defaults['reduce']))
    input_paths = conf_or_default_template('input_paths', kwargs.get('input_paths', ''))
    output_path = conf_or_default_template('output_path', kwargs.get('output_path', ''))
    output_shards = conf_or_default_template('output_shards', kwargs.get('output_shards', '1'))
    shuffle_directory = conf_or_default_template('shuffle_directory', kwargs.get('shuffle_directory', ''))
    num_workers = kwargs.get('num_workers', 1)

    job_args = '--jobid ' + jobid + ' --map ' + mapper + ' --reduce ' + reducer + ' --numWorkers ' + str(num_workers) + ' --shuffleDirectory ' + shuffle_directory + ' ' + config + ' '
    input_args = '--inputPaths ' + input_paths + ' '
    output_args = '--outputPath ' + output_path + ' --outputShards ' + output_shards + ' '

    begin_operator = DummyOperator(task_id='mapreduce_begin')
    complete_operator = DummyOperator(task_id='mapreduce_complete')
    operators = [ begin_operator ]

    for i in range(num_workers):
        ecs_operator = DockerOperator(
            dag=dag,
            do_xcom_push=True,
            auto_remove=True,
            image='wholebuzz/mapreduce',
            task_id=kwargs.get('task_id', 'mapreduce') + '-' + str(i),
            environment={
                # 'AWS_REGION': '',
                # 'AWS_ACCESS_KEY_ID': '',
                # 'AWS_SECRET_ACCESS_KEY': '',
                'RUN_ARGS': job_args + input_args + output_args + kwargs.get('extra_args', '') + ' --workerIndex ' + str(i),
            },
        )
        operators.append(ecs_operator)
        begin_operator >> ecs_operator >> complete_operator

    operators.append(complete_operator)
    return operators
