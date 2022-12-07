import json
import os

import pandas as pd


def create_json_data(flsname):
    #print(flsname)
    m = 0
    size=0
    writejson = open("new.json", "w")
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


if __name__ == '__main__':
    entire_df = pd.DataFrame()
    listoffls=['adsblog_ny0.txt.2022101800','adsblog_ny0.txt.2022101700']
    for fls in listoffls:
        create_json_data(fls)
        df = pd.read_json('new.json')
        entire_df.append(df)
        print(len(df))
        print(f"Min pickup time: {df.datetime.min()}")
        print(f"Min pickup time: {df.datetime.max()}")
        os.remove("new.json")

    print(f"Min pickup time: {entire_df.datetime.min()}")
    print(f"Min pickup time: {entire_df.datetime.max()}")
    print(entire_df)
