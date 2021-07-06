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

def isInRange(size, coords):
    return (coords[0] >= 0 and coords[0] < size[0] and coords[1] >=0 and coords[1] < size[1])

def count3x3Neighbours (matrix, size, coords, color):
    result = []
    for x in range(coords[0]-1, coords[0]+2):
        for y in range(coords[1]-1, coords[1]+2):
            if x!=coords[0] or y!=coords[1]:
                if isInRange(size, [x,y]): 
                    if matrix[x,y] == color:
                        result.append([x,y])          
    return result
#####################################################################################################################
def detectMergePoints(matrix, size, mergePoints):
    
    result = mergePoints
    while True:
        newAddition=False
        
        for mergePoint in mergePoints:
            for x in range(mergePoint[0]-1, mergePoint[0]+2):
                for y in range(mergePoint[1]-1, mergePoint[1]+2):
                    if isInRange(size, [x,y]) and not [x,y] in mergePoints and matrix[x,y] == LANDMARK_RIVER_MERGE:
                        mergePoints.append([x,y])
                        newAddition = True
        
        if not newAddition:
            break
    return result

#####################################################################################################################
def detectRivers(matrix, size, inputRivers):
    print('DEBUG: START OF RIVERS')
    #print(inputRivers)
    
    mergeCoords = []
    for x in range(size[0]):
        for y in range(size[1]):
            if matrix[x,y] == BIOM_RIVER and len(count3x3Neighbours(matrix, size, [x,y], BIOM_RIVER)) >= 3:
                mergeCoords.append([x,y])
    for mergePoint in mergeCoords:
        matrix[mergePoint[0], mergePoint[1]] = LANDMARK_RIVER_MERGE
    
    rivers = []
    riverID = 0
    for inputRiver in inputRivers:
        riverID = riverID+1
        riverName = routes.getGeneratedName(GENERATOR_RIVER_NAME_PATH)
        riverCoords = [[[inputRiver[0], inputRiver[1]], 1]]
        river = {
            "id": riverID,
            "name": riverName,
            "startCoords": inputRiver,
            "coords": riverCoords,
            "length": 1
            }
        rivers.append(river)
        
    controlCounter = 0
    
    
    
    while True:
        controlCounter = controlCounter + 1
        if controlCounter > 2:
            break
    
        shouldStop = True
        for river in rivers:
            firstBigger = True
            if not 'endCoord' in river:
                
                if 'mergePoints' in river:
                    print('Merge points of river '+str(river['id'])+':\n'+str(river['mergePoints'])+'')
                    river2Id = -1
                    for river2 in rivers:
                        if not 'endCoord' in river2 and 'mergePoints' in river2 and river2['id'] != river['id'] and river2['mergePoints'][0] in river['mergePoints']:
                            print('Rivers '+str(river['id']) + ' and '+str(river2['id']) + ' have same merge points!!!')
                            shouldStop = False
                            river2Id=river2['id']
                            break
                    
                    if river2Id > 0:
                        river1Id = river['id']
                        print('')
                        print('Starting merge')
                        
                        bigRiver = river
                        smallRiver = rivers[river2Id-1]
                        
                        #TODO: figure out which river is bigger
                        firstBigger = True
                        
                        #swap
                        if not firstBigger:
                            swapRiver = bigRiver
                            bigRiver = smallRiver
                            smallRiver = swapRiver
                        
                        #TODO Merge!
                        
                        #swap back
                        if not firstBigger:
                            swapRiver = bigRiver
                            bigRiver = smallRiver
                            smallRiver = swapRiver

                        rivers[river1Id-1] = bigRiver
                        rivers[river2Id-1] = smallRiver

                        print('Finishing merge')
                    
                    print('')
                    
                if firstBigger and not 'endCoord' in river:
                    firstTime = True
                    while True:
                        currentCell = river['coords'][len(river['coords'])-1]
                        neighbours = count3x3Neighbours(matrix, size, currentCell[0], BIOM_RIVER)
                        if len(neighbours) >= 2 or firstTime:
                            firstTime=False
                            #go downstream
                            for neigbour in neighbours:
                                formattedNeighbour = [[neigbour[0], neigbour[1]], currentCell[1]]
                                isFound = False
                                for coord in river['coords']:
                                    if formattedNeighbour[0] == coord[0]:
                                        isFound=True
                                        break
                                if not isFound:
                                    river['coords'].append(formattedNeighbour)
                                    river['length'] = river['length']+1
                                
                        else:
                            mergePoints = count3x3Neighbours(matrix, size, currentCell[0], LANDMARK_RIVER_MERGE)
                            if len(mergePoints) > 0:
                                river['mergePoints'] = detectMergePoints(matrix, size, mergePoints)
                            else:
                                river['endCoord'] = [currentCell[0], currentCell[1]]
                            break
                    #print(river)
                    #print('')
        print('Should we stop?')
        print(shouldStop)
        print('')
            
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
            #matrix[coords[0]-1, coords[1]] = BIOM_MOUNTAIN
            matrix[coords[0], coords[1]] = BIOM_MOUNTAIN
        
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
    detectRivers(matrix, [width, height], rivers)
    
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
