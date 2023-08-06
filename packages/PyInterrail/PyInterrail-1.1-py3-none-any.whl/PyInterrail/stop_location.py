"""The module which represents a stop location."""

import json

from PyInterrail.config import LOCATION_ID, LOCATION_NAME, LOCATION_LONGITUDE, LOCATION_LATITUDE


class StopLocation:
    """
    A class used to represent the stop locations.

    ...

    Attributes
    ----------
    id : str
        the id of the stop location
    name : str
        the name of the stop location
    lon : float
        the longitude of the stop location
    lat: float
        the latitude of the stop location
    """

    def __init__(self, id: str, name: str, lon: float, lat: float):
        self.id = id
        self.name = name
        self.lon = lon
        self.lat = lat

    def __str__(self):
        return f"id: {self.id}, name: {self.name},  long: {self.lon}, lat : {self.lat}"


def locations_from_json(data):
    """
    The method to parse a json to a list of StopLocation.

    Parameters
    ----------
    data : str
        the json-encoded representation for the stop locations

    Returns
    -------
    list
        a list of StopLocations
    """

    if data is None:
        raise ValueError("Error")

    locations = data.get("stopLocationOrCoordLocation")

    if locations is None:
        raise ValueError("Error")

    results = []
    for location in [x.get("StopLocation") for x in locations]:
        result = StopLocation(id=location.get(LOCATION_ID), name=location.get(LOCATION_NAME),
                              lon=location.get(LOCATION_LONGITUDE),
                              lat=location.get(LOCATION_LATITUDE))
        results.append(result)
    return results
