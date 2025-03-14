# preprocess_all.py
import re
import os


count_sumary = 0


def wrap_formulas(content):
    global count_sumary
    content, count = re.subn(r"src\s*=([\s\"]*)/imgs/", r"src=\1/blog/imgs/", content)
    count_sumary += count
    return content


input_dir = "public"  # 你的 Markdown 文件目录
for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if filename.endswith(".html"):
            print("process:", filename)
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            processed_content = wrap_formulas(content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(processed_content)

print(f"完成{count_sumary}处替换")
