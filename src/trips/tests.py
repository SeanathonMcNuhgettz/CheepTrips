from django.test import TestCase
from trips.models import *
import datetime
import pytz

from django.contrib import auth

# for testing things as a Client ex: using webpages
from django.test import Client

# just to test Django TestCase and Travis CI
class TestSumDjango(TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertNotEqual(sum((1, 2, 2)), 6, "This should not be 6.")

# The next several tests are for testing the creation of the modes
class TestRegion(TestCase):

    def test_region_creation(self):
        northAmerica = Region(name="North America")
        asia = Region(name='Asia')

        self.assertEqual(northAmerica.name, 'North America')
        self.assertEqual(asia.name, 'Asia')

class TestLocation(TestCase):

    def setUp(self):
        self.northAmerica = Region(name='North America')
        self.asia = Region(name='Asia')

    def test_location_creation(self):
        losAngeles = Location(airport="LAX", country="United States", \
                              city="Los Angeles", state="California", \
                              exchange_rate=3.8, cost_of_living=75, \
                              region=self.northAmerica)
        tokyo = Location(airport="Narita Airport", country="Japan", \
                         city="Tokyo", state="Tokyo", \
                         exchange_rate=1.5, cost_of_living=100, region=self.asia)
        self.assertEqual(losAngeles.airport, 'LAX')
        self.assertEqual(losAngeles.country, 'United States')
        self.assertEqual(losAngeles.city, 'Los Angeles')
        self.assertEqual(losAngeles.state, 'California')
        self.assertEqual(losAngeles.exchange_rate, 3.8)
        self.assertEqual(losAngeles.cost_of_living, 75)
        self.assertEqual(losAngeles.region.name, 'North America')
        self.assertEqual(tokyo.airport, 'Narita Airport')
        self.assertEqual(tokyo.country, 'Japan')
        self.assertEqual(tokyo.city, 'Tokyo')
        self.assertEqual(tokyo.state, 'Tokyo')
        self.assertEqual(tokyo.exchange_rate, 1.5)
        self.assertEqual(tokyo.cost_of_living, 100)
        self.assertEqual(tokyo.region.name, 'Asia')

class TestActivity(TestCase):

    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')

        # must save Location objects to be used in ManyToManyField
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(airport="LAX", country="United States", \
                              city="Los Angeles", state="California", \
                              exchange_rate=3.8, cost_of_living=75, \
                              region=northAmerica)
        self.tokyo = Location(airport="Narita Airport", country="Japan", \
                         city="Tokyo", state="Tokyo", \
                         exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

    def test_activity_creation(self):
        shopping = Activity(name="Shopping")

        # must save Flight to be able to add Location objects to it
        shopping.save()
        shopping.locations.add(self.losAngeles)
        shopping.locations.add(self.tokyo)

        self.assertEqual(shopping.name, 'Shopping')

        # use <QueryList>[i] to access individual objects of QueryList
        # maybe implement __str__() method  
        self.assertEqual(shopping.locations.all()[0], self.losAngeles)
        self.assertEqual(shopping.locations.all()[1], self.tokyo)
    
class TestFlight(TestCase):

    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(airport="LAX", country="United States", \
                              city="Los Angeles", state="California", \
                              exchange_rate=3.8, cost_of_living=75, \
                              region=northAmerica)
        self.tokyo = Location(airport="Narita Airport", country="Japan", \
                         city="Tokyo", state="Tokyo", \
                         exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

        # used to avoid Warning about DateTimeField not aware of timezones
        self.timezone = pytz.timezone("America/Los_Angeles")

    def test_flight_creation(self):

        flight = Flight(departure_location=self.losAngeles, destination=self.tokyo,\
                        flight_carrier="Japan Airlines", \
                        departure_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 8, 0, 0, 0)), \
                        arrival_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 20, 0, 0, 0)))
        
        self.assertEqual(flight.departure_location, self.losAngeles)
        self.assertEqual(flight.destination, self.tokyo)
        self.assertEqual(flight.flight_carrier, "Japan Airlines")
        self.assertEqual(flight.departure_time, self.timezone.localize( \
                         datetime.datetime(2020, 5, 11, 8, 0, 0, 0)))
        self.assertEqual(flight.arrival_time, self.timezone.localize( \
                         datetime.datetime(2020, 5, 11, 20, 0, 0, 0)))
        

