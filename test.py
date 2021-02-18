import os

images = []
for filepath, _, files in list(os.walk('pose_illustrations')):
    for img in files:
        images.append(filepath.replace('\\','/') + '/' + img)
    

print(images)
