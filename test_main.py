import chardet

file_path=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Package\official_package.csv'

with open(file_path, "rb") as f:
    rawdata = f.read(10000)  # 只读前一部分就足够检测了

result = chardet.detect(rawdata)
print(result)