from datetime import datetime
import time

from airflow.providers.amazon.aws.operators.ecs import ECSOperator
from airflow.operators.dummy import DummyOperator
from airflow import DAG


mapreduce_defaults = {
    'map': 'IdentityMapper',
    'reduce': 'IdentityReducer',
    'shuffle_directory': 's3://mapreduce-jobs/',
    'cpu': '256',
    'memory': '512',
}


def conf_or_default_template(name, default):
    return '{{dag_run.conf.get("' + name + '") or "' + default + '"}}'


def mapreduce_ecs_operator(dag, **kwargs):
    user = kwargs.get('user', 'mr-user')
    name = kwargs.get('name', 'mr-job')
    jobid = name + '-' + str(int(time.time()))
    config = conf_or_default_template('config', '')
    mapper = conf_or_default_template('map', kwargs.get('map', mapreduce_defaults['map']))
    reducer = conf_or_default_template('reduce', kwargs.get('reduce', mapreduce_defaults['reduce']))
    input_paths = conf_or_default_template('input_paths', kwargs.get('input_paths', ''))
    output_path = conf_or_default_template('output_path', kwargs.get('output_path', ''))
    output_shards = conf_or_default_template('output_shards', kwargs.get('output_shards', ''))
    num_workers = kwargs.get('num_workers', 1)

    job_args = '--jobid ' + jobid + ' --map ' + mapper + ' --reduce ' + reducer + ' --numWorkers ' + str(num_workers) + ' --shuffleDirectory ' + mapreduce_defaults['shuffle_directory'] + ' ' + config + ' '
    input_args = '--inputPaths ' + input_paths + ' '
    output_args = '--outputPath ' + output_path + ' --outputShards ' + output_shards + ' '

    begin_operator = DummyOperator(task_id='mapreduce_begin')
    complete_operator = DummyOperator(task_id='mapreduce_complete')
    operators = [ begin_operator ]

    for i in range(num_workers):
        ecs_operator = ECSOperator(
            dag=dag,
            do_xcom_push=True,
            task_definition='Your ECS Task for wholebuzz/mapreduce container',
            task_id=kwargs.get('task_id', 'mapreduce') + '-' + str(i),
            cluster='Your cluster',
            launch_type='EC2',
            aws_conn_id='aws_default',
            overrides={
                'cpu': conf_or_default_template('cpu', kwargs.get('cpu', mapreduce_defaults['cpu'])),
                'memory': conf_or_default_template('memory', kwargs.get('memory', mapreduce_defaults['memory'])),
                'containerOverrides': [
                    {
                        'name': 'wholebuzz/mapreduce',
                        'environment': [
                            {
                                'name': 'RUN_ARGS',
                                'value': 'mapreduce ' + job_args + input_args + output_args + kwargs.get('extra_args', '') + ' --workerIndex ' + str(i),
                            },
                        ],
                    },
                ],
            },
            network_configuration={
                'awsvpcConfiguration': {
                    'securityGroups': ['Your security group'],
                    'subnets': ['Your subnet'],
                },
            },
            tags={
                'Application': 'mapreduce',
            },
            awslogs_group='Your log group',
            awslogs_stream_prefix='Your log prefix',
        )
        operators.append(ecs_operator)
        begin_operator >> ecs_operator >> complete_operator

    operators.append(complete_operator)
    return operators
