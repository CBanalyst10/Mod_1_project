from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
from dash_package.dash_crime_models import *
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import plotly.graph_objs as go
import pandas as pd
import datetime
import calendar

########Level of Offense Graphs/Queries

month_names = ['January','February','March','April','May','June']
boroughs = ['Manhattan',"Brooklyn",'Bronx',"Queens",'Staten Island']

def return_all_crime_instances_in_month(months):
    year = 2018
    num_days = calendar.monthrange(year, months)[1]
    start_date = datetime.date(year, months, 1)
    end_date = datetime.date(year, months, num_days)
    return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date).all())

def crime_graph_creator():
    month_crime_totals = list(map(lambda month:return_all_crime_instances_in_month(month),list(range(1,len(month_names)+1))))
    return [{'x':month_names,'y':month_crime_totals,'name':'Overall'}]

def return_all_crime_instances_in_month_for_boro(boro_input,month):
    year = 2018
    num_days = calendar.monthrange(year, month)[1]
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    return len(db.session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input).all())

def crime_graph_all_boroughs(boros,months):
    output = []
    for boro in boroughs:
        total_list = []
        for month in list(range(1,len(months)+1)):
            month_total = return_all_crime_instances_in_month_for_boro(boro,month)
            total_list.append(month_total)
        output.append({'x':months,'y':total_list,'name':boro})
    return output

def return_felony_instances_in_month_general(category,months,typeOf):
    years = 2018
    num_days = calendar.monthrange(years, months)[1]
    start_date = datetime.date(years, months, 1)
    end_date = datetime.date(years, months, num_days)
    if category == 'level':
        return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Crime_Event.level_of_offense==typeOf).all())
    if category == 'desc':
        return len(db.session.query(Crime_Event.report_date).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Crime_Event.offense_descr==typeOf).all())
    print('Invalid Category Parameter!')
    return None

#Define new function to handle sorting by type.
def general_graph_creator_all(category, typeOf, seriesName, chartType):
    #Need a function for other type of sorting besides month.
    if category == 'level' or 'desc':
        #Add an IF branch to choose between the following sort methods: month, type
        #This If branch requires a new parameter for this function and the wrapper function.

        #month_crime_totals: the map function passes a range of numbers 
        # corresponding to months, with each number representing a calendar month to
        # pass as a parameter for return_felony_instances_in_month_general which calculates
        #  the dates to filter query results by. The filtered results are then assigned
        #  to a month name.
        #
        # This function can also display all crime descriptions by month, 
        #    although there are so many it would be easier to loop general_graph_creator_all
        #    and display all traces, the large amount on the chart wouldn't make sense.
        #   Feeding in typeOf by a drop-down list is significantly better.
        month_crime_totals = list(map(lambda month:return_felony_instances_in_month_general(category,month,typeOf),list(range(1,len(month_names)+1))))
        return [{'x':month_names,'y':month_crime_totals,'type':chartType,'name':seriesName}]
        #Add alternate path here.
        # the map function passes in a function to calculate a list of keys from a field,
        #  in which each key is passed to return_felony_instances_in_field which filters
        #  the query that field for that key. The filtered results are then assigned to
        # their corresponding key value.
    print('Invalid Category Parameter!')
    return None

def return_instances_in_month_for_boro_general(category,boro_input,months,typeOf):
    year = 2018
    num_days = calendar.monthrange(year, months)[1]
    start_date = datetime.date(year, months, 1)
    end_date = datetime.date(year, months, num_days)
    if category == 'level':
        return len(db.session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input,Crime_Event.level_of_offense==typeOf).all())
    if category == 'desc':
        return len(db.session.query(Crime_Event.report_date).join(Location).filter(Crime_Event.report_date >= start_date, Crime_Event.report_date <= end_date,Location.borough==boro_input,Crime_Event.offense_descr==typeOf).all())

def general_graph_all_boroughs(category,boros,months,typeOf,chartType):
    output = []
    for boro in boros:
        total_list = []
        for month in list(range(1,len(months)+1)):
            month_total = return_instances_in_month_for_boro_general(category,boro,month,typeOf)
            total_list.append(month_total)
        output.append({'x':months,'y':total_list,'type':chartType,'name':boro})
    return output

######## Offense Description Map Functions

##Initial Map

def return_len_of_all_crimes():
    return len(db.session.query(Crime_Event.crime_completed_y_n).all())

total_crimes = return_len_of_all_crimes()

def setlist_of_crime_event_objects():
    return list(set(db.session.query(Crime_Event.offense_descr).all()))

def fulllist_of_crime_event_objects():
    return list(db.session.query(Crime_Event.offense_descr).all())

