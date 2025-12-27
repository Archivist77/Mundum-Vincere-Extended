#--------------------------------------------------#
#--------------------------------------------------#
#---------------AI GENERATED CONTENT---------------#
#--------------------------------------------------#
#--------------------------------------------------#

#!/usr/bin/env python

from gimpfu import *
import os
import glob

def process_images_in_folder(image, drawable, folder_path):
    # Change to the specified directory
    os.chdir(folder_path)
    
    # Loop through all PNG files in the directory
    for png_file in glob.glob(os.path.join(folder_path, '*.png')):
        # Load the image
        img = pdb.gimp_file_load(png_file, png_file)
        layer = pdb.gimp_image_get_active_layer(img)

        # Alpha to selection
        pdb.gimp_image_select_item(img, CHANNEL_OP_REPLACE, layer)

        # Shrink selection by 1 pixel
        pdb.gimp_selection_shrink(img, 1)

        # Invert selection
        pdb.gimp_selection_invert(img)

        # Apply Gaussian Blur with a radius of 0.5
        pdb.plug_in_gauss(img, layer, 1.75, 1.75, 1)
        
        # Alpha to selection again
        pdb.gimp_image_select_item(img, CHANNEL_OP_REPLACE, layer)
        
        # Apply anti-aliasing
        pdb.plug_in_antialias(img, layer)
        
        # Replace LAYER MODE
        pdb.gimp_layer_set_mode(layer, NORMAL_MODE)
        
        # Opacity 100
        pdb.gimp_layer_set_opacity(layer, 100)

        # Update the layer to apply changes (this is important)
        pdb.gimp_drawable_update(layer, 0, 0, layer.width, layer.height)

        # Save the modified image
        output_file = os.path.join(folder_path, "processed_" + os.path.basename(png_file))
        pdb.gimp_file_save(img, layer, output_file, output_file)

        # Clean up
        pdb.gimp_image_delete(img)

register(
    "python_fu_process_images_in_folder",
    "Process images in a folder",
    "Processes all PNG images in a specified folder.",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/File/Process Images in Folder",
    "*",
    [
        (PF_DIRNAME, "folder_path", "Folder Path", None),
    ],
    [],
    process_images_in_folder)

main()