#importing neccessary library
import pandas as pd
import os
from sqlalchemy import create_engine
import time
import logging

logging.basicConfig(
    filename = 'logs/.log',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filemode = 'a')

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    ''' This function will ingest the dataframe into database file....'''
    df.to_sql(table_name,con=engine,if_exists = 'append',index = False)

def load_raw_data():
    ''' This function will load CSVs as dataframe and ingest into db...'''
    start = time.time()
    for i in os.listdir('data'):
        for chunk in pd.read_csv('data/'+i,chunksize = 50000):
            logging.info(f'ingesting {i} in db')
            ingest_db(chunk,i[:-4],engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info('ingestion complete')
    logging.info(f' Total time taken {total_time} minutes')
load_raw_data()
