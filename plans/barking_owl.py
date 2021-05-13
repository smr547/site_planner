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
house = house.move(-6.0, -37.0)
house.rotate(-15)

house.move(east_metres=17, north_metres=2)
n_offset = 3.5 # 
e_offset = 3 # -9
s.add_structure(house)

water_tank1= Structure("Water Tank 1")
water_tank1.add(Circle(Point(0,0), 5))
water_tank1.move(-35,-9)
s.add_structure(water_tank1)

water_tank2= Structure("Water Tank 2")
water_tank2.add(Circle(Point(0,0), 5))
water_tank2.move(-35,2)
s.add_structure(water_tank2)

shed = Structure("Shed", description="18x9m 15deg pitched roof")

shed.add(Rectangle(width=20, height=4))
shed.add(Rectangle(origin=Point(0,4.05), width=20, height=4))
# add shed doors
for i in range(0,3):
    shed.add(Rectangle(Point(0.5+(3.875*i), 6.80), width=2.8, height=0.35))
shed.rotate(-90)
shed.move(-35+e_offset, -15+n_offset)
s.add_structure(shed)

# genset and solar panels

sg = Structure("Genset")
# sg.add(Rectangle(width = 12.0, height=4.0))
sg.add(Rectangle(Point(14,0), width=1, height=2))
sg.move(-35+e_offset, -15+n_offset)
# s.add_structure(sg)
# sg.move(8.5, 2)

# roof mounted solar panels

spw = Structure("Solar Panels - West")
for c in range(0,2):
    for r in range(0,12):
        panel = Rectangle(origin=Point(c*1.75,r*1.05), width=1.7, height=1)
        spw.add(panel)
spw.move(-28.75+e_offset, -19.5+n_offset)
s.add_structure(spw)

spe = Structure("Solar Panels - East")
for c in range(0,2):
    for r in range(0,12):
        panel = Rectangle(origin=Point(c*1.75,r*1.05), width=1.7, height=1)
        spe.add(panel)
spe.move(-24.75+e_offset, -19.5+n_offset)
s.add_structure(spe)

# shipping container

sc = Structure("Shipping Container", description="40' shipping container")
sc.add(Rectangle(width = 2.44, height=12.2))
sc.move(-32.5+e_offset, -14+n_offset)
s.add_structure(sc)




print s.get_kml()
