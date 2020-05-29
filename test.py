#!/usr/bin/env python

from shapely.geometry import Point  
from site_planner import Site, SiteRenderer, Structure, Rectangle

s = Site("Barking Owl Farm", Point(149.250230, -34.897297))

house = Structure("Main house")
# main body of house
house = house.add(Rectangle(width=30.4, height=7.2))
# garage and mud room
house = house.add(Rectangle(origin=Point(4,6), width=8.9, height=9.5))
# north verandah
house = house.add(Rectangle(origin=Point(12,6), width=13.4, height=2.3))
# south verandah
house = house.add(Rectangle(origin=Point(11,-4.6), width=11.3, height=5.2))
house = house.move(-10.0, -38.0)

s.add_structure(house)

print s.get_kml()  
