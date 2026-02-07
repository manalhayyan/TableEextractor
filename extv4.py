import streamlit as st

import re

st.set_page_config(page_title="Table Extractor", layout="wide")

st.title("📊 استخراج وتصنيف الجداول")

st.write("ارفع ملف نصي (TXT) وسيتم استخراج أسماء الجداول وتصنيفها مع إمكانية تحميل النتائج.")

# ============================

# تهيئة المتغيرات

# ============================

tables_unique = []

admin_tables = []

dp_tables = []

no_schema_tables = []

output_text = ""

# ============================

# رفع الملف

# ============================

uploaded_file = st.file_uploader("📂 ارفع ملف TXT", type=["txt"])

def clean_table_name(name):

    return name.strip('()[]{}"').strip()

if uploaded_file is not None:

    try:

        file_text = uploaded_file.read().decode("utf-8")

    except UnicodeDecodeError:

        file_text = uploaded_file.read().decode("utf-8-sig")

    # ============================

    # التحقق من أن الملف ليس كود

    # ============================

    if any(keyword in file_text for keyword in ["import ", "def ", "streamlit"]):

        st.error("❌ الملف يحتوي على كود برمجي، الرجاء رفع ملف بيانات TXT فقط.")

        st.stop()

    # ============================

    # تنظيف التعليقات

    # ============================

    text_clean = re.sub(r'--.*', '', file_text)

    text_clean = re.sub(r'/\*.*?\*/', '', text_clean, flags=re.DOTALL)

    tables = []

    # ============================

    # استخراج أسماء الجداول

    # ============================

    from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'

    join_pattern = r'\bJOIN\s+([^\s\(\);]+)'

    for part in re.findall(from_pattern, text_clean, re.IGNORECASE):

        for t in part.split(','):

            name = t.split('#(lf)')[0].strip()

            if name and not name.startswith('('):

                tables.append(clean_table_name(name.split()[0]))

    for t in re.findall(join_pattern, text_clean, re.IGNORECASE):

        name = t.split('#(lf)')[0].strip()

        if name and not name.startswith('('):

            tables.append(clean_table_name(name.split()[0]))

    # Views (Power Query)

    view_pattern = r'Name\s*=\s*"([^"]+)"'

    for v in re.findall(view_pattern, text_clean):

        tables.append(clean_table_name(v))

    # إزالة التكرار

    tables_unique = list(dict.fromkeys(tables))

    # ============================

    # التصنيف

    # ============================

    for table in tables_unique:

        if '.' in table:

            schema = table.split('.')[0].lower()

            if 'omi' in schema:

                admin_tables.append(table)

            else:

                dp_tables.append(table)

        else:

            no_schema_tables.append(table)

    # ============================

    # عرض النتائج

    # ============================

    st.success(f"✅ عدد الجداول الكلي: {len(tables_unique)}")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("📝 جداول الإدارة")

        st.write(admin_tables if admin_tables else "لا يوجد")

    with col2:

        st.subheader("📝 جداول المستودعات التقنية")

        st.write(dp_tables if dp_tables else "لا يوجد")

    with col3:

        st.subheader("📝 جداول بدون سكيما")

        st.write(no_schema_tables if no_schema_tables else "لا يوجد")

    st.subheader("📋 جميع الجداول")

    st.write(tables_unique if tables_unique else "لا توجد نتائج")

    # ============================

    # تجهيز ملف TXT

    # ============================

    output_text += f"عدد الجداول الكلي: {len(tables_unique)}\n\n"

    output_text += "جداول الإدارة:\n"

    for t in admin_tables:

        output_text += f"- {t}\n"

    output_text += "\nجداول المستودعات التقنية:\n"

    for t in dp_tables:

        output_text += f"- {t}\n"

    output_text += "\nجداول بدون سكيما:\n"

    for t in no_schema_tables:

        output_text += f"- {t}\n"

    output_text += "\nجميع الجداول:\n"

    for t in tables_unique:

        output_text += f"- {t}\n"

    st.download_button(

        label="⬇️ تحميل النتائج (TXT)",

        data=output_text,

        file_name="tables_list.txt",

        mime="text/plain"

    )

else:

    st.info("⬆️ الرجاء رفع ملف TXT للبدء")
Buy st.info | Spaceship
Own st.info today. Secure checkout and guided transfer support. No hidden fees.
 
