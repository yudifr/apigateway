from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8003'
URL = 'http://localhost:'
ALUMNI_PORT = '8002'


@router.get('/', name="Get Consumer")
def getConsumer():
    response = requests.get(URL+PORT+'/consumer/', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.get('/name/{consumer_name}', name="Get Consumer")
def getConsumer(consumer_name: str):
    response = requests.get(URL+PORT+'/consumer/name/'+consumer_name, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.get('/{consumer_id}', name="Get Consumer", summary="showing Consumer by id", description="showing Consumer data by id")
def getConsumerbyId(consumer_id: str):
    response = requests.get(URL+PORT+'/consumer/'+consumer_id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.get('/worker/{consumer_id}', name="Get data  alumni", summary="showing  alumni by consumer_id", description="showing  alumni data by consumer_id")
def getAlumni(consumer_id: str):
    response = requests.get(URL+ALUMNI_PORT+'/alumni/worker/'+consumer_id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.post('/', name='Post Consumer')
async def newConsumer(request: Request):
    form = await request.form()
    formdata = {
        'jenis': form['jenis'],
        'nama': form['nama'],
        'alamat': form['alamat'],
        'provinsi': form['provinsi'],
        'kab_kota': form['kab_kota'],
        'kecamatan': form['kecamatan'],
        'kelurahan': form['kelurahan'],
        'no_telp': form['no_telp'],
    }

    response = requests.post(URL+PORT+'/consumer/', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    return response.json()


@router.put('/{id}', name='update Consumer', summary='update Consumer data')
async def updateConsumer(id: str, request: Request):
    form = await request.form()
    formdata = {
        'jenis': form['jenis'],
        'nama': form['nama'],
        'alamat': form['alamat'],
        'provinsi': form['provinsi'],
        'kab_kota': form['kab_kota'],
        'kecamatan': form['kecamatan'],
        'kelurahan': form['kelurahan'],
        'no_telp': form['no_telp'],
    }
    response = requests.put(URL+PORT+'/consumer/'+id, data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.delete('/{id}', name="delete Consumer", summary='soft delete Consumer data')
async def deleteConsumer(id: str, request: Request):
    response = requests.delete(URL+PORT+'/consumer/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()
