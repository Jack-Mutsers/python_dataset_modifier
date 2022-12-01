import split_test as split
import filter_letter as filter
from glob import glob
import os

search_dir = "models/test/"
folder_names = [name for name in os.listdir(search_dir) if os.path.isdir(os.path.join(search_dir, name))]

old_csv_filename = "upper_lower.csv"
count = 0
for folder in folder_names:
    csv_filename = "upper_lower"+str(count+1)+".csv"
    model_paths = glob(search_dir+folder+"/*.model")

    for model_path in model_paths:
        print(model_path)
        split.run(model_path, old_csv_filename)
        filter.run(old_csv_filename, csv_filename)
        print("finished: "+model_path)
        old_csv_filename = csv_filename
    
    count += 1


