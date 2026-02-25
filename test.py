import re
import os
import json
from function import *
#
# text=r'''
# %(T_52_META_API_10076_P3_D)
# '''
# pattern = r'''
# (?<![A-Za-z0-9_])(?:
#     # 裸 key：不允许结尾空格，遇到符号即停,例如:T_40_WZY_WS_FONT_NOTOSANS
#     ((?:FE_|T_)\d+_[^\s=#$%()'`,;\.]+(?:\s+\d+)*)(?<![,;.\'"`])
#   |
#     # 单引号：允许结尾空格,例如'T_40_WZY_WS_FONT_NOTOSANS  '
#     '((?:FE_|T_)\d+_[^']*?\s*)'
#   |
#     # 双引号：允许结尾空格,例如"T_40_WZY_WS_FONT_NOTOSANS  "
#     "((?:FE_|T_)\d+_[^"]*?\s*)"
#   |
#     # 圆括号：允许 / 不允许结尾空格,例如(T_40_WZY_WS_FONT_NOTOSANS   )
#     \(((?:FE_|T_)\d+_[^)]*?)\)
# )
# '''
#
# result_set = {
#     next(g for g in m.groups() if g)
#     for m in re.finditer(pattern, text, re.VERBOSE)
# }
#
# print(result_set)
# for key in result_set:
#     print(key)
#
path_branch = r"D:\p4_workspace\Branch\FF_RCT"
path=path_branch+r'\GGC'
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

aaa=['FE_00_M_WS_AITYPE']
missing_rows=[]
for key in aaa:
    print(key)
    files = ['a','b','c','d','e','f','g','h']
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
        all_exist,any_empty, diff_files = check_key_in_group(
            key, keys_dict_fe, values_dict_fe
        )
        print( f'{all_exist, any_empty, diff_files}结束')
        # print(f'all_exist:{all_exist}')
        # print(f'all_empty:{all_empty}')
        # print(f'diff_files:{diff_files}')
        if any_empty:
            print('>>>>>>>')
            missing_rows.append([key, file_path, '翻译为空', ''])
        elif all_exist and not any_empty:
            continue
        else:
            print('-----')
            missing_rows.append([key, file_path, '', ','.join(diff_files)])
        continue

    # FF 逻辑
    if in_ff:
        all_exist, any_empty, diff_files = check_key_in_group(
            key, keys_dict_ff, values_dict_ff
        )

        if any_empty:
            missing_rows.append([key, file_path, '翻译为空', ''])
        elif all_exist and not any_empty:
            continue
        else:
            missing_rows.append([key, file_path, '', ','.join(diff_files)])