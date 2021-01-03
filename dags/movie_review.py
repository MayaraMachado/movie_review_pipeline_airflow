from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from etl_scripts.load_to_s3 import local_to_s3
from etl_scripts.web_scraping import collect_adoro_cinema_data
from etl_scripts.remove_local_file import remove_local_file



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 1, 1),
    "retries": 0,
}

with DAG(
    "etl_movie_review", 
    schedule_interval=timedelta(minutes=1),
    catchup=False,
    default_args=default_args
) as dag:

    # Inicio do Pipeline
    start_of_data_pipeline = DummyOperator(task_id='start_of_data_pipeline', dag=dag)

    # Definindo a tarefa para realização de web scrapping
    movie_review_web_scraping_stage = PythonOperator(
        task_id='movie_review_web_scraping_stage',
        python_callable=collect_adoro_cinema_data,
        op_kwargs={
            'quantidade_paginas': 1,
        },
    )

    # definindo a tarefa para enviar o arquivo csv para S3.
    movie_review_to_s3_stage = PythonOperator(
        task_id='movie_review_to_s3_stage',
        python_callable=local_to_s3,
        op_kwargs={
            'bucket_name': 'movie-review-airflow'
        },
    )

    movie_review_remove_local = PythonOperator(
        task_id='movie_review_remove_local',
        python_callable=remove_local_file,
    )

    # Fim da Pipeline
    end_of_data_pipeline = DummyOperator(task_id='end_of_data_pipeline', dag=dag)

# Definição do padrão de execução
start_of_data_pipeline >> movie_review_web_scraping_stage >> movie_review_to_s3_stage >> movie_review_remove_local >> end_of_data_pipeline
