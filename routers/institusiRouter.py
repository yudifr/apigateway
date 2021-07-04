from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8001'
URL = 'http://localhost:'

@router.get('/', name="Get Institution")
def getInstitution():
    response = requests.get(URL+PORT+'/institution/',headers={
        'api-access':'yes',
        'Content-Type':'application/json',
    })
    return {'data' : json.loads(response.text),'status_code' :response.status_code}


@router.get('/{institution_id}', name="Get Institution",summary="showing institution by id",description="showing institution data by id")
def getInstitutionbyId(institution_id : str):
    response = requests.get(URL+PORT+'/institution/'+institution_id,headers={
        'api-access':'yes',
        'Content-Type':'application/json',
    })
    return {'message' : json.loads(response.text),'status_code' :response.status_code}



@router.post('/',name='Post institution')
async def newInstitution(request: Request):
    form = await request.form()
    formdata = {
        'kode_sekolah':form['kode_sekolah'],
        'nama':form['nama'],
        'tipe':form['tipe'],
        'alamat':form['alamat'],
        'kab_kota':form['kab_kota'],
        'provinsi':form['provinsi'],
        'email':form['email'],
        'no_telp':form['no_telp'],
        'nama_fakultas':form['nama_fakultas'],
        'email_fakultas':form['email_fakultas'],
        'nama_prodi':form['nama_prodi'],
        'email_prodi':form['email_prodi'],
    }
    
    response =  requests.post(URL+PORT+'/institution/', data=json.dumps(formdata),headers={
        'api-access':'yes',
        'content-type':'application/json'
    }
    
    )
    return {'message' : json.loads(response.text),'status_code' :response.status_code}
    
    
@router.put('/{id}',name='update institution',summary='update institution data')
async def updateInstitution(id : str,request: Request):
    form = await request.form()
    formdata = {
        'kode_sekolah':form['kode_sekolah'],
        'nama':form['nama'],
        'tipe':form['tipe'],
        'alamat':form['alamat'],
        'kab_kota':form['kab_kota'],
        'provinsi':form['provinsi'],
        'email':form['email'],
        'no_telp':form['no_telp'],
        'nama_fakultas':form['nama_fakultas'],
        'email_fakultas':form['email_fakultas'],
        'nama_prodi':form['nama_prodi'],
        'email_prodi':form['email_prodi'],
    }
    response = requests.put(URL+PORT+'/institution/'+id,data=json.dumps(formdata),headers={
        'api-access':'yes',
        'Content-Type':'application/json',
    })
    return response.json()

@router.delete('/{id}',name="delete institution",summary='soft delete institution data')
async def deleteInstitution(id: str, request:Request):
    response = requests.delete(URL+PORT+'/institution/'+id,headers={
        'api-access':'yes',
        'Content-Type':'application/json',
    })
    return {'message' : json.loads(response.text),'status_code' :response.status_code}
