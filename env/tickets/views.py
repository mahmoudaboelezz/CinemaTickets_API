from django.http import response
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import serializers
from .models import Guest, Reservation, Movie
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins,viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#from .permissions import IsAuthorOrReadOnly

# first without Reset and no model query
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'omar',
            'mobile': 123213
        },
        {
            'id': 2,
            'name': 'aboelezz',
            'mobile': 984234
        }
    ]
    return JsonResponse(guests, safe=False)


# second without Reset but models
def no_reset_from_model(reqeust):
    data = Guest.objects.all()
    response = {
        'guest': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# third
# GET - POST _ PUT - DELETE

# 3.1 GET - POST


@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 3.2 PUT - DELETE


@api_view(['GET', 'POST', 'DELETE'])
def FPV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Get
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT
    elif request.method == 'POST':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV Class Based views
# 4.1 GET POST
class CBV_LIST(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 4.2 GET PUT DELETE bassed on pk


class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# MIXINS
# 5.1 mixins list


class mixins_list(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2
class mixins_pk(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request,pk):
        return self.retrieve(request)

    def put(self, request,pk):
        return self.update(request)
    def delete(self, request,pk):
        return self.destroy(request)
    
    
#Generics
#6.1
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
#6.2 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
#8 find movie 'search'
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializers = MovieSerializer(movies,many=True)
    return Response(serializers.data)

#create new reservation
@api_view(['GET','POST'])
def create_reservation(request):
    
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)