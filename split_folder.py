# split 20% of last files in a folder to test folder

import os
import random
import shutil

def split_files(folder_path: str, test_folder: str, split_ratio: float) -> None:
    files = os.listdir(folder_path)
    random.shuffle(files)
    split_index = int(len(files) * split_ratio)
    test_files = files[:split_index]
    for file in test_files:
        shutil.move(os.path.join(folder_path, file), os.path.join(test_folder, file))
        
split_files("/Users/hoangtv/Projects-Every-Week/plate_number_recognition/datasets", "/Users/hoangtv/Projects-Every-Week/plate_number_recognition/validation", 0.2)