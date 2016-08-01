from __future__ import absolute_import
from __future__ import print_function
import fedmsg
import fedmsg.meta
import calendar
import json
import requests
from collections import Counter

# This dictionary will be passed as param to requests later
values = dict()
values['user'] = None
values['delta'] = 604800
values['rows_per_page'] = 100
values['not_category'] = 'meetbot'
values['topic'] = 'org.fedoraproject.prod.fas.user.create'
values['page'] = 1
values['size'] = 'small'
category = ''
start = ''
group = ''
end = ''
logs = False
weeks = 0
filename = ''
baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
unicode_json = {}


def return_epoch(time):
    if time == '':
        return ''
    tup = map(int, time.split('/'))
    l = (tup[2], tup[0], tup[1], 0, 0, 0)
    epochs = calendar.timegm(l)
    return (int(epochs))

# Checks if unicode_json is empty, pulls datagrepper values and returns
# the json


def return_json():
    global unicode_json
    total_pages = 1

    # Only pull the values from datagrepper if it's the first run
    if True:
        if start != '' and end != '':
            values['start'] = return_epoch(start)
            values['end'] = return_epoch(end)
            del(values['delta'])


        # If the user value is passed as all, remove it from the dict and pass
        # arguments
        del(values['user'])
        response = requests.get(baseurl, params=values)
        unicode_json = json.loads(response.text)
        total_pages = unicode_json['pages']
        print ("Total pages found : " + str(total_pages))
        total = total_pages
        # If multiple pages exist, get them all.
        while total_pages > 0:
            print("In here!!!\n", values)
            print("  [*] Loading Page " + str(values['page']) + "/" + str(total))
            values['page'] += 1
            response = requests.get(baseurl, params=values)
            paginated_json = json.loads(response.text)
            # Pull data from multiple pages and append them to the main JSON
            for activity in paginated_json['raw_messages']:
                unicode_json['raw_messages'].append(activity)
            total_pages -= 1
        values['page'] = 1
    return unicode_json

# Analyzes the JSON and return categories present as a list.




def return_users():
    user_list = dict()
    unicode_json = return_json()
    print("[*] Identifying Users..")
    for activity in unicode_json['raw_messages']:
	try:
        	print(activity['msg']['user'])
        	user_list[activity['msg']['user']] = activity['timestamp']
	except TypeError:
		user_list[activity['msg']['user']['username']] = activity['timestamp']
        print(len(user_list.keys()))
    json.dump(user_list, open(filename + '.json','w'))
