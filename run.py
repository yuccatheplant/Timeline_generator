from PIL import Image
import math 
import os
import shutil
import random

###CONSTANTS
#RATIO
PIXELS_PER_KILOMETER = 5

#PROBABILITIES
VOLCANO_SPAWN_CHANCE = [[1, 1], [0.25, 2]] #ONE, TWO

#DIRS
INPUT_DIR = 'map'
OUTPUT_DIR = 'results'

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
VOID = (255, 255, 255)

BIOM_OCEAN = (0, 0, 255) #0000ff ocean
BIOM_LAKE = (0, 136, 255) #0088ff - lake
BIOM_RIVER = (0, 255, 255) #00ffff - river

BIOM_MOUNTAIN = (0, 0, 0) #000000 - mountain
#004400 - taiga forest
#008800 - swamp
#00ff00 - decisious forest
#88ff00 - grassland
BIOM_DESERT = (255, 255, 0)#ffff00 - desert

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
    html = open(OUTPUT_DIR+'/'+'bullshit'+HTML_FORMAT, 'w')
    html.write('<html>\n<head>\n</head>\n<body>\n<img src="../map/biomes.png" usemap="#navmap">\n<map name="navmap">\n')

    image = Image.open(image_path)
    matrix = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            cell_size = 10
            if (i % cell_size == 0) and (j % cell_size == 0):
                html.write('<area shape="rect" coords="'+str(i)+','+str(j)+','+str(i+cell_size-1)+','+str(j+cell_size-1)+'" alt="volcano1" href="bioms/biom_r'+str(matrix[i,j][0])+'g'+str(matrix[i,j][1])+'b'+str(matrix[i,j][2])+'.html">')
            if ((matrix[i,j] != BIOM_OCEAN) and (matrix[i,j] != BIOM_LAKE) and (matrix[i,j] != BIOM_RIVER)):
                matrix[i,j] = VOID
                
    image.save(image_path)
    image.close()
    
    html.write('</map>\n</body>\n</html>\n')
    html.close()
    
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
    for x in range(toGenerate):
        while True:
            y = random.randint(0, count_mountain_pixels-1)
            if not y in volcanoPos:
                break;
        volcanoPos.append(y)  
    
    image = Image.open(image_path)
    matrix = image.load()
    
    html = open(OUTPUT_DIR+'/'+LANDMARK_FILE_NAME+HTML_FORMAT, 'w')
    html.write('<html>\n<head>\n</head>\n<body>\n<img src="landmark_map.png" usemap="#navmap">\n<map name="navmap">\n')

    count_mountain_pixels = 0
    for x in range(len(inputMatrix)-1):
        for y in range(len(inputMatrix[x])-1):
            if inputMatrix[x][y] == BIOM_MOUNTAIN: 
                if count_mountain_pixels in volcanoPos:
                    print('['+str(x)+' ; '+str(y)+']')
                    coords = [[x-math.floor(PIXELS_PER_KILOMETER), y-math.floor(PIXELS_PER_KILOMETER)],[x+math.ceil(PIXELS_PER_KILOMETER/2), y+math.ceil(PIXELS_PER_KILOMETER/2)]]
                    html.write('<area shape="rect" coords="'+str(coords[0][0])+','+str(coords[0][1])+','+str(coords[1][0])+','+str(coords[1][1])+'" alt="volcano1" href="volcano.html">')
                    for i in range(coords[0][0], coords[1][0]):
                        for j in range(coords[0][1], coords[1][1]):
                            matrix[i,j] = LANDMARK_VOLCANO
                        
                    
                count_mountain_pixels=count_mountain_pixels+1
    html.write('</map>\n</body>\n</html>\n')
    html.close()
    
    image.save(image_path)
    image.close()

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

generate_volcano(biomesMatrix, OUTPUT_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT, VOLCANO_SPAWN_CHANCE)

#####################################################################################################################