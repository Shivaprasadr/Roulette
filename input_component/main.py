from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from datetime import datetime, time, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-18938.c243.eu-west-1-3.ec2.cloud.redislabs.com",
    port=18938,
    password="NXjtUgNrIrJSA4eaOLaySOWZUmc4RfHP",
    decode_responses=True
)

class tabledata(HashModel):
    dealer_name: str
    win_number: int
    spindirection: str
    spintype: str
    sound: str
    table_number: int
    date: datetime

    class Meta:
        database = redis

@app.get("/tabledata")

def all():
    return [format(pk) for pk in tabledata.all_pks()]

def format(pk: str):
    tabledata = tabledata.get(pk)

    return {
        'id': tabledata.pk,
        'dealer_name': tabledata.dealer_name,
        'win_number':tabledata.win_number,
        'spindirection': tabledata.spindirection,
        'spintype': tabledata.spintype,
        'sound': tabledata.sound,
        'table_number': tabledata.table_number,
        'date': tabledata.date
    }

@app.post('/tabledata')
def create(tabledata: tabledata):
    return tabledata.save()

@app.get('/tabledata/{pk}')
def get(pk: str):
    return tabledata.get(pk)

@app.delete('/tabledata/{pk}')
def delete(pk: str):
    return tabledata.delete(pk)