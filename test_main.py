import chardet

file_path=r'D:\p4_workspace\Branch\FF_RCT\GGC\public\Server\Config\0cb2b45dcd8a686181aad7db4682e32e'

with open(file_path, "rb") as f:
    rawdata = f.read(10000)  # 只读前一部分就足够检测了

result = chardet.detect(rawdata)
print(result['encoding'] is not None)
print(type(result))