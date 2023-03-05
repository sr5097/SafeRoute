
import math
from diffprivacytest1 import random_laplace_noise_trial
from distance_calculator import geodesic_meters, caldistance, caldistance_peturbed
from translate import Translator
from geopy.geocoders import Nominatim
loc = Nominatim(user_agent="GetLoc")
avg = 0

epislon = [0.1]
listoflocations = []
loca = ["Al Nahda", "Deira", "Bur Dubai"]

for i in range(3):
    x = input("Hey there please enter your location: ")
    getLoc = loc.geocode(x)
    print("Original location's coordinates", getLoc.latitude, getLoc.longitude)
    location = (getLoc.latitude,getLoc.longitude)
    listoflocations.append(location)


for e in range(len(epislon)):
    #print("Trial for epislon", epislon[e])
    all_values = []
    totalsum = 0

    for i in range(1):
        #print("The trial count is ", i)
        actual_sum_lat = 0
        actual_sum_log = 0
        perturbed_sum_lat = 0
        perturbed_sum_log = 0
        D1 = 0
        
        counter = len(listoflocations)
        eps = epislon[e]/counter
        #print("the length is = ", len(listoflocations))
        noisylocations = []
        #print("noisy", noisylocations)

        for z in range(counter):
            #x, y = [float(x) for x in input("Enter the latitude and longitude values: ").split()]
            
            location = listoflocations[z]
            #print("The Original location is = ", location)
            actual_sum_lat = actual_sum_lat + location[0]
            actual_sum_log = actual_sum_log + location[1]

            trial_noise = random_laplace_noise_trial(eps, location[0])
            #print("The noise is", trial_noise)

            latitude = location[0] + trial_noise[0] * 180/math.pi
            longitude = location[1] + trial_noise[1] * 180/math.pi
            perturbed_location = latitude, longitude

            perturbed_sum_lat = perturbed_sum_lat + latitude
            perturbed_sum_log = perturbed_sum_log + longitude

            #print("The Peturbed location is = ", perturbed_location)
            noisylocations.append(perturbed_location)
            #print("The distance b/w is ",   geodesic_meters (location, perturbed_location), "meters")

        #print(noisylocations)
        #True centroid
        x_centroid = actual_sum_lat/counter 
        y_centroid = actual_sum_log/counter

        #Additional Noisy location: Test 1
        #add_loc = (x_centroid,y_centroid)

        x4 = (counter+1)*(x_centroid) - perturbed_sum_lat
        y4 = (counter+1)*(y_centroid) - perturbed_sum_log
        fakelocation =(x4, y4)
        noisylocations.append(fakelocation)
        print(noisylocations)

        #Adding the noisy location to existing sum of latitudes and longitudes 
        perturbed_sum_lat = perturbed_sum_lat + x4
        perturbed_sum_log = perturbed_sum_log + y4
        #print("the additional noise is = ",add_x, add_y)
        
        
        #centroid of the perturbed locations 
        x_perturbed_centroid = perturbed_sum_lat/(counter + 1)
        y_perturbed_centroid = perturbed_sum_log/(counter + 1)
        
        #Printing the centroids and the distance between them
        centroid = (x_centroid, y_centroid)
        perturbed_centroid = (x_perturbed_centroid, y_perturbed_centroid)


        original_rest = caldistance(listoflocations)
        perturbed_rest = caldistance_peturbed(noisylocations)
        
        print("We ran it through our database of restaurents in Manhatten ")
        print ("The closest restaurent to your actual locations is", round(original_rest[0],2), "with the id",original_rest[1], "at", original_rest[2])
        print ("The closest restaurent to your perturbed locations is", round(perturbed_rest[0],2), "with the id",perturbed_rest[1], "at", perturbed_rest[2])
        

        # total Distance of true locations to the restaurent that is returned by the cloud server when input = perturbed and fake locations
        # D2 = geodesic_meters(perturbed_rest[2], listoflocations[0]) + geodesic_meters(perturbed_rest[2], listoflocations[1]) + geodesic_meters(perturbed_rest[2], listoflocations[2])
        D2 = 0
        for userloc in range(len(listoflocations)):
            D2 = geodesic_meters(perturbed_rest[2], listoflocations[userloc]) + D2
        #total distance of true locations to closest restaurent 
        D1 = original_rest[0]
        
        #print("D1=",original_rest[0] )
        avg = avg + round(D2-D1, 2)
        print(str(round(D2-D1, 2)))
        all_values.append(round(D2-D1, 2))

print("The extra distance to ensure your privacy that you may have to travel is", avg)
x = input("Are you done???")

