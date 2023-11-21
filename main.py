import requests
import json
from itertools import permutations
import itertools
from datetime import datetime, timedelta
from datetime import date
from flask import Flask, render_template, request
import re

travel_time_cache = {}
api_key = "SECRET API KEY"

def building_to_address(building):
    building_mapping = {
        #class buildings
        'Angel Hall': '435 S State St, Ann Arbor, MI 48109',
        'Mason Hall': '419 S State St Mason Hall, Ann Arbor, MI 48109',
        'Michigan Union': '530 S State St, Ann Arbor, MI 48109',
        'Baits II': '1440 Hubbard Ann Arbor, Michigan 48109',
        'Alumni Memorial Hall': '525 S State St, Ann Arbor, MI 48109',
        'Architecture Building': '2000 Bonisteel Blvd, Ann Arbor, MI 48109',
        'Barbour Gymnasium': '700 N University Ave, Ann Arbor, MI 48109',
        'Burton Memorial Tower': '230 N Ingalls St, Ann Arbor, MI 48109',
        'Clements Library': '909 S University Ave, Ann Arbor, MI 48109',
        'Couzens Hall': '1300 E Ann St, Ann Arbor, MI 48109',
        'Dana Building': '440 Church St, Ann Arbor, MI 48109',
        'Dental Building': '1011 N University Ave, Ann Arbor, MI 48109',
        'East Engineering Building': '505 E University Ave, Ann Arbor, MI 48109',
        'East Hall': '530 Church St, Ann Arbor, MI 48109',
        'Economics Building': '238 Lorch Hall, 611 Tappan Ave, Ann Arbor, MI 48109',
        'Electrical Engineering & Computer Science': '1301 Beal Ave, Ann Arbor, MI 48109',
        'Exhibit Museum': '1109 Geddes Ave, Ann Arbor, MI 48109',
        'General Library': '913 S University Ave, Ann Arbor, MI 48109',
        'Helen Newberry Residence': '432 S State St, Ann Arbor, MI 48109',
        'Hill Auditorium': '825 N University Ave, Ann Arbor, MI 48109',
        'Hutchins Hall': '625 S State St, Ann Arbor, MI 48109',
        'Kellogg Institute': '1150 W Medical Center Dr, Ann Arbor, MI 48109',
        'Lane Hall': '204 S State St, Ann Arbor, MI 48109',
        'Lawyers Club': '551 S State St, Ann Arbor, MI 48109',

        'Art & Architecture Building': '2000 Bonisteel Blvd, Ann Arbor, MI 48109',
        'Blanch Anderson Moore Hall, School of Music': '1100 Baits Dr., Ann Arbor, MI, 48109',
        'Bob and Betty Beyster Building': '2260 Hayward St Ann Arbor, MI 48109',
        'Biological Science Building': '1105 North University Avenue, Ann Arbor, MI 48109',
        'Central Campus Classroom Bldg': '1225 Geddes Ave. Ann Arbor, MI 48109',
        'Chemistry Building': '930 University Ave, Ann Arbor, MI 48109',
        'Dana Building (School of Environment & Sustainability)': '440 Church St, Ann Arbor, MI 48109',
        'Dance Building': '1000 Baits Dr, Ann Arbor, MI 48109',
        'Duderstadt Center': '2281 Bonisteel Blvd, Ann Arbor, MI 48109',
        'Dow Engineering Building': '2300 Hayward St, Ann Arbor, MI 48109',
        'Electrical Engineering and Computer Science Building': '301 Beal Ave, Ann Arbor, MI 48109',
        'Francois-Xavier Bagnoud Building': '1320 Beal Ave, Ann Arbor, MI 48109',
        'Gorguze Family Laboratory': '2609 Draper Dr Ann Arbor, MI 48109',
        'G. G. Brown Laboratory': '2350 HAYWARD ST Ann Arbor, MI 48109',
        'Haven Hall': '505 STATE ST Ann Arbor, MI 48109',
        'Hutchins Hall': '625 S State St, Ann Arbor, MI 48109',
        'Modern Languages Building': '812 E Washington St, Ann Arbor, MI 48104',
        'Industrial and Operations Engineering Building': '1891 IOE Building 1205, Beal Ave, Ann Arbor, MI 48109',
        'Institute for Social Research': '426 Thompson St, Ann Arbor, MI 48104',
        'Jeffries Hall, Law School': '701 S State St, Ann Arbor, MI 48104',

        #dorms
        'Baits II': '1440 Hubbard Rd, Ann Arbor, MI 48109',
        'Betsy Barbour': '420 S State St, Ann Arbor, MI 48109',
        'Bursley Hall': '1931 Duffield St, Ann Arbor, MI 48109',
        'Couzens Hall': '1300 E Ann St, Ann Arbor, MI 48109',
        'East Quadrangle': '701 E University Ave, Ann Arbor, MI 48109',
        'Fletcher Hall': '915 Sybil St, Ann Arbor, MI 48104',
        'Helen Newberry': '432 S State St, Ann Arbor, MI 48109',
        'Henderson House': '1330 Hill St, Ann Arbor, MI 48104',
        'Martha Cook Building': '906 S University Ave, Ann Arbor, MI 48109',
        'Mary Markley Hall': '1425 Washington Heights, Ann Arbor, MI 48109',
        'Mosher-Jordan Hall': '200 Observatory St, Ann Arbor, MI 48109',
        'North Quadrangle': '105 S State St, Ann Arbor, MI 48109',
        'Oxford Houses': '627 Oxford Rd, Ann Arbor, MI 48104',
        'South Quadrangle': '600 E Madison St, Ann Arbor, MI 48109',
        'Stockwell Hall': '324 S Observatory St, Ann Arbor, MI 48109',
        'West Quadrangle & Cambridge House': '541 Thompson St, Ann Arbor, MI 48109'
    }

    return building_mapping[building]

