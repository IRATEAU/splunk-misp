#!/usr/bin/env python
from __future__ import print_function

import re
import sys
import csv
import json

# We need to import from the OS' python packages directory
sys.path.append('/usr/lib/python2.7/site-packages')
from pymisp import PyMISP

misp_url = "http://misp.example.net"
misp_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
verifyCert = False

DEFAULT_FIELDS = ["category", "type", "value", "comment", "to_ids"]
SEARCH_FIELDS = ["search"]

def main():
    event_ids = []
    event_tags = None
    search = False
    attr_type = None
    attr_category = None
    attr_to_ids = None

    # Parse parameters
    for param in sys.argv:
        if param.startswith('event='):
            for event_id in param.split('=')[1].split(','):
                event_ids.append(event_id)

        if param.startswith('tag='):
            event_tags = re.split('tag=', param)[1].split(',')

        if param.startswith('search='):
            search = param.split('=')[1]

        if param.startswith('type='):
            attr_type = param.split('=')[1].split(',')

        if param.startswith('category='):
            attr_category = param.split('=')[1].split(',')

        if param.startswith('to_ids='):
            attr_to_ids = param.split('=')[1]

    if not event_ids and not event_tags:
        print("You must specify one or more arguements to either event= tag= or both")
        exit(-1)

    misp = PyMISP(misp_url, misp_apikey, verifyCert, 'json')

    if search:
        writer = csv.DictWriter(sys.stdout, fieldnames=SEARCH_FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=DEFAULT_FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()

    if event_tags:
        events = misp.search(tags=event_tags)
        for event in events.get('response'):
            event_ids.append(event.get('Event').get('id'))

    for event_id in event_ids:
        event = misp.get_event(event_id)
        
        if event.get('errors'):
            print('Error: {}'.format(event.get('message')))

#        print(json.dumps(event))

        for attribute in event['Event']['Attribute']:
            # Filter by indicator
            if attr_type and not attribute.get('type') in attr_type:
                continue
            
            # Filter by category
            if attr_category and not attribute.get('category') in attr_category:
                continue
            
            # Filter by to_ids
            if attr_to_ids and str(attribute.get('to_ids')) != attr_to_ids:
                continue

            if search:
                row = {}
                row["search"] = attribute.get('value')
                writer.writerow(row)
            else:
                row = {}
                row["category"] = attribute.get('category')
                row["type"] = attribute.get('type')
                row["value"] = attribute.get('value')
                row["comment"] = attribute.get('comment')
                row["to_ids"] = attribute.get('to_ids')
                writer.writerow(row)

        for obj in event['Event']['Object']:
            for attribute in obj['Attribute']:
                # Filter by indicator
                if attr_type and not attribute.get('type') in attr_type:
                    continue
                    
                # Filter by category
                if attr_category and not attribute.get('category') in attr_category:
                    continue
                        
                # Filter by to_ids
                if attr_to_ids and str(attribute.get('to_ids')) != attr_to_ids:
                    continue
                        
                if search:
                    row = {}
                    row["search"] = attribute.get('value')
                    writer.writerow(row)
                else:
                    row = {}
                    row["category"] = attribute.get('category')
                    row["type"] = attribute.get('type')
                    row["value"] = attribute.get('value')
                    row["comment"] = attribute.get('comment')
                    row["to_ids"] = attribute.get('to_ids')
                    writer.writerow(row)
main()
