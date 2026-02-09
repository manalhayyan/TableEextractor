import streamlit as st
import re
from collections import defaultdict

st.title("Extractor of Shared Queries and Tables")

uploaded_file = st.file_uploader("اختر ملف txt يحتوي على shared queries", type="txt")

if uploaded_file is not None:
    results = []
    current_shared = None
    current_query_lines = []

    # قراءة الملف سطر بسطر لتجنب مشاكل الملفات الكبيرة
    for raw_line in uploaded_file:
        line = raw_line.decode("utf-8").strip()
        
        shared_match = re.match(r'shared\s+([A-Z0-9_]+)\s*=', line, re.IGNORECASE)
        if shared_match:
            if current_shared and current_query_lines:
                query_text = " ".join(current_query_lines)
                results.append((current_shared, query_text))
            current_shared = shared_match.group(1)
            current_query_lines = []

        if 'Query=' in line:
            query_line = line.split('Query=')[1].strip().strip('"')
            current_query_lines.append(query_line)
        elif current_shared:
            current_query_lines.append(line.strip())

    if current_shared and current_query_lines:
        query_text = " ".join(current_query_lines)
        results.append((current_shared, query_text))

    all_unique_tables = set()
    classified = defaultdict(list)

    for shared_name, query_text in results:
        # إزالة علامات #(lf) و #(tab) وأي markers مشابهة
        clean_query = re.sub(r'#\([a-z]+\)', ' ', query_text)
        tables = re.findall(r'(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([A-Z0-9_]+\.[A-Z0-9_]+)', clean_query, re.IGNORECASE)
        for t in tables:
            t_upper = t.upper()
            if t_upper not in all_unique_tables:
                all_unique_tables.add(t_upper)
                if t_upper.startswith('OMI.'):
                    classified['جداول الإدارة'].append(t_upper)
                else:
                    classified['جداول المستودعات'].append(t_upper)

    # عرض النتائج
    st.write(f"**عدد الجداول: {len(all_unique_tables)}**\n")

    for cat in ['جداول الإدارة', 'جداول المستودعات']:
        st.write(f"**{cat}:**")
        if cat in classified:
            for tbl in classified[cat]:
                st.write(tbl)
        else:
            st.write("لا توجد جداول")
