from math import sqrt


BASE_FARE = 50
FARE_PER_KM = 10
MAX_CANCELLATION_DISTANCE = 0
CANCELLATION_ALLOWED_STATUSES = [
    'REQUESTED',
    'ACCEPTED',
]


def calculate_fare(distance_km):
    """
    Calculate ride fare.
    """

    if distance_km < 0:
        raise ValueError("Distance cannot be negative")

    return BASE_FARE + (distance_km * FARE_PER_KM)


def is_driver_available(driver):
    """
    Check whether a driver is available.
    """

    return driver.is_available


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Simple distance calculation for testing purposes.
    """

    return sqrt(
        (lat2 - lat1) ** 2 +
        (lon2 - lon1) ** 2
    )


def find_nearby_drivers(drivers, latitude, longitude, max_distance=10):
    """
    Return available drivers within the given distance.
    """

    nearby_drivers = []

    for driver in drivers:

        if not driver.is_available:
            continue

        distance = calculate_distance(
            latitude,
            longitude,
            driver.latitude,
            driver.longitude
        )

        if distance <= max_distance:
            nearby_drivers.append(driver)

    return nearby_drivers


def validate_ride(distance_km, user):
    """
    Validate whether a ride can be created.
    """

    if user is None:
        raise ValueError("User is required")

    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero")

    return True


def can_cancel_ride(ride):
    """
    Check whether a ride can be cancelled.
    """

    return ride.status in CANCELLATION_ALLOWED_STATUSES