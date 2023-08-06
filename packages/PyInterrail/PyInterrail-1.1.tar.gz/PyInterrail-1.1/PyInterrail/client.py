"""The module with the main functions."""

import requests
import datetime
from PyInterrail.stop_location import locations_from_json
from PyInterrail.config import URL_GET_LOCATIONS, URL_GET_TRIPS, FORMAT_DATE, FORMAT_HOURS
from PyInterrail.trip import trips_from_json


def get_locations(name: str):
    """
    The method to call Interrail server for list of locations.

    Parameters
    ----------
    name : str
        the name of the location

    Returns
    -------
    list
        a list of StopLocations
    """

    params = {'input': name}
    response = requests.get(URL_GET_LOCATIONS, params)
    return locations_from_json(response.json())


def get_trips(origin_id: str, destination_id: str, time: str, date: str):
    """
    The method to call Interrail server for list of trips.

    Parameters
    ----------
    origin_id : str
        the id of the origin location
    destination_id : str
        the id of the destination location
    time : str
        the time of the departure
    date : str
        the date of the departure

    Returns
    -------
    list
        a list of Trips
    """
    try:
        datetime.datetime.strptime(date, FORMAT_DATE)
    except ValueError:
        raise ValueError("Incorrect date format, should be in format YYYY-MM-DD ")
    try:
        datetime.datetime.strptime(time, FORMAT_HOURS)
    except ValueError:
        raise ValueError("Incorrect time format, should be in format HH:MM:SS")

    params = {'originId': origin_id, 'destId': destination_id, 'date': date, 'time': time}
    response = requests.get(URL_GET_TRIPS, params)
    return trips_from_json(response.json())