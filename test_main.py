import chardet
from function import *

file_path=r'D:\p4_workspace\Branch\FF_RCT\GGC\Tools\FBXImportWithAssimp\FBXimport\FBXImportWA\FBXImportWA\DataOutput.h'

with open(file_path, "rb") as f:
    rawdata = f.read()  # 只读前一部分就足够检测了

result = chardet.detect(rawdata)
print(result['encoding'])
print(type(result))

content_program=''

# with open(file_path, 'r', encoding=result['encoding']) as f:
#     content_program += f.read()
print(decode_file(file_path))