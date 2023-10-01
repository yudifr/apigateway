from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8004'
ALUMNI_PORT = '8002'
CONSUMER_PORT = '8003'
URL = 'http://localhost:'
# get by alumni


@router.get('/kuisioner/alumni/{id}', name="Get data kuisioner alumni", summary="showing kuisioner alumni by id", description="showing kuisioner alumni data by id")
def getKuisionerAlumni(id: str):
    response = requests.get(URL+PORT+'/kuisioner/alumni/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': json.loads(response.text)}

# get by consumer


@router.get('/kuisioner/consumer/{id}', name="Get data kuisioner consumer", summary="showing kuisioner consumer by id", description="showing kuisioner consumer data by id")
def getKuisionerConsumer(id: str):
    response = requests.get(URL+PORT+'/kuisioner/consumer/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': json.loads(response.text)}


@router.get('/kuisioner/institution/alumni/{institutionId}/{institutionType}', name="Get Alumni Kuisioner By Institution")
def getAlumniKuisionerByInstitution(institutionId: str, institutionType: str):
    alumniDataQueries = {
        'institution_id': institutionId,
        'institution_type': institutionType

    }
    response = requests.post(URL+ALUMNI_PORT+'/alumni/getalumnidata', data=json.dumps(alumniDataQueries), headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    responseData = response.json()
    alumniFromInstitutionData = responseData.get('data')

    # todo get by in
    alumniKuisionerPayload = {
        'id_alumnis': alumniFromInstitutionData
    }
    responseTracer = requests.post(URL+PORT+'/kuisioner/get-multiple-alumni-kuisioner', data=json.dumps(alumniKuisionerPayload), headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    responseTracerData = responseTracer.json()
    return responseTracerData


@router.get('/kuisioner/institution/consumer/{institutionId}/{institutionType}', name="Get consumer Kuisioner By Institution")
def getConsumerKuisionerByInstitution(institutionId: str, institutionType: str):
    consumerDataQueries = {
        'institution_id': institutionId,
        'institution_type': institutionType

    }
    response = requests.post(URL+ALUMNI_PORT+'/alumni/getworkerdata', data=json.dumps(consumerDataQueries), headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    responseData = response.json()
    consumerFromInstitutionData = responseData.get('data')

    # todo get by in
    consumerKuisionerPayload = {
        'id_consumer': consumerFromInstitutionData
    }
    responseTracer = requests.post(URL+PORT+'/kuisioner/get-multiple-consumer-kuisioner', data=json.dumps(consumerKuisionerPayload), headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    responseTracerData = responseTracer.json()
    return responseTracerData


@router.post('/kuisioner/alumni', name='Post tracer')
async def newAlumniKuisioner(request: Request):
    form = await request.json()
    formData = {
        'id_alumni': form.get('id_alumni'),
        'pindah': form.get('pindah', ''),
        'alasan_pindah': form.get('alasan_pindah', ''),
        'bidangkerja': form.get('bidangkerja', ''),
        'gaji_sekarang': form.get('gaji_sekarang', ''),
        'gajipertama': form.get('gajipertama', ''),
        'kerja_pertama': form.get('kerja_pertama', ''),
        'sesuaikah': form.get('sesuaikah', 'false'),
        'syaratipk': form.get('syaratipk', 'false'),
        'kuisioner1': form.get('kuisioner1'),
        'kuisioner2': form.get('kuisioner2'),
        'kuisioner3': form.get('kuisioner3'),
        'kuisioner4': form.get('kuisioner4'),
        'kuisioner5': form.get('kuisioner5'),
        'kuisioner6': form.get('kuisioner6'),
        'kuisioner7': form.get('kuisioner7'),
        'kuisioner8': form.get('kuisioner8'),
    }
    response = requests.post(URL+PORT+'/kuisioner/alumni', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseAlumniUserValue = json.loads(response.text)

    return {'data': responseAlumniUserValue}


@router.put('/kuisioner/alumni/{id}', name='Post tracer')
async def updateAlumniKuisioner(request: Request, id: str):
    form = await request.json()
    formData = {
        'pindah': form.get('pindah', ''),
        'alasan_pindah': form.get('alasan_pindah', ''),
        'bidangkerja': form.get('bidangkerja', ''),
        'gaji_sekarang': form.get('gaji_sekarang', ''),
        'gajipertama': form.get('gajipertama', ''),
        'kerja_pertama': form.get('kerja_pertama', ''),
        'sesuaikah': form.get('sesuaikah', ''),
        'syaratipk': form.get('syaratipk', ''),
        'kuisioner1': form.get('kuisioner1'),
        'kuisioner2': form.get('kuisioner2'),
        'kuisioner3': form.get('kuisioner3'),
        'kuisioner4': form.get('kuisioner4'),
        'kuisioner5': form.get('kuisioner5'),
        'kuisioner6': form.get('kuisioner6'),
        'kuisioner7': form.get('kuisioner7'),
        'kuisioner8': form.get('kuisioner8'),
    }
    response = requests.put(URL+PORT+'/kuisioner/alumni/'+id, data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseAlumniUserValue = json.loads(response.text)

    return {'data': responseAlumniUserValue}


@router.post('/kuisioner/consumer', name='Post tracer consumer')
async def newConsumerKuisioner(request: Request):
    form = await request.json()
    formData = {
        'id_consumer': form.get('id_consumer'),
        'saran_prodi': form.get('saran_prodi'),
        'saran_fasilitas': form.get('saran_fasilitas'),
        'saran_dosen': form.get('saran_dosen'),
        'saran_kurikulum': form.get('saran_kurikulum'),
        'saran_administrasi': form.get('saran_administrasi'),
        'kekurangan': form.get('kekurangan'),
    }
    response = requests.post(URL+PORT+'/kuisioner/consumer', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseConsumerUserValue = json.loads(response.text)

    return {'data': responseConsumerUserValue}


@router.put('/kuisioner/consumer/{id}', name='Post tracer')
async def updateConsumerKuisioner(request: Request, id: str):
    form = await request.json()
    formData = {
        'saran_prodi': form.get('saran_prodi'),
        'saran_fasilitas': form.get('saran_fasilitas'),
        'saran_dosen': form.get('saran_dosen'),
        'saran_kurikulum': form.get('saran_kurikulum'),
        'saran_administrasi': form.get('saran_administrasi'),
        'kekurangan': form.get('kekurangan'),
    }
    response = requests.put(URL+PORT+'/kuisioner/consumer/'+id, data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseConsumerUserValue = json.loads(response.text)

    return {'data': responseConsumerUserValue}
