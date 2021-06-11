from PIL import Image
import numpy
import os
import shutil

###CONSTANTS
#DIRS
INPUT_DIR = 'map'
OUTPUT_DIR = 'results'

#MAPS
BIOMES_MAP_NAME = 'biomes.png'
HEIGHT_MAP_NAME = 'heightmap.png'
CLEAN_MAP_NAME = 'clean_map.png'

#COLORS
VOID = (255, 255, 255)

BIOM_OCEAN = (0, 0, 255) #0000ff ocean
BIOM_LAKE =(0, 136, 255) #0088ff - lake
BIOM_RIVER = (0, 255, 255)#00ffff - river

#000000 - mountain
#004400 - taiga forest
#008800 - swamp
#00ff00 - decisious forest
#88ff00 - grassland
#ffff00 - desert

#####################################################################################################################
###FUNCTIONS
def read_image(image_path):
    image = Image.open(image_path, "r")
    matrix = image.load()
    
    width, height = image.size
    
    myMatrix = []
    for x in range(width):
        myMatrixY = []
        for y in range(height):
            pixel = matrix[x, y]
            myMatrixY.append(pixel)
        myMatrix.append(myMatrixY)
    
    image.close()
    return myMatrix

#####################################################################################################################
def write_image(image_path, width, height):
    image = Image.new( mode = "RGB", size = (width, height))
    image.show()
    return image
   
#####################################################################################################################
def clean_image(image_path):
    image = Image.open(image_path)
    matrix = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if ((matrix[i,j] != BIOM_OCEAN) and (matrix[i,j] != BIOM_LAKE) and (matrix[i,j] != BIOM_RIVER)):
                matrix[i,j] = VOID
    image.save(image_path)
    image.close()
    

#####################################################################################################################
#MAIN#
#####################################################################################################################

#Create empty copy of the map
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME, OUTPUT_DIR+'/'+CLEAN_MAP_NAME)
clean_image(OUTPUT_DIR+'/'+CLEAN_MAP_NAME)

#Load Biom and Height info into arrays
biomesMatrix = read_image(INPUT_DIR+'/'+BIOMES_MAP_NAME)
heightMatrix = read_image(INPUT_DIR+'/'+HEIGHT_MAP_NAME)

print(biomesMatrix)

#####################################################################################################################