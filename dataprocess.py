import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np
import seaborn as sns
import geopandas as gpd
import plotly.graph_objects as go


def create_json_data(flsname):
    #print(flsname)
    m = 0
    size=0
    writejson = open("new.json", "w")
    flsdata = open(flsname, "r")
    flsdata = open(flsname, "r")
    data = []
    for line in flsdata:
        temp_dict={}
        data_dict = json.loads(line)
        if 'flight' in data_dict['payload']:
            temp_dict['datetime'] = data_dict['dt']
            for payload_keys,payload_value in data_dict['payload'].items():
                temp_dict[payload_keys] = payload_value
        if temp_dict:
            data.append(temp_dict)
        #if temp_dict :
         #   print(temp_dict)
    #print(data)

    writejson.write(json.dumps(data))
    writejson.close()

def create_df():
    listoffls=['adsblog_ny0.txt.2022101800','adsblog_ny0.txt.2022101700','adsblog_ny0.txt.2022101600']
    for fls in listoffls:
        create_json_data(fls)
        df = pd.read_json('new.json')
        entire_list.append(df)
        os.remove("new.json")
        entire_df = pd.concat(entire_list, ignore_index=True)
    return(entire_df)

def groupby_flight_date(data):
    '''
    :param data:
    Plot the data by groupby with datetime and flight
    :return:
    '''
    df_new = df.groupby([df.datetime.dt.date]).count()['flight'].reset_index(name="#messages")
    df_new.plot(x='datetime', y='#messages', kind='bar')
    # print(df_new.columns.tolist())
    plt.bar(df_new['datetime'], df_new['#messages'])
    plt.xlabel("datetime")
    plt.ylabel("messages")
    plt.show()

def plot_by_flights(data):
    df_new = df.groupby(['flight']).count()['datetime'].reset_index(name="count").sort_values(['count'], ascending=False).head(5)
    print(df_new)
    df_new.plot(x='flight', y='count', kind='bar')
    plt.bar(df_new['flight'], df_new['count'])
    plt.xlabel("flight")
    plt.ylabel("Number of messages per Flight")
    plt.show()
    # for f in data.flight.unique():
    #     print (f)
    #     testdf = df.query("flight == @f ")
    #     print(f"length of {f} : {len(testdf)}")

def plot_heat_map1(data):
    #testdf = data.query("flight == 'SWQ2816 '").head(5)
    testdf = data.query("flight in ('SWQ2816 ','JZA478  ')").head(5)
    print(testdf[['lat','lon']].values.tolist())
    testdata=testdf[['lat','lon']].values.tolist()
    uniform_data = np.random.rand(10, 12)
    print(testdata)
    print("Old")
    ax = sns.heatmap(testdata, linewidth=0.5)
    plt.show()

def num_of_flights(data):
    count=data.flight.unique().size
    #print(data['flight'].unique().tolist())
    #print(count)
    df_new = df.groupby([df.datetime.dt.date])['flight'].nunique().reset_index(name="#flight")
    print(df_new)
    df_new.plot(x='datetime', y='#flight', kind='bar')
    plt.bar(df_new['datetime'], df_new['#flight'])
    plt.show()


def flat_list(lst):
    #print(lst)
    flat_list = []
    for ele in lst:
        ##print (ele)
        if type(ele) is list:
            for e in ele:
                flat_list.append(e)
    print(flat_list)
    ax = sns.heatmap(flat_list, linewidth=0.5)
    ax.set_xlabel('Lat / Lon')
    #ax.set_ylabel('Y-axis')
    plt.show()


def plot_heat_map(data):
    flightlist=['JZA478  ','SWQ2816 ','ACA56   ']
    temp_list=[]
    for fl in flightlist:
        testdf = data.query("flight == @fl").head(5)
        temp_list.append(testdf[['lat', 'lon']].values.tolist())
        ##flat_list(testdf[['lat', 'lon']].values.tolist())
        #print(temp_list)
    ##print(testdf[['lat','lon']].values.tolist())
    flat_list(temp_list)
    #ax = sns.heatmap(temp_list, linewidth=0.5)
    #plt.show()

def map_in_world1(data):
    #world= gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #gpd.plot()
    fig, ax = plt.subplots(facecolor='#FCF6F5FF')
    fig.set_size_inches(14, 7)
    flightlist = ['JZA478  ','SWQ2816 ','ACA56   ']
    temp_list = []
    for fl in flightlist:
        testdf = data.query("flight == @fl")
        ax.scatter(data['lon'], data['lat'], s=1, alpha=1, edgecolors='none')
        ax.axis('off')
    plt.show()

def map_in_world(data):
    fig = go.Figure()
    #flightlist = ['JZA478  ','SWQ2816 ','ACA56   ']
    temp_list = []
    for fl in data['flight'].unique().tolist():
        testdf = data.query("flight == @fl")
        lonmin=testdf.lon.min() ##df.pickup_longitude.min()
        lonmax=testdf.lon.max()
        latmin=testdf.lat.min()
        latmax=testdf.lat.max()
        flightnm=str(testdf.flight.unique())
        fig.add_trace(go.Scattergeo(lat=[latmin,latmax],
                                   lon=[lonmin,lonmax],
                                    mode='lines',
                                    hoverinfo='lon+lat',
                                    line=dict(color="red")))
    fig.update_layout(height=700,width=900,margin={"t":0,"b":0,"l":0,"r":0,"pad":0},
                      showlegend=False)
    fig.show()

if __name__ == '__main__':
    entire_list = []
    df=create_df()
    print (len(df))
    ###groupby_flight_date(df)
    plot_by_flights(df)
    #plot_heat_map1(df)
    ###plot_heat_map(df)
    ###num_of_flights(df)
    ###map_in_world(df)
    #testdf=df.query("flight == 'SWQ2816 '")
    #print(testdf)
    #print(df.flight.unique())



