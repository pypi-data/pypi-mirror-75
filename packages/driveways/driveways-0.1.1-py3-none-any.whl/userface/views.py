from django.shortcuts import render, redirect
from django.views import generic
from .models import User, Vehicle, ParkingSpot, Destination, UserDetails
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import Distance, D
from geopy.distance import distance
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import RegisterForm, VehicleForm, ParkingSpaceForm
#from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import fromstr
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.views.generic import DetailView


def words_to_point(q):
    geolocator = Nominatim(user_agent="driveways")
    location = geolocator.geocode(q)
    point = Point(location.latitude, location.longitude)
    return point



def index(request):

    return render(request, 'userface/index.html')


def portal(request):

    return render(request, 'userface/adminportal.html')

def search(request):

    if request.method == "GET":
        resultss = request.GET.get('results', False)
        if not resultss:
            resultss = ""

        try:

            destination = words_to_point(resultss)

        except (GeocoderTimedOut, AttributeError) as e:
            request.session['spot'] = []
            return render(request, 'userface/search.html', {'resultss': resultss})

        spot_distance = request.GET.get('distance', False )
        try:
            val = int(spot_distance)
        except ValueError:
            print("That's not an int!")
            spot_distance = 3
        request.session['spot'] = "unknown"
        if request.user.is_authenticated:
            c_user = request.user
            dest = c_user.destination_set.create(
                address=resultss, location=destination)
            dest.save()
            request.session['spot'] = []
            near_spots = ParkingSpot.objects.filter(
                location__distance_lt=(destination, Distance(km=spot_distance)))
            for spot in near_spots:
                if len(spot.address) > 0:
                    try :

                        details = UserDetails.objects.get(owner = spot.owner)
                        number = details.number

                    except UserDetails.DoesNotExist:
                        number = ""

                    request.session['spot'].append(
                        {"address": spot.address,
                         "owner": spot.owner.first_name + " " + spot.owner.last_name,
                         "lon": spot.location.y,
                         "lat": spot.location.x,
                         "number": number})
    return render(request, 'userface/search.html', {'resultss': resultss, 'dest': dest})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/userface")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})


class VehicleListView(LoginRequiredMixin, generic.ListView):
    model = Vehicle
    #context_object_name = 'vehicles'
    template_name = 'userface/user_vehicle_list.html'

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)[:5]

class ParkingSpotListView(LoginRequiredMixin, generic.ListView):
    model = ParkingSpot
    #context_object_name = 'vehicles'
    template_name = 'userface/parking_spot_list.html'

    def get_queryset(self):
        return ParkingSpot.objects.filter(owner=self.request.user)[:]

def registervehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.make = form.cleaned_data.get('make')
            vehicle.model = form.cleaned_data.get('model')
            vehicle.plateNum = form.cleaned_data.get('plateNum')
            vehicle.user = request.user
            vehicle.save()
        return redirect("/userface/myvehicles")
    else:
        form = VehicleForm()

    return render(request, "userface/register_vehicle.html", {"form": form})


def addspot(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            parkingspot = form.save(commit=False)
            parkingspot.address = form.cleaned_data.get('address')
            parkingspot.city = form.cleaned_data.get('city')
            fullAddress = form.cleaned_data.get(
                'address') + " " + form.cleaned_data.get('city')
            parkingspot.location = words_to_point(fullAddress)
            parkingspot.owner = request.user
            parkingspot.save()
        return redirect("/userface/myparking")
    else:
        form = ParkingSpaceForm()

    return render(request, "userface/addspot.html", {"form": form})
