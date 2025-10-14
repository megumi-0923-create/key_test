import json
import os
import re
import logging

logging.basicConfig(
    filename='error.log',        # 日志文件名
    level=logging.ERROR,         # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)


path = r"D:\\p4_workspace\\Branch\\FF_RCT\\GGC"

content=''
ext_skip_test=['.bytes','.meta','.fab','.fbx','.library','.png','.DS_Store','.dll','.exe','.ico','.cur','.unityweb']
dir_skip_test=['node_modules','packages','StreamingAssets']

for root, dirs, files in os.walk(path):
    try:
        dirs[:] = [d for d in dirs if d not in dir_skip_test]

        for file in files:
            print("=========")
            print(root)
            print(dirs)
            print(file)
            filepath = os.path.join(root, file)
            name,ext=os.path.splitext(file)
            if ext in ext_skip_test:
                continue
            with open(filepath,'r',encoding='utf-8') as f:
                content+=f.read()
            print("=========")

    except Exception as e:
        logging.error(e)

pattern=r'["\']((?:FE_|T_)\w*)["\']'
result=re.findall(pattern,content)
#列表去重
result=list(dict.fromkeys(result))

print(result)

json_en_fe=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Config\loc\FE\fe_loc-en.json'
json_en_ff=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Config\loc\FF\en.json'

with open(json_en_fe,'r',encoding='utf-8') as f:
    data_fe=json.load(f)
with open(json_en_ff,'r',encoding='utf-8') as f:
    data_ff=json.load(f)



list_result=[]
for key in result:
    try:
        if key in data_fe:
            continue
        elif key not in data_fe:
            if key in data_ff:
                continue
            else:
                list_result.append(key)
        else:
            logging.error(f'不知道啥情况出现的,key的名字是{key}')
    except Exception as e:
        logging.exception(e)

print(list_result)
with open('result_test2.txt','w',encoding='utf-8') as f:
    for key in list_result:
        f.write(key+'\n')