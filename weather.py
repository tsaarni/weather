#!/usr/bin/env python3

import requests
from lxml import etree
import json

# https://opendata.fmi.fi/meta?observableProperty=observation
series_metadata = {'obs-obs-1-1-t2m':      {'name': 'Air temperature'         , 'uom': 'degC'},
                   'obs-obs-1-1-ws_10min': {'name': 'Wind speed'              , 'uom': 'm/s' },
                   'obs-obs-1-1-wg_10min': {'name': 'Gust speed'              , 'uom': 'm/s' },
                   'obs-obs-1-1-wd_10min': {'name': 'Wind direction'          , 'uom': 'deg' },
                   'obs-obs-1-1-rh':       {'name': 'Relative humidity'       , 'uom': '%'   },
                   'obs-obs-1-1-td':       {'name': 'Dew-point temperature'   , 'uom': 'degC'},
                   'obs-obs-1-1-r_1h':     {'name': 'Precipitation amount'    , 'uom': 'mm'  },
                   'obs-obs-1-1-ri_10min': {'name': 'Precipitation intensity' , 'uom': 'mm/h'},
                   'obs-obs-1-1-snow_aws': {'name': 'Snow depth'              , 'uom': 'cm'  },
                   'obs-obs-1-1-p_sea':    {'name': 'Pressure (msl)'          , 'uom': 'hPa' },
                   'obs-obs-1-1-vis':      {'name': 'Horizontal visibility'   , 'uom': 'm'   },
                   'obs-obs-1-1-n_man':    {'name': 'Cloud amount'            , 'uom': '1/8' },
                   'obs-obs-1-1-wawa':     {'name': 'Present weather (auto)'  , 'uom': ''    }
}


# http://catalog.fmi.fi/geonetwork/srv/fin/catalog.search#/metadata/d6878046-65f3-4270-a38c-6ea8586314cd
url = 'https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi%3A%3Aobservations%3A%3Aweather%3A%3Atimevaluepair&crs=EPSG%3A%3A3067&fmisid=100949'
r = requests.get(url)

#doc = etree.parse('artukainen.xml')
#root = doc.getroot()
root = etree.fromstring(r.content)

time_series = root.xpath('//wml2:MeasurementTimeseries', namespaces=root.nsmap)
output = {'Weather station': 'Turku Artukainen', 'measurements': []}

for s in time_series:
    measured_values = []
    for e in s.xpath('.//wml2:MeasurementTVP', namespaces=root.nsmap):
        measurement = {'time':  e.find('{http://www.opengis.net/waterml/2.0}time').text,
                       'value': e.find('{http://www.opengis.net/waterml/2.0}value').text}
        measured_values.append(measurement)

    entry = series_metadata[s.attrib['{http://www.opengis.net/gml/3.2}id']]
    entry['values'] = measured_values
    output['measurements'].append(entry)

print(json.dumps(output, indent=4, sort_keys=True))