class TestTrip(TestCase):

    def setUp(self):
        northAmerica = Region(name='North America')
        asia = Region(name='Asia')
        northAmerica.save()
        asia.save()

        self.losAngeles = Location(exchange_rate=3.8, cost_of_living=75, \
                                   region=northAmerica)
        self.tokyo = Location(exchange_rate=1.5, cost_of_living=100, region=asia)
        self.losAngeles.save()
        self.tokyo.save()

        self.timezone = pytz.timezone("America/Los_Angeles")

        self.firstFlight = Flight(departure_location=self.losAngeles, destination=self.tokyo,\
                        flight_carrier="Japan Airlines", \
                        departure_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 8, 0, 0, 0)), \
                        arrival_time=self.timezone.localize( \
                        datetime.datetime(2020, 5, 11, 20, 0, 0, 0)))
        self.secondFlight = Flight(departure_location=self.tokyo, \
                                   destination=self.losAngeles, \
                                   flight_carrier="Japan Airlines", 
                                   departure_time=self.timezone.localize( \
                                   datetime.datetime(2020, 5, 16, 8, 0, 0, 0)), \
                                   arrival_time=self.timezone.localize( \
                                   datetime.datetime(2020, 5, 16, 20, 0, 0, 0)))
        self.firstFlight.save()
        self.secondFlight.save()

    def test_trip_creation(self):
        trip = Trip(name="Trip", budget=1000, cost=500, num_passengers=2, num_bags=4)
        trip.save()
        trip.flights.add(self.firstFlight, self.secondFlight)

        self.assertEqual(trip.name, 'Trip')
        self.assertEqual(trip.budget, 1000)
        self.assertEqual(trip.cost, 500)
        self.assertEqual(trip.flights.all()[0], self.firstFlight)
        self.assertEqual(trip.flights.all()[1], self.secondFlight)
        self.assertEqual(trip.num_passengers, 2)
        self.assertEqual(trip.num_bags, 4)

#Note will have to change from username to email when the user model is fixed
class TestAuthentication(TestCase):

    def setUp(self):
        self.oldUser = User.objects.create_user(username = 'oldAccount', \
                                                email='oldAccount@test.com', \
                                                password='oldPassword10')

    def test_signup_page_url(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 
                                template_name='django_registration/registration_form.html')

    def test_sign_up(self): 

        #self.assertEqual(User.objects.all()[0], newUser)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        response = self.client.post('/accounts/register/', {'username': 'newAccount', \
                                    'email': 'newAccount@test.com', 'password1': 'newPassword10', \
                                    'password2': 'newPassword10'}, follow=True)  
        
        newUser = User.objects.filter(username='newAccount')[0]
        self.assertEqual(newUser.username, 'newAccount')
        self.assertEqual(newUser.email, 'newAccount@test.com')

        self.assertTrue(response.context['user'].is_authenticated)

    def test_login(self):
        self.assertEqual(User.objects.filter(email="oldAccount@test.com")[0], self.oldUser)

        # test for wrong email
        response = self.client.post('/accounts/login/', {'username': 'oldAccount1', \
                                    'password': 'oldPassword10'}, follow=True)      
        self.assertFalse(response.context['user'].is_authenticated)

        # test for wrong password
        response = self.client.post('/accounts/login/', {'username': 'oldAccount', \
                                    'password': 'oldPassword11'})      
        self.assertFalse(response.context['user'].is_authenticated)

        # test for correct email and password
        response = self.client.post('/accounts/login/', {'username': 'oldAccount', \
                                        'password': 'oldPassword10'}, follow=True)      
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):

        self.client.login(username='oldAccount', password='oldPassword10')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        #execute log out
        self.client.post('/accounts/logout/')

        self.assertTrue(self.oldUser.is_authenticated)
        # test for user log out
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

    def test_change_password(self):
        pass
        #self.assertTrue(User.objects.filter(username='oldAccount')[0].check_password('oldPassword10'))

        # change password
        #self.client.post('/profile/', {'new_password':'newPassord10', \
        #                               'confirm_password':'newPassord10'})

        #self.assertTrue(User.objects.filter(username='oldAccount')[0].check_password('newPassword10'))

    def test_save_destination_view_info(self):
        pass

        #fill out destination form

        #save info in destination form

        #test that info has been saved properly

    def test_save_view_flights_view_info(self):
        pass

        #fill out destination form

        #save info in destination form

        #test that info has been saved properly

    def test_load_destination_view_info(self):
        pass
        
        #save info for the destination forms

        #load info back into the destination form

        #test that destination view has been filled properly

    def test_load_view_flights_view_info(self):
        pass

        #save info for the destination forms

        #load info back into the destination form

        #test that view flights view has been filled properly 