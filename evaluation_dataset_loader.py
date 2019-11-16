#%%

import json
import os
from math import floor
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_file', type=str)
    parser.add_argument('dst_folder', type=str)

    config = parser.parse_args()

    dataset = []
    with open(config.inp_file, 'r') as jsonFile:
        for jf in jsonFile:
            jf = jf.replace('\n', '')
            jf = jf.strip()
            weatherData = json.loads(jf)
            dataset.append(weatherData)

    dst_folder = config.dst_folder
    os.makedirs(dst_folder, exist_ok=True)
    all_bboxes = {}
    for i, data in enumerate(dataset):
        image_name = str(i) + '.jpg'
        url = data['content']
        os.system(f"curl {url} --output {os.path.join(dst_folder, image_name)}")
        bboxes = []
        for bbox in data['annotation']:
            lt = bbox['points'][0]
            rb = bbox['points'][1]
            w = bbox['imageWidth']
            h = bbox['imageHeight']
            #     print(f"{floor(lt['x'] * w), floor(lt['y'] * h)}")
            #     print(f"{floor(rb['x'] * w), floor(rb['y'] * h)}")
            bboxes.append(((floor(lt['x'] * w), floor(lt['y'] * h)), (floor(rb['x'] * w), floor(rb['y'] * h))))
        all_bboxes[image_name] = bboxes

    with open(os.path.join(dst_folder, 'bboxes.json'), 'w') as outfile:
        json.dump(all_bboxes, outfile, indent=2)
