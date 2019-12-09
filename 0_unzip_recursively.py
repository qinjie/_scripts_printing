import zipfile, fnmatch, os
from pathlib import Path
import argparse

path = Path(os.path.dirname(os.path.realpath(__file__)))
source_folder = path.parent
print("Unzip zip files in: ", source_folder)

parser = argparse.ArgumentParser()
parser.add_argument("-dz", "--delete_zip", help="delete zip file", action="store_true")
parser.add_argument("-cf", "--create_folder", help="Create folder for unzipped files", action="store_true")
args = parser.parse_args()
print("\tDelete zip file:", str(args.delete_zip))
print("\tCreate folder:", str(args.create_folder))
print("")

pattern = '*.zip'
for root, dirs, files in os.walk(source_folder):
    for filename in fnmatch.filter(files, pattern):
        file = os.path.join(root, filename)
        print(file)
        # create folder for unzipped files
        file_path, file_extension = os.path.splitext(file)
        if args.create_folder:
            if not os.path.isdir(file_path):
                os.mkdir(file_path)
            dest_folder = file_path
        else:
            dest_folder = Path(file).parent
        # unzip files
        zipfile.ZipFile(file).extractall(dest_folder)
        # delete zip file
        if args.delete_zip:
            os.remove(file)

