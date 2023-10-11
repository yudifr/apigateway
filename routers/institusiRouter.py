from fastapi import FastAPI, APIRouter, Request, HTTPException

import requests

import json
router = APIRouter()
PORT = '8001'
URL = 'http://localhost:'
ALUMNI_PORT = '8002'


@router.get('/', name="Get Institution")
def getInstitution():
    response = requests.get(URL+PORT+'/institution/', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': json.loads(response.text)}


@router.get('/faculty', name="Get Faculties")
def getFaculties():
    response = requests.get(URL+PORT+'/institution/getFaculty/faculty', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    print(response)
    return {'data': json.loads(response.text)}


@router.get('/major', name="Get Majors")
def getMajors():
    response = requests.get(URL+PORT+'/institution/faculty/major/', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': json.loads(response.text)}


@router.get('/{institution_id}', name="Get Institution", summary="showing institution by id", description="showing institution data by id")
def getInstitutionbyId(institution_id: str):
    response = requests.get(URL+PORT+'/institution/'+institution_id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    if response:
        responseValue = json.loads(response.text)
        print(responseValue)
        if responseValue.get('statusCode') == 400:
            return {'message': 'institution is not available', 'status': 'error'}
        else:
            return {'data': responseValue, 'status': 'ok'}


@router.post('/', name='Post institution')
async def newInstitution(request: Request):
    form = await request.json()
    formdata = {
        'kode_sekolah': form.get('kode_sekolah'),
        'nama': form.get('nama'),
        'tipe': form.get('tipe'),
        'alamat': form.get('alamat'),
        'kab_kota': form.get('kab_kota'),
        'provinsi': form.get('provinsi'),
        'no_telp': form.get('no_telp'),
        'jenis': form.get('jenis'),
        'kecamatan': form.get('kecamatan'),
        'kelurahan': form.get('kelurahan'),
        # 'nama_fakultas':form.get('nama_fakultas'),
        # 'email_fakultas':form.get('email_fakultas'),
        # 'nama_prodi':form.get('nama_prodi'),
        # 'email_prodi':form.get('email_prodi'),
    }

    response = requests.post(URL+PORT+'/institution/', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    idnya = json.loads(response.text).get('data')[0]
    return idnya.get('id')


@router.post('/university/get-id', name='get univ of alumni')
async def getUnivOfAlumni(request: Request):
    form = await request.json()
    formdata = {
        'id_alumni': form.get('id_alumni'),
    }

    response = requests.post(URL+PORT+'/institution/university/get-id', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    return json.loads(response.text)


@router.post('/university/get-alumnus-data', name='get univ of alumni')
async def getUnivOfAlumni(request: Request):
    form = await request.json()
    formdata = {
        'ids': form.get('ids'),
    }

    response = requests.post(URL+PORT+'/institution/university/get-alumnus-data', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    return response.json()


@router.post('/', name='Post Faculty')
async def newFaculty(request: Request):
    form = await request.json()
    formdata = {
        'id_institusi': form.get('id_institusi'),
        'nama_fakultas': form.get('nama_fakultas'),
        'email_fakultas': form.get('email_fakultas'),
    }

    response = requests.post(URL+PORT+'/institution/faculty', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    return {'data': json.loads(response.text)}


@router.post('/', name='Post Major')
async def newMajor(request: Request):
    form = await request.json()
    formdata = {
        'id_institusi': form.get('id_institusi'),
        'id_fakultas': form.get('id_fakultas'),
        'nama_prodi': form.get('nama_prodi'),
        'email_prodi': form.get('email_prodi'),
    }

    response = requests.post(URL+PORT+'/institution/faculty/major', data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    }

    )
    return {'data': json.loads(response.text)}


@router.put('/{id}', name='update institution', summary='update institution data')
async def updateInstitution(id: str, request: Request):
    form = await request.json()
    formdata = {
        'kode_sekolah': form.get('kode_sekolah'),
        'nama': form.get('nama'),
        'tipe': form.get('tipe'),
        'alamat': form.get('alamat'),
        'kab_kota': form.get('kab_kota'),
        'provinsi': form.get('provinsi'),
        'email': form.get('email'),
        'no_telp': form.get('no_telp'),
        'nama_fakultas': form.get('nama_fakultas'),
        'email_fakultas': form.get('email_fakultas'),
        'nama_prodi': form.get('nama_prodi'),
        'email_prodi': form.get('email_prodi'),
    }
    response = requests.put(URL+PORT+'/institution/'+id, data=json.dumps(formdata), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.delete('/{id}', name="delete institution", summary='soft delete institution data')
async def deleteInstitution(id: str, request: Request):
    response = requests.delete(URL+PORT+'/institution/'+id, headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'message': json.loads(response.text)}


@router.get('/list-alumni/{institutionId}/{institutionType}', name="Get consumer Kuisioner By Institution")
def getConsumerKuisionerByInstitution(institutionId: str, institutionType: str):
    institutionData = {
        'institution_id': institutionId,
        'institution_type': institutionType

    }
    urlToGetIds = URL+ALUMNI_PORT+'/alumni/getworkerdata'
    if institutionType == '4':
        urlToGetIds = URL+PORT+'/institution/kuisioner/alumni'
    print(urlToGetIds, 'ffffffffffffffff')
    response = requests.post(urlToGetIds, data=json.dumps(institutionData), headers={
        'app-origins': 'yes',
        'Content-Type': 'application/json',
    })
    responseData = response.json()
    alumniFromInstitutionData = responseData.get('data')
    print(alumniFromInstitutionData)
    if len(alumniFromInstitutionData) > 0:
        idsfff = {
            'ids': alumniFromInstitutionData
        }
        print(alumniFromInstitutionData)
        alumni = requests.post(URL+ALUMNI_PORT+'/alumni/get-alumni-data', data=json.dumps(idsfff), headers={
            'app-origins': 'yes',
            'Content-Type': 'application/json',
        })
        alumniData = alumni.json()
        return alumniData
    else:
        raise HTTPException(
            status_code=400,
            detail="No Alumni Available",
        )
