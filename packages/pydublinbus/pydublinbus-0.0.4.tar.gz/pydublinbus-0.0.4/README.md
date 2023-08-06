# PyDublinBus

Python Interface for the Dublin Bus RTPI API.

## Example usage

#### Time table:

```
>>> from pydublinbus import DublinBusRTPI
>>> mybus=DublinBusRTPI(stopid='312')
>>> mybus.bus_timetable()
[{'due_in': '6', 'route': '26'},
 {'due_in': '8', 'route': '25B'},
 {'due_in': '15', 'route': '67'},
 {'due_in': '22', 'route': '66B'},
 {'due_in': '23', 'route': '25A'},
 {'due_in': '31', 'route': '66A'},
 {'due_in': '38', 'route': '25B'},
 {'due_in': '39', 'route': '66'},
 {'due_in': '41', 'route': '26'},
 {'due_in': '41', 'route': '25'},
 {'due_in': '45', 'route': '67'},
 {'due_in': '46', 'route': '25A'}]
```

#### Time table filtered by route

```
>>> from pydublinbus import DublinBusRTPI
>>> mybus=DublinBusRTPI(stopid='312', route='25A')
>>> from pprint import pprint
>>> mybus.bus_timetable()
[{'due_in': '20', 'route': '25A'},
 {'due_in': '43', 'route': '25A'}]

```

#### Raw json data:

```
>>> from pydublinbus import DublinBusRTPI
>>> mybus=DublinBusRTPI(stopid='312')
>>> mybus.get_rtpi_data()
```
