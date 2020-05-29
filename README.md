# Site Planner

Build a site plan for your new home or farm and have it displayed on Google Earth

![Sample result in Google Earth](/screen_grab.png)

## Site Plans

Each site plan is a simple python program

## Publishing your plans
[publish_plan.py](./publish_plan.py) takes a plan from the [plans directory]/(./plans)
and publishes the resulting KML file to the [served_plans directory](./served_plans)

## Serving the KML
Serve the plans by running [start_server.sh](start_server.sh)

## Displaying on Google Earth
1. Start Google Earth on your laptop or desktop computer
1. Select ``add / Network Link`` from the menu
1. Enter a name for your plan
1. Enter a URL like ``http:localhost:8000//barking_owl.kml``
1. Press OK
1. Zoom in to see your site plan
