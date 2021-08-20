from fastapi import FastAPI, APIRouter, Request

import requests

import json
router = APIRouter()
PORT = '8002'
URL = 'http://localhost:'


@router.get('/', name="Get Alumni")
def getAlumni():
    response = requests.get(URL+PORT+'/',headers={
        'app-origins':'yes',
        'Content-Type':'application/json',
    })
    return response.text