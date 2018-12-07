# Splunk Search Addon for MISP

## Installation
1. Place the app under $SPLUNK_HOME/etc/apps/TA-MISP
2. Run the following to install the python2 MISP pymisp package
```
pip2 install -r TA-MISP/bin/requirements.txt
```
3. Configure a url (ie: https://misp.example.net:8000) and API Key in the app's setup screen. You must set the Realm field to "MISP".


## Usage
This addon for Splunk contains a custom search command called "mispsearch". The command can take a combination of event= and tag= parameters where multiple events and tags can be specified using comma seperated lists to return results from all matching MISP events. For example:
```
| mispsearch event="5,21" tags="tlp:green"
```

The above query would return indicators from events 5, 21 and any event with a tag of "tlp:green". So, these two parameters have an implicit "OR" between them and can be used to match a variety of different events based on their id and tags. Any events that match any of the event ids or tags given by these two parameters will be returned.

To filter search results, the category, type and to_ids parameters can be used. These will filter out the list of search results to only those events that match the criteria supplied by these paramters. For example:
```
| mispsearch event="3231" type="url,ip-src,ip-dst" to_ids=True
```

The above would only match events from event 3231 where the attribute type is url, ip-src or ip-dst and the to_ids flag has been set. So there is an implicit "AND" between these parameters where only attributes matching each of these criteria will be returned.

Finally, the search parameter can be specified to return results in a format that can be easily used in a subsearch. For example:
```
| mispsearch event="3231" type="url,ip-src,ip-dst" to_ids=True search=True | format
```

Wrapping the above in a subsearch (square brackets) will result in the results being searched within Splunk. For example:
```
index=proxy sourcetype=bluecoat [| mispsearch event="3231" type="url" search=True | format]
```
