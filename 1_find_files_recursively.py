import argparse
import fnmatch
import os
import shutil
from pathlib import Path


### List immediate sub folders under root
def list_sub_dirs(root):
    return filter(os.path.isdir, [os.path.join(root, f) for f in os.listdir(root)])


### Recursively search for a file by pattern under a root folder
def recursive_find(treeroot, patterns):
    matches = []
    not_found = []
    for pattern in patterns:
        found = False
        for root, dirnames, filenames in os.walk(treeroot):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
                found = True
        if not found:
            not_found.append(pattern)
    return matches, not_found


## Look into parent folder
path = Path(os.path.dirname(os.path.realpath(__file__)))
source_folder = path.parent
print("Find files in: ", source_folder)

parser = argparse.ArgumentParser()
parser.add_argument("-ftf", "--files_to_find", help="File to load files-to-find", default=r'files_to_find.txt')
parser.add_argument("-ftp", "--files_to_print", help="File to save files-to-print", default=r'files_to_print.txt')
parser.add_argument("-fnf", "--files_not_found", help="File to save files-not-found", default=r'files_not_found.txt')
parser.add_argument("-cf", "--combine_files", help="Combine found files", action='store_true', default=True)

args = parser.parse_args()
print("\tFile to save files-to-find:", str(args.files_to_find))
print("\tFile to save files-to-print:", str(args.files_to_print))
print("\tFile to save files-not-found:", str(args.files_not_found))
print("\tCombine found files:", str(args.combine_files))
print("")

## List of files to be deleted
patterns = {}
with open(args.files_to_find, 'r') as doc:
    for line in doc:
        line = line.split()
        if not line: continue
        patterns[line[0]] = line[1:]
        print("Folder = ", line[0], ", Files = ", str(line[1:]))

open(args.files_to_print, 'w').close()
open(args.files_not_found, 'w').close()

# find top folders in source directory
_, top_folders, _ = next(os.walk(source_folder))

for folder_name in top_folders:
    target_folder = os.path.join(source_folder, folder_name)
    print(target_folder)
    for root, dirs, files in os.walk(target_folder):
        for idx, key in enumerate(patterns):
            if not bool(fnmatch.fnmatch(root, key)):
                continue

            matches, not_founds = recursive_find(root, patterns[key])
            print('\t', key, '\tmatched ', len(matches), '\tnot found ', len(not_founds))

            # Combine found text files into one
            if args.combine_files:
                out_file = target_folder + '_' + str(idx) + '.txt'

                with open(out_file, 'w') as outfile:
                    for f in matches:
                        outfile.write(f + '\n')
                        outfile.write("#" * 80 + '\n\n')
                        with open(f, 'r') as fd:
                            shutil.copyfileobj(fd, outfile)
                        outfile.writelines('\n\n\n\n\n')

            if matches:
                with open(args.files_to_print, "a") as myfile:
                    if args.combine_files:
                        myfile.write(out_file + "\n")
                    else:
                        for match in matches:
                            myfile.write(match + "\n")
                        for nf in not_founds:
                            myfile.write("\n")

            if not_founds:
                with open(args.files_not_found, "a") as myfile:
                    myfile.write(root + "\n")
                    for not_found in not_founds:
                        myfile.write(not_found + "\n")
