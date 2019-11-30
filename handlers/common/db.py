import boto3
import models
import json
import utils
import sqlalchemy

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import MetaData
import pg8000
import os


def get_db_password():
    client = boto3.client('ssm')
    print('Getting db-password')

    return boto3.get_parameter(Name='snowflake.password', WithDecryption=True)


def get_engine(user: str, db_endpoint: str):
    connection_string = f'postgres+pg8000://{user}:{get_db_password()}@{db_endpoint}'

    return sqlalchemy.create_engine(connection_string)


def init_db():
    engine = get_engine(
        user=os.getenv('DB_USER'),
        db_endpoint=os.getenv('DB_ENDPOINT')
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def insert_s3_object(s3_object):
    session = init_db()

    client = boto3.client('s3')
    s3_object = client.get_object(
        Bucket='work-test-wh',
        Key=s3_object['key'],
    )

    body = json.loads(s3_object['Body'].read())
    for row in body['timeTableRows']:
        if row.get('trainReady'):
            del row['trainReady']
        if row.get('causes'):
            del row['causes']

        model = models.TrainTime(**utils.keys_to_snake(row))
        session.add(model)

    session.commit()

