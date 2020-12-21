from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
# from django.contrib.gis.geos import GEOSGeometry
# from django.contrib.gis.measure import D
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

#define's the type of request
@api_view(['POST'])
def user_login(request):
    #Serializes JSON
    serializer = UserLoginSerializer(data=request.data)
    #checks there is no problem
    serializer.is_valid(raise_exception=True)
    #response
    response = {
        'success' : 'True',
        'status code' : status.HTTP_200_OK,
        'message': 'User logged in  successfully',
        #security token
        'token' : serializer.data['token'],
        }
    status_code = status.HTTP_200_OK

    return Response(response, status=status_code)

#https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = ['username', 'email', 'id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            serialized = json.dumps(obj)
            return Response(serialized, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def users_detail(request, pk):
    try:
        #gets user to change/delete
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #change user
    if request.method == 'PUT':
        #serialize request data to change user
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            #save this serializer as the old user
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #deletes user
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    try:
        #gets patient to change/delete
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #change patient
    if request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete patient
    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#gives list mainly for debug purposes
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    ordering_fields = ['age']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

@api_view(['POST'])
def patient_create(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#gets resources
class ModalityResourceListCreate(generics.ListCreateAPIView):
    queryset = ModalityResource.objects.all()
    serializer_class = ModalityResourceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('publishDate', 'typeArticle')


#filters resources
class ModalityResourceFilter(filters.FilterSet):
    class Meta:
        model = ModalityResource
        fields = ('publishDate', 'typeArticle')


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payer_detail(request, pk):
    try:
        #gets payer to change/delete
        payer = Payer.objects.get(pk=pk)
    except Payer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #change payer
    if request.method == 'PUT':
        serializer = PayerSerializer(payer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete payer
    elif request.method == 'DELETE':
        payer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# gives list mainly for debug purposes
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PayerListCreate(generics.ListCreateAPIView):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer
    ordering_fields = ['corporationName']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


@api_view(['POST'])
def payer_create(request):
    if request.method == 'POST':
        serializer = PayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def patient_profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patientToGet = Patient.objects.get(user=request.user)
            serialized = json.dumps(patientToGet)
            return Response(serialized, status=status.HTTP_201_CREATED)
        return Response("User Not Authenticated", status=status.HTTP_400_BAD_REQUEST)


#gets closest hospitals
# @api_view(['GET'])
# def closest(request, pk):
#     patient = Patient.objects.get(pk=pk)
#     pnt = patient.currentPos
#     rg = patient.searchRange
#     # qs = Point.objects.filter(point__distance_lte=(pnt, D(km=rg)))
#     outcome = "OBJECTID,ID,NAME,ZIPCODE"
#     x = f"{HOSPITAL_URL}/query?where=1%3D1&outFields=*&geometry={pnt[0]},{pnt[1]}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&distance={rg}&units=esriSRUnit_Kilometer&outSR=4326&f=json"
#     with urllib.request.urlopen(x) as url:
#         data = json.loads(url.read().decode())
#     x = f"https://clinicaltrials.gov/api/query/full_studies?expr=SEARCH%5BLocation%5D%28AREA%5BLocationZip%5D{data['features'][0]['attributes']['ZIP']}+AND+AREA%5BLocationStatus%5DRecruiting%29&min_rnk=1&max_rnk=&fmt=json"
#     with urllib.request.urlopen(x) as url:
#         data = json.loads(url.read().decode())
#     return Response(data, status=status.HTTP_200_OK)
