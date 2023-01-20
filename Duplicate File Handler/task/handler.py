import os
import sys

if len(sys.argv) != 2:
    print('Directory is not specified')
else:
    root_folder = sys.argv[1]
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            print(os.path.join(root, file))
