from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient
from django.contrib.auth.models import User
import requests
from .serializers import *
from django.http import JsonResponse
import urllib.request
import json
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

HOSPITAL_URL = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Hospitals_1/FeatureServer/0/'.rstrip("/")


@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    response = {
        'success' : 'True',
        'status code' : status.HTTP_200_OK,
        'message': 'User logged in  successfully',
        'token' : serializer.data['token'],
        }
    status_code = status.HTTP_200_OK

    return Response(response, status=status_code)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = ['username', 'email', 'id']

@api_view(['PUT', 'DELETE'])
def users_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
def patient_detail(request, pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    ordering_fields = ['age']

@api_view(['GET'])
def loginView(request):
    return Response(data={"Test":"Login"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def closest(request, pk):
    patient = Patient.objects.get(pk=pk)
    pnt = patient.currentPos
    rg = patient.searchRange
    qs = Point.objects.filter(point__distance_lte=(pnt, D(km=rg)))
    outcome = "OBJECTID,ID,NAME"
    x = f"{HOSPITAL_URL}/query?where=1%3D1&outFields={outcome}&geometry={pnt[0]},{pnt[1]}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&distance={rg}&units=esriSRUnit_Kilometer&outSR=4326&f=json"
    with urllib.request.urlopen(x) as url:
        data = json.loads(url.read().decode())

        return Response(data, status=status.HTTP_200_OK)