def address_to_building(address):
    address_mapping = {
        '435 S State St, Ann Arbor, MI 48109': 'Angel Hall',
        '419 S State St Mason Hall, Ann Arbor, MI 48109': 'Mason Hall',
        '530 S State St, Ann Arbor, MI 48109': 'Michigan Union',
        '1440 Hubbard Ann Arbor, Michigan 48109': 'Baits II',
        '525 S State St, Ann Arbor, MI 48109': 'Alumni Memorial Hall',
        '2000 Bonisteel Blvd, Ann Arbor, MI 48109': 'Architecture Building',
        '700 N University Ave, Ann Arbor, MI 48109': 'Barbour Gymnasium',
        '230 N Ingalls St, Ann Arbor, MI 48109': 'Burton Memorial Tower',
        '909 S University Ave, Ann Arbor, MI 48109': 'Clements Library',
        '1300 E Ann St, Ann Arbor, MI 48109': 'Couzens Hall',
        '440 Church St, Ann Arbor, MI 48109': 'Dana Building',
        '1011 N University Ave, Ann Arbor, MI 48109': 'Dental Building',
        '505 E University Ave, Ann Arbor, MI 48109': 'East Engineering Building',
        '530 Church St, Ann Arbor, MI 48109': 'East Hall',
        '238 Lorch Hall, 611 Tappan Ave, Ann Arbor, MI 48109': 'Economics Building',
        '1301 Beal Ave, Ann Arbor, MI 48109': 'Electrical Engineering & Computer Science',
        '1109 Geddes Ave, Ann Arbor, MI 48109': 'Exhibit Museum',
        '913 S University Ave, Ann Arbor, MI 48109': 'General Library',
        '432 S State St, Ann Arbor, MI 48109': 'Helen Newberry Residence',
        '825 N University Ave, Ann Arbor, MI 48109': 'Hill Auditorium',
        '625 S State St, Ann Arbor, MI 48109': 'Hutchins Hall',
        '1150 W Medical Center Dr, Ann Arbor, MI 48109': 'Kellogg Institute',
        '204 S State St, Ann Arbor, MI 48109': 'Lane Hall',
        '551 S State St, Ann Arbor, MI 48109': 'Lawyers Club',

        '2000 Bonisteel Blvd, Ann Arbor, MI 48109': 'Art & Architecture Building',
        '1100 Baits Dr., Ann Arbor, MI, 48109': 'Blanch Anderson Moore Hall, School of Music',
        '2260 Hayward St Ann Arbor, MI 48109': 'Bob and Betty Beyster Building',
        '1105 North University Avenue, Ann Arbor, MI 48109': 'Biological Science Building',
        '1225 Geddes Ave. Ann Arbor, MI 48109': 'Central Campus Classroom Bldg',
        '930 University Ave, Ann Arbor, MI 48109': 'Chemistry Building',
        '440 Church St, Ann Arbor, MI 48109': 'Dana Building (School of Environment & Sustainability)',
        '1000 Baits Dr, Ann Arbor, MI 48109': 'Dance Building',
        '2281 Bonisteel Blvd, Ann Arbor, MI 48109': 'Duderstadt Center',
        '2300 Hayward St, Ann Arbor, MI 48109': 'Dow Engineering Building',
        '301 Beal Ave, Ann Arbor, MI 48109': 'Electrical Engineering and Computer Science Building',
        '1320 Beal Ave, Ann Arbor, MI 48109': 'Francois-Xavier Bagnoud Building',
        '2609 Draper Dr Ann Arbor, MI 48109': 'Gorguze Family Laboratory',
        '2350 HAYWARD ST Ann Arbor, MI 48109': 'G. G. Brown Laboratory',
        '505 STATE ST Ann Arbor, MI 48109': 'Haven Hall',
        '625 S State St, Ann Arbor, MI 48109': 'Hutchins Hall',
        '812 E Washington St, Ann Arbor, MI 48104': 'Modern Languages Building',
        '1891 IOE Building 1205, Beal Ave, Ann Arbor, MI 48109': 'Industrial and Operations Engineering Building',
        '426 Thompson St, Ann Arbor, MI 48104': 'Institute for Social Research',
        '701 S State St, Ann Arbor, MI 48104': 'Jeffries Hall, Law School',

        '1440 Hubbard Rd, Ann Arbor, MI 48109': 'Baits II',
        '420 S State St, Ann Arbor, MI 48109': 'Betsy Barbour',
        '1931 Duffield St, Ann Arbor, MI 48109': 'Bursley Hall',
        '1300 E Ann St, Ann Arbor, MI 48109': 'Couzens Hall',
        '701 E University Ave, Ann Arbor, MI 48109': 'East Quadrangle',
        '915 Sybil St, Ann Arbor, MI 48104': 'Fletcher Hall',
        '432 S State St, Ann Arbor, MI 48109': 'Helen Newberry',
        '1330 Hill St, Ann Arbor, MI 48104': 'Henderson House',
        '906 S University Ave, Ann Arbor, MI 48109': 'Martha Cook Building',
        '1425 Washington Heights, Ann Arbor, MI 48109': 'Mary Markley Hall',
        '200 Observatory St, Ann Arbor, MI 48109': 'Mosher-Jordan Hall',
        '105 S State St, Ann Arbor, MI 48109': 'North Quadrangle',
        '627 Oxford Rd, Ann Arbor, MI 48104': 'Oxford Houses',
        '600 E Madison St, Ann Arbor, MI 48109': 'South Quadrangle',
        '324 S Observatory St, Ann Arbor, MI 48109': 'Stockwell Hall',
        '541 Thompson St, Ann Arbor, MI 48109': 'West Quadrangle & Cambridge House'
    }

    return address_mapping[address]

