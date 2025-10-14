import os
import re

# ==== 路径配置 ====
source_folder = r"D:\\p4_workspace\\Branch\\FF_RCT\\GGC"  # 主扫描目录
exclude_folder = os.path.normpath(r"D:\P4\Dev\GGC\public\GameApp")  # 排除文件夹
target_folders = [
    r"D:\P4\Dev\GGC\public\Config\loc\FE",
    r"D:\P4\Dev\GGC\public\Config\loc\FF"
]  # 对比目录
output_found = r"D:\found_keys.txt"
output_missing = r"D:\missing_keys.txt"

# ==== 文件类型 ====
valid_extensions = ('.csv', '.json', '.vue', '.js')

# ==== 正则匹配规则 ====
csv_pattern = re.compile(r'\b(?:T|FE)_[A-Za-z0-9_]+\b')
quoted_pattern = re.compile(r'["\']?(T|FE)_[A-Za-z0-9_]+["\']?')  # 可匹配有/无引号

# ==== 第一步：扫描源文件夹，提取字段 ====
all_keys = set()
key_sources = {}  # key -> 来源文件

print(f"开始扫描源文件夹：{source_folder}")

for root, _, files in os.walk(source_folder):
    if os.path.commonpath([root, exclude_folder]) == exclude_folder:
        continue

    for file in files:
        if not file.endswith(valid_extensions):
            continue

        file_path = os.path.join(root, file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"[读取失败] {file_path} - {e}")
            continue

        # 根据文件类型选择正则
        if file.endswith('.csv'):
            matches = csv_pattern.findall(content)
        else:  # .json 或 .vue
            matches = [m.group(0).strip('"\'') for m in quoted_pattern.finditer(content)]

        # 记录 key 及来源文件
        for key in matches:
            all_keys.add(key)
            key_sources[key] = file_path
            print(f"提取到: {key} (来自 {file_path})")

print(f"\n扫描完成，共提取到 {len(all_keys)} 个唯一字段。")

# ==== 第二步：在目标文件夹中检查是否存在 ====
missing_keys = []
found_count = 0

print(f"\n开始对比目标目录（FE + FF）...\n")

for idx, key in enumerate(sorted(all_keys), 1):
    found = False
    found_in_folder = None

    for target_folder in target_folders:
        for root, _, files in os.walk(target_folder):
            for file in files:
                if not file.endswith(valid_extensions):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if key in f.read():
                            found = True
                            found_in_folder = os.path.basename(target_folder)
                            break
                except Exception as e:
                    print(f"[读取失败] {file_path} - {e}")
            if found:
                break
        if found:
            break

    if found:
        found_count += 1
        print(f"[{idx}/{len(all_keys)}] 找到: {key} (在 {found_in_folder})")
    else:
        missing_keys.append(key)
        print(f"[{idx}/{len(all_keys)}] 未找到: {key}")

# ==== 第三步：输出结果 ====
with open(output_found, 'w', encoding='utf-8') as f:
    for key in sorted(all_keys):
        f.write(f"{key} (来自 {key_sources[key]})\n")

with open(output_missing, 'w', encoding='utf-8') as f:
    for key in sorted(missing_keys):
        f.write(key + '\n')

print("\n扫描完成！")
print(f"总计字段: {len(all_keys)}")
print(f"已找到: {found_count}")
print(f"未找到: {len(missing_keys)}")
print(f"所有字段保存至：{output_found}")
print(f"缺失字段保存至：{output_missing}")