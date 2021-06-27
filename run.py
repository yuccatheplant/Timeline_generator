from PIL import Image
import math 
import os
import shutil
import random
import routes

###CONSTANTS
#RATIO
PIXELS_PER_KILOMETER = 5

#PROBABILITIES
VOLCANO_SPAWN_CHANCE = [[1, 1], [0.25, 2]] #ONE, TWO

#DIRS
INPUT_DIR = 'map'
OUTPUT_DIR = 'results'

MAPS_DIR = 'maps'
HTML_DIR = 'html'
TEXTS_DIR = 'texts'

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
    html = open(OUTPUT_DIR+'/'+HTML_DIR+'/'+'clickable_biomes'+HTML_FORMAT, 'w')
    html.write('<html>\n<head>\n</head>\n<body>\n<img src="../'+MAPS_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT+'" usemap="#navmap">\n<map name="navmap">\n')

    image = Image.open(image_path)
    matrix = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            cell_size = 10
            if (i % cell_size == 0) and (j % cell_size == 0):
                html.write('<area shape="rect" coords="'+str(i)+','+str(j)+','+str(i+cell_size-1)+','+str(j+cell_size-1)+'" alt="volcano1" href="bioms/biom_r'+str(matrix[i,j][0])+'g'+str(matrix[i,j][1])+'b'+str(matrix[i,j][2])+'.html">')
            if ((matrix[i, j] != BIOM_OCEAN) and (matrix[i, j] != BIOM_LAKE) and (matrix[i, j] != BIOM_RIVER) and (matrix[i, j] != BIOM_MOUNTAIN)):
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
def generateLandmarkHTMLs(inputPath):
    textfile = open(OUTPUT_DIR+'/'+TEXTS_DIR+'/'+LANDMARK_FILE_NAME+TEXTFILE_FORMAT, 'r')
    textlines = textfile.readlines()
    textfile.close()
    
    html = open(OUTPUT_DIR+'/'+HTML_DIR+'/'+LANDMARK_FILE_NAME+HTML_FORMAT, 'w')
    html.write('<html>\n<head>\n</head>\n<body>\n<img src="../'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT+'" usemap="#navmap">\n<map name="navmap">\n')

    for line in textlines:
        if not '#' in line:
            x=int(line.split(";")[0].split('[')[1])
            y=int(line.split(";")[1].split(']')[0])
            if 'VOLCANO' in line:
                coords = getVolcanoRect(x, y)
                html.write('<area shape="rect" coords="'+str(coords[0][0])+','+str(coords[0][1])+','+str(coords[1][0])+','+str(coords[1][1])+'" href="'+line.split('[')[0]+'.html">')
            if 'RIVER' in line:
                offset = 2
                html.write('<area shape="rect" coords="'+str(x-offset)+','+str(y-offset)+','+str(x+offset)+','+str(y+offset)+'" href="'+line.split('[')[0]+'.html">')
    html.write('</map>\n</body>\n</html>\n')
    html.close()

#####################################################################################################################
def getVolcanoRect(x, y):
    return [[x-math.floor(PIXELS_PER_KILOMETER), y-math.floor(PIXELS_PER_KILOMETER)],[x+math.ceil(PIXELS_PER_KILOMETER/2), y+math.ceil(PIXELS_PER_KILOMETER/2)]]

#####################################################################################################################
def detectMountains(matrix, mountainPixels):
    mountains = []
    mountainsLen = 0
    
    while True:
        mountains.append([])
        mountainsLen = mountainsLen+1
        color = (255, 255, 255-mountainsLen, 255)
        coord = mountainPixels[0]
        matrix[coord[0], coord[1]] = color
        while True:
            jumpOut=True
            
            for coords in mountainPixels:
                #print(coords)
                if ((matrix[coords[0]-1, coords[1]] == color) or (matrix[coords[0]+1, coords[1]] == color) or (matrix[coords[0], coords[1]-1] == color) or (matrix[coords[0], coords[1]+1] == color)):
                    #print('test')
                    mountains[mountainsLen-1].append(coords)
                    matrix[coords[0], coords[1]] = color
                    mountainPixels.remove(coords)
                    jumpOut=False
            if jumpOut:
                break
        
        for coords in mountains[mountainsLen-1]:
            matrix[coords[0]-1, coords[1]] = BIOM_MOUNTAIN
        
        #
        
        if len(mountainPixels) == 0:
            break
    #print (mountains)   
    return mountains
    
def coordsDistancePerpendicular(coord1, coord2):
    return max(abs(coord1[0]-coord2[0]), abs(coord1[1]-coord2[1]))
    
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
    
    textfile = open(OUTPUT_DIR+'/'+TEXTS_DIR+'/'+LANDMARK_FILE_NAME+TEXTFILE_FORMAT, 'w')
    textfile.write('#NATURAL LANDMARKS#')
    
    mountainPixels = []
    volcanoCoords = []
    
    count_mountain_pixels = 0
    
    count_rivers=0
    count_volcanoes=0
    for x in range(len(inputMatrix)):
        for y in range(len(inputMatrix[x])):
            if inputMatrix[x][y] == BIOM_RIVER:
                count_river_blocks = 0
                count_other_water_blocks = 0
                for rx in range(x-1, x+2):
                    for ry in range(y-1, y+2):
                        if (inputMatrix[rx][ry] == BIOM_OCEAN or inputMatrix[rx][ry] == BIOM_LAKE):
                            count_other_water_blocks=count_other_water_blocks+1
                        if (inputMatrix[rx][ry] == BIOM_RIVER):
                            count_river_blocks = count_river_blocks+1
                if count_river_blocks == 2 and count_other_water_blocks == 0:
                    count_rivers = count_rivers+1
                    textfile.write('\nRIVER'+str(count_rivers)+'['+str(x)+';'+str(y)+']')   
            if inputMatrix[x][y] == BIOM_MOUNTAIN: 
                mountainPixels.append([x,y])
                if count_mountain_pixels in volcanoPos:
                    count_volcanoes = count_volcanoes+1
                    textfile.write('\nVOLCANO'+str(count_volcanoes)+'['+str(x)+';'+str(y)+']')
                    volcanoCoords.append([x, y])
                count_mountain_pixels=count_mountain_pixels+1
    width, height = image.size
    
    mountains = detectMountains(matrix, mountainPixels)
    textfile.write('\n#'+str(mountains))
    
    for coords in volcanoCoords:
        coords = getVolcanoRect(coords[0],coords[1])
        for i in range(coords[0][0], coords[1][0]+1):
            for j in range(coords[0][1], coords[1][1]+1):
                matrix[i,j] = LANDMARK_VOLCANO
    
    
    textfile.close()
    
    image.save(image_path)
    image.close()
    
    generateLandmarkHTMLs(OUTPUT_DIR+'/'+TEXTS_DIR+'/'+LANDMARK_FILE_NAME+TEXTFILE_FORMAT)

#####################################################################################################################
#MAIN#
#####################################################################################################################
#Create result directory
os.makedirs(OUTPUT_DIR+'/'+MAPS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR+'/'+HTML_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR+'/'+TEXTS_DIR, exist_ok=True)

#Create empty copy of the map
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)
shutil.copy(INPUT_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT)
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)
clean_image(OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)

#Load Biom and Height info into arrays
biomesMatrix = read_image(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)
heightMatrix = read_image(INPUT_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT)
size = getImageSize(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)

#print(biomesMatrix)

shutil.copy(OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT)

generate_volcano(biomesMatrix, OUTPUT_DIR+'/'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT, VOLCANO_SPAWN_CHANCE)

#####################################################################################################################