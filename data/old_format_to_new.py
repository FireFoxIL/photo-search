import json
import glob
import os
from collections import defaultdict

if __name__ == '__main__':
    events_paths = glob.glob(os.path.join('CVDataset', '*'))
    metadata_filename = 'metadata.json'
    cache_file = 'cache.pickle'

    for event_path in events_paths:
        if os.path.exists(os.path.join(event_path, metadata_filename)):
            continue
        images_data = defaultdict(list)
            
        for person in os.listdir(event_path):
            if os.path.isdir(os.path.join(event_path, person)):
                images_data[person].extend(os.listdir(os.path.join(event_path, person)))
                if cache_file in images_data[person]:
                    images_data[person].remove(cache_file)
        
        with open(os.path.join(event_path, metadata_filename), 'w+') as out_file:
            json.dump(images_data, out_file, indent=4)