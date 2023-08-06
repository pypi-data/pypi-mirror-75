# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:35:30 2020

@author: Reza
"""

import math

class Points:
    """
    The Parent Points class represents two points in euclidean plane or geodesic plane
    """

    def __init__(self, coordinate_1, coordinate_2):
        """
        Method for initializing a Point Class

        Args:
            coordinate_1 (tuple)
            coordinate_2 (tuple)
            distance (float)

        Attributes:
            coordinate_1 (tuple): Coordinates in euclidean or geodesic plane
            coordinate_2 (tuple): Coordinates in euclidean or geodesic plane
            distance(float): Distance between two points
        """

        self.coordinate_1 = coordinate_1
        self.coordinate_2 = coordinate_2
        self.distance = math.nan

class GeodesicPoints(Points):
    """
    The GeodesicPoints represents points in geodesic plane
    """

    def __init__(self, coordinate_1, coordinate_2):
        """
        Method for initializing two geodesic points

        Args:
            coordinate_1 (tuple): (latitude, longitude)
            coordinate_2 (tuple): (latitude, longitude)
            distance (float)

        Attributes:
            coordinate_1 (tuple): Coordinates in geodesic plane
            coordinate_2 (tuple): Coordinates in geodesic plane
            distance(float): Distance between two geodesic points
        """

        Points.__init__(self, coordinate_1, coordinate_2)
        """
        Methods for inheriting Points class
        """
        
        def geodesic_distance(self):
            """
            Method for finding the distance between two geodesic points
            Haversine Formula
            """

            lat_1, lon_1 = self.coordinate_1
            lat_2, lon_2 = self.coordinate_2
            radius = 6371 # radius of earth in km
            
            # Check the limits of the coordinates
            coordinate_limit = [lat_1 >= -90,
                                lat_1 <= 90,
                                lat_2 >= -90,
                                lat_2 <= 90,
                                lon_1 >= -180,
                                lon_1 <= 180,
                                lon_2 >= -180,
                                lon_2 <= 180]
        
            if all(coordinate_limit):
                del_lat = math.radians(lat_2-lat_1)
                del_lon = math.radians(lon_2-lon_1)
                a = math.sin(del_lat/2) * math.sin(del_lat/2) + math.cos(math.radians(lat_1)) \
                    * math.cos(math.radians(lat_2)) * math.sin(del_lon/2) * math.sin(del_lon/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return round(radius * c, 4)
        
        # Assign distance to the class
        self.distance = geodesic_distance(self)
             
class EuclideanPoints(Points):
    """
    The EuclideanPoints represents points in euclidean plane
    """

    def __init__(self, coordinate_1, coordinate_2):
        """
        Method for initializing two geodesic points

        Args:
            coordinate_1 (tuple): (x, y)
            coordinate_2 (tuple): (x, y)
            distance (float)

        Attributes:
            coordinate_1 (tuple): Coordinates in euclidean plane
            coordinate_2 (tuple): Coordinates in euclidean plane
            distance(float): Distance between two points
        """
        
        Points.__init__(self, coordinate_1, coordinate_2)
        """
        Methods for inheriting Points class
        """
        
        def euclidean_distance(self):
            """
            Method for finding the distance between two euclidean points
            """

            x_1, y_1 = self.coordinate_1
            x_2, y_2 = self.coordinate_2
            return round(math.sqrt((x_1-x_2)**2 + (y_1-y_2)**2), 4)
        
        # Assign distance to the class
        self.distance = euclidean_distance(self)