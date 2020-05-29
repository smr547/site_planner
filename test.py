#!/usr/bin/env python

from shapely.geometry import Point  
from site_planner import Site, SiteRenderer, Structure, Rectangle, Circle

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
house = house.move(-10.0, -28.0)

s.add_structure(house)

water_tank = Structure("Water Tank")
water_tank.add(Circle(Point(-32,-24), 4))
s.add_structure(water_tank)

shed = Structure("Shed")
shed.add(Rectangle(width=15, height=7))
# add shed doors
for i in range(0,3):
    shed.add(Rectangle(Point(0.5+(3.875*i), 6.80), width=2.8, height=0.35))
shed.rotate(-90)
shed.move(-35, -15)
s.add_structure(shed)

# genset and solar panels

sg = Structure("Solar panels and Genset")
sg.add(Rectangle(width = 12.0, height=4.0))
sg.add(Rectangle(Point(14,0), width=1, height=2))
sg.move(-52, -24)
s.add_structure(sg)

print s.get_kml()  
