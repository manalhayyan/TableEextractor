import re
from collections import defaultdict

filename = "queries.txt"

results = []
current_shared = None
current_query_lines = []

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        # البحث عن بداية shared block
        shared_match = re.match(r'shared\s+([A-Z0-9_]+)\s*=', line, re.IGNORECASE)
        if shared_match:
            # حفظ البلوك السابق إذا موجود
            if current_shared and current_query_lines:
                query_text = " ".join(current_query_lines)
                results.append((current_shared, query_text))
            # بدء بلوك جديد
            current_shared = shared_match.group(1)
            current_query_lines = []
        # جمع الأسطر التي تحتوي على Query
        if 'Query=' in line:
            # إزالة علامات اقتباس أو #lf / #tab لاحقًا
            query_line = line.split('Query=')[1].strip().strip('"')
            current_query_lines.append(query_line)
        elif current_shared:
            # إضافة باقي الأسطر التابعة للـ Query
            current_query_lines.append(line.strip())

# إضافة آخر بلوك
if current_shared and current_query_lines:
    query_text = " ".join(current_query_lines)
    results.append((current_shared, query_text))

# معالجة كل بلوك لاستخراج الجداول وتصنيفها
final_results = []
for idx, (shared_name, query_text) in enumerate(results, 1):
    clean_query = re.sub(r'#\([a-z]+\)', ' ', query_text)
    tables = re.findall(r'(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([A-Z0-9_]+\.[A-Z0-9_]+)', clean_query, re.IGNORECASE)
    seen = set()
    unique_tables = []
    for t in tables:
        t_upper = t.upper()
        if t_upper not in seen:
            seen.add(t_upper)
            unique_tables.append(t_upper)
    classified = defaultdict(list)
    for t in unique_tables:
        if t.upper().startswith('OMI.'):
            classified['جداول الإدارة'].append(t)
        else:
            classified['جداول المستودعات'].append(t)
    final_results.append((idx, shared_name, unique_tables, classified))

# طباعة النتائج
for idx, shared_name, all_tables, classified in final_results:
    print(f"\n--- Shared Block {idx}: {shared_name} ---")
    for cat, tbls in classified.items():
        print(f"{cat}: {', '.join(tbls)}")
