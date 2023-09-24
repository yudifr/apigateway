from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8002'
URL = 'http://localhost:'
CONSUMER_PORT = '8003'


@router.get('/', name="Get Alumni")
def getAlumni():
    response = requests.get(URL+PORT+'/alumni', headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    return {'data': response.json()}


@router.get('/{id}', name="Get data  alumni", summary="showing  alumni by id", description="showing  alumni data by id")
def getAlumni(id: str):
    response = requests.get(URL+PORT+'/alumni/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': response.json()}


@router.get('/riwayat/{id}', name="Get riwayat by id", summary="showing  riwayat by id", description="showing  riwayat data by id")
def getWorkHistory(id: str):
    response = requests.get(URL+PORT+'/alumni/riwayat/history/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    print(response)
    return {'data': response.json()}


@router.post('/riwayat', name="Post new work history")
async def postWorkHistory(request: Request):
    form = await request.json()
    formData = {
        'is_active': form.get('is_active', 'false'),
        'id_alumni': form.get('id_alumni'),
        'tahun': form.get('tahun'),
    }
    print(formData)
    consumerData = {
        'nama': form['nama_perusahaan'],
    }
    responseConsumer = requests.get(URL+CONSUMER_PORT+'/consumer/name/'+form.get('nama_perusahaan'), data=json.dumps(consumerData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseConsumerValue = json.loads(responseConsumer.text)
    if responseConsumerValue.get('statusCode') == 400:
        newConsumer = requests.post(URL+CONSUMER_PORT+'/consumer/', data=json.dumps(consumerData), headers={
            'app-origins': "yes",
            'content-type': 'application/json'
        })
        id_consumer = json.loads(newConsumer.text).get('data')[0]
        formData['id_perusahaan'] = id_consumer.get('id')
    else:
        print(responseConsumerValue.get('statusCode'))
        id_perusahaan = responseConsumerValue.get('data')[0]
        formData['id_perusahaan'] = id_perusahaan.get('id')
    print(formData)
    response = requests.post(URL+PORT+'/alumni/riwayat', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': response.json()}
