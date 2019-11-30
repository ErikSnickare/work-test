import boto3
import handlers.common.models.TrainTime as TrainTime
import json
import sqlalchemy

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import MetaData
import pg8000
import os


def get_db_password():
    client = boto3.client('ssm')
    print('Getting db-password')
    return client.get_


def get_engine(user: str, db_endpoint: str):
    connection_string = f'postgres+pg8000://{user}:{get_db_password()}@{db_endpoint}'

    return sqlalchemy.create_engine(connection_string)


def init_db():
    engine = get_engine(
        user='postgres',
        db_endpoint='wd1xahto9pb1465.crkvillkum9s.eu-west-1.rds.amazonaws.com'
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def main():
    session = init_db()

    query = (
        session.query(TrainTime)
            .filter(TrainTime.station_short_code == 'TPE')
            .filter(TrainTime.type == 'ARRIVAL')
            .order_by(TrainTime.actual_time.asc())
            .all()
    )


if __name__ == "__main__":
    main()