def count_function_sorted_most_least_w_removal(unique_list, full_list):
    CF=[]
    CF_other = []
    CF_other_names = []
    for list_item in unique_list:
        CF_dict = {}
        CF_dict['key'] = list_item.offense_descr
        CF_dict['count'] = full_list.count(list_item)
        if full_list.count(list_item) > total_crimes*.005:
            CF.append(CF_dict)
        else:
            CF_other.append(full_list.count(list_item))
            CF_other_names.append(list_item.offense_descr)
    CF.append({'key':'OTHER','count':sum(CF_other)})
    #return CF_dict
    return [sorted(CF, key=lambda k:k['count'],reverse=True),CF_other_names]

ofns_occurances = count_function_sorted_most_least_w_removal(setlist_of_crime_event_objects(),fulllist_of_crime_event_objects())[0]

option_values_geomap = list(map(lambda x: x['key'],ofns_occurances))

def option_creator(opt_vals):
    s_vals = sorted(opt_vals)
    oc_list = []
    for val in s_vals:
        if val != "SEX CRIMES":
            oc_dict = {}
            oc_dict['label'] = val.title()
            oc_dict['value'] = val
            oc_list.append(oc_dict)
    return oc_list

drop_options_geomap = option_creator(option_values_geomap)
drop_options_bySeverity = [
# Long Values
#    {'label': 'Felonies', 'value': {'typeOf': 'Felony', 'chartName': 'Felonies', 'seriesName': 'All Felonies', 'chartTitle': 'Felonies'}},
#    {'label': 'Misdemeanors', 'value': {'typeOf': 'Misdemeanor', 'chartName': 'Misdemeanors', 'seriesName': 'All Misdemeanors', 'chartTitle': 'Misdemeanors'}},
#    {'label': 'Violations', 'value': {'typeOf': 'Violation', 'chartName': 'Violations', 'seriesName': 'All Violations', 'chartTitle': 'Violations'}}
# Short Values
    {'label': 'Felonies', 'value': 'Felony'},
    {'label': 'Misdemeanors', 'value': 'Misdemeanor'},
    {'label': 'Violations', 'value': 'Violation'}

]

#['DANGEROUS WEAPONS', 'PETIT LARCENY OF MOTOR VEHICLE', 'FRAUDULENT ACCOSTING', None, 'ROBBERY', 'ENDAN WELFARE INCOMP', 'HOMICIDE-NEGLIGENT,UNCLASSIFIE', 'THEFT-FRAUD', 'RAPE', 'ABORTION', 'OFFENSES AGAINST PUBLIC ADMINI', "BURGLAR'S TOOLS", 'SEX CRIMES', 'OFFENSES INVOLVING FRAUD', 'MISCELLANEOUS PENAL LAW', 'GAMBLING', 'OFFENSES AGAINST THE PERSON', 'MURDER & NON-NEGL. MANSLAUGHTER', 'ARSON', 'JOSTLING', 'POSSESSION OF STOLEN PROPERTY', 'INTOXICATED/IMPAIRED DRIVING', 'OFF. AGNST PUB ORD SENSBLTY &', 'HARRASSMENT 2', 'ANTICIPATORY OFFENSES', 'LOITERING/GAMBLING (CARDS, DIC', 'CRIMINAL TRESPASS', 'OFFENSES RELATED TO CHILDREN', 'FELONY ASSAULT', 'ESCAPE 3', 'NEW YORK CITY HEALTH CODE', 'AGRICULTURE & MRKTS LAW-UNCLASSIFIED', 'KIDNAPPING', 'DISORDERLY CONDUCT', 'OTHER STATE LAWS', 'GRAND LARCENY', 'CHILD ABANDONMENT/NON SUPPORT', 'BURGLARY', 'PETIT LARCENY', 'GRAND LARCENY OF MOTOR VEHICLE', 'OFFENSES AGAINST PUBLIC SAFETY', 'THEFT OF SERVICES', 'PROSTITUTION & RELATED OFFENSES', 'FRAUDS', 'DANGEROUS DRUGS', 'INTOXICATED & IMPAIRED DRIVING', 'VEHICLE AND TRAFFIC LAWS', 'OTHER OFFENSES RELATED TO THEF', 'FORGERY', 'UNAUTHORIZED USE OF A VEHICLE', 'ADMINISTRATIVE CODE', 'NYS LAWS-UNCLASSIFIED FELONY', 'OTHER STATE LAWS (NON PENAL LA', 'ALCOHOLIC BEVERAGE CONTROL LAW', 'ASSAULT 3 & RELATED OFFENSES', 'CRIMINAL MISCHIEF & RELATED OF', 'KIDNAPPING & RELATED OFFENSES', 'NYS LAWS-UNCLASSIFIED VIOLATION']

