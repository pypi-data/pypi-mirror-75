"""
Dublin Bus RTPI REST API client
"""

import json
import requests

_RESOURCE = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation"


class APIError(Exception):
    """An API Error Exception"""

    pass


class DublinBusRTPI:
    """Class to interact with the Dublin Bus RTPI API"""

    def __init__(self, stopid=None, route=None):
        """
        :param stopid: Dublin bus stop id (default None).
        :type stopid: int
        :param route: Dublin bus route number (default None)
        :type route: int
        """
        self.stopid = stopid
        self.route = route

    def raw_rtpi_data(self):
        """
        Method to get the raw data from Dublin Bus RTPI API
        :returns: Return a json object containing Dublin Bus RTPI data
        :rtype: json
        """
        params = {"stopid": self.stopid, "format": "json"}

        try:
            response = requests.get(_RESOURCE, params, timeout=10)

        except (
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects,
        ) as error_name:
            raise ConnectionError(str(error_name))

        try:
            results = json.loads(response.text)
            results = response.json()

        except ValueError:
            raise APIError("JSON parse failed.")

        if results["errorcode"] not in ["0", "1"]:
            raise APIError(results["errormessage"])

        return results

    def bus_timetable(self):
        """
        Method to return a minimal timetable data
        :return: List of the dictioneries of the due bus routes.
        :rtype: list

        eg:
         [{'due_in': '5', 'route': '67'},
         {'due_in': '12', 'route': '66B'},
         {'due_in': '13', 'route': '25A'},
         {'due_in': '21', 'route': '66'}]
        """
        timetable = []
        raw_data = self.raw_rtpi_data()

        for item in raw_data["results"]:
            duetime = item.get("duetime")
            route = item.get("route")
            if not self.route:
                timetable.append({"due_in": duetime, "route": route})
            else:
                if self.route == route:
                    timetable.append({"due_in": duetime, "route": route})
        return timetable
