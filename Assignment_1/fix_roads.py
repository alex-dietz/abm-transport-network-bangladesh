import os
import urllib.parse

import math
def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the earth (specified in decimal degrees)
    Parameters:
    lat1, lon1 (float): Latitude and longitude of the first point
    lat2, lon2 (float): Latitude and longitude of the second point
    Returns:
    distance (float): Distance between the two points in km
    """
    p = 0.017453292519943295 # math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2.0 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1.0 - math.cos((lon2 - lon1) * p)) / 2.0
    return 12742.0 * math.asin(math.sqrt(a)) # 2 * R; R = 6371 km


class RoadRecord:
    """
    
    """
    def __init__(self, lat, lon, lrp, chainage, type, name):
        self.lat = lat
        self.lon = lon
        self.lrp = lrp
        self.chainage = chainage
        self.type = type
        self.name = name
        self.bf = ""        

    def __str__(self):
        return self.lrp+ "\t"+str(self.lat)+"\t"+str(self.lon)

def process_file(file):
    """
    Process a single file
    Parameters:
        file (str): Name of the file to process
    Returns:
        number_fixed_start_point (int): Number of start points that were fixed
        number_duplicates (int): Number of duplicate entries that were removed
        number_fixed_chainage (int): Number of chainages that were fixed
        number_fixed_outliers (int): Number of outliers that were fixed
    """

    #Check if fixed roads file already exists
    if not os.path.exists("WBSIM/_roads3.csv"):
        with open("WBSIM/_roads3.csv", "w", encoding="UTF-8") as overview:
            #write header line
            overview.write("\"road\",\"chainage\",\"lrp\",\"lat\",\"lon\",\"gap\",\"type\",\"name\"\n")
    if not os.path.exists("WBSIM/infrastructure/_roads.tcv"):
        with open("WBSIM/infrastructure/_roads.tcv", "w", encoding="UTF-8") as overview:
            #write header line
            header = ["road", "lrp1","lat1","lon1","lrp2","lat2","lon2"]
            overview.write("\t".join(header) + "\n")
    
    #Define road_name globally    
    global road_name
    road_name = file.split(os.extsep)[0]
    

    #Create list of road records
    rr_list = []
    rr_list = create_list_of_road_records(file)
    
    #Initialize counters for road
    number_fixed_start_point = 0
    number_duplicates = 0
    number_fixed_chainage = 0
    number_fixed_outliers = 0

    #Cleaning Steps
    rr_list,number_fixed_start_point = correct_road_start_points(rr_list)    
    rr_list,number_duplicates = remove_duplicates(rr_list)
    rr_list,number_fixed_chainage = fix_chainage(rr_list)
    rr_list,number_fixed_outliers = correct_outliers(rr_list)
    
    #Write to file
    write_cleaned_road_to_file(rr_list)
    #Return number of fixed entries
    return number_fixed_start_point,number_duplicates,number_fixed_chainage,number_fixed_outliers

def read_road_files():
    """
    Read all road files in the directory
    Parameters:
        None
    Returns:
        None
    """
     #loop through all files in the directory
    number_fixed_start_point=number_duplicates=number_fixed_chainage=number_fixed_outliers = 0
    for file in os.listdir(path):
        #select overview file with LRPs of each road
        if os.path.isfile(os.path.join(path, file)) and file.endswith(".lrps.htm"):   
            #process information of file                     
            numbers = process_file(file)
            #add numbers to total numbers
            number_fixed_start_point += numbers[0]
            number_duplicates += numbers[1]
            number_fixed_chainage += numbers[2]
            number_fixed_outliers += numbers[3]
    print("Fixed Start Points: ",number_fixed_start_point)
    print("Removed Duplicates: ",number_duplicates)
    print("Fixed Chainage: ",number_fixed_chainage)
    print("Fixed Outliers: ",number_fixed_outliers)


def create_list_of_road_records(file):
    """
    Create a list of road records from a file
    Parameters:
        file (str): Name of the file to process
    Returns:
        rr_list (list): List of road records
    """
    rr_list = []
    #read file line by line
    with open(path+file, 'r') as f:
        #loop through all lines of file
        for line in f:
            
            if "<a href=\"lrpmaps.asp?Latitude=" in line:
                
                parts = line.split("&amp;")
                
                if len(parts) > 2 and "Latitude=&amp;" not in line:
                    #all information is in html code of road page
                    lats = parts[0].split("=")[2]
                    lat = float(lats)
                    lons = parts[1].split("=")[1]
                    lon = float(lons)
                    lrps = parts[2].split("=")[1].replace("+", "")
                    chas = parts[6].split("=")[1].replace("%2E", ".")
                    chainage = float(chas)
                    type = parts[3].split("=")[1].replace("%2C", ",").replace("+", "")
                    type = " ".join(type.split())
                    name = parts[4].split("=")[1].replace("+", " ") if "=" in parts[4] and len(parts[4].split("=")) > 1 else "."
                    name = urllib.parse.unquote(name, 'UTF-8')
                    name = " ".join(name.split())
                    #create road record
                    rr = RoadRecord(lat, lon, lrps, chainage, type, name)
                    #add road record to list
                    rr_list.append(rr)
    return rr_list

def correct_road_start_points(rr_list):
    """ Correct start points of selected roads
    Parameters:
        rr_list (list): list of road records
    Returns:
        rr_list (list): list of road records
        i (int): number of corrected roads
    """
    #17832
    #Count of fixed entries
    i = 0
    #Fix Start Point of Z3711 and Z7717
    if road_name == 'Z3711' or road_name =='Z7717':
        rr_list[0].lat -= 1
        i += 1
    #Fix Start Point of Z5019 and Z1611
    if road_name == 'Z5019' or road_name =='Z1611':
        rr_list[0].lat += 1
        i += 1
    #Fix Start Point of N602 and Z8604
    if road_name == 'N602' or road_name =='Z8604':
        rr_list[0].lon += 1
        i += 1
    #Fix Start Point of Z4606 and Z1129
    if road_name == 'Z4606' or road_name =='Z1129':
        rr_list[0].lon -= 1
        i += 1
   
    return rr_list,i

def remove_duplicates(rr_list):
    """ Remove duplicate road records
    Parameters:
        rr_list (list): list of road records
    Returns:
        rr_list (list): list of road records
        j (int): number of removed duplicates
      """
    # Loop variable
    i = 0
    #Count of fixed entries
    j = 0
    while i < len(rr_list):
        if i + 1 < len(rr_list):
            #select current and next road record
            rr1 = rr_list[i]
            rr2 = rr_list[i + 1]
            #Check if two road records are the same
            if rr1.lrp == rr2.lrp or (rr1.lat == rr2.lat and rr1.lon == rr2.lon) or rr1.chainage == rr2.chainage:
                #remove duplicate
                rr_list.pop(i + 1)
                #add type and name to first road record
                rr1.name += " / " + rr2.name
                rr1.type += " / " + rr2.type              
                #increase counter of removed duplicates
                j += 1
            else:
                i += 1
        else:
            i += 1
    return rr_list,j

def fix_chainage(rr_list):
    """ Remove duplicate road records
    Parameters:
        rr_list (list): list of road records
    Returns:
        rr_list (list): list of road records
        j (int): number of removed duplicates
    """
    
    # Loop variable
    i = 0
    #Count of fixed entries
    j = 0
    while i < len(rr_list) - 2:
        #select current, next and next next road record
        rr1 = rr_list[i]
        rr2 = rr_list[i + 1]
        rr3 = rr_list[i + 2]
        #distance and chainage between first and second road record
        d12 = calculate_distance_km(rr1.lat, rr1.lon, rr2.lat, rr2.lon)
        c12 = rr2.chainage - rr1.chainage
        #distance and chainage between second and third road record
        d23 = calculate_distance_km(rr2.lat, rr2.lon, rr3.lat, rr3.lon)
        c23 = rr3.chainage - rr2.chainage
        #distance and chainage between first and third road record
        d13 = calculate_distance_km(rr1.lat, rr1.lon, rr3.lat, rr3.lon)
        c13 = rr3.chainage - rr1.chainage
        #Check if quotients are larger/below treshold
        if d12 / c12 > 1.2 and d23 / c23 > 1.2 and d13 / c13 < 2.0:
            #repair chainage by adjusting second road record assuming chainage values are correct
            rr2.lat = rr1.lat + (rr3.lat - rr1.lat) * (c12 / c13)
            rr2.lon = rr1.lon + (rr3.lon - rr1.lon) * (c12 / c13)
            #increase counter of repaired road records
            j += 1       
        i += 1
    return rr_list,j

def correct_outliers(rr_list):
    """ 
     Function to adjust coordinates that are too far away from the previous coordinate by a treshhold of 0.7 which would
     mean a distance of circa 55km.
     Parameters:
        rr_list (list): list of road records
    Returns:
        rr_list (list): list of road records
       """
    # Loop variable
    i = 0
    #Count of fixed entries
    j = 0
    while i < len(rr_list) - 1:
        #Select current and next road record
        rr1 = rr_list[i]
        rr2 = rr_list[i + 1]
        #Check if lat or lon is too far away from previous coordinate
        if rr2.lat - rr1.lat > 0.5 or rr2.lat - rr1.lat < -0.5:
            #adjust lat
            rr2.lat -= round(rr2.lat - rr1.lat)
            #increase counter of repaired road records
            j += 1
        if rr2.lon - rr1.lon > 0.5 or rr2.lon - rr1.lon < -0.5:
            #adjust lon
            rr2.lon -= round(rr2.lon - rr1.lon)
            #increase counter of repaired road records
            j += 1
        i += 1

    return rr_list,j

def write_cleaned_road_to_file(rr_list):
    """ Remove duplicate road records
    Parameters:
        rr_list (list): list of road records
    Returns:
        None
      """
    #Check if road has at least 4 points
    if len(rr_list) < 4:
        print(road_name + " not included -- #points < 4")
    else:             
        #Write to csv for overview used in bridge corrections
        with open("WBSIM/_roads3.csv", "a", encoding="UTF-8") as overview:
            for rr in rr_list:
                overview.write("\"" + road_name + "\",\"" + str(rr.chainage) + "\",\"" + rr.lrp + "\",\"" + str(rr.lat) + "\",\"" + str(rr.lon) + "\",\"" + rr.bf + "\",\"" + rr.type + "\",\"" + rr.name + "\"\n")
        #write to tcv for visualization
        with open("WBSIM/infrastructure/_roads.tcv", "a", encoding="UTF-8") as overview:                
            overview.write(road_name+'\t'+'\t'.join([str(x) for x in rr_list])+"\n")

def reset_road_files():
    """ Reset road files
    Parameters:
        None
    Returns:
        None
      """
    file = open("WBSIM/_roads3.csv", "w", encoding="UTF-8") 
    file.truncate()
    file.close()
    file = open("WBSIM/infrastructure/_roads.tcv", "w", encoding="UTF-8")
    file.truncate()
    file.close()
        

if __name__ == '__main__':
    #defines path to RMMS folder
    path = "RMMS/"
    #reset cleaned road files
    reset_road_files()
    #loop through all roads of RMMS
    read_road_files()