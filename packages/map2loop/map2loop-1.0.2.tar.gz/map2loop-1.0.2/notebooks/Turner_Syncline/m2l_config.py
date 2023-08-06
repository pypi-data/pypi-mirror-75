#ROI

step_out=0.1   #padding arounf dtm to ensure reprojected dtm covers target area (in degrees)
inset=0      #unused??

minx=500000 #region of interest coordinates in metre-based system (or non-degree system)
maxx=545000
miny=7490000
maxy=7520000
model_top=1200
model_base=-3200

#PATHS

local_paths=True       #flag to use local or WFS source for data inputs (True = local)
import os


last=os.path.split(os.getcwd())[1]

test_data_path='../'+last+'/'
clut_path='../source_data/500kibg_colours.csv'

data_path='../source_data/'

geology_file='hams2_geol.shp'   #input geology file (if local)
fault_file='GEOS_GEOLOGY_LINEARSTRUCTURE_500K_GSD.shp' #input fault file (if local)
structure_file='hams2_structure.shp' #input bedding orientation file (if local)
mindep_file='mindeps_2018.shp' #input mineral deposit file (if local)

#CRS

src_crs = {'init': 'epsg:4326'}  # coordinate reference system for imported dtms (geodetic lat/long WGS84)
dst_crs = {'init': 'epsg:28350'} # coordinate system for data

#CODES AND LABELS 
# these refer to specific fields (codes) in GIS layer or database that contain the info needed for these calcs and text substrings (labels) in the contents of these fields
c_l= {
#Orientations
  "d": "DIP",                  #field that contains dip information
  "dd": "DIP_DIR",             #field that contains dip direction information
  "sf": 'FEATURE',             #field that contains information on type of structure
  "bedding": 'Bed',            #text to search for in field defined by sf code to show that this is a bedding measurement
  "otype": 'dip direction',            #flag to determine measurement convention (currently 'strike' or 'dip direction')
  "bo": "TYPE",             #field that contains type of foliation
  "btype": 'overturned',            #text to search for in field defined by bo code to show that this is an overturned bedding measurement
#Stratigraphy
  "g": 'GROUP_',               #field that contains coarser stratigraphic coding
  "g2": 'SUPERSUITE',              #field that contains alternate coarser stratigraphic coding if 'g' is blank
  "c": 'UNITNAME',                 #field that contains finer stratigraphic coding
  "ds": 'DESCRIPTN',           #field that contains information about lithology
  "u": 'CODE',             #field that contains alternate stratigraphic coding (not used??)
  "r1": 'ROCKTYPE1',           #field that contains  extra lithology information
  "r2": 'ROCKTYPE2',           #field that contains even more lithology information
  "sill": 'sill',              #text to search for in field defined by ds code to show that this is a sill
  "intrusive": 'intrusive',    #text to search for in field defined by ds code to show that this is an intrusion
  "volcanic": 'volcanic',      #text to search for in field defined by ds code to show that this is an volv=canic (not intrusion)
#Mineral Deposits
  "msc": 'SITE_CODE',          #field that contains site code of deposit
  "msn": 'SHORT_NAME',         #field that contains short name of deposit
  "mst": 'SITE_TYPE_',         #field that contains site type of deposit
  "mtc": 'TARGET_COM',         #field that contains target commodity of deposit
  "mscm": 'SITE_COMMO',        #field that contains site commodity of deposit
  "mcom": 'COMMODITY_',        #field that contains commodity group of deposit
  "minf": 'Infrastructure',    #text to search for in field defined by mst code that shows site to ignore
#Timing
  "min": 'MIN_AGE_MA',         #field that contains minimum age of unit defined by ccode
  "max": 'MAX_AGE_MA',         #field that contains maximum age of unit defined by ccode
#faults and folds
  "f": 'FEATURE',              #field that contains information on type of structure
  "fault": 'Fault',            #text to search for in field defined by f code to show that this is a fault
  "fold": 'Fold axial trace',  #text to search for in field defined by f code to show that this is a fold axial trace
  "fdip": 'DIP',               # field for numeric fault dip value
  "fdipnull": '0',         # text to search for in field defined by fdip to show that this has no known dip
  "fdipdir": 'DIP_DIR',        # field for text fault dip direction value 
  "fdipdir_flag": 'alpha',        # flag for text fault dip direction type num e.g. 045 or alpha e.g. southeast    
  "fdipest": 'DIP_EST',        # field for text fault dip estimate value
  "fdipest_vals": 'gentle,moderate,steep',        # text to search for in field defined by fdipest to give fault dip estimate in increasing steepness
  "n": 'NAME',                 #field that contains information on name of fault (not used??)
  "t": 'TYPE',                 #field that contains information on type of fold
  "syn": 'syncline',           #text to search for in field defined by t to show that this is a syncline
#ids
  "o": 'OBJECTID',             #field that contains unique id of geometry object
  "gi": 'GEOPNT_ID'            #field that contains unique id of structure point
}

