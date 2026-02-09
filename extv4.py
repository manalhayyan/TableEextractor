import streamlit as st
import re

st.set_page_config(page_title="Table Extractor", layout="wide")
st.title("📊 استخراج أسماء الجداول")
st.write("اختر طريقة استخراج الجداول: من أي SELECT في الملف أو فقط من المتغير query.")

# رفع الملف
uploaded_file = st.file_uploader("📂 ارفع ملف TXT", type=["txt"])

def clean_table_name(name):
    return name.strip('()[]{}"').strip()

def display_list_numbered(lst):
    return [f"{i+1}. {clean_table_name(t)}" for i, t in enumerate(lst)]

if uploaded_file is not None:
    try:
        file_text = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        file_text = uploaded_file.read().decode("utf-8-sig")

    # تنظيف التعليقات
    text_clean = re.sub(r'--.*', '', file_text)
    text_clean = re.sub(r'/\*.*?\*/', '', text_clean, flags=re.DOTALL)

    # ============================
    # اختيار نوع الاستخراج
    # ============================
    extract_mode = st.radio(
        "اختر طريقة الاستخراج:",
        ("من أي SELECT في النص", "من داخل query فقط")
    )

    tables = []

    if extract_mode == "من أي SELECT في النص":
        # استخراج FROM / JOIN من النص كله
        from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'
        join_pattern = r'\bJOIN\s+([^\s\(\);]+)'

        for part in re.findall(from_pattern, text_clean, re.IGNORECASE):
            for t in part.split(','):
                name = clean_table_name(t.split()[0])
                if name:
                    tables.append(name)

        for t in re.findall(join_pattern, text_clean, re.IGNORECASE):
            name = clean_table_name(t.split()[0])
            if name:
                tables.append(name)

    else:  # "من داخل query فقط"
        # استخراج SQL داخل query = "" أو ''' '''
        query_blocks = []

        query_blocks += re.findall(
            r'query\s*=\s*"([\s\S]*?)"',
            text_clean,
            re.IGNORECASE
        )
        query_blocks += re.findall(
            r"query\s*=\s*'''([\s\S]*?)'''",
            text_clean,
            re.IGNORECASE
        )

        from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'
        join_pattern = r'\bJOIN\s+([^\s\(\);]+)'

        for qb in query_blocks:
            for part in re.findall(from_pattern, qb, re.IGNORECASE):
                for t in part.split(','):
                    name = clean_table_name(t.split()[0])
                    if name:
                        tables.append(name)
            for t in re.findall(join_pattern, qb, re.IGNORECASE):
                name = clean_table_name(t.split()[0])
                if name:
                    tables.append(name)

    tables_unique = list(dict.fromkeys(tables))

    # التصنيف
    admin_tables = []
    dp_tables = []

    for table in tables_unique:
        if '.' in table and 'omi' in table.split('.')[0].lower():
            admin_tables.append(table)
        else:
            dp_tables.append(table)

    # عرض النتائج
    st.success(f"✅ عدد الجداول: {len(tables_unique)}")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 جداول الإدارة")
        st.write(display_list_numbered(admin_tables) if admin_tables else "لا يوجد")

    with col2:
        st.subheader("📝 جداول المستودعات التقنية")
        st.write(display_list_numbered(dp_tables) if dp_tables else "لا يوجد")

    st.subheader("📋 جميع الجداول")
    st.write(display_list_numbered(tables_unique) if tables_unique else "لا توجد نتائج")

    # تجهيز ملف TXT للتحميل
    output_text = f"عدد الجداول: {len(tables_unique)}\n\n"
    output_text += "جداول الإدارة:\n" + "\n".join(display_list_numbered(admin_tables)) + "\n\n"
    output_text += "جداول المستودعات التقنية:\n" + "\n".join(display_list_numbered(dp_tables)) + "\n\n"
    output_text += "جميع الجداول:\n" + "\n".join(display_list_numbered(tables_unique)) + "\n"

    st.download_button(
        label="⬇️ تحميل النتائج (TXT)",
        data=output_text,
        file_name="tables_list.txt",
        mime="text/plain"
    )

else:
    st.info("⬆️ الرجاء رفع ملف TXT للبدء")
