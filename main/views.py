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

from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient
from django.contrib.auth.models import User

from .serializers import *

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


@api_view(['GET'])
def loginView(request):
    return Response(data={"Test":"Login"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def closest(request, pk):
    user = User.objects.get(pk=pk)
    pnt = user.patient.location
    rg = user.patient.searchRange
    qs = Point.objects.filter(point__distance_lte=(pnt, D(km=rg)))
    return Response(data={qs}, status=status.HTTP_200_OK)