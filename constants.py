from pictures import *

###CONSTANTS
#RATIO
PIXELS_PER_KILOMETER = 5

#PROBABILITIES
VOLCANO_SPAWN_CHANCE = [[1, 1], [0.25, 2]] #ONE, TWO

#DIRS
INPUT_DIR = 'map'


MAPS_DIR = 'maps'
HTML_DIR = 'html'
TEXTS_DIR = 'texts'

RESOURCES_DIR = 'resources'
RESOURCES_HTML_DIR = RESOURCES_DIR+'/html'
RESOURCES_HTML_BIOMES_DIR = RESOURCES_HTML_DIR+'/biomes'
RESOURCES_HTML_LANDMARKS_DIR = RESOURCES_HTML_DIR+'/landmarks'
RESOURCES_GENERATORS_DIR = RESOURCES_DIR + '/generators'

GENERATOR_VOLCANO_NAME_PATH = [RESOURCES_GENERATORS_DIR+'/volcano1.txt', RESOURCES_GENERATORS_DIR+'/volcano2.txt']
GENERATOR_RIVER_NAME_PATH = [RESOURCES_GENERATORS_DIR+'/river1.txt', RESOURCES_GENERATORS_DIR+'/river2.txt']

OUTPUT_DIR = 'results'
OUTPUT_HTML_DIR = OUTPUT_DIR+'/html'
OUTPUT_HTML_BIOMES_DIR = OUTPUT_HTML_DIR+'/biomes'
OUTPUT_HTML_LANDMARKS_DIR = OUTPUT_HTML_DIR+'/landmarks'
OUTPUT_HTML_LANDMARKS_VOLCANOES_DIR = OUTPUT_HTML_LANDMARKS_DIR+'/volcanoes'
OUTPUT_HTML_LANDMARKS_RIVERS_DIR = OUTPUT_HTML_LANDMARKS_DIR+'/rivers'
OUTPUT_TEXTS_DIR = OUTPUT_DIR + '/texts'
OUTPUT_TEXTS_LANDMARKS_DIR = OUTPUT_TEXTS_DIR + '/landmarks'
OUTPUT_TEXTS_LANDMARKS_RIVERS_DIR = OUTPUT_TEXTS_LANDMARKS_DIR + '/rivers'

#FORMATS
PICTURE_FORMAT = '.png'
TEXTFILE_FORMAT = '.txt'
HTML_FORMAT = '.html'

#FILES
BIOMES_MAP_NAME = 'biomes'
HEIGHT_MAP_NAME = 'heightmap'
CLEAN_MAP_NAME = 'clean_map'

LANDMARK_FILE_NAME = 'landmark_map'

#COLORS
VOID = (255, 255, 255, 255)

BIOM_OCEAN = (0, 0, 255, 255) #0000ff ocean
BIOM_LAKE = (0, 136, 255, 255) #0088ff - lake
BIOM_RIVER = (0, 255, 255, 255) #00ffff - river

BIOM_MOUNTAIN = (0, 0, 0, 255) #000000 - mountain
#004400 - taiga forest
#008800 - swamp
#00ff00 - decisious forest
#88ff00 - grassland
BIOM_DESERT = (255, 255, 0, 255)#ffff00 - desert

LANDMARK_VOLCANO = (255, 0, 0, 255) ##ff0000 Volcano
LANDMARK_RIVER_MERGE = (255, 0, 0, 254) ##ff0000 Volcano