def specific_travel_time(dorm_loc, schedule):
    #add error function
    total_times = [0, 0, 0, 0, 0]
    daily_classes = {'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': []}
    idx = 0
    while idx < len(schedule):
        _, start,  days, loc = schedule[idx:idx +4]
        print(days)
        print("LOC", loc)
        days = days.lower().strip().split(", ")
        idx += 4
        for day in days:
            daily_classes[day].append((loc,  start))

    idx = 0
    for _, class_info in daily_classes.items():
        origin = dorm_loc
        class_info = sorted(class_info, key=lambda x: x[1])
        for class0 in class_info:
            total_times[idx] += get_travel_time(building_to_address(origin), building_to_address(class0[0]))
            origin = class0[0]
        idx+=1
    print(total_times)
    return int(sum(total_times))

def error_exists(section):
    days = {'mon','tue', 'wed',  'thu', 'fri'}

    if any(day not in days for day in section[3]):
        return True, ["ERROR", "ERROR: 'Days' are incorrectly formatted."]
    if not section[2].replace('.', '', 1).isdigit():
        return True, ["ERROR", "ERROR: 'Duration' is incorrectly formatted."]
    if not section[4].replace('.', '', 1).isdigit():
        return True, ["ERROR", "ERROR: 'Credits' is incorrectly formatted."]

    return False, []

def get_travel_time(origin, destination):
    if origin == destination:
        return 0

    if (origin, destination) in travel_time_cache:
        return travel_time_cache[(origin, destination)]

    base_url = "https://maps.googleapis.com/maps/api/directions/json?"

    transit_modes = ['transit', 'walking']
    shortest_time = float('inf')

    for mode in transit_modes:
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "key": api_key,
            "transit_mode": "bus" if mode == "transit" else None
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            route = data['routes'][0]
            total_time = sum([leg['duration']['value'] for leg in route['legs']])

            if total_time < shortest_time:
                shortest_time = total_time
        else:
            print("Error: " + data['status'])
            print(origin)
            print(destination)
            return float('inf') 

    travel_time_cache[(origin, destination)] = int(shortest_time / 60)
    return travel_time_cache[(origin, destination)]