drop_options_byTypeOfCrime = [
 {'label': 'Dangerous Weapons', 'value': 'DANGEROUS WEAPONS'},
 {'label': 'Petit Larceny Of Motor Vehicle',
  'value': 'PETIT LARCENY OF MOTOR VEHICLE'},
 {'label': 'Fraudulent Accosting', 'value': 'FRAUDULENT ACCOSTING'},
 {'label': 'Robbery', 'value': 'ROBBERY'},
 {'label': 'Endan Welfare Incomp', 'value': 'ENDAN WELFARE INCOMP'},
 {'label': 'Homicide-Negligent,Unclassifie',
  'value': 'HOMICIDE-NEGLIGENT,UNCLASSIFIE'},
 {'label': 'Theft-Fraud', 'value': 'THEFT-FRAUD'},
 {'label': 'Rape', 'value': 'RAPE'},
 {'label': 'Abortion', 'value': 'ABORTION'},
 {'label': 'Offenses Against Public Admini',
  'value': 'OFFENSES AGAINST PUBLIC ADMINI'},
 {'label': "Burglar's Tools", 'value': "BURGLAR'S TOOLS"},
 {'label': 'Sex Crimes', 'value': 'SEX CRIMES'},
 {'label': 'Offenses Involving Fraud', 'value': 'OFFENSES INVOLVING FRAUD'},
 {'label': 'Miscellaneous Penal Law', 'value': 'MISCELLANEOUS PENAL LAW'},
 {'label': 'Gambling', 'value': 'GAMBLING'},
 {'label': 'Offenses Against The Person',
  'value': 'OFFENSES AGAINST THE PERSON'},
 {'label': 'Murder & Non-Negl. Manslaughter',
  'value': 'MURDER & NON-NEGL. MANSLAUGHTER'},
 {'label': 'Arson', 'value': 'ARSON'},
 {'label': 'Jostling', 'value': 'JOSTLING'},
 {'label': 'Possession Of Stolen Property',
  'value': 'POSSESSION OF STOLEN PROPERTY'},
 {'label': 'Intoxicated/Impaired Driving',
  'value': 'INTOXICATED/IMPAIRED DRIVING'},
 {'label': 'Off. Agnst Pub Ord Sensblty &',
  'value': 'OFF. AGNST PUB ORD SENSBLTY &'},
 {'label': 'Harrassment 2', 'value': 'HARRASSMENT 2'},
 {'label': 'Anticipatory Offenses', 'value': 'ANTICIPATORY OFFENSES'},
 {'label': 'Loitering/Gambling (Cards, Dic',
  'value': 'LOITERING/GAMBLING (CARDS, DIC'},
 {'label': 'Criminal Trespass', 'value': 'CRIMINAL TRESPASS'},
 {'label': 'Offenses Related To Children',
  'value': 'OFFENSES RELATED TO CHILDREN'},
 {'label': 'Felony Assault', 'value': 'FELONY ASSAULT'},
 {'label': 'Escape 3', 'value': 'ESCAPE 3'},
 {'label': 'New York City Health Code', 'value': 'NEW YORK CITY HEALTH CODE'},
 {'label': 'Agriculture & Mrkts Law-Unclassified',
  'value': 'AGRICULTURE & MRKTS LAW-UNCLASSIFIED'},
 {'label': 'Kidnapping', 'value': 'KIDNAPPING'},
 {'label': 'Disorderly Conduct', 'value': 'DISORDERLY CONDUCT'},
 {'label': 'Other State Laws', 'value': 'OTHER STATE LAWS'},
 {'label': 'Grand Larceny', 'value': 'GRAND LARCENY'},
 {'label': 'Child Abandonment/Non Support',
  'value': 'CHILD ABANDONMENT/NON SUPPORT'},
 {'label': 'Burglary', 'value': 'BURGLARY'},
 {'label': 'Petit Larceny', 'value': 'PETIT LARCENY'},
 {'label': 'Grand Larceny Of Motor Vehicle',
  'value': 'GRAND LARCENY OF MOTOR VEHICLE'},
 {'label': 'Offenses Against Public Safety',
  'value': 'OFFENSES AGAINST PUBLIC SAFETY'},
 {'label': 'Theft Of Services', 'value': 'THEFT OF SERVICES'},
 {'label': 'Prostitution & Related Offenses',
  'value': 'PROSTITUTION & RELATED OFFENSES'},
 {'label': 'Frauds', 'value': 'FRAUDS'},
 {'label': 'Dangerous Drugs', 'value': 'DANGEROUS DRUGS'},
 {'label': 'Intoxicated & Impaired Driving',
  'value': 'INTOXICATED & IMPAIRED DRIVING'},
 {'label': 'Vehicle And Traffic Laws', 'value': 'VEHICLE AND TRAFFIC LAWS'},
 {'label': 'Other Offenses Related To Thef',
  'value': 'OTHER OFFENSES RELATED TO THEF'},
 {'label': 'Forgery', 'value': 'FORGERY'},
 {'label': 'Unauthorized Use Of A Vehicle',
  'value': 'UNAUTHORIZED USE OF A VEHICLE'},
 {'label': 'Administrative Code', 'value': 'ADMINISTRATIVE CODE'},
 {'label': 'Nys Laws-Unclassified Felony',
  'value': 'NYS LAWS-UNCLASSIFIED FELONY'},
 {'label': 'Other State Laws (Non Penal La',
  'value': 'OTHER STATE LAWS (NON PENAL LA'},
 {'label': 'Alcoholic Beverage Control Law',
  'value': 'ALCOHOLIC BEVERAGE CONTROL LAW'},
 {'label': 'Assault 3 & Related Offenses',
  'value': 'ASSAULT 3 & RELATED OFFENSES'},
 {'label': 'Criminal Mischief & Related Of',
  'value': 'CRIMINAL MISCHIEF & RELATED OF'},
 {'label': 'Kidnapping & Related Offenses',
  'value': 'KIDNAPPING & RELATED OFFENSES'},
 {'label': 'NYS Laws-Unclassified Violation',
  'value': 'NYS LAWS-UNCLASSIFIED VIOLATION'}
]


