import datetime
from PyInterrail.config import FORMAT_DATE, FORMAT_HOURS, LOCATION_ID, SERVICE_DATE, SERVICE_TIME, SERVICE_OPERATOR, \
    LOCATION_NAME, SERVICE_ORIGIN, SERVICE_DESTINATION, SERVICE_PRODUCT

"""The module which represents a service."""


class Service:
    """
    A class used to represent a service in a trip.

    ...

    Attributes
    ----------
    origin_id : str
        the id of the origin
    departure_time : str
        the departure time
    departure_date : str
        the departure date
    destination_id: str
        the id of the destination
    arrival_time: str
        the arrival time
    arrival_date: str
        the arrival date
    train_name: str
        the train name
    train_operator: str
        the operator name of the train
    sleeper_train: bool
        the boolean to indicate that the train has beds
    """

    def __init__(self, origin_id: str, departure_time: str, departure_date: str, destination_id: str,
                 arrival_time: str, arrival_date: str, train_name: str, train_operator: str, sleeper_train: bool):
        self.origin_id = origin_id
        self.departure_time = departure_time
        self.departure_date = departure_date
        self.departure_date_object = datetime.datetime.strptime(f"{departure_date}{departure_time}",
                                                                f"{FORMAT_DATE}{FORMAT_HOURS}")
        self.destination_id = destination_id
        self.arrival_time = arrival_time
        self.arrival_date = arrival_date
        self.arrival_date_object = datetime.datetime.strptime(f"{arrival_date}{arrival_time}",
                                                              f"{FORMAT_DATE}{FORMAT_HOURS}")
        self.train_name = train_name
        self.train_operator = train_operator
        self.sleeper_train = sleeper_train

    def __str__(self):
        return f"origin id: {self.origin_id}, departure time: {self.departure_time}, " \
               f"departure date: {self.departure_date}, destination id: {self.destination_id}, " \
               f"arrival time: {self.arrival_time}, arrival date: {self.arrival_date}, " \
               f"train name: {self.train_name}, train operator: {self.train_operator}, " \
               f"sleeper train: {self.sleeper_train}"


def service_from_json(data):
    """
    The method to parse a json to a Service.

    Parameters
    ----------
    data : str
        the json-encoded representation for the service

    Returns
    -------
    Service
        a Service object
    """

    if data is None:
        raise ValueError("Error. Please check the information")

    service = data

    result = Service(origin_id=service.get(SERVICE_ORIGIN, {}).get(LOCATION_ID),
                     departure_time=service.get(SERVICE_ORIGIN, {}).get(SERVICE_TIME),
                     departure_date=service.get(SERVICE_ORIGIN, {}).get(SERVICE_DATE),
                     destination_id=service.get(SERVICE_DESTINATION, {}).get(LOCATION_ID),
                     arrival_time=service.get(SERVICE_DESTINATION, {}).get(SERVICE_TIME),
                     arrival_date=service.get(SERVICE_DESTINATION, {}).get(SERVICE_DATE),
                     train_name=service.get(SERVICE_PRODUCT, {}).get(LOCATION_NAME),
                     train_operator=service.get(SERVICE_PRODUCT, {}).get(SERVICE_OPERATOR), sleeper_train=False)

    for note in [x for x in service.get("Notes", {}).get("Note")]:
        if "sleeper" in note.get("value"):
            result.sleeper_train = True

    return result
