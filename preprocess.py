# preprocess_all.py
import re
import os


def wrap_formulas(content):
    content = re.sub(
        r"\$\$(.*?)\$\$",
        r'<div class="math display">\1</div>',
        content,
        flags=re.DOTALL,
    )
    # content = re.sub(r'\$(.*?)\$', r'<div class="math inline">\1</div>', content)
    return content


input_dir = "content"  # 你的 Markdown 文件目录
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