#DECIMATION

orientation_decimate=0  #store every nth orientation (in object order) 0 = save all
contact_decimate=10     #store every nth contact point (in object order) 0 = save all
fault_decimate=5        #store every nth fault point (in object order) 0 = save all
fold_decimate=5         #store every nth fold axial trace point (in object order) 0 = save all

#INTERPOLATION

gridx=50                #x grid dimensions (no of points, not distance) for interpolations
gridy=50                #x grid dimensions (no of points, not distance) for interpolations
scheme='scipy_rbf'      #interpolation scheme
dist_buffer=5           #buffer distance for clipping points by faults (in metres or same units as dst_crs)
intrusion_mode=0        # 1 all intrusions exluded from basal contacts, 0 only sills
use_interpolations=False    # flag to use interpolated orientations or not.

#ASSUMPTIONS

pluton_dip=45           #surface dip of pluton contacts
pluton_form='domes'     #saucers: \__+_+__/  batholith: +/       \+   domes: /  +  + \  pendant: +\_____/+
fault_dip=90            #surface dip of faults

#DERIVED AND FIXED PATHS

m2m_cpp_path='../m2m_cpp/'

graph_path=test_data_path+'graph/'
tmp_path=test_data_path+'tmp/'
#data_path=test_data_path+'data/'
dtm_path=test_data_path+'dtm/'
output_path=test_data_path+'output/'
vtk_path=test_data_path+'vtk/'

fault_file_csv=tmp_path+fault_file.replace(".shp",".csv")
structure_file_csv=tmp_path+structure_file.replace(".shp",".csv")
geology_file_csv=tmp_path+geology_file.replace(".shp",".csv")
mindep_file_csv=tmp_path+mindep_file.replace(".shp",".csv")

fault_file=data_path+fault_file
structure_file=data_path+structure_file
geology_file=data_path+geology_file
mindep_file=data_path+mindep_file

strat_graph_file=test_data_path+'graph/graph_strat_NONE.gml'

dtm_file=dtm_path+'dtm.tif'
dtm_reproj_file=dtm_path+'dtm_rp.tif'

if(not os.path.isdir(test_data_path)):
   os.mkdir(test_data_path)
if(not os.path.isdir(tmp_path)):
   os.mkdir(tmp_path)
if(not os.path.isdir(output_path)):
   os.mkdir(output_path)
if(not os.path.isdir(dtm_path)):
   os.mkdir(dtm_path)
if(not os.path.isdir(vtk_path)):
   os.mkdir(vtk_path)
if(not os.path.isdir(graph_path)):
   os.mkdir(graph_path)

print('Default parameters loaded from '+test_data_path+'m2l_config.py:')
with open(test_data_path+'m2l_config.py', 'r') as myfile:
  data = myfile.read()
  print(data)
  myfile.close()

print('\nModify these parameters in the cell below')