from PIL import Image
import numpy
import os
import shutil

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



def read_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values
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

shutil.copy('map/biomes.png', 'results/experiment.png')

clean_image('results/experiment.png')


###


#####################################################################################################################