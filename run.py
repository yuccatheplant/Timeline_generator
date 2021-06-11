from PIL import Image
import numpy
import os
import shutil
import random

###CONSTANTS
#RATIO
PIXELS_PER_KILOMETER = 5

#PROBABILITIES
VOLCANO_SPAWN_CHANCE = [[0.5, 1], [0.25, 2]] #ONE, TWO

#DIRS
INPUT_DIR = 'map'
OUTPUT_DIR = 'results'

#FORMATS
PICTURE_FORMAT = '.png'
TEXTFILE_FORMAT = '.txt'

#FILES
BIOMES_MAP_NAME = 'biomes'
HEIGHT_MAP_NAME = 'heightmap'
CLEAN_MAP_NAME = 'clean_map'

LANDMARK_FILE_NAME = 'landmark_map'

#COLORS
VOID = (255, 255, 255)

BIOM_OCEAN = (0, 0, 255) #0000ff ocean
BIOM_LAKE = (0, 136, 255) #0088ff - lake
BIOM_RIVER = (0, 255, 255) #00ffff - river

BIOM_MOUNTAIN = (0, 0, 0) #000000 - mountain
#004400 - taiga forest
#008800 - swamp
#00ff00 - decisious forest
#88ff00 - grassland
#ffff00 - desert

LANDMARK_VOLCANO = (255, 0, 0) ##ff0000 Volcano

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
def getImageSize(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    size = [width, height]
    image.close()
    return size

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
def readChances(chances):
    chance = random.random()
    result = 0
    for i in chances:
        if chance <= i[0]:
            result = i[1]
        else:
            break
    
    return result
    
#####################################################################################################################
def generate_volcano(inputMatrix, image_path, chances):
    chance = random.random()
    toGenerate = readChances(chances)
    
    count_mountain_pixels = 0
    for x in inputMatrix:
        for y in x:
            if y == BIOM_MOUNTAIN: 
                count_mountain_pixels=count_mountain_pixels+1
                
    if toGenerate > count_mountain_pixels:
        toGenerate = count_mountain_pixels
    
    volcanoPos = []
    for i in range(toGenerate):
        
        while True:
            new_place = random.randint(0, count_mountain_pixels-1)
            if not new_place in volcanoPos:
                break;
        volcanoPos.append(new_place)  
    
    count_mountain_pixels = 0
    for x in range(len(inputMatrix)-1):
        for y in range(len(inputMatrix[x])-1):
            if inputMatrix[x][y] == BIOM_MOUNTAIN: 
                if count_mountain_pixels in volcanoPos:
                    print('['+str(x)+' ; '+str(y)+']')
                count_mountain_pixels=count_mountain_pixels+1
        
    
    return count_mountain_pixels

#####################################################################################################################
#MAIN#
#####################################################################################################################

#Create empty copy of the map
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)
clean_image(OUTPUT_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)

#Load Biom and Height info into arrays
biomesMatrix = read_image(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)
heightMatrix = read_image(INPUT_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT)
size = getImageSize(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)

#print(biomesMatrix)

shutil.copy(OUTPUT_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT)

print(generate_volcano(biomesMatrix, OUTPUT_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT, VOLCANO_SPAWN_CHANCE))

#####################################################################################################################