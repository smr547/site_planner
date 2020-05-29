#!/bin/bash 
#
# Start the KML server
#
cd plans/
python3 -m http.server &
