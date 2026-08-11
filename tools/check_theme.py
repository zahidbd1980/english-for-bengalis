from pathlib import Path
import re

p = Path(r"H:/project/English_Learning_Platform/themeCode.txt")
t = p.read_text(encoding="utf-8")
print("size", len(t))
print("CDATA open/close", t.count("<![CDATA["), t.count("]]>"))
print("b:skin", t.count("<b:skin"), t.count("</b:skin>"))
print("has html close", "</html>" in t)
m = re.search(r'name="body\.background\.height"[\s\S]*?/>', t)
print("HEIGHT VAR:\n", m.group(0) if m else "missing")
# Find font values that might break
for name in ["blog.title.font", "tabs.font", "posts.title.font", "body.text.font"]:
    m = re.search(rf'name="{name}"[\s\S]*?/>', t)
    if m:
        line = m.group(0).replace("\n", " ")
        print(name, "=>", line[-120:])
