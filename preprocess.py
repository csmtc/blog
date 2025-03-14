# preprocess_all.py
import re
import os


count_sumary = 0


def wrap_formulas(content):
    content, count = re.subn(
        r"\$\$(.*?)\$\$",
        r'<div class="math display">\1</div>',
        content,
        flags=re.DOTALL,
    )
    count_sumary += count
    content, count = re.subn(r"\([\s\./]*assets/(.*)\)", r"(../assets/\1)", content)
    count_sumary += count
    return content


input_dir = "content/post"  # 你的 Markdown 文件目录
for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if filename.endswith(".md"):
            print("process:", filename)
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            processed_content = wrap_formulas(content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(processed_content)
print(f"完成{count_sumary}处替换")
