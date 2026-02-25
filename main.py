import json
import os
import re
import logging
import chardet

from function import *  # 确保 decode_file 函数在 function.py 中
from datetime import datetime
import csv

# ===== 日志配置 =====
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===== 扫描路径 =====
path_branch = r"D:\p4_workspace\Branch\FF_RCT"
path=path_branch+r'\GGC'

# ===== 初始化过滤规则 =====
ext_skip_test = ['.bytes', '.meta', '.fab', '.fbx', '.library', '.png', '.DS_Store', '.dll', '.exe', '.ico', '.cur',
                 '.unityweb', '.package', '.pdf', '.jpg', '.PNG', '.zip', '.bin', '.js', '.fcc', '.tga', '.FBX',
                 '.asset', '.exr', '.mmd', '.ttc', '.so', '.tif', '.cs', '.ttf', '.mmdb', '.gif', '.pdb', '.ilk',
                 '.obj', '.idb', '.iobj', '.ipdb', '.lib','.respck']

dir_skip_test = ['node_modules', 'packages', 'StreamingAssets', 'GameApp_Beta',
                 'GameApp', 'EditorApp','loc','Loc','ShareLoc2','ShareLoc','Server','UGCTemplateMap','fe-blockly-web']

file_skip_test = ['fe_loc-en.json', 'fe_loc-vi.json', 'fe_loc-zh-Hans.json',
                  'fe_loc-zh-Hant.json', 'en.json', 'vi.json', 'zh-cn.json',
                  'zh-tw.json', 'protoc', 'protoc-gen-go']

ext_decode_type = ['.eca', '.gdvar', '.mdc', '.cs', '.json', '.h']

key_source_map = {}   # { key: set([file1, file2]) }

skip_key=['FE_0_B_PGC_INTERNAL_WITH_TEMPLATE','FE_0_F_PROJECT_CLOSE_2','FE_0_HW_GAME_EDITOR_INTERNALSETTING','FE_47_PERSONANAME','T_45_HL_Moderation_fail']

# ===== 遍历文件 =====
#非版本更新所用的key,即FE_或者T_开头
# pattern_not_upgrade=r'(?<![A-Za-z0-9_])(?:FE_|T_)\d+_[A-Za-z0-9_-]*(?:_[A-Za-z0-9_-]+)*'
pattern_not_upgrade = r'''
(?<![A-Za-z0-9_])(?:
    # 裸 key：不允许结尾空格，遇到符号即停,例如:T_40_WZY_WS_FONT_NOTOSANS
    ((?:FE_|T_)\d+_[^\s=#$%()'`,;\.]+(?:\s+\d+)*)(?<![,;.\'"`])
  |
    # 单引号：允许结尾空格,例如'T_40_WZY_WS_FONT_NOTOSANS  '
    '((?:FE_|T_)\d+_[^']*?\s*)'
  |
    # 双引号：允许结尾空格,例如"T_40_WZY_WS_FONT_NOTOSANS  "
    "((?:FE_|T_)\d+_[^"]*?\s*)"
  |
    # 圆括号：允许 / 不允许结尾空格,例如(T_40_WZY_WS_FONT_NOTOSANS   )
    \(((?:FE_|T_)\d+_[^)]*?)\)
)
'''
#版本更新所用的key,即OB_开头
pattern_upgrade=r'OB_[\w]+(?:_[\w]+)*'

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
        print(file)

        try:
            if ext == '.csv':
                # with open(filepath, 'r', encoding=encoding_type, errors='ignore') as f:
                #     for line in f:
                #         keys_in_line = re.findall(r'\b((?:FE_|T_)\w+)\b', line)
                #         for key in keys_in_line:
                #             key_source_map.setdefault(key, set()).add(filepath)
                #             print(f"[FOUND] {key} | {filepath}")
                continue
            elif ext in ext_decode_type:
                text = decode_file(filepath)
                keys_in_file = {
                    next(g for g in m.groups() if g)
                    for m in re.finditer(pattern_not_upgrade, text, re.VERBOSE)
                }
                for key in keys_in_file:
                    key_source_map.setdefault(key, set()).add(filepath)
                    print(f"[FOUND] {key} | {filepath}")
            else:
                with open(filepath, 'r', encoding=encoding_type, errors='ignore') as f:
                    for line in f:
                        keys_in_line = {
                            next(g for g in m.groups() if g)
                            for m in re.finditer(pattern_not_upgrade, line, re.VERBOSE)
                        }
                        for key in keys_in_line:
                            key_source_map.setdefault(key, set()).add(filepath)
                            print(f"[FOUND] {key} | {filepath}")
        except Exception as e:
            logging.exception(f"读取文件失败: {filepath} - {e}")
            continue

# ===== 遍历csv_file_total和csv_file_upgrade中包含的文件 =====
csv_file_total_list=[]
csv_file_upgrade_list=[]
with open('csv_file_total.txt','r',encoding='utf-8') as f:
    for line in f:
        line=line.strip('\n')
        csv_file_total_list.append(path_branch+line)

