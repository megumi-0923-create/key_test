import json
import os
import re
import logging
import chardet

from function import *

logging.basicConfig(
    filename='error.log',        # 日志文件名
    level=logging.ERROR,         # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)


path = r"D:\p4_workspace\Branch\FF_RCT\GGC\Tools"
# path_test=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Config\csv\UGCAnimStateChange.csv'

content_program= ''
content_csv=''
ext_skip_test=['.bytes','.meta','.fab','.fbx','.library','.png','.DS_Store','.dll','.exe','.ico','.cur','.unityweb',
               '.package','.pdf','.jpg','.PNG','.zip','.bin','.js','.fcc','.tga','.FBX','.asset','.exr','.mmd','.ttc',
               '.so','.tif','.cs','.ttf','.mmdb','.gif','.pdb','.ilk','.obj','.idb','.iobj','.ipdb']

dir_skip_test=['node_modules','packages','StreamingAssets','GameApp_Beta','GameApp','EditorApp','ProjectTemplate']
file_skip_test=['fe_loc-en.json','fe_loc-vi.json','fe_loc-zh-Hans.json','fe_loc-zh-Hant.json','en.json','vi.json','zh-cn.json','zh-tw.json','protoc','protoc-gen-go']
# ext_include_test=['.eca']
ext_decode_type=['.eca','.gdvar','.mdc','.cs','.json','.h']

for root, dirs, files in os.walk(path):
    dirs[:] = [d for d in dirs if d not in dir_skip_test]
    #
    for file in files:
        print("=========")
        print(root)
        print(dirs)
        print(file)
        filepath = os.path.join(root, file)

        name,ext=os.path.splitext(file)
        # ext_type.append(ext)
        # 单独处理.eca文件
        if ext not in ext_decode_type:
            with open(filepath, "rb") as f:
                rawdata = f.read(10000)
                encoding_type = chardet.detect(rawdata)['encoding']

        # print('----- ',ext)
        if ext in ext_skip_test or file in file_skip_test or ext=='' or 'Workshop' in file:
            continue
        elif ext=='.csv':
            with open(filepath, 'r', encoding=encoding_type) as f:
                content_csv += f.read()
        elif ext in ext_decode_type:
            content_program += decode_file(filepath)

        else:
            try:
                with open(filepath, 'r', encoding=encoding_type) as f:
                    content_program += f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content_program += f.read()
        print("=========")


pattern_program= r'["\']((?:FE_|T_)\w*)["\']'
result_program=re.findall(pattern_program, content_program)

pattern_csv=r',((?:FE_|T_)\w*),'
result_csv=re.findall(pattern_csv, content_csv)
result=result_program+result_csv
#列表去重

# result=list(dict.fromkeys(ext_type))
# print(result)
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