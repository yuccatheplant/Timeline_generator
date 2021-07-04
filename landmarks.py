from constants import *
import random
from readchances import readChances
from PIL import Image
import math 
import routes
import json

def generateLandmarkHTMLs(inputPath):
    textfile = open(OUTPUT_DIR+'/'+TEXTS_DIR+'/'+LANDMARK_FILE_NAME+TEXTFILE_FORMAT, 'r')
    textlines = textfile.readlines()
    textfile.close()
    
    html = open(OUTPUT_DIR+'/'+HTML_DIR+'/'+LANDMARK_FILE_NAME+HTML_FORMAT, 'w')
    html.write('<html>\n<head>\n<title>Natural landmarks</title>\n</head>\n<body>\n<a href="index.html"><<-BACK</a>\n<h1>Natural landmarks</h1>\n<img src="../'+MAPS_DIR+'/'+LANDMARK_FILE_NAME+PICTURE_FORMAT+'" usemap="#navmap">\n<map name="navmap">\n')

    riverCount = 0
    volcanoCount = 0

    for line in textlines:
        if not '#' in line:
            x=int(line.split(";")[0].split('[')[1])
            y=int(line.split(";")[1].split(']')[0])
            if 'VOLCANO' in line:
                coords = getVolcanoRect(x, y)
                html.write('<area shape="rect" coords="'+str(coords[0][0])+','+str(coords[0][1])+','+str(coords[1][0])+','+str(coords[1][1])+'" href="landmarks/volcanoes/'+line.split('[')[0]+'.html">')
                
                volcanoCount = volcanoCount+1
                generateVolcanoHTML(volcanoCount, [x,y])
            if 'RIVER' in line:
                offset = 2
                html.write('<area shape="rect" coords="'+str(x-offset)+','+str(y-offset)+','+str(x+offset)+','+str(y+offset)+'" href="landmaks/rivers/'+line.split('[')[0]+'.html">')
                
                riverCount = riverCount+1
    html.write('</map>\n</body>\n</html>\n')
    html.close()
        
    
def generateVolcanoHTML(number, coords):
    template = open(RESOURCES_HTML_LANDMARKS_DIR+'/landmark_volcano_template.html', 'r')
    templateString = template.read()
    template.close()
    
    textfile = open(OUTPUT_HTML_LANDMARKS_VOLCANOES_DIR+'/VOLCANO'+str(number)+'.html', 'w')
    templateArray = templateString.split('{coords}')
    textfile.write(templateArray[0]+'Coords=['+str(coords[0])+';'+str(coords[1])+']')
    
    templateProcessedString = templateArray[1]
    templateArray = templateProcessedString.split('{name}')
    
    volcanoName = routes.getGeneratedName(GENERATOR_VOLCANO_NAME_PATH)
    
    firstTime = True
    
    for line in templateArray:
        if not firstTime:
            textfile.write(volcanoName)
        firstTime = False
        textfile.write(line)
    
    textfile.close()

#####################################################################################################################
def getVolcanoRect(x, y):
    return [[x-math.floor(PIXELS_PER_KILOMETER), y-math.floor(PIXELS_PER_KILOMETER)],[x+math.ceil(PIXELS_PER_KILOMETER/2), y+math.ceil(PIXELS_PER_KILOMETER/2)]]


#####################################################################################################################

def detectRivers(matrix, inputRivers):
    print('DEBUG: START OF RIVERS')
    print(inputRivers)
    
    rivers = []
    
    for inputRiver in inputRivers:
        riverName = routes.getGeneratedName(GENERATOR_RIVER_NAME_PATH)
        riverCoords = [[inputRiver[0], inputRiver[1], 1]]
        river = {
            "name": riverName,
            "startCoords": inputRiver,
            "coords": riverCoords
            }
        rivers.append(river)
    
    while True:
        for river in rivers:
            print(river)
            
            print(river)
            print('')
        break
    
    
    print('DEBUG: END OF RIVERS')
    
    
    
    

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
    
def generate_landmarks(inputMatrix, image_path, chances):
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
    rivers = []
    
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
                    rivers.append([x,y])
            if inputMatrix[x][y] == BIOM_MOUNTAIN: 
                mountainPixels.append([x,y])
                if count_mountain_pixels in volcanoPos:
                    count_volcanoes = count_volcanoes+1
                    textfile.write('\nVOLCANO'+str(count_volcanoes)+'['+str(x)+';'+str(y)+']')
                    volcanoCoords.append([x, y])
                count_mountain_pixels=count_mountain_pixels+1
    width, height = image.size
    
    mountains = detectMountains(matrix, mountainPixels)
    detectRivers(matrix, rivers)
    
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
