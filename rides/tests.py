from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Driver, Ride
from .services import (
    calculate_fare,
    is_driver_available,
    find_nearby_drivers,
    validate_ride,
    can_cancel_ride,
)


class FareCalculationTests(TestCase):

    def test_fare_for_five_km(self):
        fare = calculate_fare(5)

        self.assertEqual(fare, 100)

    def test_fare_for_zero_km(self):
        fare = calculate_fare(0)

        self.assertEqual(fare, 50)

    def test_negative_distance_is_invalid(self):
        with self.assertRaises(ValueError):
            calculate_fare(-5)


class DriverAvailabilityTests(TestCase):

    def test_available_driver(self):

        driver = Driver.objects.create(
            name="Driver 1",
            is_available=True
        )

        self.assertTrue(
            is_driver_available(driver)
        )

    def test_unavailable_driver(self):

        driver = Driver.objects.create(
            name="Driver 2",
            is_available=False
        )

        self.assertFalse(
            is_driver_available(driver)
        )


class NearbyDriverTests(TestCase):

    def test_find_nearby_driver(self):

        driver = Driver.objects.create(
            name="Nearby Driver",
            is_available=True,
            latitude=1,
            longitude=1
        )

        nearby_drivers = find_nearby_drivers(
            [driver],
            latitude=0,
            longitude=0,
            max_distance=2
        )

        self.assertIn(
            driver,
            nearby_drivers
        )

    def test_far_driver_is_not_selected(self):

        driver = Driver.objects.create(
            name="Far Driver",
            is_available=True,
            latitude=10,
            longitude=10
        )

        nearby_drivers = find_nearby_drivers(
            [driver],
            latitude=0,
            longitude=0,
            max_distance=2
        )

        self.assertNotIn(
            driver,
            nearby_drivers
        )

    def test_unavailable_driver_is_not_selected(self):

        driver = Driver.objects.create(
            name="Busy Driver",
            is_available=False,
            latitude=1,
            longitude=1
        )

        nearby_drivers = find_nearby_drivers(
            [driver],
            latitude=0,
            longitude=0,
            max_distance=2
        )

        self.assertNotIn(
            driver,
            nearby_drivers
        )


class RideValidationTests(TestCase):

    def test_valid_ride(self):

        user = User.objects.create_user(
            username="harshitha",
            password="password123"
        )

        result = validate_ride(
            distance_km=5,
            user=user
        )

        self.assertTrue(result)

    def test_ride_without_user_is_invalid(self):

        with self.assertRaises(ValueError):
            validate_ride(
                distance_km=5,
                user=None
            )

    def test_zero_distance_is_invalid(self):

        user = User.objects.create_user(
            username="user1",
            password="password123"
        )

        with self.assertRaises(ValueError):
            validate_ride(
                distance_km=0,
                user=user
            )


class CancellationRuleTests(TestCase):

    def test_requested_ride_can_be_cancelled(self):

        user = User.objects.create_user(
            username="user1",
            password="password123"
        )

        ride = Ride.objects.create(
            user=user,
            distance_km=5,
            status="REQUESTED"
        )

        self.assertTrue(
            can_cancel_ride(ride)
        )

    def test_accepted_ride_can_be_cancelled(self):

        user = User.objects.create_user(
            username="user2",
            password="password123"
        )

        ride = Ride.objects.create(
            user=user,
            distance_km=5,
            status="ACCEPTED"
        )

        self.assertTrue(
            can_cancel_ride(ride)
        )

    def test_ongoing_ride_cannot_be_cancelled(self):

        user = User.objects.create_user(
            username="user3",
            password="password123"
        )

        ride = Ride.objects.create(
            user=user,
            distance_km=5,
            status="ONGOING"
        )

        self.assertFalse(
            can_cancel_ride(ride)
        )

    def test_completed_ride_cannot_be_cancelled(self):

        user = User.objects.create_user(
            username="user4",
            password="password123"
        )

        ride = Ride.objects.create(
            user=user,
            distance_km=5,
            status="COMPLETED"
        )

        self.assertFalse(
            can_cancel_ride(ride)
        )