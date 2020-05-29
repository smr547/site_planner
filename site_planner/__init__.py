from shapely.geometry import Point, box, MultiPolygon
from shapely.affinity import translate, rotate
from functools import partial
import pyproj
from shapely.ops import transform
from fastkml import kml



# class Rectangle(Polygon):
#     def __init__(self, origin=Point(0,0), width=1.0, height=1.0):
#         self = box(origin.x, orign.y, origin.x+width, origin.y+height)

def Rectangle(origin=Point(0,0), width=1.0, height=1.0):
    return box(origin.x, origin.y, origin.x+width, origin.y+height)

def Circle(origin=Point(0,0), radius=10.0):
    return origin.buffer(radius)

class Site(object):
    '''
    A site on which buildings and other structures are erected
    A Site's position on the Earth's surface is defined by 
    by a surveyor's mark called ref_mark
    '''
    def __init__(self, name='Name of site', ref_mark=Point(0,0)):
        '''
        Construct a new Site with a specified name and ref_mark
        The ref_mark is a Point on the Earth's surface in WSG84 coordinates usually describing 
        the position of some survey mark embedded in the ground
        See: https://rg-guidelines.nswlrs.com.au/deposited_plans/boundary_definition/boundary_and_reference_marks
        '''
       
        self.name = name
        self.ref_mark = ref_mark
        self.structures = []
        self.renderer = SiteRenderer(self)

    def add_structure(self, structure):
        if not isinstance(structure, Structure):
            raise ValueError("Cannot add %s to a Site, it must be a Structure" % (type(structure)))
        self.structures.append(structure)


    def get_kml(self):
        '''
        Render the Site as KML
        '''
        return self.renderer.get_kml()


    

class SiteRenderer(object):
    '''
    Renders a Site in KML
    '''
    def __init__(self, site):
        self.site = site
        if not isinstance(site, Site):
            raise ValueError("SiteRenderer requires a Site")

    def get_kml(self):
        '''
        Render the Site as KML
        '''
        k = kml.KML()
        ns = '{http://www.opengis.net/kml/2.2}'
        d = kml.Document(ns, self.site.name, self.site.name, "Site plan for %s" % (self.site.name))
        k.append(d)
        # nf = kml.Folder(ns, 'B1', 'building 1', 'Building one')
        # d.append(nf)

        # render the site reference mark as a KML Placemark
        p = kml.Placemark(ns, 'ref_mark', self.site.name, 'Reference survey mark')
        p.geometry = self.site.ref_mark
        d.append(p)

        # compute the UTM coords of the Site reference point

        crs = get_epsg(self.site.ref_mark)
        site_UTM = get_UTM_from_long_lat(self.site.ref_mark)
        project_UTM_to_WGS84 = partial(
            pyproj.transform,
            pyproj.Proj(init=crs),
            pyproj.Proj(init='epsg:4326'))

        folder = kml.Folder(ns, 'Structures', 'Structures','Structures on the site')
        d.append(folder)

        # render each Structure 

        for s in self.site.structures:
            name = s.name
            # work with the outline of the structure
            outline = s.geometry.buffer(0)
            # move outline into UTM coordinates for the site
            outline = translate(outline, xoff=site_UTM.x, yoff=site_UTM.y)
            # and transform to WGS84
            outline = transform(project_UTM_to_WGS84, outline)

            # place the outline in Structures folder
            p = kml.Placemark(ns, name, name, "Footprint of %s" % (name,))
            p.geometry = outline
            folder.append(p)
           
        # return the KML 

        return k.to_string(prettyprint=True)


class Structure(object):
    '''
    A named collection of Polygons representing a building or other construction
    on a Site. A structure is assembled by adding Polygons to the Structure. 
    The extent of the final structure is determined by the outline of the polygons
    Polygon dimensions and locations are expressed in metres
    The structure may be moved within it's own reference frame, only when a
    Structure is added to a Site is it's position on the Earth's surface determined
    '''
    def __init__(self, name='Name of structure', polygons=[]):
        self.name = name
        self.geometry = MultiPolygon(polygons)

    def add(self, polygon):
        '''
        Add the specified polygon to the Structure and return a new Structure 
        representing the assembly
        '''
        pgs = [p for p in self.geometry]
        pgs.append(polygon)
        self.geometry = MultiPolygon(pgs)
        return self

    def move(self, east_metres=0.0, north_metres=0.0):
        '''
        Move the Structure by the specified distance 
        To move south specify a negative value for north_metres. Same for west
        '''
        self.geometry = translate(self.geometry, xoff=east_metres, yoff=north_metres, zoff=0.0)
        return self

    def rotate(self, angle_deg, origin='center'):
        '''
        Rotate the structure CCW around origin (which may be 'centre', 'centroid'
        or a specified Point)
        '''
        self.geometry = rotate(self.geometry, angle=angle_deg, origin=origin, use_radians=False)  
        return self  

    def __str__(self):
        return "Structure %s with %d components" % (self.name, len(self.geometry))




_projections = {}


def zone(coordinates):
    if 56 <= coordinates[1] < 64 and 3 <= coordinates[0] < 12:
        return 32
    if 72 <= coordinates[1] < 84 and 0 <= coordinates[0] < 42:
        if coordinates[0] < 9:
            return 31
        elif coordinates[0] < 21:
            return 33
        elif coordinates[0] < 33:
            return 35
        return 37
    return int((coordinates[0] + 180) / 6) + 1


def letter(coordinates):
    return 'CDEFGHJKLMNPQRSTUVWXX'[int((coordinates[1] + 80) / 8)]


def project(coordinates):
    z = zone(coordinates)
    l = letter(coordinates)
    if z not in _projections:
        _projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
    x, y = _projections[z](coordinates[0], coordinates[1])
    if y < 0:
        y += 10000000
    return z, l, x, y


def unproject(z, l, x, y):
    if z not in _projections:
        _projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
    if l < 'N':
        y -= 10000000
    lng, lat = _projections[z](x, y, inverse=True)
    return (lng, lat)

def get_epsg(aPoint):
    (latitude, longitude) = (aPoint.y, aPoint.x)
    EPSG = int(32700-round((45+latitude)/90,0)*100+round((183+longitude)/6,0))
    return "epsg:%d" % (EPSG, ) 

def get_UTM_from_long_lat(aPoint):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(init=get_epsg(aPoint)))
    return transform(project, aPoint)

def get_WGS84_from_UTM(geom, site_origin_ll):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init=get_epsg(site_origin_ll)),
        pyproj.Proj(init='epsg:4326'))
    return transform(project, geom)

