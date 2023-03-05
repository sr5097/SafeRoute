from tkinter.tix import PopupMenu
from geopy.distance import geodesic
import csv
import pandas as pd
 

restaurents_coordinates = []
rests = []

data = open("poiYelpManhattan.csv" , "r") 
reader_variable = csv.reader(data, delimiter=',')
for rest_cord in reader_variable:
    lat, log = float(rest_cord[1]), float(rest_cord[2])
    if (lat > 40.749000 and lat < 40.762268 and log > -73.993678 and log < -73.98800):
        location = (lat, log)
        #print(location)
        restaurents_coordinates.append(location)
        rests.append(rest_cord[0])
     

def geodesic_meters(pt1, pt2):
    dist = geodesic(pt1, pt2).meters
    return round(dist,2)
 

def caldistance (userlocations):
    minimum = 0
    coordinate = 0
    for r in range(len(restaurents_coordinates)):
        totaldis = 0
        for z in range(len(userlocations)):
            dis = geodesic_meters(restaurents_coordinates[r], userlocations[z])            
            totaldis = dis + totaldis
        if(minimum == 0): 
            minimum = totaldis
            coordinate = restaurents_coordinates[r]
        elif (totaldis< minimum):
            minimum = totaldis
            coordinate = restaurents_coordinates[r]
        else:
            pass

    #print("coordinate", point)
    for i in range(len(restaurents_coordinates)):
        point = restaurents_coordinates[i]
        for j in range(len(coordinate)):
            if(point[j] == coordinate[j]):
                index = i
            else:
                break

    rest_id = rests[index]
            
    #print(list(final.keys())[list(final.values()).index([coordinate])])
    return minimum, rest_id, coordinate

     
def caldistance_peturbed (userlocations):
    minimum = 0
    coordinate = (0,0)
    for r in range(len(restaurents_coordinates)):
        totaldis_peturbed = 0
        for z in range(len(userlocations)): 
            dis = geodesic_meters(restaurents_coordinates[r], userlocations[z])            
            totaldis_peturbed = dis + totaldis_peturbed
        if(minimum == 0): 
            minimum = totaldis_peturbed
            coordinate = restaurents_coordinates[r]
        elif (totaldis_peturbed <= minimum):
            minimum = totaldis_peturbed
            coordinate = restaurents_coordinates[r]
        else:
            pass

    for i in range(len(restaurents_coordinates)):
        point = restaurents_coordinates[i]
        for j in range(len(coordinate)):
            if(point[j] == coordinate[j]):
                index = i
            else:
                break
    
    rest_id = rests[index]
    
    return minimum, rest_id, coordinate
