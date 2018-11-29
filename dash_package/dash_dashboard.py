from dash_package.dash_queries import *
import dash
from dash.dependencies import Input, Output
# from folium import Iframe
# from dash_package.robbery_locations_1K import *


app.layout = html.Div([
    html.H1('NYC Crime Data - 1H 2018'),
    html.Div([
        html.H2('Crime by Level of Offense & Offense Description Graph'),
        dcc.Tabs(id="tabs", children=[
            ############################################################
            ###Common theme identified: calling query via a specific value of a field.
            ####This can be streamlined via automatic key creation and through sets.
            #####All 4 of these tabs can be shortened into a single tab,
            ###### which picks traces based on input from a dropdown list.
            dcc.Tab(id='NYC', label='Crimes by Borough',
                children=[
                dcc.Graph(figure=
                {'data': crime_graph_creator()+crime_graph_all_boroughs(boroughs,month_names),
                'layout': {'title':'All Complaints'},
                })
                ]
            ),
#            dcc.Tab(id='Felony', label='Felony Complaints',
#                children=[
#                dcc.Graph(figure=generalDashWrapper('level','Felony',boroughs,month_names,'Felonies','All Felonies','Felonies','line'))
#                ]
#            ),
#            dcc.Tab(id='Misdemeanor', label='Misdemeanor Complaints',
#                children=[
#                dcc.Graph(figure=generalDashWrapper('level','Misdemeanor',boroughs,month_names,'Misdemeanors','All Misdemeanors','Misdemeanors','line'))
#                ]
#            ),
#            dcc.Tab(id='Violation', label='Violation Complaints',
#                children=[
#                dcc.Graph(figure=generalDashWrapper('level','Violation',boroughs,month_names,'Violations','All Violations','Violations','line'))
#                ]
#            ),
################################################

            dcc.Tab(id='bySeverity', label='Complaints by Severity',
                children=[
                dcc.Dropdown(
                    id='bySeverity-dropdown',
                    options=drop_options_bySeverity,
                    #value format: {'typeOf': 'Violation', 'chartName': 'Violations', 'seriesName': 'All Violations', 'chartTitle': 'Violations'}
                    #placeholder = "Select Offense Severity"
                    value=drop_options_bySeverity[0]['value']
                ),
                dcc.Graph(id='bySeverityGraph',figure=generalDashWrapper('level','Felony',boroughs,month_names,'Felonies','All Felonies','Felonies','line'))
                ]
            ),

            dcc.Tab(id='byTypeOfCrime', label='Complaints by Type',
                children=[
                dcc.Dropdown(
                    id='byTypeOfCrime-dropdown',
                    options=drop_options_byTypeOfCrime,
                    value=drop_options_byTypeOfCrime[0]['value']
                ),
                dcc.Graph(id='byTypeOfCrimeGraph',figure=generalDashWrapper('desc','DANGEROUS WEAPONS',boroughs,month_names,'DANGEROUS WEAPONS','All DANGEROUS WEAPONS','DANGEROUS WEAPONS','line'))
                ]
            ),

            ###Notes found for the above graphs. See note at top.
            #####################################
            dcc.Tab(id='Types', label='Types of Crime',
                children=[
                dcc.Graph(figure=
                #This input could be improved.
                {'data': [crimeTypeQueryToDash(off_desc_return(), 'bar', 'Types of Crime in New York')],
                'layout': {'title':'Types of Crime'}})
                ]
            ),
            ])
        ]),
    html.H2('Crime Clusters by Primary Description'),
    dcc.Dropdown(
        id='geomap-dropdown',
        options=drop_options_geomap,
        placeholder = "Select an Offense"
        # value=drop_down_options[0]['value']
    ),
    html.Iframe(id='output-container',srcDoc = initial_display, width = '100%', height = '600')])

###################
# Severity dropdown contents start.
@app.callback(
    Output(component_id='bySeverityGraph', component_property='figure'),
    [Input(component_id='bySeverity-dropdown', component_property='value')])
def update_value_bySeverity(value):

    if value == 'Felony':
        return generalDashWrapper('level','Felony',boroughs,month_names,'Felonies','All Felonies','Felonies','line')

    if value == 'Misdemeanor':
        return generalDashWrapper('level','Misdemeanor',boroughs,month_names,'Misdemeanors','All Misdemeanors','Misdemeanors','line')  

    if value == 'Violation':
        return generalDashWrapper('level','Violation',boroughs,month_names,'Violations','All Violations','Violations','line')   

