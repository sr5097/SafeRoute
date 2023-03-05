 
from cmath import cos
import math
import numpy as np
import random
import scipy   
from scipy import special
 

#print("Testing to generate the perturbed location using the epislon value")
 
def random_laplace_noise_trial(eps, lat):
    
    """This function generates a random planer laplace noise with the given epsilon as the scale.
        Privacy budget: eps.
        Parameters
        eps :  The scale of targeted planer laplace distribution (>0).
        -------
        x :  x coordinate of the generated laplace noise.
        y :  y coordinate of the generated laplace noise.

    """
    R = 6378137

    # generate polar coordinates
    theta = np.random.uniform(0, 2 * math.pi)  # this shall be the angular coordinate 
 
    # draw a random sample from unif(0, 1)
    p = random.random()  
   
    # this shall be the radial coordinate
    r = -1 / eps * (scipy.special.lambertw((p - 1) / math.e, k=-1, \
                                       tol=1e-8).real + 1)   
                         
    while (r>100):                                  #bound the noise
        theta = np.random.uniform(0, 2 * math.pi)  # this shall be the angular coordinate 
        p = random.random() 
        r = -1 / eps * (scipy.special.lambertw((p - 1) / math.e, k=-1, \
                                           tol=1e-8).real + 1)   
         
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    
    x = x/R
    y = y/(R*cos(math.pi*lat/180))
    #print("The distance between the actual location and perturbed location =", round(r,3), "meters")
    
    return x, y.real

 


 