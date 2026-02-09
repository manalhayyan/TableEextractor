import re
from collections import defaultdict

# اسم الملف اللي يحتوي النصوص
filename = "queries.txt"

# قراءة محتوى الملف
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# تنظيف النصوص من #(lf) و #(tab)
clean_content = re.sub(r'#\([a-z]+\)', ' ', content)
clean_content = re.sub(r'\s+', ' ', clean_content)

# تقسيم كل Query = "...."
query_blocks = re.findall(r'Query\s*=\s*"([^"]+)"', clean_content, re.IGNORECASE)

results = []

for i, query in enumerate(query_blocks, 1):
    # البحث عن الجداول بعد FROM أو JOIN
    tables = re.findall(r'(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([A-Z0-9_]+\.[A-Z0-9_]+)', query, re.IGNORECASE)
    
    # إزالة التكرار مع الحفاظ على الترتيب
    seen = set()
    unique_tables = []
    for t in tables:
        t_upper = t.upper()
        if t_upper not in seen:
            seen.add(t_upper)
            unique_tables.append(t_upper)
    
    # تصنيف الجداول
    classified = defaultdict(list)
    for t in unique_tables:
        if t.startswith('OMI.') or t.startswith('DP_OMI.'):
            classified['جداول الإدارة'].append(t)
        else:
            classified['جداول المستودعات'].append(t)
    
    results.append((i, unique_tables, classified))

# طباعة النتائج
for idx, all_tables, classified in results:
    print(f"\n--- Query {idx} ---")
    print(f"عدد الجداول: {len(all_tables)}")
    for category, tbls in classified.items():
        print(f"{category}: {', '.join(tbls)}")

