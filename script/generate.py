import bpy  # The module for Blender Python
import json
from os import path
import random
import re
import shutil

# This time, 100 characters will be generated.
TOTAL_CHARACTERS = 50

# Metadata JSON structure - Please see https://docs.opensea.io/docs/metadata-standards
METADATA_NAME = "NFT Character"
METADATA_SYMBOL = ""
METADATA_DESCRIPTION = "NFT Collectibles using Blender Python"
METADATA_IMAGE_URL = "https://example.com/"
METADATA_EXTERNAL_URL = "https://example.com/"
# Specify the directory in which generate images finally.
PROJECT_DIR = "C:/Users/natha/Desktop/Nft/"
OUTPUTS_DIR = "C:/Users/natha/Desktop/Nft/data/"

list_bg = [
    "green", "navy", "red", "yellow"
]

# List of parts (the file name (collection name) of each created part is included in this.)
list_hair = [
    "hair1",
    "hair2",
    "hair3",
    "hair4",
    "hair5",
    "hair6",
    "hair7",
    "hair8",
    "hair9",
    "hair10",
    "hair11",
    "hair12",
    "hair13",
    "hair14",
    "hair15",
    "hair16",
    "hair17",
    "hair18",
    "hair19",
    "hair20",
    "hair21",
    "hair22",
    "hair23",
    "hair24",
    "hair25",
    "hair26"
]
list_skin = [
    "skin1",
    "skin2",
    "skin3",
    "skin4",
    "skin5",
    "skin6",
]
list_eye = [
    "eye1",
    "eye2",
    "eye3",
    "eye4",
    "eye5",
    "eye6",
    "eye7",
    "eye8",
    "eye9",
    "eye10",
    "eye11",
    "eye12",
    "eye13",
    "eye14",
    "eye15"
]

list_color = [
    [255, 149, 110], #orange
    [255, 231, 113], #jaune
    [203, 255, 118], #vert jaune
    [117, 255, 115], #vert
    [159, 255, 229], #cyan
    [163, 177, 255], #bleu cyan
    [255, 143, 143], #rose
    [219, 103, 255], #violet"
    [255, 86, 67], #rouge

]


def rand_attributes(i):

    random_skin = random.choice(list_skin)
    random_hair = random.choice(list_hair)
    random_eye = random.choice(list_eye)
    random_color1 = random.choice(list_color)

    random_skin = random_skin.replace("_", " ").title()
    random_hair = random_hair.replace("_", " ").title()
    random_eye = random_eye.replace("_", " ").title()
    

    attributes = [
        {
            "trait_type": "Hair",
            "value": random_hair
        },
        {
            "trait_type": "skin",
            "value": random_skin
        },
        {
            "trait_type": "Eye",
            "value": random_eye
        },
        {
            "trait_type": "color1",
            "value": random_color1
        },
    ]

    return attributes
def rand_attr_bg():
    rand_bg = random.choice(list_bg).title()

    attr = {
        "trait_type": "Background",
        "value": rand_bg
    }

    return attr

def main():
    # Check settings
    if path.exists(PROJECT_DIR) == False:
        print("ERROR: Project directory does not exist. Set the absolute path to the PROJECT_DIR.")
        return
    if path.exists(OUTPUTS_DIR) == False:
        print("ERROR: Outputs directory does not exist. Set the absolute path to the OUTPUTS_DIR.")
        return

    print("Start generating metadata...")

    # Create dict
    dict_list = []

    for i in range(TOTAL_CHARACTERS):
        attributes = rand_attributes(i)
        adict = {
            "attributes": attributes
        }
        dict_list.append(adict)

    # Remove duplicates for json
    unique_list = list(map(json.loads, set(map(json.dumps, dict_list))))
    # Check duplicates
    if len(unique_list) < TOTAL_CHARACTERS:
        print("ERROR: Properties duplicate. Please run again.")
        return
    # Add background to attribute
    for u in unique_list:
        u["attributes"].append(rand_attr_bg())

    json_data = {}

    for i, adict in enumerate(unique_list):
        # Create metadata
        obj = {
            "name": METADATA_NAME + " #" + str(i),
            "symbol": METADATA_SYMBOL,
            "description": METADATA_DESCRIPTION,
            "image": METADATA_IMAGE_URL + str(i) + ".png",
            "external_url": METADATA_EXTERNAL_URL + str(i),
            "attributes": adict["attributes"]
        }
        with open(OUTPUTS_DIR + str(i) + ".json", 'w') as outjson:
            json.dump(obj, outjson, indent=4)

        print("Generated metadata id: {}\n".format(i))

    print("Done.")


main()