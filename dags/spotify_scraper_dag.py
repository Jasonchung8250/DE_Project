from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator 
from datetime import datetime, timedelta
import time

default_args = {
	'owner' : 'jason',
	'depends_no_past' : False,
	'email' : ['jasonchung8250@gmail.com'],
	'email_on_failure' : True,
	'email_on_retry' : False,
	'retries' : 3
}

dag = DAG('spotify_scraper_dag',
	default_args = default_args,
	start_date = datetime(2020,8,11),
	schedule_interval=timedelta(days=1)
)


create_spotify_daily_top_50_global = MySqlOperator(
	task_id='create_spotify_daily_top_50_global',
	dag=dag,
	mysql_conn_id=airflow_mysql_db,
	sql="""
	CREATE TABLE IF NOT EXISTS spotify_daily_top_50_global 
	(
	artist_name VARCHAR(100),
	track_id VARCHAR(100),
	track_name VARCHAR(100),
	duration_ms INT,
	explicit BOOL,
	popularity INT,
	daily_rank INT,
	album_id VARCHAR(100),
	album_name VARCHAR(100),
	album_type VARCHAR(100),
	release_date VARCHAR(100),
	dt VARCHAR(100)
	) 
	; 
	"""
)

populate_spotify_daily_top_50_global = BashOperator(
	task_id='populate_spotify_daily_top_50_global',
	dag=dag,
	bash_command='python Scraper.py'
	)