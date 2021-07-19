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
                html.write('<area shape="rect" coords="'+str(x-offset)+','+str(y-offset)+','+str(x+offset)+','+str(y+offset)+'" href="landmarks/rivers/'+line.split('[')[0]+'.html">')
                
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
            
    
    firstRun = True
    while True:
        
        shouldStop = True
        for river in rivers:
            firstBigger = True
            if not 'endCoord' in river:
                
                if 'mergePoints' in river:
                    river2Id = -1
                    for river2 in rivers:
                        if not 'endCoord' in river2 and 'mergePoints' in river2 and river2['id'] != river['id'] and river2['mergePoints'][0] in river['mergePoints']:
                            shouldStop = False
                            river2Id=river2['id']
                            break
                    
                    if river2Id > 0:
                        river1Id = river['id']                        
                        
                        bigRiver = river
                        smallRiver = rivers[river2Id-1]
                        
                        #Figure out which river is bigger
                        firstBigger = bigRiver['coords'][len(bigRiver['coords'])-1][1] > smallRiver['coords'][len(smallRiver['coords'])-1][1]
                        if bigRiver['coords'][len(bigRiver['coords'])-1][1] == smallRiver['coords'][len(smallRiver['coords'])-1][1]:
                            firstBigger = bigRiver['length'] > smallRiver['length']
                
                        
                        #swap
                        if not firstBigger:
                            swapRiver = bigRiver
                            bigRiver = smallRiver
                            smallRiver = swapRiver
                        
                        newWidth = smallRiver['coords'][len(smallRiver['coords'])-1][1] + bigRiver['coords'][len(bigRiver['coords'])-1][1]
                        
                        smallRiver['endCoord'] = smallRiver['coords'][len(smallRiver['coords'])-1][0]
                        del(smallRiver['mergePoints'])
                        smallRiver['mergeInto'] = [bigRiver['id'], bigRiver['name'], bigRiver['length'], bigRiver['mergePoints'][0]]
                        
                        bigRiver['coords'].append(smallRiver['coords'][len(smallRiver['coords'])-1])
                        
                        mergeInfo = [smallRiver['id'], smallRiver['name'], (bigRiver['length']+1)//PIXELS_PER_KILOMETER, bigRiver['mergePoints'][0]]
                        if not 'mergeInfo' in bigRiver:
                            bigRiver['mergeInfo'] = [mergeInfo]
                        else:
                            bigRiver['mergeInfo'].append(mergeInfo)
                        
                        continuePoint = []
                        
                        for mergePoint in bigRiver['mergePoints']:
                            bigRiver['coords'].append([mergePoint, newWidth])
                            bigRiver['length'] = bigRiver['length'] + 1
                            neigbours = count3x3Neighbours(matrix, size, mergePoint, BIOM_RIVER)
                            for neigbour in neigbours:
                                isFound = False
                                for coord in bigRiver['coords']:
                                    if coord[0] == neigbour:
                                        isFound = True
                                        break
                                if not isFound:
                                    continuePoint = [neigbour, newWidth]
                        if len(continuePoint)==2:
                            bigRiver['coords'].append(continuePoint)
                        del(bigRiver['mergePoints'])
                        
                        #swap back
                        if not firstBigger:
                            swapRiver = bigRiver
                            bigRiver = smallRiver
                            smallRiver = swapRiver

                        rivers[river1Id-1] = bigRiver
                        rivers[river2Id-1] = smallRiver
                    
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
                                river['endCoord'] = currentCell[0]
                            break
                            
        if not firstRun and shouldStop:
            for river in rivers:
                if not 'endCoord' in river and 'mergePoints' in river:
                    continuePoints = []
                    for mergePoint in river['mergePoints']:
                        river['coords'].append([mergePoint, river['coords'][len(river['coords'])-1][1]])
                        river['length'] = river['length'] + 1
                        neigbours = count3x3Neighbours(matrix, size, mergePoint, BIOM_RIVER)
                        for neigbour in neigbours:
                            isFound = False
                            for coord in river['coords']:
                                if coord[0] == neigbour:
                                    isFound = True
                                    break
                            if not isFound:
                                newWidth = river['coords'][len(river['coords'])-1][1]-1
                                if newWidth < 1:
                                    newWidth = 1
                                continuePoints.append([neigbour, newWidth])
                    river['coords'].append(continuePoints[random.randrange(0, len(continuePoints)-1)])
                    shouldStop = False
        
        if not firstRun and shouldStop:
            break
        firstRun = False
    
    
    for river in rivers:
        river['length'] = river['length'] // PIXELS_PER_KILOMETER
    
    colorRiversUp(matrix, size, rivers)
    
    generateRiversHTMLs(rivers)

#####################################################################################################################
def generateRiversHTMLs(rivers):
    templateString = ''
    HTMLnewLine= '<br>\n'


    with open(RESOURCES_HTML_LANDMARKS_DIR + '/landmark_river_template.html', 'r') as tempFile:
        templateString = tempFile.read()

    for river in rivers:
        with open(OUTPUT_HTML_LANDMARKS_RIVERS_DIR + '/RIVER'+ str(river['id']) +'.html', 'w') as writeFile:
            #Length
            text = 'Length: ' + str(river['length'])+ 'km'
            
            #What flows into
            if 'mergeInfo' in river:
                text = text + HTMLnewLine
                text = text + 'Inflowing streams:'+HTMLnewLine
                text = text + '<ol>'
                for inMerge in river['mergeInfo']:
                    text = text + '<li><a href="RIVER'+ str(inMerge[0]) +'.html">'+str(inMerge[1])+'</a> at '+ str(inMerge[2]) +'th km</li>'
                text = text + '</ol>\n'
                
            
            #End of river
            text = text+HTMLnewLine
            text = text+'Flows into: '
            if 'mergeInto' in river:
                text = text+ '<a href="RIVER'+ str(river['mergeInto'][0]) +'.html">'+str(river['mergeInto'][1])+'</a>'
            else:
                text = text+ 'Ocean'
            
            data = [river, river['name'], river['name'], text]
        
            templateArray = templateString.split('{}')
            indexPos = 0
            for templateLine in templateArray:
                writeFile.write(templateLine)
                
                if indexPos < len(data):
                    writeFile.write(str(data[indexPos]))
                indexPos = indexPos+1
        
        
    return    
    
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
def colorRiversUp(matrix, size, rivers):
    lakeRiverPixels = []

    for x in range(size[0]):
        for y in range(size[1]):
            if matrix[x,y] == BIOM_RIVER and len(count3x3Neighbours (matrix, size, [x,y], BIOM_LAKE)) >=3:
                    lakeRiverPixels.append([x,y])
        
            if matrix[x,y] == LANDMARK_RIVER_MERGE:
                matrix[x,y] = BIOM_RIVER
  
    for lakeRiverPixel in lakeRiverPixels:
        matrix[lakeRiverPixel[0], lakeRiverPixel[1]] = BIOM_LAKE
    
    for river in rivers:
        for coord in river['coords']:
            x = coord[0][0]
            y = coord[0][1]

            if coord[1] >=2:
                if isInRange(size, [x, y+1]):
                    if matrix[x, y+1] != BIOM_LAKE and matrix[x, y+1] != BIOM_OCEAN:
                        matrix[x, y+1] = BIOM_RIVER
                if isInRange(size, [x+1, y]):
                    if matrix[x+1, y] != BIOM_LAKE and matrix[x+1, y] != BIOM_OCEAN:
                        matrix[x+1, y] = BIOM_RIVER
            if coord[1] >=4:
                if isInRange(size, [x, y-1]):
                    if matrix[x, y-1] != BIOM_LAKE and matrix[x, y-1] != BIOM_OCEAN:
                        matrix[x, y-1] = BIOM_RIVER
                if isInRange(size, [x-1, y]):
                    if matrix[x-1, y] != BIOM_LAKE and matrix[x-1, y] != BIOM_OCEAN:
                        matrix[x-1, y] = BIOM_RIVER
            if coord[1] >= 5: 
                if isInRange(size, [x+1, y+1]):
                    if matrix[x+1, y+1] != BIOM_LAKE and matrix[x+1, y+1] != BIOM_OCEAN:
                        matrix[x+1, y+1] = BIOM_RIVER
                if isInRange(size, [x-1, y-1]):
                    if matrix[x-1, y-1] != BIOM_LAKE and matrix[x-1, y-1] != BIOM_OCEAN:
                        matrix[x-1, y-1] = BIOM_RIVER
                if isInRange(size, [x+1, y-1]):
                    if matrix[x+1, y-1] != BIOM_LAKE and matrix[x+1, y-1] != BIOM_OCEAN:
                        matrix[x+1, y-1] = BIOM_RIVER
                if isInRange(size, [x-1, y+1]):
                    if matrix[x-1, y+1] != BIOM_LAKE and matrix[x-1, y+1] != BIOM_OCEAN:
                        matrix[x-1, y+1] = BIOM_RIVER
    return


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
                if ((matrix[coords[0]-1, coords[1]] == color) or (matrix[coords[0]+1, coords[1]] == color) or (matrix[coords[0], coords[1]-1] == color) or (matrix[coords[0], coords[1]+1] == color)):
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
    
    with Image.open(image_path) as image:
         
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
        
    generateLandmarkHTMLs(OUTPUT_DIR+'/'+TEXTS_DIR+'/'+LANDMARK_FILE_NAME+TEXTFILE_FORMAT)
