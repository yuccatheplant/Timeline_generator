from PIL import Image
import sys
import os
import shutil
import random
import json
import landmarks

###CONSTANTS
from constants import *

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
    html.write('<html>\n<head>\n<title>Biomes</title>\n</head>\n<body><a href="index.html"><<-BACK</a><h1>Biomes</h1>\n<img src="../'+MAPS_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT+'" usemap="#navmap">\n<map name="navmap">\n')

    image = Image.open(image_path)
    matrix = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            cell_size = 10
            if (i % cell_size == 0) and (j % cell_size == 0):
                html.write('<area shape="rect" coords="'+str(i)+','+str(j)+','+str(i+cell_size-1)+','+str(j+cell_size-1)+'" alt="volcano1" href="biomes/biom_r'+str(matrix[i,j][0])+'g'+str(matrix[i,j][1])+'b'+str(matrix[i,j][2])+'.html">')
            if ((matrix[i, j] != BIOM_OCEAN) and (matrix[i, j] != BIOM_LAKE) and (matrix[i, j] != BIOM_RIVER) and (matrix[i, j] != BIOM_MOUNTAIN)):
                matrix[i,j] = VOID
                
    image.save(image_path)
    image.close()
    
    html.write('</map>\n</body>\n</html>\n')
    html.close()
    
#####################################################################################################################

    
#####################################################################################################################

#####################################################################################################################
#MAIN#
#####################################################################################################################
random.seed(5)

#Clean result directory
print ('Cleaning result directories')
try:
    shutil.rmtree(OUTPUT_DIR)
except FileNotFoundError:
    print ('Skipping cleaning')
except:
    print('One or more files are opened and could not be removed!')
    sys.exit()

#Create result directory
print ('Creating result directories')
os.makedirs(OUTPUT_DIR+'/'+MAPS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR+'/'+HTML_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR+'/'+TEXTS_DIR, exist_ok=True)

os.makedirs(OUTPUT_HTML_BIOMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_HTML_LANDMARKS_RIVERS_DIR, exist_ok=True)
os.makedirs(OUTPUT_HTML_LANDMARKS_VOLCANOES_DIR, exist_ok=True)

os.makedirs(OUTPUT_TEXTS_LANDMARKS_RIVERS_DIR, exist_ok=True)

#Copy everything from the Biomes resources
print ('Making copies of maps')
shutil.copy(RESOURCES_HTML_DIR + '/index.html', OUTPUT_HTML_DIR)
for file_name in os.listdir(RESOURCES_HTML_BIOMES_DIR):
    full_file_name = os.path.join(RESOURCES_HTML_BIOMES_DIR, file_name)
    shutil.copy(full_file_name, OUTPUT_HTML_BIOMES_DIR)

print ('Creating empty version of the map')
#Create empty copy of the map
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)
shutil.copy(INPUT_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT)
shutil.copy(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)
clean_image(OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT)

print ('Loading Biom and Heightmap into arrays')
#Load Biom and Height info into arrays
biomesMatrix = read_image(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)
heightMatrix = read_image(INPUT_DIR+'/'+HEIGHT_MAP_NAME+PICTURE_FORMAT)
size = getImageSize(INPUT_DIR+'/'+BIOMES_MAP_NAME+PICTURE_FORMAT)

#print(biomesMatrix)

shutil.copy(OUTPUT_DIR+'/'+MAPS_DIR+'/'+CLEAN_MAP_NAME+PICTURE_FORMAT, OUTPUT_DIR+'/'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT)

print ('Generating landmarks')
landmarks.generate_landmarks(biomesMatrix, OUTPUT_DIR+'/'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT, VOLCANO_SPAWN_CHANCE)

print('DONE')

#####################################################################################################################