import os
from PIL import Image
import pillow_heif
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delete', action='store_true', help='delete the heic file if it has been successfully converted or has already been converted')
parser.add_argument('directory', type=str, help='the directory to process')
args = parser.parse_args()

directory = args.directory
destination_directory = os.path.join(directory, 'converted')

def delete_file_if_enabled(path):
    if(args.delete):
        print("Deleting file:", filename)
        os.remove(path)

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

for filename in os.listdir(directory):
    if filename.lower().endswith(".heic"):
        full_filepath = os.path.join(directory, filename)
        new_filename = os.path.splitext(filename)[0] + ".png"
        new_filepath = os.path.join(destination_directory, new_filename)
        if os.path.exists(new_filepath):
            print("Skipping image where converted file already exists:", filename)
            delete_file_if_enabled(full_filepath)
            continue

        filepath = os.path.join(directory, filename)
        print("Converting:", filepath)
        try:
            heif_file = pillow_heif.read_heif(filepath)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
        except Exception as e:
            print("Failed to convert:", filepath)
            print(e)
            continue

        image.save(new_filepath, format("png"))
        delete_file_if_enabled(full_filepath)

