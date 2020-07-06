"""
Name: Gina McKeown

This code will take data from online and display it onto graphs for easier visualization. This informs
users of the latest coronavirus data.

Sources and Credits:
https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html
New York Times: https://github.com/nytimes/covid-19-data
John Hopkins University of Medicine: https://github.com/CSSEGISandData/COVID-19
"""

# json conversion
import json  # JavaScript Object Notation
import urllib.request

# # csv conversion
# import csv  # comma separated variables
# from io import StringIO

# Data Organization
import numpy as np
import pandas as pd

# Graphs: Plotly
import plotly.graph_objects as go
import plotly.express as px

# Graphic User Interface
import dash
import dash_core_components as dcc
import dash_html_components as html


class DataVisualization:
    def __init__(self):
        """
        creates a Dash Web App using API data and plotly graphs
        """

    def get_json(self, url):
        """
        converts an API url into a parsed jason file
        :param url: the url for the API with a jason file
        :return: the parsed json file
        """
        opened_url = urllib.request.urlopen(url)  # access the url
        url_data = opened_url.read()  # reads out the information
        return json.loads(url_data)  # return parsed info

    # def get_csv(self, url):
    #     """
    #         converts an API url into a readable object
    #         :param url: the url for the API with a csv file
    #         :return: the read csv file
    #     """
    #     # opened_url = urllib.request.urlopen(url)  # get the object location from url
    #     # url_data = opened_url.read()
    #     # csv_location = url_data.decode("utf8", "ignore")  # get the object location from memory
    #     # csv_file = StringIO(csv_location)  # file to accessible string
    #     # read_file = csv.reader(csv_file)
    #     # return read_file
    #     return pd.read_csv(url)  # return info as string

    def generate_global_map(self):
        """
        make worldwide Choreopleth map of cases
        :return: plotly Choreopleth map
        """
        # Global Map Data
        global_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
        global_df = pd.read_csv(global_csv)

        # Global Map
        global_map = go.Figure(data=go.Choropleth(
            locations=global_df["ISO3"],
            z=global_df['Confirmed'],  # variable displayed
            text=global_df['Country_Region'],
            colorscale=["#022a52", "#153e66", "#2a4c6e", "#405e7d", "#5d7894", "#7695b5", "#a1b5c9", "#bccee0",
                        "#d8e2ed", "#e1e7ed"],
            autocolorscale=False,
            reversescale=True,
            marker_line_color='white',  # lines between countries
            marker_line_width=0.2,
            colorbar_title='Cases',
            zmin=0,
            zmid=2000,
            zmax=100000
        ))

        global_map.update_layout(
            font={"size": 16, "color": "White"},  # style title text
            title_text='Global Cases',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

        # Edit Colors
        global_map.update_layout(geo=dict(bgcolor='#4E5D6C',
                                          lakecolor='#4E5D6C',
                                          landcolor='#253342'
                                          ),
                                 paper_bgcolor='#4E5D6C',
                                 plot_bgcolor='#4E5D6C',
                                 )
        return global_map

    def generate_US_line_graph(self):
        """
        plots US cases over time on line graph
        :return: plotly line graph
        """
        # US Case Data Over Time
        us_csv = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
        us = pd.read_csv(us_csv)
        us_line_graph = px.line(us,
                                x='date',
                                y='cases',
                                title="Cases in the US",
                                template="plotly_dark")
        return us_line_graph

    def generate_global_table(self):
        """
        creates table for countries and provinces with columns for cases, deaths, recovered and active
        :return: plotly data table
        """
        # Global Data By Country/Region
        global_cases_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
        country_cases_df = pd.read_csv(global_cases_csv)
        country_cases_df = country_cases_df.drop(
            labels=["Last_Update", "Lat", "Long_", "Incident_Rate", "People_Tested", "People_Hospitalized",
                    "Mortality_Rate",
                    "UID", "ISO3"], axis=1)

        worldwide_table = go.Figure(data=[go.Table(
            header=dict(values=["Country/Region", "Cases", "Active Cases", "Deaths", "Recovered"],  # top row headers
                        fill_color='#17181a',
                        font=dict(color='white', size=12),  # text color
                        align='left'),
            cells=dict(values=[country_cases_df.Country_Region, country_cases_df.Confirmed, country_cases_df.Active,
                               country_cases_df.Deaths, country_cases_df.Recovered],  # columns
                       fill_color='#555863',
                       font=dict(color='white', size=12),  # text color
                       align='left'))
        ])

        return worldwide_table

    def generate_US_map(self):
        """
        US cases by county on a tile based map
        :return: Choreopleth Mapbox map
        """
        # Get County Tile Info
        with urllib.request.urlopen(
                'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

        # US Data by County
        US_county_df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                                   dtype={"fips": str})
        # Choreopleth Mabox Tile Based Map
        US_county_map = go.Figure(go.Choroplethmapbox(geojson=counties,  # based on county
                                                      locations=US_county_df.fips,  # use fips to graph
                                                      z=US_county_df.cases,
                                                      text=US_county_df.state + ", " + US_county_df.county,
                                                      # hover label
                                                      colorscale=["#022a52", "#153e66", "#2a4c6e", "#405e7d", "#5d7894",
                                                                  "#7695b5", "#a1b5c9", "#bccee0",
                                                                  "#d8e2ed", "#e1e7ed"],
                                                      reversescale=True,  # darker for more cases
                                                      zmin=0,
                                                      zmax=200,  # color scale max
                                                      marker_line_color='#c7cdd4',  # county lines
                                                      marker_line_width=0.02))

        US_county_map.update_layout(mapbox_style="carto-positron",
                                    mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129})  # default zoom
        US_county_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return US_county_map

    def generate_multiline_graph(self):
        """
        compares global cases, deaths, recovered and active on multi-line graph
        :return: plotly multi-line graph
        """
        # Global Data Sorted by Cases, Deaths, and Recovered Over Time
        global_cases_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        global_deaths_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        global_recovered_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

        # Read Data
        global_cases_df = pd.read_csv(global_cases_csv)
        global_deaths_csv_df = pd.read_csv(global_deaths_csv)
        global_recovered_csv_df = pd.read_csv(global_recovered_csv)

        # Data Time Series - remove non-essential
        total_cases_ts = global_cases_df.copy().drop(["Lat", "Long", "Country/Region", "Province/State"], axis=1).sum()
        total_deaths_ts = global_deaths_csv_df.copy().drop(["Lat", "Long", "Country/Region", "Province/State"],
                                                           axis=1).sum()
        total_recovered_ts = global_recovered_csv_df.copy().drop(["Lat", "Long", "Country/Region", "Province/State"],
                                                                 axis=1).sum()
        # Calculate Active Case Based on the Others
        total_active_cases_ts = pd.Series(
            data=np.array(
                [x1 - x2 - x3 for (x1, x2, x3) in zip(total_cases_ts, total_deaths_ts, total_recovered_ts)]),
            index=total_cases_ts.index)

        # Graph With All Time Series Data as Traces
        global_multi_line_graph = go.Figure()
        global_multi_line_graph.add_trace(go.Scatter(x=total_cases_ts.index,
                                                     y=total_cases_ts.values,
                                                     fill='tozeroy',  # fill color underneath line
                                                     mode='lines',
                                                     name='Total Cases'))
        global_multi_line_graph.add_trace(go.Scatter(x=total_active_cases_ts.index,
                                                     y=total_active_cases_ts.values,
                                                     fill='tozeroy',  # fill color underneath line
                                                     mode='lines',
                                                     name='Active Cases'))
        global_multi_line_graph.add_trace(go.Scatter(x=total_recovered_ts.index,
                                                     y=total_recovered_ts.values,
                                                     fill='tozeroy',  # fill color underneath line
                                                     mode='lines',
                                                     name='Total Recovered'))
        global_multi_line_graph.add_trace(go.Scatter(x=total_deaths_ts.index,
                                                     y=total_deaths_ts.values,
                                                     fill='tozeroy',  # fill color underneath line
                                                     mode='lines',
                                                     name='Total Deaths'))
        global_multi_line_graph.update_layout(title='Global Case Status',
                                              xaxis_title='Date',
                                              yaxis_title='Number of People')
        global_multi_line_graph.update_layout(template="plotly_dark")
        return global_multi_line_graph

    def generate_US_table(self):
        """
        creates table for countries and provinces with columns for cases, deaths, recovered and active
        :return: plotly data table
        """
        # US Data by State
        state_cases_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_state.csv"
        state_df = pd.read_csv(state_cases_csv)

        # List for Data Columns
        names = []
        cases = []
        recovered = []
        deaths = []

        # Access the Latest State Information (first 50 regions + districts) as lists
        for i in range(57):
            names.append(state_df["Province_State"][i])
            cases.append(state_df["Confirmed"][i])
            deaths.append(state_df["Deaths"][i])
            rec = state_df["Recovered"][i]
            if rec > 0:
                recovered.append(rec)
            else:
                recovered.append("No Data")

        US_table = go.Figure(data=[go.Table(
            header=dict(values=["State", "Cases", "Deaths", "Recovered"],
                        fill_color='#17181a',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[names, cases, deaths, recovered],
                       fill_color='#555863',
                       font=dict(color='white', size=12),
                       align='left'))
        ])
        return US_table

    def display_data(self):
        """
        displays all graphs and tables using Dash and Plotly Graphs. Html and DCC formatting tools from dash are used to
        organize graphs.
        :return: Dash user interface single-page web app
        """

        # WEB APP SECTIONS
        def build_banner():
            summary_json = "https://api.covid19api.com/summary"
            summary_df = self.get_json(summary_json)
            last_updated = summary_df["Date"]
            return html.Div(
                id="banner",
                className="container",
                children=[
                    html.Div(
                        id="banner-text",
                        children=[
                            html.H1(style={'color': 'white', 'padding-top': "25px", 'padding-bottom': "00px", "margin-bottom": "00px"},
                                    children="Coronavirus Tracker"),
                            html.H6(style={'color': '#d2d3d6', 'padding-top': "00px", "margin-top": "00px", "margin-bottom": "15px"}, children="Trevor Day School Intermediate Programming: Gina Mckeown"),
                            html.P(style={'color': '#d2d3d6', 'padding-top': "00px", 'padding-bottom': "00px", "margin-top": "00px", "margin-bottom": "00px"}, children="Data Last Updated: " + last_updated),
                        ]
                    )
                ],
            )

        # Organizes Tabs
        def build_tabs():
            return html.Div(
                id="tabs",
                className="tab-container container",
                children=[
                    dcc.Tabs(
                        id="main-tabs",
                        value="tab1",  # set default tab
                        className="custom-tabs",
                        children=[
                            dcc.Tab(
                                id="global-tab",
                                label="Global Data",
                                value="tab1",
                                className="custom-tabs",
                                selected_className="custom-tab-selected-left",
                                style={
                                    "border-radius": "5px",
                                    "margin-bottom": "15px",
                                    "margin-right": "10px",
                                    "background-color": "#535a66",
                                    'color': 'white',
                                    "border-color": "#535a66",
                                    "padding-bottom": "15 px",
                                    "box-shadow": "0 10px 6px -6px #282b2e",
                                },
                                children=[
                                    build_global_tab()
                                ]
                            ),
                            dcc.Tab(
                                id="us-tab",
                                label="United States Data",
                                value="tab2",
                                className="custom-tabs",
                                selected_className="custom-tab-selected-right",
                                style={
                                    "border-radius": "5px",
                                    "margin-bottom": "15px",
                                    "margin-left": "10px",
                                    "background-color": "#535a66",
                                    'color': 'white',
                                    "border-color": "#535a66",
                                    "padding-bottom": "15 px",
                                    "box-shadow": "0 10px 6px -6px #282b2e",
                                },
                                children=[
                                    build_US_tab()
                                ]
                            ),
                        ],
                    ),
                ]
            )

        # Individual Tabs
        def build_global_tab():
            # Global Widget Data for Global Tab
            summary_json = "https://api.covid19api.com/summary"
            summary_df = self.get_json(summary_json)
            total_cases = summary_df["Global"]["TotalConfirmed"]
            total_deaths = summary_df["Global"]["TotalDeaths"]
            total_recovered = summary_df["Global"]["TotalRecovered"]

            return html.Div(
                id="tab1-layout",
                children=[
                    # Main Data Widgets
                    html.Div(
                        id="widgets",
                        className="row",
                        style={'color': 'white', 'text-align': 'center'},
                        children=[
                            html.Div(
                                id="cases",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(total_cases))),  # convert str and add commas
                                    html.H6(html.P("Total Cases"))
                                ],
                            ),
                            html.Div(
                                id="deaths",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(total_deaths))),  # convert str and add commas
                                    html.H6(html.P("Total Deaths"))
                                ],
                            ),
                            html.Div(
                                id="recovered",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(total_recovered))),  # convert str and add commas
                                    html.H6(html.P("Total Recovered"))
                                ],
                            )
                        ],
                    ),
                    # Global Graphs Underneath Widgets
                    html.Div(
                        id="map",
                        className="pretty_container twelve columns",
                        children=[dcc.Graph(figure=self.generate_global_map())]
                    ),
                    html.Div(
                        id="multi-line-graph",
                        className="pretty_container twelve columns",
                        children=[dcc.Graph(figure=self.generate_multiline_graph())]
                    ),
                    html.Div(
                        id="global-table",
                        className="pretty_container twelve columns",
                        children=[dcc.Graph(figure=self.generate_global_table())]
                    ),
                ])

        # Individual Tabs
        def build_US_tab():
            # US Widget Data
            global_csv = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
            global_df = pd.read_csv(global_csv)
            US_cases = global_df["Confirmed"][17]
            US_deaths = global_df["Deaths"][17]
            US_recovered = global_df["Recovered"][17]

            return html.Div(
                id="tab2-layout",
                children=[
                    # Main Data Widgets
                    html.Div(
                        id="us-widgets",
                        className="row",
                        style={'color': 'white', 'text-align': 'center'},
                        children=[
                            html.Div(
                                id="us-cases",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(int(US_cases)))),  # convert str and add commas
                                    html.H6(html.P("U.S. Cases"))
                                ],
                            ),
                            html.Div(
                                id="us-deaths",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(int(US_deaths)))),  # convert str and add commas
                                    html.H6(html.P("U.S. Deaths"))
                                ],
                            ),
                            html.Div(
                                id="us-recovered",
                                className="mini_container four columns",
                                children=[
                                    html.H4(str("{:,}".format(int(US_recovered)))),  # convert str and add commas
                                    html.H6(html.P("U.S. Recovered"))
                                ],
                            )
                        ],
                    ),
                    # Global Graphs Underneath Widgets
                    html.Div(
                        id="us-map",
                        className="pretty_container twelve columns",
                        children=[dcc.Graph(figure=self.generate_US_map())]
                    ),
                    # Row Split into Two Containers
                    html.Div(className="row,",
                             children=[
                                 html.Div(
                                     id="us-line-graph",
                                     className="pretty_container six columns",
                                     children=[dcc.Graph(figure=self.generate_US_line_graph())]
                                 ),
                                 html.Div(
                                     id="us_table",
                                     className="pretty_container six columns",
                                     children=[dcc.Graph(figure=self.generate_US_table())]
                                 ),
                             ])
                ])

        # CREATE WEB APP
        app = dash.Dash(__name__)

        # Build Full App Layout
        app.layout = html.Div(
            id="full-app-container",
            className="big-app-container",
            style={'backgroundColor': '#383e47'},
            children=[
                build_banner(),
                html.Div(
                    id="tab-container",
                    children=[
                        # Two Main Data Tabs
                        build_tabs(),
                    ],
                ),
            ],
        )

        # Run the App
        app.run_server()


if __name__ == "__main__":
    COVID19_web_app = DataVisualization()
    COVID19_web_app.display_data()
