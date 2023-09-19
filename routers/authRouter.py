from fastapi import FastAPI, APIRouter, Request, HTTPException

import requests

import json
router = APIRouter()
PORT = '8030'
URL = 'http://localhost:'
INSTITUTION_PORT = '8001'
ALUMNI_PORT = '8002'
CONSUMER_PORT = '8003'


@router.post('/logout', name="Logout")
async def logout(request: Request):
    # https://stackoverflow.com/questions/64139023/how-to-set-cookies-with-fastapi-for-cross-origin-requests/71131572#71131572
    form = await request.json()
    formData = {
        'username': form.get('username'),
    }
    response = requests.post(URL+PORT+'/auth/logout/', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json',
    })
    return response.json()


@router.post('/ping', name="ping")
async def ping(request: Request):
    form = await request.json()
    formData = {
        'username': form.get('username'),
        'cache_key': form.get('cache_key'),
    }
    response = requests.post(URL+PORT+'/auth/current-user/', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'Content-Type': 'application/json'
    })
    return response.json()


@router.post('/register', name='Register')
async def register(request: Request):
    # try:
    form = await request.json()
    formData = {
        'username': form.get('username'),
        'password': form.get('password'),
        'email': form.get('email'),
        'no_telp': form.get('no_telp'),
        'cache_key': form.get('cache_key'),
        'type': form.get('type'),
    }
    print(form)
    response = requests.post(URL+PORT+'/auth/register', data=json.dumps(formData), headers={
        'app-origins': "yes",
        'content-type': 'application/json'
    })
    responseValue = json.loads(response.text)
    if responseValue.get('statusCode') == 400:
        print(responseValue)
        raise HTTPException(
            status_code=400,
            detail="User Already Exist",
            headers={"X-Error": "There goes my error"},
        )
    else:
        # alumni tested
        if form.get('type') == '1':
            alumniData = {
                'motherName': form.get('motherName'),
                'fatherName': form.get('fatherName'),
                'address': form.get('address'),
                'nama': form.get('nama'),
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
                        'id_major': ''
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
                for item in tempUniversityArray:
                    print(item)
                    alumniUniversityData = {
                        'id_alumni': user_id.get('id'),
                        'id_pt': item.get('id_pt'),
                        'id_fakultas': item.get('id_faculty'),
                        'id_prodi': item.get('id_major')
                    }
                    newPt = requests.post(URL+INSTITUTION_PORT+'/institution/university', data=json.dumps(alumniUniversityData), headers={
                        'app-origins': "yes",
                        'content-type': 'application/json'
                    })
                    id_pt = json.loads(newPt.text).get('data')[0]
                    print(id_pt.get('id'))
                responseUpdateUser = requests.put(URL+PORT+'/auth/update-user', data=json.dumps(formData), headers={
                    'app-origins': "yes",
                    'content-type': 'application/json'
                })
                responseUpdateUserValue = json.loads(
                    responseUpdateUser.text)
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
                'jenis': form.get('jenis'),
                'kecamatan': form.get('kecamatan'),
                'kelurahan': form.get('kelurahan'),
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
                id_institution = json.loads(
                    newInstitution.text).get('data')[0]
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
                    # print(institutionData.get('jenis'))
                    # if (institutionData.get('jenis') == '4'):
                    #     facultyId = None
                    #     majorId = None
                    #     faculty = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/'+str(user_id)+'/'+form.get('nama_fakultas'),   headers={
                    #         'app-origins': "yes",
                    #         'content-type': 'application/json'
                    #     })
                    #     facultyValue = json.loads(faculty.text)
                    #     if facultyValue.get('statusCode') == 400:
                    #         facultyData = {
                    #             'nama_fakultas': form.get('nama_fakultas'),
                    #             'id_institusi': user_id
                    #         }
                    #         newFaculty = requests.post(URL+INSTITUTION_PORT+'/institution/faculty', data=json.dumps(facultyData), headers={
                    #             'app-origins': "yes",
                    #             'content-type': 'application/json'
                    #         })
                    #         facultyValue = json.loads(
                    #             newFaculty.text)
                    #         print(facultyValue)

                    #         facultyId = facultyValue.get('data')[
                    #             0].get('id')
                    #     else:
                    #         facultyId = facultyValue.get('data')[
                    #             0].get('id')
                    #     major = requests.get(URL+INSTITUTION_PORT+'/institution/faculty/major/'+str(user_id)+'/'+str(facultyId)+'/'+form.get('nama_prodi'),   headers={
                    #         'app-origins': "yes",
                    #         'content-type': 'application/json'
                    #     })
                    #     majorValue = json.loads(major.text)
                    #     if majorValue.get('statusCode') == 400:
                    #         majorData = {
                    #             'id_institusi': user_id,
                    #             'id_fakultas': facultyId,
                    #             'nama_prodi': form.get('nama_prodi'),
                    #         }
                    #         newmajor = requests.post(URL+INSTITUTION_PORT+'/institution/faculty/major', data=json.dumps(majorData), headers={
                    #             'app-origins': "yes",
                    #             'content-type': 'application/json'
                    #         })
                    #         majorValue = json.loads(newmajor.text)
                    #         print(majorValue)
                    #         print(
                    #             '=============================================================')
                    #         if majorValue.get('statusCode') == 400:
                    #             return {'message': 'error occured on create major', 'status': 'error'}
                    #     else:
                    #         print('major found, no need to add')

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
            }
            responseConsumer = requests.get(URL+CONSUMER_PORT+'/consumer/name/'+form.get('nama'), data=json.dumps(consumerData), headers={
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
    return {'data': json.loads(response.text), 'status': 'ok', 'userId': formData.get('user_id')}
    # except:
    #     print('something went wrong')


@ router.post('/login', name='userLogin')
async def userLogin(request: Request):
    form = await request.json()
    formData = {
        'username': form.get('username'),
        'password': form.get('password'),
        'cache_key': form.get('cache_key')
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
