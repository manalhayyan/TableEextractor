import re
from collections import defaultdict

# اسم الملف يدخله المستخدم
filename = input("أدخل اسم ملف الـ txt: ")

results = []
current_shared = None
current_query_lines = []

try:
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
                query_line = line.split('Query=')[1].strip().strip('"')
                current_query_lines.append(query_line)
            elif current_shared:
                current_query_lines.append(line.strip())
except FileNotFoundError:
    print(f"الملف '{filename}' غير موجود!")
    exit()

# إضافة آخر بلوك
if current_shared and current_query_lines:
    query_text = " ".join(current_query_lines)
    results.append((current_shared, query_text))

# معالجة كل بلوك لاستخراج الجداول وتصنيفها
all_unique_tables = set()
classified_final = defaultdict(list)

for shared_name, query_text in results:
    # تنظيف العلامات #lf و #tab
    clean_query = re.sub(r'#\([a-z]+\)', ' ', query_text)
    # استخراج الجداول بعد FROM و JOIN
    tables = re.findall(r'(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([A-Z0-9_]+\.[A-Z0-9_]+)', clean_query, re.IGNORECASE)
    
    for t in tables:
        t_upper = t.upper()
        if t_upper not in all_unique_tables:
            all_unique_tables.add(t_upper)
            # تصنيف الجداول
            if t_upper.startswith('OMI.') or '_OMI.' in t_upper:
                classified_final['جداول الإدارة'].append(t_upper)
            else:
                classified_final['جداول المستودعات'].append(t_upper)

# طباعة النتائج النهائية
print(f"\nعدد الجداول: {len(all_unique_tables)}\n")

for cat in ['جداول الإدارة', 'جداول المستودعات']:
    print(f"{cat}:")
    if cat in classified_final and classified_final[cat]:
        for tbl in classified_final[cat]:
            print(tbl)
    else:
        print("لا توجد جداول")
    print()