import streamlit as st

import re

st.set_page_config(page_title="Table Extractor", layout="wide")

st.title("📊 استخراج وتصنيف الجداول")

st.write("ارفع ملف نصي (TXT) وسيتم استخراج أسماء الجداول وتصنيفها مع إمكانية تحميل النتائج.")

# ============================

# تهيئة المتغيرات

# ============================

tables_unique = []

admin_tables = []

dp_tables = []

no_schema_tables = []

output_text = ""

# ============================

# رفع الملف

# ============================

uploaded_file = st.file_uploader("📂 ارفع ملف TXT", type=["txt"])

def clean_table_name(name):

    return name.strip('()[]{}"').strip()

if uploaded_file is not None:

    try:

        file_text = uploaded_file.read().decode("utf-8")

    except UnicodeDecodeError:

        file_text = uploaded_file.read().decode("utf-8-sig")

    # ============================

    # التحقق من أن الملف ليس كود

    # ============================

    if any(keyword in file_text for keyword in ["import ", "def ", "streamlit"]):

        st.error("❌ الملف يحتوي على كود برمجي، الرجاء رفع ملف بيانات TXT فقط.")

        st.stop()

    # ============================

    # تنظيف التعليقات

    # ============================

    text_clean = re.sub(r'--.*', '', file_text)

    text_clean = re.sub(r'/\*.*?\*/', '', text_clean, flags=re.DOTALL)

    tables = []

    # ============================

    # استخراج أسماء الجداول

    # ============================

    from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'

    join_pattern = r'\bJOIN\s+([^\s\(\);]+)'

    for part in re.findall(from_pattern, text_clean, re.IGNORECASE):

        for t in part.split(','):

            name = t.split('#(lf)')[0].strip()

            if name and not name.startswith('('):

                tables.append(clean_table_name(name.split()[0]))

    for t in re.findall(join_pattern, text_clean, re.IGNORECASE):

        name = t.split('#(lf)')[0].strip()

        if name and not name.startswith('('):

            tables.append(clean_table_name(name.split()[0]))

    # Views (Power Query)

    view_pattern = r'Name\s*=\s*"([^"]+)"'

    for v in re.findall(view_pattern, text_clean):

        tables.append(clean_table_name(v))

    # إزالة التكرار

    tables_unique = list(dict.fromkeys(tables))

    # ============================

    # التصنيف

    # ============================

    for table in tables_unique:

        if '.' in table:

            schema = table.split('.')[0].lower()

            if 'omi' in schema:

                admin_tables.append(table)

            else:

                dp_tables.append(table)

        else:

            no_schema_tables.append(table)

    # ============================

    # عرض النتائج

    # ============================

    st.success(f"✅ عدد الجداول الكلي: {len(tables_unique)}")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("📝 جداول الإدارة")

        st.write(admin_tables if admin_tables else "لا يوجد")

    with col2:

        st.subheader("📝 جداول المستودعات التقنية")

        st.write(dp_tables if dp_tables else "لا يوجد")

    with col3:

        st.subheader("📝 جداول بدون سكيما")

        st.write(no_schema_tables if no_schema_tables else "لا يوجد")

    st.subheader("📋 جميع الجداول")

    st.write(tables_unique if tables_unique else "لا توجد نتائج")

    # ============================

    # تجهيز ملف TXT

    # ============================

    output_text += f"عدد الجداول الكلي: {len(tables_unique)}\n\n"

    output_text += "جداول الإدارة:\n"

    for t in admin_tables:

        output_text += f"- {t}\n"

    output_text += "\nجداول المستودعات التقنية:\n"

    for t in dp_tables:

        output_text += f"- {t}\n"

    output_text += "\nجداول بدون سكيما:\n"

    for t in no_schema_tables:

        output_text += f"- {t}\n"

    output_text += "\nجميع الجداول:\n"

    for t in tables_unique:

        output_text += f"- {t}\n"

    st.download_button(

        label="⬇️ تحميل النتائج (TXT)",

        data=output_text,

        file_name="tables_list.txt",

        mime="text/plain"

    )

else:

    st.info("⬆️ الرجاء رفع ملف TXT للبدء")
Buy st.info | Spaceship
Own st.info today. Secure checkout and guided transfer support. No hidden fees.
 