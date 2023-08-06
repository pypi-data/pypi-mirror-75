"""The module which represents a trip."""
from PyInterrail.service import Service, service_from_json


class Trip:
    """
    A class used to represent the trip.

    ...

    Attributes
    ----------
    num_services : int
        the id of the stop location
    services_list : list
        a list of Services in order
    """

    def __init__(self, num_services: int, services_list: list):
        self.num_services = num_services
        self.services_list = services_list

    def __str__(self):
        return f"number of services: {self.num_services}, services_list: {self.services_list}"


def trips_from_json(data):
    """
    The method to parse a json to list of trips.

    Parameters
    ----------
    data : str
        the json-encoded representation for the trip

    Returns
    -------
    list
        a list of Trips
    """

    if data is None:
        raise ValueError("Error")

    trips = data.get("Trip")

    if trips is None:
        raise ValueError("Error")

    results = []
    for trip in trips:

        result = Trip(num_services=0, services_list=[])

        services = trip.get("LegList").get("Leg")
        for service in services:
            result.services_list.append(service_from_json(service))

        result.num_services = len(result.services_list)

        results.append(result)
    return results