# new_list = [expression(i) for i in old_list if filter(i)]

other_ofns = count_function_sorted_most_least_w_removal(setlist_of_crime_event_objects(),fulllist_of_crime_event_objects())[1]

#returns "OTHER" cluster; Defined by ofns_type that makes up > 5% of all crime; BUG: drops 'nan'/'None' values;
def return_other_ofn_locations():
    return db.session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr.in_(other_ofns)).all()

def return_ofns_type_locs(type):
    return db.session.query(Location.latitude, Location.longitude).join(Crime_Event).filter(Crime_Event.offense_descr==type.upper()).all()

#tri-boro bridge coordinates
NY_COORDINATES = (40.7797, -73.9266)
#inital map creation

ny_map = folium.Map(location=NY_COORDINATES,tiles='Stamen Terrain',zoom_start=10)
initial_display_creator = ny_map.save('dash_package/map_storage/initial_map.html')
initial_display = open('dash_package/map_storage/initial_map.html', 'r').read()
#insert

def map_ofns_coord(coord_list):
    marker_cluster = plugins.MarkerCluster(name=None).add_to(ny_map)
    for item in coord_list:
        folium.Marker([item.latitude,item.longitude]).add_to(marker_cluster)
    return ny_map

def map_html_creator(value):
    if value == 'OTHER':
        location_map = map_ofns_coord(return_other_ofn_locations())
        location_map.save('dash_package/map_storage/{}.html'.format(value))
        # location_map.save('dash_package/map_storage/"{}".html').format(value)
    else:
        location_map = map_ofns_coord(return_ofns_type_locs(value))
        location_map.save('dash_package/map_storage/{}.html'.format(value))

#create_all_html_maps
#only need to run once to initialize
# for value in option_values:
#     if value != "SEX CRIMES":
#         print('.....NOW PROCESSING.....'+str(value))
#         map_html_creator(value)


def generalDashWrapper(category,typeOf,boroughs,months,chartName,seriesName,chartTitle,chartType):
    return {'data': general_graph_creator_all(category,typeOf,seriesName,chartType)+general_graph_all_boroughs(category,boroughs,months,typeOf,chartType),'layout':{'title':chartTitle}}

def off_desc_return():
    return db.session.query(Crime_Event.offense_descr).all()

def resultListFromDescr(resultList):
    newList = list()
    for x in resultList:
        newList.append(x.offense_descr)
    return newList

def setList1Count(inputList):
    newDatDict = dict()
    listKeys = list(set(inputList))

    #'Initialize '
    for a in listKeys:
        newDatDict[a] = 0
        #'Fill'
        for b in inputList:
            if a == b:
                newDatDict[a] += 1

    return newDatDict

def dictToDash(inputDict, chartType, chartName):
    listX = list()
    listY = list()

    for a,b in inputDict.items():
        listX.append(a)
        listY.append(b)
    return {'x': listX, 'y': listY, 'type': chartType, 'name': chartName}

def crimeTypeQueryToDash(crimeTypeQuery, chartType, chartName):
    return dictToDash(setList1Count(resultListFromDescr(crimeTypeQuery)), chartType, chartName)
