from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse #icon formate me response bhejta hai
from django.views.decorators.csrf import csrf_exempt #CSRF removes taken value
from django.views.decorators.http import require_http_methods
from .models import Todo
import json


#helper function  for the purpose of Cross Origin Request (CURS)


def cors_response(response):
    response["Access-Control-Allow-Oigin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,PATCH,OP"
    response["Access-Control-Allow-Header"] = "Control-Type"
    return response