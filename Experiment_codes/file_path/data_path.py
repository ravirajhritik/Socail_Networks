import sys
import os

# Add file path to sys.path
sys.path.append(r'D:Social Networks\data')

# Access a file from the added path
file_path = os.path.join(sys.path[-1], 'lkml.txt')
with open(file_path, 'r') as file:
    contents = file.read()
    print(contents)
