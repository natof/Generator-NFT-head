from platform import node
import bpy
import glob
import json
from os import path
import random
import shutil


# ----------- Settings -----------------------------------------------------------

# An absolute path for the root directory
PROJECT_DIR = "C:/Users/natha/Desktop/Nft/"

# Parts directory containing each directory like "body" or "head" or "misc"
PARTS_DIR = PROJECT_DIR + "parts/"

# Output directory to where all metadata files generated
OUTPUTS_DIR = PROJECT_DIR + "data"
# --------------------------------------------------------------------------------

def color_srgb_to_scene_linear(c):
    if c < 0.04045:
        return 0.0 if c < 0.0 else c * (1.0 / 12.92)
    else:
        return ((c + 0.055) * (1.0 / 1.055)) ** 2.4

# Set render config
def set_render_config():

    r = bpy.context.scene.render
    r.engine = "CYCLES"
    r.resolution_x = 1024
    r.resolution_y = 1024

    # File format
    r.image_settings.file_format = 'PNG'

def assign_bg_material_1(color1):
    mat = bpy.data.materials["background"]
    node = mat.node_tree.nodes["Principled BSDF"]
    node.inputs["Base Color"].default_value = (color_srgb_to_scene_linear(color1[0]/255), color_srgb_to_scene_linear(color1[1]/255), color_srgb_to_scene_linear(color1[2]/255), 1)

def append_asset_hair(t):

    mat = bpy.data.materials["head"]
    node1 = mat.node_tree.nodes["hair"]
    hair = bpy.data.images.load(PARTS_DIR  + t + ".png")
    node1.image = hair

def append_asset_skin(t):

    mat = bpy.data.materials["head"]
    node1 = mat.node_tree.nodes["skin"]
    hair = bpy.data.images.load(PARTS_DIR  + t + ".png")
    node1.image = hair

def append_asset_eye(t):

    mat = bpy.data.materials["head"]
    node1 = mat.node_tree.nodes["eye"]
    hair = bpy.data.images.load(PARTS_DIR  + t + ".png")
    node1.image = hair   



def render(id):
    # Render
    bpy.ops.render.render(write_still=1)

    # Save
    bpy.data.images['Render Result'].save_render(filepath=OUTPUTS_DIR + id + ".png")

def generate(id, adict):
    for attr in adict["attributes"]:
        if attr["trait_type"] == "Hair" and attr["value"] != "":
            append_asset_hair(attr["value"].replace(" ", "_").lower())
        if attr["trait_type"] == "skin" and attr["value"] != "":
            append_asset_skin(attr["value"].replace(" ", "_").lower())
        if attr["trait_type"] == "Eye" and attr["value"] != "":
            append_asset_eye(attr["value"].replace(" ", "_").lower())    
        if attr["trait_type"] == "color1" and attr["value"] != "":
            assign_bg_material_1(attr["value"])       
        
    

    render(str(id))
    print("Generated model id: {}\n".format(id))


def main():
    # Check settings
    if path.exists(PROJECT_DIR) == False:
        print("ERROR: Project directory does not exist. Set the absolute path to the PROJECT_DIR.")
        return
    if path.exists(OUTPUTS_DIR) == False:
        print("ERROR: Outputs directory does not exist. Set the absolute path to the OUTPUTS_DIR.")
        return

    print("Start generating models...")

    # Initialize
    set_render_config()

    # Get all metadata files in "outputs" directory
    metadata_files = glob.glob(OUTPUTS_DIR + "/*.json")
    # Generate models
    for i, metadata in enumerate(metadata_files):
        with open(metadata, 'r') as metaJson:
            data = json.load(metaJson)
            generate(i, data)

    print("Done.")

main()