def total_travel_time(dorm_loc, schedule):
    total_times = [0, 0, 0, 0, 0]
    daily_classes = {'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': []}

    for class_info in schedule:
        _,(loc, start, _, days, _, _) = class_info
        for day in days:
            daily_classes[day].append((loc,  start))

    idx = 0
    for _, class_info in daily_classes.items():
        origin = dorm_loc
        class_info = sorted(class_info, key=lambda x: x[1])
        for class0 in class_info:
            total_times[idx] += get_travel_time(origin, class0[0])
            origin = class0[0]
        idx+=1

    return total_times


def str_to_time(time_str):
    return datetime.strptime(time_str, '%H:%M').time()

def str_to_delta(delta_str):
    hours = float(delta_str)
    total_minutes = int(hours * 60)
    return timedelta(minutes=total_minutes)

def valid_times(schedule, earliest_time, latest_time):
    for _, (_, start_time, _, _, dur, _) in schedule:
        date_today  = datetime.combine(date.today(), start_time)
        end_time = (date_today + timedelta(hours=dur)).time()

        if start_time < earliest_time or end_time > latest_time:
            return False

    return True

def valid_creds(schedule, min_creds, max_creds):
    total_creds = sum(creds for _, (_, _, creds, _, _, _) in schedule)
    return min_creds <= total_creds <= max_creds

def is_conflict(schedule, get_travel_time):
    days = ['mon','tue', 'wed',  'thu', 'fri']

    for day in days:
        day_schedule = [class_info for class_info in schedule if day in class_info[1][3]]

        for i in range(len(day_schedule) - 1):
            if not day_schedule or len(day_schedule) == 1:
                continue
            _, (loc1, time1, _, days1, dur1, _) = day_schedule[i]
            _, (loc2, time2, _, days2, dur2, _) = day_schedule[i + 1]

            if time1 >= time2:
                return True

            start1, start2 =time1, time2

            start1_datetime = datetime.combine(datetime.today(), start1)
            start2_datetime = datetime.combine(datetime.today(), start2)

            end1 = (start1_datetime + str_to_delta(dur1)).time()
            end1_datetime = datetime.combine(datetime.today(), end1)

            # Subtract 10 minutes
            end1_datetime -= timedelta(minutes=10)
            end1 = end1_datetime.time()

            if end1 > start2 or end1_datetime + timedelta(minutes=(get_travel_time(loc1, loc2))) > start2_datetime:
                return True
    return False

def generate_all_schedules(classes, min_creds, max_creds,earliest, latest, get_travel_time):
    valid_schedules = set()

    def helper(schedule, remaining_classes):
        if valid_times(schedule, earliest, latest) and valid_creds(schedule, min_creds, max_creds) and not is_conflict(schedule, get_travel_time):
            # Sort the classes within a day and add the sorted schedule to the set of valid schedules
            sorted_schedule = sorted(schedule, key=lambda x: (x[1][3], x[1][1]))
            valid_schedules.add(tuple((class_name, (info[0], info[1], info[2], tuple(info[3]), info[4], info[5])) for class_name, info in sorted_schedule))

        for class_name, sections in remaining_classes.items():
            for section in sections:
                new_schedule = schedule + [(class_name, section)]
                if not is_conflict(new_schedule, get_travel_time):
                    helper(new_schedule, {k: v for k, v in remaining_classes.items() if k != class_name})

    helper([], classes)

    for i in range(len(classes)):
        for subset in itertools.combinations(classes, i):
            subset_classes = {k: classes[k] for k in subset}
            helper([], subset_classes)

    return [list((class_name, (info[0], info[1], info[2], list(info[3]), info[4], info[5])) for class_name, info in schedule) for schedule in valid_schedules]

