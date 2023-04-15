from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8004'
URL = 'http://localhost:'

@router.get('/kuisioner/alumni/{id}', name="Get data kuisioner alumni",summary="showing kuisioner alumni by id",description="showing kuisioner alumni data by id")
def getKuisionerAlumni(id : str):
    response = requests.get(URL+PORT+'/kuisioner/alumni/'+id,headers={
        'app-origins':"yes",
        'Content-Type':'application/json',
    })
    return {'data' : json.loads(response.text)}
@router.get('/kuisioner/consumer/{id}', name="Get data kuisioner consumer",summary="showing kuisioner consumer by id",description="showing kuisioner consumer data by id")
def getKuisionerConsumer(id : str):
    response = requests.get(URL+PORT+'/kuisioner/consumer/'+id,headers={
        'app-origins':"yes",
        'Content-Type':'application/json',
    })
    return {'data' : json.loads(response.text)}



@router.post('/kuisioner/alumni',name='Post tracer')
async def newAlumniKuisioner(request: Request):
    
    formData = await request.json()
    # print ( json.dumps(await request.json()))
    response =  requests.post(URL+PORT+'/kuisioner/alumni', data=json.dumps(formData),headers={
        'app-origins':"yes",
        'content-type':'application/json'
    })
    
    return {'data' : json.loads(response.text)}

    
# @router.put('/{id}',name='update Consumer',summary='update Consumer data')
# async def updateConsumer(id : str,request: Request):
#     form = await request.form()
#     formdata = {
#         'kode_sekolah':form['kode_sekolah'],
#         'nama':form['nama'],
#         'tipe':form['tipe'],
#         'alamat':form['alamat'],
#         'kab_kota':form['kab_kota'],
#         'provinsi':form['provinsi'],
#         'email':form['email'],
#         'no_telp':form['no_telp'],
#         'nama_fakultas':form['nama_fakultas'],
#         'email_fakultas':form['email_fakultas'],
#         'nama_prodi':form['nama_prodi'],
#         'email_prodi':form['email_prodi'],
#     }
#     response = requests.put(URL+PORT+'/consumer/'+id,data=json.dumps(formdata),headers={
#         'app-origins':"yes",
#         'Content-Type':'application/json',
#     })
#     return response.json()

# @router.delete('/{id}',name="delete Consumer",summary='soft delete Consumer data')
# async def deleteConsumer(id: str, request:Request):
#     response = requests.delete(URL+PORT+'/consumer/'+id,headers={
#         'app-origins':"yes",
#         'Content-Type':'application/json',
#     })
#     return {'message' : json.loads(response.text)}
