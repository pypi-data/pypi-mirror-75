import time

import psutil
import os

from meridian import Dataset, Record


def pretty_bytes(i):
    return f"{round(i/1e6, 2)} MB"


def count_nodes(geom):
    if geom.type == "Polygon":
        coords = len(geom.exterior.coords)
        for ring in geom.interiors:
            coords += len(ring.coords)
        return coords
    elif geom.type == "MultiPolygon":
        coords = 0
        for part in geom:
            coords += count_nodes(part)
        return coords
    else:
        raise ValueError("Unhandled geom type {}".format(geom.type))


class Building(Record):
    pass


class Parcel(Record):
    OBJECTID: int
    SPAN: str
    GLIST_SPAN: str
    MAPID: str
    PARCID: str
    PROPTYPE: str
    YEAR: int
    GLYEAR: str
    TOWN: str
    TNAME: str
    SOURCENAME: str
    SOURCETYPE: str
    SOURCEDATE: str
    EDITMETHOD: str
    EDITOR: str
    EDITDATE: str
    MATCHSTAT: str
    EDITNOTE: str
    OWNER1: str
    OWNER2: str
    ADDRGL1: str
    ADDRGL2: str
    CITYGL: str
    STGL: str
    ZIPGL: str
    DESCPROP: str
    LOCAPROP: str
    CAT: str
    RESCODE: str
    ACRESGL: str
    REAL_FLV: str
    HSTED_FLV: str
    NRES_FLV: str
    LAND_LV: str
    IMPRV_LV: str
    EQUIPVAL: str
    EQUIPCODE: str
    INVENVAL: str
    HSDECL: str
    HSITEVAL: str
    VETEXAMT: str
    EXPDESC: str
    ENDDATE: str
    STATUTE: str
    EXAMT_HS: str
    EXAMT_NR: str
    UVREDUC_HS: str
    UVREDUC_NR: str
    GLVAL_HS: str
    GLVAL_NR: str
    CRHOUSPCT: str
    MUNGL1PCT: str
    AOEGL_HS: str
    AOEGL_NR: str
    E911ADDR: str
    SHAPESTAre: float
    SHAPESTLen: float


process = psutil.Process(os.getpid())

try:
    # data = neighborhood_generator()

    print("Memory usage before load: ", pretty_bytes(process.memory_info().rss))

    print("loading data")

    start = time.time()

    """
    ---------------------------
    mx_nbrs_encoded.shp
    
    205.4 MB on disk
    Nodes: 9700219
    Geometries: 169483
    Nodes / Geometry: 57.2
    
    Meridian
    Memory usage: 541.01 MB
    Took 21.726
    
    GeoPandas
    Memory usage: 730.21 MB
    Took 26.306
    ---------------------------
    vt_buildings.json
    
    104 MB on disk
    Nodes: 2087498
    Geometries: 346038
    Nodes / Geometry: 6.0
    
    Meridian
    Memory usage: 329.13 MB
    Loading time: 48.549s
    
    GeoPandas
    Memory usage: 465.09 MB
    Loading time: 58.631s
    ---------------------------
    vt_parcels.geojson
    
    1.0 GB on disk
    Nodes: 14260763
    Geometries: 335550
    Nodes / Geometry: 42.5
    
    Meridian
    Memory usage: 1456.98 MB
    Loading time: 75.75s
    
    GeoPandas
    Memory usage: 3618.64 MB
    Loading time: 83.505s
    ---------------------------
    """
    # test_file = '/Users/tom/data/general/maponics_neighborhoods_2162/mx_nbrs_encoded.shp'
    # test_file = "/Users/tom/data/vt_buildings.geojson"
    test_file = '/Users/tom/data/vt_parcels.geojson'

    dataset = Parcel.load_from(test_file)
    print(dataset[0])

    # df = gpd.read_file(test_file)
    # spatial_index = df.sindex

    stop = time.time()

    print(f"Memory usage after load: {pretty_bytes(process.memory_info().rss)}")
    print("Took {}".format(round(stop - start, 3)))
except Exception as e:
    print(e)
finally:
    process.kill()
