import json
import os
import re
import logging
import chardet
from function import *

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 扫描路径
path = r"D:\P4\Branch\FF_RCT\GGC"

# 初始化
ext_skip_test = ['.bytes', '.meta', '.fab', '.fbx', '.library', '.png', '.DS_Store', '.dll', '.exe', '.ico', '.cur',
                 '.unityweb', '.package', '.pdf', '.jpg', '.PNG', '.zip', '.bin', '.js', '.fcc', '.tga', '.FBX',
                 '.asset', '.exr', '.mmd', '.ttc', '.so', '.tif', '.cs', '.ttf', '.mmdb', '.gif', '.pdb', '.ilk',
                 '.obj', '.idb', '.iobj', '.ipdb', '.lib']

dir_skip_test = ['node_modules', 'packages', 'StreamingAssets', 'GameApp_Beta',
                 'GameApp', 'EditorApp', 'ProjectTemplate','loc']
file_skip_test = ['fe_loc-en.json', 'fe_loc-vi.json', 'fe_loc-zh-Hans.json',
                  'fe_loc-zh-Hant.json', 'en.json', 'vi.json', 'zh-cn.json',
                  'zh-tw.json', 'protoc', 'protoc-gen-go']
ext_decode_type = ['.eca', '.gdvar', '.mdc', '.cs', '.json', '.h']

key_source_map = {}   # { key: set([file1, file2]) }

# ========= 遍历文件 =========
for root, dirs, files in os.walk(path):
    dirs[:] = [d for d in dirs if d not in dir_skip_test]

    for file in files:
        filepath = os.path.join(root, file)
        name, ext = os.path.splitext(file)

        if ext in ext_skip_test or file in file_skip_test or ext == '' or 'Workshop' in file:
            continue

        encoding_type = 'utf-8'
        if ext not in ext_decode_type:
            with open(filepath, "rb") as f:
                rawdata = f.read(10000)
                encoding_type = chardet.detect(rawdata)['encoding'] or 'utf-8'

        try:
            if ext == '.csv':
                with open(filepath, 'r', encoding=encoding_type, errors='ignore') as f:
                    for line in f:
                        keys_in_line = re.findall(r'\b((?:FE_|T_)\w+)\b', line)
                        for key in keys_in_line:
                            key_source_map.setdefault(key, set()).add(filepath)
                            print(f"[FOUND] {key}  ←  {filepath}")
            elif ext in ext_decode_type:
                text = decode_file(filepath)
                keys_in_file = re.findall(r'\b((?:FE_|T_)\w+)\b', text)
                for key in keys_in_file:
                    key_source_map.setdefault(key, set()).add(filepath)
                    print(f"[FOUND] {key}  ←  {filepath}")
            else:
                with open(filepath, 'r', encoding=encoding_type, errors='ignore') as f:
                    for line in f:
                        keys_in_line = re.findall(r'\b((?:FE_|T_)\w+)\b', line)
                        for key in keys_in_line:
                            key_source_map.setdefault(key, set()).add(filepath)
                            print(f"[FOUND] {key}  ←  {filepath}")
        except Exception as e:
            logging.exception(f"读取文件失败: {filepath} - {e}")
            continue

# ========= 加载语言包 =========
json_en_fe = r'D:\P4\Branch\FF_RCT\GGC\public\Config\loc\FE\fe_loc-en.json'
json_en_ff = r'D:\P4\Branch\FF_RCT\GGC\public\Config\loc\FF\en.json'

with open(json_en_fe, 'r', encoding='utf-8') as f:
    data_fe = json.load(f)
with open(json_en_ff, 'r', encoding='utf-8') as f:
    data_ff = json.load(f)

# ========= 输出所有找到的 key =========
with open('all_found_keys.txt', 'w', encoding='utf-8') as f_all:
    for key, files in key_source_map.items():
        line = f"{key} | {'; '.join(sorted(files))}"
        print(f"[ALL FOUND] {line}")
        f_all.write(line + '\n')

# ========= 比对 key 是否存在 =========
existing_keys = []
missing_keys = []

for key, files in key_source_map.items():
    line = f"{key} | {'; '.join(sorted(files))}"
    if key in data_fe or key in data_ff:
        existing_keys.append(line)
        print(f"[EXIST] {line}")
    else:
        missing_keys.append(line)
        print(f"[MISSING] {line}")

# ========= 输出存在 key 文件 =========
with open('existing_keys.txt', 'w', encoding='utf-8') as f_exist:
    for line in existing_keys:
        f_exist.write(line + '\n')

# ========= 输出缺失 key 文件 =========
with open('result_test2.txt', 'w', encoding='utf-8') as f_missing:
    for line in missing_keys:
        f_missing.write(line + '\n')

print("\n扫描完成！")
print("所有找到的 key → all_found_keys.txt")
print("存在的 key → existing_keys.txt")
print("缺失的 key → result_test2.txt")
