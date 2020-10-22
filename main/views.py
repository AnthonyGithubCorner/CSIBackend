from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
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
import django_filters.rest_framework
from .models import ModalityResource
from .serializers import ModalityResourceSerializer
from django_filters import rest_framework as filters


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


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = ['username', 'email', 'id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    ordering_fields = ['age']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]



@api_view(['GET'])
def loginView(request):
    return Response(data={"Test":"Login"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def closest(request, pk):
    patient = Patient.objects.get(pk=pk)
    pnt = patient.currentPos
    rg = patient.searchRange
    # qs = Point.objects.filter(point__distance_lte=(pnt, D(km=rg)))
    outcome = "OBJECTID,ID,NAME,ZIPCODE"
    x = f"{HOSPITAL_URL}/query?where=1%3D1&outFields=*&geometry={pnt[0]},{pnt[1]}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&distance={rg}&units=esriSRUnit_Kilometer&outSR=4326&f=json"
    with urllib.request.urlopen(x) as url:
        data = json.loads(url.read().decode())
    x = f"https://clinicaltrials.gov/api/query/full_studies?expr=SEARCH%5BLocation%5D%28AREA%5BLocationZip%5D{data['features'][0]['attributes']['ZIP']}+AND+AREA%5BLocationStatus%5DRecruiting%29&min_rnk=1&max_rnk=&fmt=json"
    with urllib.request.urlopen(x) as url:
        data = json.loads(url.read().decode())
    return Response(data, status=status.HTTP_200_OK)


class ModalityResourceListCreate(generics.ListCreateAPIView):
    queryset = ModalityResource.objects.all()
    serializer_class = ModalityResourceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('publishDate', 'typeArticle')


class ModalityResourceFilter(filters.FilterSet):
    class Meta:
        model = ModalityResource
        fields = ('publishDate', 'typeArticle')