with open('csv_file_upgrade.txt','r',encoding='utf-8') as f:
    for line in f:
        line=line.strip('\n')
        csv_file_upgrade_list.append(path_branch+line)

for file in csv_file_total_list:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        # for line in f:
        #     keys_in_line = re.findall(pattern_not_upgrade, line)
        #     for key in keys_in_line:
        #         key_source_map.setdefault(key, set()).add(file)
        #         print(f"[FOUND] {key} | {file}")
        reader=csv.DictReader(f)
        if 'FEShowControl' in reader.fieldnames:
            for row in reader:
                fe_value = row.get('FEShowControl', '').strip().upper()  # 防止大小写不一致
                if fe_value == 'FALSE':
                    continue
                line_str = ','.join(row.values())
                keys_in_line = {
                    next(g for g in m.groups() if g)
                    for m in re.finditer(pattern_not_upgrade, line, re.VERBOSE)
                }
                for key in keys_in_line:
                    key_source_map.setdefault(key, set()).add(file)
                    # print(f"[FOUND] {key} | {file}")
        else:
            f.seek(0)
            next(f)  # 跳过表头行
            for line in f:
                keys_in_line = {
                    next(g for g in m.groups() if g)
                    for m in re.finditer(pattern_not_upgrade, line, re.VERBOSE)
                }
                for key in keys_in_line:
                    key_source_map.setdefault(key, set()).add(file)
                    # print(f"[FOUND] {key} | {file}")

for file in csv_file_upgrade_list:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            keys_in_line = {
                next(g for g in m.groups() if g)
                for m in re.finditer(pattern_not_upgrade, line, re.VERBOSE)
            }
            for key in keys_in_line:
                key_source_map.setdefault(key, set()).add(file)
                # print(f"[FOUND] {key} | {file}")


# ===== 加载语言包 =====
json_dir_fe=path+r'\public\Config\loc\FE'
json_dir_ff= path+r'\public\Config\loc\FF'

json_files_fe=os.listdir(json_dir_fe)
json_files_ff=os.listdir(json_dir_ff)

json_datas_fe = {}
for i, filename in enumerate(json_files_fe):
    path = os.path.join(json_dir_fe, filename)
    with open(path, "r", encoding="utf-8") as f:
        json_datas_fe[filename] = json.load(f)

json_datas_ff = {}
for i, filename in enumerate(json_files_ff):
    path = os.path.join(json_dir_ff, filename)
    with open(path, "r", encoding="utf-8") as f:
        json_datas_ff[filename] = json.load(f)

keys_dict_fe={name:set(data.keys()) for name,data in json_datas_fe.items()}
values_dict_fe={name:data for name,data in json_datas_fe.items()}
keys_dict_ff={name:set(data.keys()) for name,data in json_datas_ff.items()}
values_dict_ff={name:data for name,data in json_datas_ff.items()}
# print(keys_dict_fe)
# with open('test.txt','w',encoding='utf-8') as f:
#     f.write(str(key_source_map.keys()))

# key_source_map = {k: [] for k in ['FE_00_M_WS_AITYPE']}
# print(key_source_map)

# ===== 准备数据并去重排序 =====
missing_rows = []
# #用于测试
# file_path=r'aaaaa'

for key in sorted(key_source_map.keys()):
    print(key)
# for key in sorted(key_source_map):
    if key in skip_key:
        continue

    files = sorted(key_source_map[key])
    # print(files)
    file_path = files[0]

    in_fe = any(key in keys for keys in keys_dict_fe.values())
    in_ff = any(key in keys for keys in keys_dict_ff.values())

    # print(in_fe, in_ff)

    # 情况 3：都不在
    if not in_fe and not in_ff:
        missing_rows.append([key, file_path, '', ''])
        continue

    # FE 逻辑
    if in_fe:
        all_exist,any_empty, empty_files = check_key_in_group(
            key, keys_dict_fe, values_dict_fe
        )
        # print(f'all_exist:{all_exist}')
        # print(f'all_empty:{all_empty}')
        # print(f'diff_files:{diff_files}')
        if any_empty:
            print('-----')
            missing_rows.append([key, file_path, '翻译为空', ','.join(empty_files)])
        elif all_exist and not any_empty:
            continue
        else:
            print('-----')
            missing_rows.append([key, file_path, '不知道什么情况', ''])
        continue

    # FF 逻辑
    if in_ff:
        all_exist, any_empty, empty_files = check_key_in_group(
            key, keys_dict_ff, values_dict_ff
        )

        if any_empty:
            missing_rows.append([key, file_path, '翻译为空', ','.join(empty_files)])
        elif all_exist and not any_empty:
            continue
        else:
            missing_rows.append([key, file_path, '不知道什么情况', ''])

# ===== 输出 CSV =====
now_str = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
result_file='result_test/result_test2_'+now_str+'.csv'
write_csv(result_file, missing_rows)

print(f"缺失的 key → result_test/result_test2_'+{now_str}+'.csv")
