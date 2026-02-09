import streamlit as st
import re
from collections import defaultdict

st.set_page_config(page_title="تحليل الجداول", layout="wide")

st.title("📊 محلل الجداول من ملفات SQL")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف txt", type=["txt"])

if uploaded_file is not None:
    # قراءة الملف سطر سطر
    results = []
    current_shared = None
    current_query_lines = []

    for line in uploaded_file:
        line = line.decode("utf-8").strip()
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

    # معالجة الجداول
    all_unique_tables = set()
    classified_final = defaultdict(list)

    for shared_name, query_text in results:
        clean_query = re.sub(r'#\([a-z]+\)', ' ', query_text)
        tables = re.findall(r'(?:FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN)\s+([A-Z0-9_]+\.[A-Z0-9_]+)', clean_query, re.IGNORECASE)
        
        for t in tables:
            t_upper = t.upper()
            if t_upper not in all_unique_tables:
                all_unique_tables.add(t_upper)
                if t_upper.startswith('OMI.') or '_OMI.' in t_upper:
                    classified_final['جداول الإدارة'].append(t_upper)
                else:
                    classified_final['جداول المستودعات'].append(t_upper)

    # عرض النتائج مع تأثير Fade
    st.markdown(f"### ✨ عدد الجداول: {len(all_unique_tables)}")

    for cat in ['جداول الإدارة', 'جداول المستودعات']:
        st.markdown(f"#### {cat}")
        if cat in classified_final and classified_final[cat]:
            for tbl in classified_final[cat]:
                st.markdown(f"- {tbl}")
        else:
            st.markdown("لا توجد جداول")