def sort_priority(classes, min_creds, max_creds, earliest, latest, get_travel_time, dorm_loc, num_classes, friday_off):
    special_schedules = []
    valid_schedules = generate_all_schedules(classes, min_creds, max_creds, earliest, latest, get_travel_time)

    top_no_friday_schedules = []
    top_schedules = []

    if friday_off:
        special_schedules = [schedule for schedule in valid_schedules if all('fri' not in info[3] for class_name, info in schedule)]
        valid_schedules = [schedule for schedule in valid_schedules if any('fri' in info[3] for class_name, info in schedule)]

    if not valid_schedules and not special_schedules:
        return []

    if valid_schedules:
        top_schedules = [valid_schedules[0]]
        valid_schedules.pop(0)
    if special_schedules:
        top_no_friday_schedules = [special_schedules[0]]
        special_schedules.pop(0)

    for schedule in special_schedules:
        sum_info = sum(info[5] for class_name, info in schedule) / sum(info[2] for class_name, info in schedule) #sum of priority points/ sum of num_credits
        inserted = False

        for i in range(len(top_no_friday_schedules)):
            if sum_info < sum(info[5] for class_name, info in top_no_friday_schedules[i]) / sum(info[2] for class_name, info in top_no_friday_schedules[i]):
                top_no_friday_schedules.insert(i, schedule)
                inserted = True
                break

            elif sum_info == sum(info[5] for class_name, info in top_no_friday_schedules[i]) /sum(info[2] for class_name, info in top_no_friday_schedules[i]):
                j = i
                early_insert = False
                while j < len(top_no_friday_schedules) and sum_info == (sum(info[5] for class_name, info in top_no_friday_schedules[j]) / sum(info[2] for class_name, info in top_no_friday_schedules[j])):
                    if sum(total_travel_time(dorm_loc, schedule)) > sum(total_travel_time(dorm_loc, top_no_friday_schedules[j])):
                        j +=1
                    else:
                        early_insert = True
                        top_no_friday_schedules.insert(j, schedule)
                        inserted = True
                        break

                if not early_insert:
                    top_no_friday_schedules.insert(j, schedule)
                    inserted = True

                break

        if not inserted:
            top_no_friday_schedules.append(schedule)
        top_no_friday_schedules = top_no_friday_schedules[:num_classes]

    for schedule in valid_schedules:
        sum_info = sum(info[5] for class_name, info in schedule) / sum(info[2] for class_name, info in schedule) #sum of priority points/ sum of num_credits
        inserted = False
        for i in range(len(top_schedules)):
            if sum_info < sum(info[5] for class_name, info in top_schedules[i]) / sum(info[2] for class_name, info in top_schedules[i]):
                top_schedules.insert(i, schedule)
                inserted = True
                break

            elif sum_info == sum(info[5] for class_name, info in top_schedules[i]) /sum(info[2] for class_name, info in top_schedules[i]):
                j = i
                early_insert = False
                while j < len(top_schedules) and sum_info == (sum(info[5] for class_name, info in top_schedules[j]) / sum(info[2] for class_name, info in top_schedules[j])):
                    if sum(total_travel_time(dorm_loc, schedule)) > sum(total_travel_time(dorm_loc, top_schedules[j])):
                        j +=1
                    else:
                        early_insert = True
                        top_schedules.insert(j, schedule)
                        inserted = True
                        break

                if not early_insert:
                    top_schedules.insert(j, schedule)
                    inserted = True

                break

        if not inserted:
            top_schedules.append(schedule)
        top_schedules = top_schedules[:num_classes]

    comb_sched = top_no_friday_schedules + top_schedules
    return comb_sched[:num_classes]

