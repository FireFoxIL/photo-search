# %%

import argparse
import json
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_file', type=str)
    parser.add_argument('dst_folder', type=str)

    config = parser.parse_args()

    dataset = []
    with open(config.inp_file, 'r') as json_file:
        for jf in json_file:
            jf = jf.replace('\n', '')
            jf = jf.strip()
            inp_data = json.loads(jf)
            dataset.append(inp_data)

    dst_folder = config.dst_folder
    os.makedirs(dst_folder, exist_ok=True)
    for i, data in enumerate(dataset):
        image_name = str(i) + '.jpg'
        url = data['content']
        os.system(f"curl {url} --output {os.path.join(dst_folder, image_name)}")
