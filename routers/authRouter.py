from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8030'
URL = 'http://localhost:'
INSTITUTION_PORT = '8001'
ALUMNI_PORT = '8002'
CONSUMER_PORT = '8003'


@router.get('/logout', name="Logout")
def logout(id: str):
    response = requests.get(URL+PORT+'/auth/logout/', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return {'data': json.loads(response.text)}


@router.get('/ping', name="ping")
def ping():
    response = requests.get(URL+PORT+'/auth/current-user/', headers={
        'app-origins': "yes",
        'Content-Type': 'application/json'
    })
    return {'data': json.loads(response.text)}


@router.post('/register', name='Register')
async def register(request: Request):
    form = await request.form()
    formData = {
        'username': form.get('username'),
        'is_active': form.get('is_active', 'false'),
        'type': form.get('type'),
    }
    response = requests.post(URL+PORT+'/auth/register', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseValue = json.loads(response.text)
    if responseValue.get('statusCode') == 400:
        return {'message': 'user already exist', 'status': 'error'}
    else:
        # alumni tested
        if form.get('type') == '1':
            alumniData = {
                'idPelajar': form.get('idPelajar'),
                'lulusanSd': form.get('lulusanSd'),
                'tahunSd': form.get('tahunSd'),
                'lulusanSmp': form.get('lulusanSmp'),
                'tahunSmp': form.get('tahunSmp'),
                'lulusanSma': form.get('lulusanSma'),
                'tahunSma': form.get('tahunSma'),
                'lulusanPt': form.get('lulusanPt'),
                'tahunPt': form.get('tahunPt'),
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

            if (form.get('lulusanPt')):
                responseAlumniPt = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+form.get('lulusanPt'),   headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                responseAlumniPtValue = json.loads(responseAlumniPt.text)
                if responseAlumniPtValue.get('statusCode') == 400:
                    ptData = {
                        'nama': form.get('lulusanPt'),
                        'jenis': '4'
                    }
                    newPt = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(ptData), headers={
                        'app-origins': "yes",
                        'content-type': 'application/json'
                    })
                    id_pt = json.loads(newPt.text).get('data')[0]
                    alumniData['id_pt'] = id_pt.get('id')
                else:
                    alumniData['id_pt'] = responseAlumniPtValue.get('data')[
                        0].get('id')
            print(alumniData)
            responseAlumniUser = requests.post(URL+ALUMNI_PORT+'/alumni', data=json.dumps(alumniData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseAlumniUserValue = json.loads(responseAlumniUser.text)
            if responseAlumniUserValue.get('statusCode') == 400:
                print(responseAlumniUserValue, '154')
                return {'message': 'error occured on create alumniData', 'status': 'error'}
            else:
                user_id = responseAlumniUserValue.get('data')[0]
                formData['user_id'] = user_id.get('id')
                responseUpdateUser = requests.put(URL+PORT+'/auth/update-user', data=json.dumps(formData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                responseUpdateUserValue = json.loads(responseUpdateUser.text)
                print(responseUpdateUserValue)
                if responseUpdateUserValue.get('statusCode') == 400:
                    return {'message': 'error occured on update user', 'status': 'error'}
        # institution tested
        if form.get('type') == '2':
            institutionData = {
                'kode_sekolah': form.get('kode_sekolah'),
                'nama': form.get('nama'),
                'alamat': form.get('alamat'),
                'kab_kota': form.get('kab_kota'),
                'provinsi': form.get('provinsi'),
                'no_telp': form.get('no_telp'),
                'jenis': form.get('jenis'),
                'kecamatan': form.get('kecamatan'),
                'kelurahan': form.get('kelurahan'),
                'email': form.get('email'),
            }
            responseInsitution = requests.get(URL+INSTITUTION_PORT+'/institution/name/'+form.get('nama'), data=json.dumps(institutionData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseInsitutionValue = json.loads(responseInsitution.text)
            print(responseInsitutionValue)
            if responseInsitutionValue.get('statusCode') == 400:
                newInstitution = requests.post(URL+INSTITUTION_PORT+'/institution/', data=json.dumps(institutionData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                id_institution = json.loads(newInstitution.text).get('data')[0]
                formData['user_id'] = id_institution.get('id')
            else:
                user_id = responseInsitutionValue.get('data')[0].get('id')
                formData['user_id'] = user_id
                updateInstitution = requests.put(URL+INSTITUTION_PORT+'/institution/'+str(user_id), data=json.dumps(institutionData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                updateInstitutionValue = json.loads(updateInstitution.text)
                print(updateInstitutionValue)
                if updateInstitutionValue.get('statusCode') == 400:
                    return {'message': 'error occured on update institution', 'status': 'error'}
                else:
                    print('success updating institution')
                    print(institutionData.get('jenis'))
                    if (institutionData.get('jenis') == '4'):
                        facultyId = None
                        faculty = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/'+str(user_id)+'/'+form.get('nama_fakultas'),   headers={
                            'app-origins': "yes",
                            'content-type': 'application/json'
                        })
                        facultyValue = json.loads(faculty.text)
                        if facultyValue.get('statusCode') == 400:
                            facultyData = {
                                'nama_fakultas': form.get('nama_fakultas'),
                                'id_institusi': user_id
                            }
                            newFaculty = requests.post(URL+INSTITUTION_PORT+'/institution/faculty', data=json.dumps(facultyData), headers={
                                'app-origins': "yes",
                                'content-type': 'application/json'
                            })
                            facultyValue = json.loads(
                                newFaculty.text)
                            print(facultyValue)

                            facultyId = facultyValue.get('data')[0].get('id')
                        else:
                            facultyId = facultyValue.get('data')[0].get('id')
                        major = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/major/'+str(user_id)+'/'+str(facultyId)+'/'+form.get('nama_prodi'),   headers={
                            'app-origins': "yes",
                            'content-type': 'application/json'
                        })
                        majorValue = json.loads(major.text)
                        if majorValue.get('statusCode') == 400:
                            majorData = {
                                'id_institusi': user_id,
                                'id_fakultas': facultyId,
                                'nama_prodi': form.get('nama_prodi'),
                            }
                            newmajor = requests.post(URL+INSTITUTION_PORT+'/institution/faculty/major', data=json.dumps(majorData), headers={
                                'app-origins': "yes",
                                'content-type': 'application/json'
                            })
                            majorValue = json.loads(newmajor.text)
                            print(majorValue)
                            print(
                                '=============================================================')
                            if majorValue.get('statusCode') == 400:
                                return {'message': 'error occured on create major', 'status': 'error'}
                        else:
                            print('major found, no need to add')

            responseUpdateUser = requests.put(URL+PORT+'/auth/update-user', data=json.dumps(formData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseUpdateUserValue = json.loads(responseUpdateUser.text)
            print(responseUpdateUserValue, '197')
            if responseUpdateUserValue.get('statusCode') == 400:
                return {'message': 'error occured on update user', 'status': 'error'}
        if form.get('type') == '3':
            consumerData = {
                'jenis': form['jenis'],
                'nama': form['nama'],
                'alamat': form['alamat'],
                'provinsi': form['provinsi'],
                'kab_kota': form['kab_kota'],
                'kecamatan': form['kecamatan'],
                'kelurahan': form['kelurahan'],
                'no_telp': form['no_telp'],
            }
            responseConsumer = requests.get(URL+CONSUMER_PORT+'/consumer/name/'+form.get('nama'), data=json.dumps(consumerData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseConsumerValue = json.loads(responseConsumer.text)
            if responseConsumerValue.get('statusCode') == 400:
                consumerData = {
                    'nama': form.get('nama')
                }
                newConsumer = requests.post(URL+CONSUMER_PORT+'/consumer/', data=json.dumps(consumerData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                id_consumer = json.loads(newConsumer.text).get('data')[0]
                formData['user_id'] = id_consumer.get('id')
            else:
                user_id = responseConsumerValue.get('data')[0]
                formData['user_id'] = user_id.get('id')

            responseUpdateUser = requests.put(URL+PORT+'/auth/update-user', data=json.dumps(formData), headers={
                'app-origins': "yes",
                'content-type': 'application/json'
            })
            responseUpdateUserValue = json.loads(responseUpdateUser.text)
            if responseUpdateUserValue.get('statusCode') == 400:
                return {'message': 'error occured on update user', 'status': 'error'}
    return {'data': json.loads(response.text), 'status': 'ok'}


@router.post('/login', name='userLogin')
async def userLogin(request: Request):
    form = await request.form()
    formData = {
        'username': form.get('username'),
    }
    response = requests.post(URL+PORT+'/auth/login', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    if response:
        responseValue = json.loads(response.text)
        print(responseValue)
        if responseValue.get('statusCode') == 400:
            return {'message': 'user is not available', 'status': 'error'}
        else:
            return {'data': responseValue, 'status': 'ok'}
