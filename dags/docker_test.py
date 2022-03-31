from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.email import EmailOperator

default_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
'depend_on_past'        : False,
'start_date'            : datetime(2021, 5, 1),
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG("docker_test",start_date=datetime(2022,3,22), schedule_interval="*/5 * * * *", catchup=False) as dag:     

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
        )
        
    t2 = DockerOperator(
        api_version='auto',
        command='echo "hello world"',
        docker_url='tcp://docker-proxy:2375',
        image='alpine:latest',
        network_mode='bridge',
        task_id='docker_op_tester',
        auto_remove='True',
        dag=dag,
        )

    
    #647183375757.dkr.ecr.eu-west-1.amazonaws.com/birdbrain:latest
    #node scripts/birdbrain.js 4chan

    t1 >> t2 

