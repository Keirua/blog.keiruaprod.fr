import os
from os import listdir
from os.path import isfile, join, exists

source_path = 'social-cards'
target_path = 'assets/cards'
source_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]

# carbon-now social-cards/rust-binary.rs --location assets/cards

# Generate all the non-existing social cards
for s in source_files:
    if exists(join(target_path, "{}.png".format(s))) == False:
        os.system("carbon-now {}/{} --location {} --target {}".format(
            source_path,
            s,
            target_path,
            s
            ))
        