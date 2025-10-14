


#将.eca,.gdvar文件先二进制读取，再decode提取文本
def decode_file(file):
    with open(file, 'rb') as f:
        rawdata=f.read()
    try:
        return rawdata.decode('utf-8')
    except UnicodeDecodeError:
        return rawdata.decode('ISO-8859-1', errors='replace')