def sort_time(classes, min_creds, max_creds, earliest, latest, get_travel_time, dorm_loc, num_classes, friday_off):
    special_schedules = []
    valid_schedules = generate_all_schedules(classes, min_creds, max_creds, earliest, latest, get_travel_time)

    top_no_friday_schedules = []
    top_schedules = []

    if friday_off:
        special_schedules = [schedule for schedule in valid_schedules if all('fri' not in info[3] for class_name, info in schedule)]
        valid_schedules = [schedule for schedule in valid_schedules if any('fri' in info[3] for class_name, info in schedule)]

    if not valid_schedules and not special_schedules:
        return []

    if valid_schedules:
        top_schedules = [valid_schedules[0]]
        valid_schedules.pop(0)
    if special_schedules:
        top_no_friday_schedules = [special_schedules[0]]
        special_schedules.pop(0)

    for schedule in special_schedules:
        sum_times = sum(total_travel_time(dorm_loc, schedule))
        inserted = False
        for i in range(len(top_no_friday_schedules)):
            if sum_times < sum(total_travel_time(dorm_loc, top_no_friday_schedules[i])):
                top_no_friday_schedules.insert(i, schedule)
                inserted = True
                break

            elif sum_times == sum(total_travel_time(dorm_loc, top_no_friday_schedules[i])):
                j = i
                early_insert = False
                while j < len(top_no_friday_schedules) and sum_times ==  sum(total_travel_time(dorm_loc, top_no_friday_schedules[j])):
                    if (sum(info[5] for class_name, info in schedule) / sum(info[2] for class_name, info in schedule)) > (sum(info[5] for class_name, info in top_no_friday_schedules[j]) / sum(info[2] for class_name, info in top_no_friday_schedules[j])):
                        j +=1
                    else:
                        early_insert = True
                        top_no_friday_schedules.insert(j, schedule)
                        inserted = True
                        break

                if not early_insert:
                    top_no_friday_schedules.insert(j, schedule)
                    inserted = True

                break

        if not inserted:
            top_no_friday_schedules.append(schedule)
        top_no_friday_schedules = top_no_friday_schedules[:num_classes]

    for schedule in valid_schedules:
        sum_times = sum(total_travel_time(dorm_loc, schedule))
        inserted = False
        for i in range(len(top_schedules)):
            if sum_times < sum(total_travel_time(dorm_loc, top_schedules[i])):
                top_schedules.insert(i, schedule)
                inserted = True
                break

            elif sum_times == sum(total_travel_time(dorm_loc, top_schedules[i])):
                j = i
                early_insert = False
                while j < len(top_schedules) and sum_times ==  sum(total_travel_time(dorm_loc, top_schedules[j])):
                    if (sum(info[5] for class_name, info in schedule) / sum(info[2] for class_name, info in schedule)) > (sum(info[5] for class_name, info in top_schedules[j]) / sum(info[2] for class_name, info in top_schedules[j])):
                        j +=1
                    else:
                        early_insert = True
                        top_schedules.insert(j, schedule)
                        inserted = True
                        break

                if not early_insert:
                    top_schedules.insert(j, schedule)
                    inserted = True

                break

        if not inserted:
            top_schedules.append(schedule)
        top_schedules = top_schedules[:num_classes]

    comb_sched = top_no_friday_schedules + top_schedules
    return comb_sched[:num_classes]

def main(class_info, dorm_loc, min_creds, max_creds, earliest, latest, num_desired_classes, friday_off, sort_by):
    dorm_loc = building_to_address(dorm_loc)

    if friday_off == ['Yes']:
        friday_off = True
    else:
        friday_off = False

    classes = {}
    idx  = 0

    while idx < len(class_info):
        class_name = class_info[idx]
        classes[class_name] = []
        idx += 1
        while idx < len(class_info) and bool(re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', class_info[idx])):
            section = [building_to_address(class_info[idx + 3]), datetime.strptime(class_info[idx], '%H:%M').time(), class_info[idx + 4] ,class_info[idx + 1].lower().replace(" ", "").split(","), class_info[idx + 2], int(class_info[idx +5])]
            if error_exists(section)[0]:
                return error_exists(section)[1]
            section[2] = float(section[2])
            section[4] = float(section[4])
            classes[class_name].append(section)
            idx+= 6

    top_scheds= []
    if sort_by == ['priority']:
        top_scheds = sort_priority(classes, min_creds, max_creds,earliest, latest, get_travel_time, dorm_loc, num_desired_classes, friday_off)
    else:
        top_scheds = sort_time(classes, min_creds, max_creds,earliest, latest, get_travel_time, dorm_loc, num_desired_classes, friday_off)


    if not top_scheds:
        return []
    else:
        all_info = []

        for idx, schedule in enumerate(top_scheds):
            total_credits = sum(info[2] for class_name, info in schedule)
            total_priority = sum(info[5] for class_name, info in schedule)
            idx1 = 0
            t_time = total_travel_time(dorm_loc, schedule)

            daily_classes = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

            days_mapping = {
                'mon': 'Monday',
                'tue': 'Tuesday',
                'wed': 'Wednesday',
                'thu': 'Thursday',
                'fri': 'Friday',
            }

            for class_info in schedule:
                class_name, (loc, start, _, days, dur, _) = class_info
                for day in days:
                    daily_classes[days_mapping[day]].append((class_name, start.strftime("%I:%M%p"), dur, address_to_building(loc) , 0))

            times = []
            for day, class_info in daily_classes.items():
                origin = dorm_loc
                temp = []
                for index, class0 in enumerate(class_info):
                    temp.append((get_travel_time(origin, building_to_address(class0[3]))))
                    origin=building_to_address(class0[3])
                times.append(temp)



            all_info.append([list(daily_classes.items()),sum(t_time), total_credits, times, total_priority])

        return all_info
