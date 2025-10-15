import json
import os
import re
import logging
import chardet
from function import *  # 确保 decode_file 函数在 function.py 中

import csv

# ===== 日志配置 =====
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===== 扫描路径 =====
path = r"D:\P4\Branch\FF_RCT\GGC"

# ===== 初始化过滤规则 =====
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

# ===== 遍历文件 =====
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
                            print(f"[FOUND] {key} | {filepath}")
            elif ext in ext_decode_type:
                text = decode_file(filepath)
                keys_in_file = re.findall(r'\b((?:FE_|T_)\w+)\b', text)
                for key in keys_in_file:
                    key_source_map.setdefault(key, set()).add(filepath)
                    print(f"[FOUND] {key} | {filepath}")
            else:
                with open(filepath, 'r', encoding=encoding_type, errors='ignore') as f:
                    for line in f:
                        keys_in_line = re.findall(r'\b((?:FE_|T_)\w+)\b', line)
                        for key in keys_in_line:
                            key_source_map.setdefault(key, set()).add(filepath)
                            print(f"[FOUND] {key} | {filepath}")
        except Exception as e:
            logging.exception(f"读取文件失败: {filepath} - {e}")
            continue

# ===== 加载语言包 =====
json_en_fe = r'D:\P4\Branch\FF_RCT\GGC\public\Config\loc\FE\fe_loc-en.json'
json_en_ff = r'D:\P4\Branch\FF_RCT\GGC\public\Config\loc\FF\en.json'

with open(json_en_fe, 'r', encoding='utf-8') as f:
    data_fe = json.load(f)
with open(json_en_ff, 'r', encoding='utf-8') as f:
    data_ff = json.load(f)

# ===== 写 CSV 函数 =====
def write_csv(filename, rows):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'File'])
        writer.writerows(rows)

# ===== 准备数据并去重排序 =====
all_rows = []
existing_rows = []
missing_rows = []

for key in sorted(key_source_map.keys()):  # 按 key 排序
    files = sorted(key_source_map[key])    # 去重并排序文件路径
    for file in files:
        all_rows.append([key, file])
        if key in data_fe or key in data_ff:
            existing_rows.append([key, file])
            print(f"[EXIST] {key} | {file}")
        else:
            missing_rows.append([key, file])
            print(f"[MISSING] {key} | {file}")

# ===== 输出 CSV =====
write_csv('all_found_keys.csv', all_rows)
write_csv('existing_keys.csv', existing_rows)
write_csv('result_test2.csv', missing_rows)

print("\n扫描完成！")
print("所有找到的 key → all_found_keys.csv")
print("存在的 key → existing_keys.csv")
print("缺失的 key → result_test2.csv")
