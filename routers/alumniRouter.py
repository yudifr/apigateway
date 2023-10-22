from fastapi import FastAPI, APIRouter, Request, HTTPException

import requests

import json
router = APIRouter()
PORT = '8002'
URL = 'http://localhost:'
CONSUMER_PORT = '8003'
INSTITUTION_PORT = '8001'


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
        'nama': form.get('nama_perusahaan'),
    }
    responseConsumer = requests.get(URL+CONSUMER_PORT+'/consumer/name/'+form.get('nama_perusahaan'), data=json.dumps(consumerData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseConsumerValue = responseConsumer.json()
    print(responseConsumerValue)
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


@router.post('/riwayat/remove-history', name="Remove work history")
async def removeWorkHistory(request: Request):
    form = await request.json()
    formData = {
        'id_alumni': form.get('id_alumni'),
    }
    response = requests.post(URL+PORT+'/alumni/riwayat/remove-history', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': response.json()}


@router.post('/update-alumni', name="Remove work history")
async def removeWorkHistory(request: Request):
    form = await request.json()
    alumniData = {
        'id_alumni': form.get('id_alumni'),
        'lulusanSd': form.get('lulusanSd'),
        'tahunSd': form.get('tahunSd'),
        'lulusanSmp': form.get('lulusanSmp'),
        'tahunSmp': form.get('tahunSmp'),
        'lulusanSma': form.get('lulusanSma'),
        'tahunSma': form.get('tahunSma'),
        'lulusanPt': form.get('lulusanPt'),
    }
    if (form.get('lulusanSd')):
        responseAlumniSd = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+form.get('lulusanSd'),   headers={
            'app-origins': "yes",
            'content-type': 'application/json'
        })
        print(responseAlumniSd)
        responseAlumniSdValue = json.loads(responseAlumniSd.text)
        print(responseAlumniSdValue)
        if responseAlumniSdValue.get('statusCode') == 400:
            sdData = {
                'nama': form.get('lulusanSd'),
                'jenis': '1'
            }
            newSd = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(sdData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            print(newSd)
            id_sd = json.loads(newSd.text).get('data')[0]
            alumniData['id_sd'] = id_sd.get('id')
        else:
            alumniData['id_sd'] = responseAlumniSdValue.get('data')[
                0].get('id')

    if (form.get('lulusanSmp')):
        responseAlumniSmp = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+form.get('lulusanSmp'),  headers={
            'app-origins': "yes",
            'content-type': 'application/json'
        })
        responseAlumniSmpValue = json.loads(responseAlumniSmp.text)
        if responseAlumniSmpValue.get('statusCode') == 400:
            smpData = {
                'nama': form.get('lulusanSmp'),
                'jenis': '2'
            }
            newSmp = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(smpData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            id_smp = json.loads(newSmp.text).get('data')[0]
            alumniData['id_smp'] = id_smp.get('id')
        else:
            alumniData['id_smp'] = responseAlumniSmpValue.get('data')[
                0].get('id')

    if (form.get('lulusanSma')):
        responseAlumniSma = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+form.get('lulusanSma'),   headers={
            'app-origins': "yes",
            'content-type': 'application/json'
        })
        responseAlumniSmaValue = json.loads(responseAlumniSma.text)
        if responseAlumniSmaValue.get('statusCode') == 400:
            smaData = {
                'nama': form.get('lulusanSma'),
                'jenis': '3'
            }
            newSma = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(smaData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            id_sma = json.loads(newSma.text).get('data')[0]
            alumniData['id_sma'] = id_sma.get('id')
        else:
            alumniData['id_sma'] = responseAlumniSmaValue.get('data')[
                0].get('id')
    tempUniversityArray = []
    if (form.get('lulusanPt')):
        print(form.get('lulusanPt'))
        jsonPTData = json.loads(
            form.get('lulusanPt'))
        print(jsonPTData[0])
        for item in jsonPTData:
            toReturnIdPt = {
                'id_pt': '',
                'id_faculty': '',
                'id_major': '',
                'tahun': item.get('tahun')
            }
            print(item.get('nama_universitas'))
            responseAlumniPt = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+item.get('nama_universitas'),   headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseAlumniPtValue = json.loads(responseAlumniPt.text)
            if responseAlumniPtValue.get('statusCode') == 400:
                ptData = {
                    'nama': item.get('nama_universitas'),
                    'jenis': '4'
                }
                newPt = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(ptData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                id_pt = json.loads(newPt.text).get('data')[0]
                toReturnIdPt['id_pt'] = id_pt.get('id')
            else:
                toReturnIdPt['id_pt'] = responseAlumniPtValue.get('data')[
                    0].get('id')
            facultyId = None
            majorId = None
            print(toReturnIdPt.get('id_pt'),
                  str(toReturnIdPt.get('id_pt')))
            if toReturnIdPt.get('id_pt'):
                faculty = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/'+str(toReturnIdPt.get('id_pt'))+'/'+item.get('fakultas'),   headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                facultyValue = json.loads(faculty.text)
                if facultyValue.get('statusCode') == 400:
                    facultyData = {
                        'nama_fakultas': item.get('fakultas'),
                        'id_institusi': toReturnIdPt.get('id_pt')
                    }
                    newFaculty = requests.post(URL+INSTITUTION_PORT+'/institution/faculty', data=json.dumps(facultyData), headers={
                        'app-origins': "yes",
                        'content-type': 'application/json'
                    })
                    facultyValue = json.loads(
                        newFaculty.text)
                    print(facultyValue)

                    facultyId = facultyValue.get('data')[
                        0].get('id')
                else:
                    facultyId = facultyValue.get('data')[
                        0].get('id')
                toReturnIdPt['id_faculty'] = facultyId
                major = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/major/'+str(toReturnIdPt.get('id_pt'))+'/'+str(facultyId)+'/'+item.get('jurusan'),   headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                majorValue = json.loads(major.text)
                if majorValue.get('statusCode') == 400:
                    majorData = {
                        'id_institusi': toReturnIdPt.get('id_pt'),
                        'id_fakultas': facultyId,
                        'nama_prodi': item.get('jurusan'),
                    }
                    newmajor = requests.post(URL+INSTITUTION_PORT+'/institution/faculty/major', data=json.dumps(majorData), headers={
                        'app-origins': "yes",
                        'content-type': 'application/json'
                    })
                    majorValue = json.loads(newmajor.text)
                    print(majorValue)
                    print(
                        '=============================================================')

                    print(majorValue)

                    majorId = majorValue.get('data')[
                        0].get('id')
                else:
                    majorId = majorValue.get('data')[
                        0].get('id')
                toReturnIdPt['id_major'] = majorId
            tempUniversityArray.append(toReturnIdPt)
    print(alumniData)
    responseAlumniUser = requests.post(URL+PORT+'/alumni/update/alumni', data=json.dumps(alumniData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    print(responseAlumniUser)
    responseAlumniUserValue = responseAlumniUser.json()
    if responseAlumniUserValue.get('statusCode') == 400:
        print(responseAlumniUserValue, '154')
        raise HTTPException(
            status_code=400,
            detail="error occured on create alumniData",
        )
    else:
        for item in tempUniversityArray:
            print(item)
            alumniUniversityData = {
                'id_alumni': alumniData.get('id_alumni'),
                'id_pt': item.get('id_pt'),
                'id_fakultas': item.get('id_faculty'),
                'id_prodi': item.get('id_major'),
                'tahun': item.get('tahun')
            }
            newPt = requests.post(URL+INSTITUTION_PORT+'/institution/university', data=json.dumps(alumniUniversityData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })

    return responseAlumniUserValue