# Severity dropdown contents end.
####################

###################
# TypeOfCrime dropdown contents start.
# I should find a better way to do this.
@app.callback(
    Output(component_id='byTypeOfCrimeGraph', component_property='figure'),
    [Input(component_id='byTypeOfCrime-dropdown', component_property='value')])
def update_value_byTypeOfCrime(value):

    if value == 'DANGEROUS WEAPONS':        
        return generalDashWrapper('desc','DANGEROUS WEAPONS',boroughs,month_names,'DANGEROUS WEAPONS','All DANGEROUS WEAPONS','DANGEROUS WEAPONS','line'),
    if value == 'PETIT LARCENY OF MOTOR VEHICLE':        
        return generalDashWrapper('desc','PETIT LARCENY OF MOTOR VEHICLE',boroughs,month_names,'PETIT LARCENY OF MOTOR VEHICLE','All PETIT LARCENY OF MOTOR VEHICLE','PETIT LARCENY OF MOTOR VEHICLE','line'),
    if value == 'FRAUDULENT ACCOSTING':        
        return generalDashWrapper('desc','FRAUDULENT ACCOSTING',boroughs,month_names,'FRAUDULENT ACCOSTING','All FRAUDULENT ACCOSTING','FRAUDULENT ACCOSTING','line'),
    if value == 'ROBBERY':        
        return generalDashWrapper('desc','ROBBERY',boroughs,month_names,'ROBBERY','All ROBBERY','ROBBERY','line'),
    if value == 'ENDAN WELFARE INCOMP':        
        return generalDashWrapper('desc','ENDAN WELFARE INCOMP',boroughs,month_names,'ENDAN WELFARE INCOMP','All ENDAN WELFARE INCOMP','ENDAN WELFARE INCOMP','line'),
    if value == 'HOMICIDE-NEGLIGENT,UNCLASSIFIE':        
        return generalDashWrapper('desc','HOMICIDE-NEGLIGENT,UNCLASSIFIE',boroughs,month_names,'HOMICIDE-NEGLIGENT,UNCLASSIFIE','All HOMICIDE-NEGLIGENT,UNCLASSIFIE','HOMICIDE-NEGLIGENT,UNCLASSIFIE','line'),
    if value == 'THEFT-FRAUD':        
        return generalDashWrapper('desc','THEFT-FRAUD',boroughs,month_names,'THEFT-FRAUD','All THEFT-FRAUD','THEFT-FRAUD','line'),
    if value == 'RAPE':        
        return generalDashWrapper('desc','RAPE',boroughs,month_names,'RAPE','All RAPE','RAPE','line'),
    if value == 'ABORTION':        
        return generalDashWrapper('desc','ABORTION',boroughs,month_names,'ABORTION','All ABORTION','ABORTION','line'),
    if value == 'OFFENSES AGAINST PUBLIC ADMINI':        
        return generalDashWrapper('desc','OFFENSES AGAINST PUBLIC ADMINI',boroughs,month_names,'OFFENSES AGAINST PUBLIC ADMINI','All OFFENSES AGAINST PUBLIC ADMINI','OFFENSES AGAINST PUBLIC ADMINI','line'),
    if value == "BURGLAR'S TOOLS":        
        return generalDashWrapper('desc',"BURGLAR'S TOOLS",boroughs,month_names,"BURGLAR'S TOOLS","All BURGLAR'S TOOLS","BURGLAR'S TOOLS",'line'),
    if value == 'SEX CRIMES':        
        return generalDashWrapper('desc','SEX CRIMES',boroughs,month_names,'SEX CRIMES','All SEX CRIMES','SEX CRIMES','line'),
    if value == 'OFFENSES INVOLVING FRAUD':        
        return generalDashWrapper('desc','OFFENSES INVOLVING FRAUD',boroughs,month_names,'OFFENSES INVOLVING FRAUD','All OFFENSES INVOLVING FRAUD','OFFENSES INVOLVING FRAUD','line'),
    if value == 'MISCELLANEOUS PENAL LAW':        
        return generalDashWrapper('desc','MISCELLANEOUS PENAL LAW',boroughs,month_names,'MISCELLANEOUS PENAL LAW','All MISCELLANEOUS PENAL LAW','MISCELLANEOUS PENAL LAW','line'),
    if value == 'GAMBLING':        
        return generalDashWrapper('desc','GAMBLING',boroughs,month_names,'GAMBLING','All GAMBLING','GAMBLING','line'),
    if value == 'OFFENSES AGAINST THE PERSON':        
        return generalDashWrapper('desc','OFFENSES AGAINST THE PERSON',boroughs,month_names,'OFFENSES AGAINST THE PERSON','All OFFENSES AGAINST THE PERSON','OFFENSES AGAINST THE PERSON','line'),
    if value == 'MURDER & NON-NEGL. MANSLAUGHTER':        
        return generalDashWrapper('desc','MURDER & NON-NEGL. MANSLAUGHTER',boroughs,month_names,'MURDER & NON-NEGL. MANSLAUGHTER','All MURDER & NON-NEGL. MANSLAUGHTER','MURDER & NON-NEGL. MANSLAUGHTER','line'),
    if value == 'ARSON':        
        return generalDashWrapper('desc','ARSON',boroughs,month_names,'ARSON','All ARSON','ARSON','line'),
    if value == 'JOSTLING':        
        return generalDashWrapper('desc','JOSTLING',boroughs,month_names,'JOSTLING','All JOSTLING','JOSTLING','line'),
    if value == 'POSSESSION OF STOLEN PROPERTY':        
        return generalDashWrapper('desc','POSSESSION OF STOLEN PROPERTY',boroughs,month_names,'POSSESSION OF STOLEN PROPERTY','All POSSESSION OF STOLEN PROPERTY','POSSESSION OF STOLEN PROPERTY','line'),
    if value == 'INTOXICATED/IMPAIRED DRIVING':        
        return generalDashWrapper('desc','INTOXICATED/IMPAIRED DRIVING',boroughs,month_names,'INTOXICATED/IMPAIRED DRIVING','All INTOXICATED/IMPAIRED DRIVING','INTOXICATED/IMPAIRED DRIVING','line'),
    if value == 'OFF. AGNST PUB ORD SENSBLTY &':        
        return generalDashWrapper('desc','OFF. AGNST PUB ORD SENSBLTY &',boroughs,month_names,'OFF. AGNST PUB ORD SENSBLTY &','All OFF. AGNST PUB ORD SENSBLTY &','OFF. AGNST PUB ORD SENSBLTY &','line'),
    if value == 'HARRASSMENT 2':        
        return generalDashWrapper('desc','HARRASSMENT 2',boroughs,month_names,'HARRASSMENT 2','All HARRASSMENT 2','HARRASSMENT 2','line'),
    if value == 'ANTICIPATORY OFFENSES':        
        return generalDashWrapper('desc','ANTICIPATORY OFFENSES',boroughs,month_names,'ANTICIPATORY OFFENSES','All ANTICIPATORY OFFENSES','ANTICIPATORY OFFENSES','line'),
    if value == 'LOITERING/GAMBLING (CARDS, DIC':        
        return generalDashWrapper('desc','LOITERING/GAMBLING (CARDS, DIC',boroughs,month_names,'LOITERING/GAMBLING (CARDS, DIC','All LOITERING/GAMBLING (CARDS, DIC','LOITERING/GAMBLING (CARDS, DIC','line'),
    if value == 'CRIMINAL TRESPASS':        
        return generalDashWrapper('desc','CRIMINAL TRESPASS',boroughs,month_names,'CRIMINAL TRESPASS','All CRIMINAL TRESPASS','CRIMINAL TRESPASS','line'),
    if value == 'OFFENSES RELATED TO CHILDREN':        
        return generalDashWrapper('desc','OFFENSES RELATED TO CHILDREN',boroughs,month_names,'OFFENSES RELATED TO CHILDREN','All OFFENSES RELATED TO CHILDREN','OFFENSES RELATED TO CHILDREN','line'),
    if value == 'FELONY ASSAULT':        
        return generalDashWrapper('desc','FELONY ASSAULT',boroughs,month_names,'FELONY ASSAULT','All FELONY ASSAULT','FELONY ASSAULT','line'),
    if value == 'ESCAPE 3':        
        return generalDashWrapper('desc','ESCAPE 3',boroughs,month_names,'ESCAPE 3','All ESCAPE 3','ESCAPE 3','line'),
    if value == 'NEW YORK CITY HEALTH CODE':        
        return generalDashWrapper('desc','NEW YORK CITY HEALTH CODE',boroughs,month_names,'NEW YORK CITY HEALTH CODE','All NEW YORK CITY HEALTH CODE','NEW YORK CITY HEALTH CODE','line'),
    if value == 'AGRICULTURE & MRKTS LAW-UNCLASSIFIED':        
        return generalDashWrapper('desc','AGRICULTURE & MRKTS LAW-UNCLASSIFIED',boroughs,month_names,'AGRICULTURE & MRKTS LAW-UNCLASSIFIED','All AGRICULTURE & MRKTS LAW-UNCLASSIFIED','AGRICULTURE & MRKTS LAW-UNCLASSIFIED','line'),
    if value == 'KIDNAPPING':        
        return generalDashWrapper('desc','KIDNAPPING',boroughs,month_names,'KIDNAPPING','All KIDNAPPING','KIDNAPPING','line'),
    if value == 'DISORDERLY CONDUCT':        
        return generalDashWrapper('desc','DISORDERLY CONDUCT',boroughs,month_names,'DISORDERLY CONDUCT','All DISORDERLY CONDUCT','DISORDERLY CONDUCT','line'),
    if value == 'OTHER STATE LAWS':        
        return generalDashWrapper('desc','OTHER STATE LAWS',boroughs,month_names,'OTHER STATE LAWS','All OTHER STATE LAWS','OTHER STATE LAWS','line'),
    if value == 'GRAND LARCENY':        
        return generalDashWrapper('desc','GRAND LARCENY',boroughs,month_names,'GRAND LARCENY','All GRAND LARCENY','GRAND LARCENY','line'),
    if value == 'CHILD ABANDONMENT/NON SUPPORT':        
        return generalDashWrapper('desc','CHILD ABANDONMENT/NON SUPPORT',boroughs,month_names,'CHILD ABANDONMENT/NON SUPPORT','All CHILD ABANDONMENT/NON SUPPORT','CHILD ABANDONMENT/NON SUPPORT','line'),
    if value == 'BURGLARY':        
        return generalDashWrapper('desc','BURGLARY',boroughs,month_names,'BURGLARY','All BURGLARY','BURGLARY','line'),
    if value == 'PETIT LARCENY':        
        return generalDashWrapper('desc','PETIT LARCENY',boroughs,month_names,'PETIT LARCENY','All PETIT LARCENY','PETIT LARCENY','line'),
    if value == 'GRAND LARCENY OF MOTOR VEHICLE':        
        return generalDashWrapper('desc','GRAND LARCENY OF MOTOR VEHICLE',boroughs,month_names,'GRAND LARCENY OF MOTOR VEHICLE','All GRAND LARCENY OF MOTOR VEHICLE','GRAND LARCENY OF MOTOR VEHICLE','line'),
    if value == 'OFFENSES AGAINST PUBLIC SAFETY':        
        return generalDashWrapper('desc','OFFENSES AGAINST PUBLIC SAFETY',boroughs,month_names,'OFFENSES AGAINST PUBLIC SAFETY','All OFFENSES AGAINST PUBLIC SAFETY','OFFENSES AGAINST PUBLIC SAFETY','line'),
    if value == 'THEFT OF SERVICES':        
        return generalDashWrapper('desc','THEFT OF SERVICES',boroughs,month_names,'THEFT OF SERVICES','All THEFT OF SERVICES','THEFT OF SERVICES','line'),
    if value == 'PROSTITUTION & RELATED OFFENSES':        
        return generalDashWrapper('desc','PROSTITUTION & RELATED OFFENSES',boroughs,month_names,'PROSTITUTION & RELATED OFFENSES','All PROSTITUTION & RELATED OFFENSES','PROSTITUTION & RELATED OFFENSES','line'),
    if value == 'FRAUDS':        
        return generalDashWrapper('desc','FRAUDS',boroughs,month_names,'FRAUDS','All FRAUDS','FRAUDS','line'),
    if value == 'DANGEROUS DRUGS':        
        return generalDashWrapper('desc','DANGEROUS DRUGS',boroughs,month_names,'DANGEROUS DRUGS','All DANGEROUS DRUGS','DANGEROUS DRUGS','line'),
    if value == 'INTOXICATED & IMPAIRED DRIVING':        
        return generalDashWrapper('desc','INTOXICATED & IMPAIRED DRIVING',boroughs,month_names,'INTOXICATED & IMPAIRED DRIVING','All INTOXICATED & IMPAIRED DRIVING','INTOXICATED & IMPAIRED DRIVING','line'),
    if value == 'VEHICLE AND TRAFFIC LAWS':        
        return generalDashWrapper('desc','VEHICLE AND TRAFFIC LAWS',boroughs,month_names,'VEHICLE AND TRAFFIC LAWS','All VEHICLE AND TRAFFIC LAWS','VEHICLE AND TRAFFIC LAWS','line'),
    if value == 'OTHER OFFENSES RELATED TO THEF':        
        return generalDashWrapper('desc','OTHER OFFENSES RELATED TO THEF',boroughs,month_names,'OTHER OFFENSES RELATED TO THEF','All OTHER OFFENSES RELATED TO THEF','OTHER OFFENSES RELATED TO THEF','line'),
    if value == 'FORGERY':        
        return generalDashWrapper('desc','FORGERY',boroughs,month_names,'FORGERY','All FORGERY','FORGERY','line'),
    if value == 'UNAUTHORIZED USE OF A VEHICLE':        
        return generalDashWrapper('desc','UNAUTHORIZED USE OF A VEHICLE',boroughs,month_names,'UNAUTHORIZED USE OF A VEHICLE','All UNAUTHORIZED USE OF A VEHICLE','UNAUTHORIZED USE OF A VEHICLE','line'),
    if value == 'ADMINISTRATIVE CODE':        
        return generalDashWrapper('desc','ADMINISTRATIVE CODE',boroughs,month_names,'ADMINISTRATIVE CODE','All ADMINISTRATIVE CODE','ADMINISTRATIVE CODE','line'),
    if value == 'NYS LAWS-UNCLASSIFIED FELONY':        
        return generalDashWrapper('desc','NYS LAWS-UNCLASSIFIED FELONY',boroughs,month_names,'NYS LAWS-UNCLASSIFIED FELONY','All NYS LAWS-UNCLASSIFIED FELONY','NYS LAWS-UNCLASSIFIED FELONY','line'),
    if value == 'OTHER STATE LAWS (NON PENAL LA':        
        return generalDashWrapper('desc','OTHER STATE LAWS (NON PENAL LA',boroughs,month_names,'OTHER STATE LAWS (NON PENAL LA','All OTHER STATE LAWS (NON PENAL LA','OTHER STATE LAWS (NON PENAL LA','line'),
    if value == 'ALCOHOLIC BEVERAGE CONTROL LAW':        
        return generalDashWrapper('desc','ALCOHOLIC BEVERAGE CONTROL LAW',boroughs,month_names,'ALCOHOLIC BEVERAGE CONTROL LAW','All ALCOHOLIC BEVERAGE CONTROL LAW','ALCOHOLIC BEVERAGE CONTROL LAW','line'),
    if value == 'ASSAULT 3 & RELATED OFFENSES':        
        return generalDashWrapper('desc','ASSAULT 3 & RELATED OFFENSES',boroughs,month_names,'ASSAULT 3 & RELATED OFFENSES','All ASSAULT 3 & RELATED OFFENSES','ASSAULT 3 & RELATED OFFENSES','line'),
    if value == 'CRIMINAL MISCHIEF & RELATED OF':        
        return generalDashWrapper('desc','CRIMINAL MISCHIEF & RELATED OF',boroughs,month_names,'CRIMINAL MISCHIEF & RELATED OF','All CRIMINAL MISCHIEF & RELATED OF','CRIMINAL MISCHIEF & RELATED OF','line'),
    if value == 'KIDNAPPING & RELATED OFFENSES':        
        return generalDashWrapper('desc','KIDNAPPING & RELATED OFFENSES',boroughs,month_names,'KIDNAPPING & RELATED OFFENSES','All KIDNAPPING & RELATED OFFENSES','KIDNAPPING & RELATED OFFENSES','line'),
    if value == 'NYS LAWS-UNCLASSIFIED VIOLATION':        
        return generalDashWrapper('desc','NYS LAWS-UNCLASSIFIED VIOLATION',boroughs,month_names,'NYS LAWS-UNCLASSIFIED VIOLATION','All NYS LAWS-UNCLASSIFIED VIOLATION','NYS LAWS-UNCLASSIFIED VIOLATION','line')

# TypeOfCrime dropdown contents end.
####################

############
# Geomap dropdown contents start.
@app.callback(
    dash.dependencies.Output('output-container', 'srcDoc'),
    [dash.dependencies.Input('geomap-dropdown', 'value')])
def update_output_geomap(value):
    srcDoc = open('dash_package/map_storage/{}.html'.format(value), 'r').read()
    return srcDoc
# Geomap dropdown contents end.
##############