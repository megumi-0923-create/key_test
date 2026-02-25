import csv


#将.eca,.gdvar文件先二进制读取，再decode提取文本
def decode_file(file):
    with open(file, 'rb') as f:
        rawdata=f.read()
    try:
        return rawdata.decode('utf-8')
    except UnicodeDecodeError:
        return rawdata.decode('ISO-8859-1', errors='replace')

# ===== 写 CSV 函数 =====
def write_csv(filename, rows):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'File','备注','存在的文件'])
        writer.writerows(rows)



def check_key_in_group(key, keys_dict, values_dict):
    # 返回：
    # - any_empty: 是否有文件的 value 为空
    # - diff_files: 状态不一致的文件名列表（value 非空或 key 不存在）
    #

    non_empty_files = []
    empty_files = []
    not_exist_files = []

    for name, keys in keys_dict.items():
        if key in keys:
            val = values_dict[name].get(key, '').strip()
            if val == '':
                empty_files.append(name)
            else:
                non_empty_files.append(name)
        else:
            not_exist_files.append(name)

    any_empty = len(empty_files) > 0
    all_exist = len(not_exist_files) == 0

    return all_exist,any_empty, empty_files





