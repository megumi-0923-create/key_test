import chardet
import re

# file_path=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Package\official_package.csv'
#
# with open(file_path, "rb") as f:
#     rawdata = f.read(10000)  # 只读前一部分就足够检测了
#
# result = chardet.detect(rawdata)
# print(result)

# file_path = r"csv_file_total.txt"
# prefix=r'D:\p4_workspace\Branch\FF_RCT'
#
# # # 定义新旧前缀
# # old_prefix = r"//DTS/Dev/Config/"
# # new_prefix = r"D:\\p4_workspace\\Branch\\FF_RCT\\Config\\"
#
# # 读取文件内容
# with open(file_path, 'r', encoding='utf-8') as f:
#     content = f.read()
#
# content=content.replace(prefix,'')
#
# # # 用正则替换（全局替换）
# # # 注意：因为 \ 是转义字符，所以写成双斜杠 \\
# # content = re.sub(re.escape(old_prefix), new_prefix, content)
#
# # # 写回文件
# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write(content)
# #
# print("✅ 所有路径前缀已替换完成！")

# with open('csv_file_total.txt','r',encoding='utf-8') as f:
#     for line in f:
#         line=line.strip('\n')
#         print(f'lllll{line}')

path_branch = r"D:\p4_workspace\Branch\FF_RCT"

#非版本更新所用的key,即FE_或者T_开头
pattern_not_upgrade=r'(?:FE_|T_)[\w]+(?:_[\w]+)*'
#版本更新所用的key,即OB_开头
pattern_upgrade=r'OB[\w]+(?:_[\w]+)*'

key_source_map = {}

csv_file_total_list = []
csv_file_upgrade_list = []
with open('csv_file_total.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip('\n')
        csv_file_total_list.append(path_branch + line)
with open('csv_file_upgrade.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip('\n')
        csv_file_upgrade_list.append(path_branch + line)

# for file in csv_file_total_list:
#     with open(file, 'r', encoding='utf-8', errors='ignore') as f:
#         for line in f:
#             keys_in_line = re.findall(pattern_not_upgrade, line)
#             for key in keys_in_line:
#                 key_source_map.setdefault(key, set()).add(file)
#                 print(f"[FOUND] {key} | {file}")

for file in csv_file_upgrade_list:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            print('=======')
            print(line)
            keys_in_line = re.findall(pattern_upgrade, line)
            for key in keys_in_line:
                key_source_map.setdefault(key, set()).add(file)
                print(f"[FOUND] {key} | {file}")
            print('=======')