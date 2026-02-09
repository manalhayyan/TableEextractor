import streamlit as st
import re
from collections import defaultdict

st.title("Extractor of Shared Queries and Tables")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف txt يحتوي على shared queries", type="txt")

if uploaded_file is not None:
    results = []
    current_shared = None
    current_query_lines = []

    # قراءة الملف سطر بسطر لتجنب مشاكل الملفات الكبيرة
    for raw_line in uploaded_file:
        line = raw_line.decode("utf-8").strip()
        
        # البحث عن بداية shared block
        shared_match = re.match(r'shared\s+([A-Z0-9_]+)\s*=', line, re.IGNORECASE)
        if shared_match:
            if current_shared and current_query_lines:
                query_text = " ".join(current_query_lines)
                results.append((current_shared, query_text))
            current_shared = shared_match.group(1)
            current_query_lines = []

        # جمع أسطر Query
        if 'Query=' in line:
            query_line = line.split('Query=')[1].strip().strip('"')
            current_query_lines.append(query_line)
        elif current_shared:
            current_query_lines.append(line.strip())

    # إضافة آخر بلوك
    if current_shared and current_query_lines:
        query_text = " ".join(current_query_lines)
        results.append((current_shared, query_text))

    # معالجة كل بلوك لاستخراج الجداول وتصنيفها
    final_results = []
    for idx, (shared_name, query_text) in enumerate(results, 1):
        # تنظيف الـ markers مثل #(lf) أو #(tab)
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

    # عرض النتائج في Streamlit
    for idx, shared_name, all_tables, classified in final_results:
        st.subheader(f"Shared Block {idx}: {shared_name}")
        for cat, tbls in classified.items():
            st.write(f"{cat}: {', '.join(tbls)}")
