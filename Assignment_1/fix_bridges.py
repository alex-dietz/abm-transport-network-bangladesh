

import os
from math import isnan

import csv
import pandas as pd
class RoadRecord:
    def __init__(self, lat, lon, lrps, chainage, road_type, name):
        self.lat = lat
        self.lon = lon
        self.lrps = lrps
        self.chainage = chainage
        self.road_type = road_type
        self.name = name
        self.bf = ""

def read_roads(filename):
    """
    Reads the road data from the csv file and returns a dictionary of road names and a list of RoadRecords
    Parameters:
        filename (str): the name of the file to read
    Returns:
        road_map (dict): a dictionary of road names and a list of RoadRecords
    """
    file = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + filename
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)  # skip the header row
        last_road = ""
        road_map = {}
        for row in reader:
            road_name = row[0]
            newRoad = not road_name == last_road
            if newRoad:
                road_list = []
                road_map[road_name] = road_list
            lrps = row[2]
            chainage = float(row[1])
            lat = float(row[3])
            lon = float(row[4])
            bf = row[5]
            road_type = row[6]
            name = row[7]
            rr = RoadRecord(lat, lon, lrps, chainage, road_type, name)
            rr.bf = bf
            road_list.append(rr)
            last_road = road_name    
    return road_map

def correct_bridge_information(bridge):
    """
    Corrects the bridge information by looking up the chainage in the road dataset
    Parameters:
        bridge (dict): the bridge information
    Returns:
        bridge (dict): the corrected bridge information
    """
    try:
        #Check if bridge is "cleanable"
        if len(bridge['road']) > 0 and bridge['chainage'] != '':
                road = bridge['road']
                chainage = bridge['chainage']
                lrpName = bridge['LRPName']
                
                if bridge['chainage'] > 0 and not isnan(bridge['chainage']):
                    # look up chainage location in cleaned Road set
                    if road not in roads:
                        print(f"{road} not found in road dataset for bridge {road}.{lrpName} at {chainage} km")
                        #Remove bridge by marking it with "not found"
                        bridge['EstimatedLoc'] = "not found"
                        

                    else:
                        roadList = roads[road]
                        if roadList[-1].chainage < chainage:
                            print(f"{road} with bridge {road}.{lrpName} at {chainage} km is beyond the chainage of the road")
                            bridge['EstimatedLoc'] = "not found"
                        else:
                            for i in range(len(roadList) - 2):
                                if roadList[i].chainage == chainage:
                                    # exact match
                                    bridge['lat'], bridge['lon'] = roadList[i].lat, roadList[i].lon
                                    bridge['EstimatedLoc'] = "exact"
                                    print(f"{road} with bridge {road}.{lrpName} at {chainage} exact location")
                                    break
                                if roadList[i].chainage < chainage and roadList[i + 1].chainage >= chainage:
                                    # interpolate with next and previous point
                                    bridge_chainage, next_road_point_chainage, previous_road_point_chainage = chainage, roadList[i + 1].chainage, roadList[i].chainage
                                    #ratio of chainages
                                    ratio = (next_road_point_chainage - bridge_chainage) / (next_road_point_chainage - previous_road_point_chainage)
                                    lat_p, lon_p = roadList[i].lat, roadList[i].lon
                                    lat_n, lon_n = roadList[i + 1].lat, roadList[i + 1].lon
                                    # interpolate by ratio of chainages
                                    bridge['lat'] = lat_n - ratio * (lat_n - lat_p)
                                    bridge['lon'] = lon_n - ratio * (lon_n - lon_p)
                                    #Mark bridge as interpolated
                                    bridge['EstimatedLoc'] = "interpolate"
                                    print(f"{road} with bridge {road}.{lrpName} at {chainage} interpolated location")
                                    break                                                                                

        return bridge
    
    except Exception as e:
        print(e)
        return bridge


def read_bridge_overview(bmms_file_path):
    """
    reads the bridge overview from the excel file and saves it to a new excel file
    Parameters:
        bmms_file_path (str): the path to the excel file
    Returns:
        None
    """
    file = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + bmms_file_path
    #read bridges
    df = pd.read_excel(file)
    #correct bridge information
    df = df.apply(correct_bridge_information, axis=1)
    #filter out bridges with not found location
    df = df[df['EstimatedLoc'] != "not found"]
    #Count number of interpolated bridges
    print(f"Number of interpolated bridges: {len(df[df['EstimatedLoc'] == 'interpolate'])}")
    #save to file called overview
    df.to_excel("WBSIM/infrastructure/BMMS_overview.xlsx", index=False,sheet_name='BMMS_overview')
        
   
   
if __name__ == '__main__':
    #set file paths
    bridges_path ="/BMMS/BMMS_overview.xls"
    roads_path = "/WBSIM/_roads3.csv"

    #loop through all roads of RMMS
    roads = read_roads(roads_path)
    #loop through all bridges of BMMS
    read_bridge_overview(bridges_path)