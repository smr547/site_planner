#!/usr/bin/env python

from shapely.geometry import Point  
from site_planner import Site, SiteRenderer

s = Site("Barking Owl Farm", Point(149.250230, -34.897297))
sr = SiteRenderer(s)

print sr.get_kml()  
