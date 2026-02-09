import streamlit as st
import re

# ============================
# إعداد الصفحة
# ============================
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
query_tables = []
output_text = ""

# ============================
# رفع الملف
# ============================
uploaded_file = st.file_uploader("📂 ارفع ملف TXT", type=["txt"])

# ============================
# دالة تنظيف اسم الجدول
# ============================
def clean_table_name(name):
    return name.strip('()[]{}"').strip()

# ============================
# دالة لترقيم القوائم
# ============================
def display_list_numbered(lst):
    return [f"{i+1}. {clean_table_name(t)}" for i, t in enumerate(lst)]

# ============================
# دالة تجهيز النص المرقم للملف
# ============================
def add_numbered_section(title, lst, prefix=""):
    txt = f"{title}\n"
    for i, t in enumerate(lst):
        txt += f"{i+1}. {prefix}{clean_table_name(t)}\n"
    return txt + "\n"

# ============================
# معالجة الملف
# ============================
if uploaded_file is not None:
    try:
        file_text = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        file_text = uploaded_file.read().decode("utf-8-sig")

    # ============================
    # التحقق من أن الملف ليس كود برمجي
    # ============================
    if any(keyword in file_text for keyword in ["import ", "def ", "streamlit"]):
        st.error("❌ الملف يحتوي على كود برمجي، الرجاء رفع ملف بيانات TXT فقط.")
        st.stop()

    # ============================
    # تنظيف التعليقات
    # ============================
    text_clean = re.sub(r'--.*', '', file_text)
    text_clean = re.sub(r'/\*.*?\*/', '', text_clean, flags=re.DOTALL)

    # ============================
    # استخراج SQL داخل query = "" أو ''' '''
    # ============================
    query_blocks = []

    # query = " ... "
    query_blocks += re.findall(
        r'query\s*=\s*"([\s\S]*?)"',
        text_clean,
        re.IGNORECASE
    )

    # query = ''' ... '''
    query_blocks += re.findall(
        r"query\s*=\s*'''([\s\S]*?)'''",
        text_clean,
        re.IGNORECASE
    )

    # ============================
    # استخراج أسماء الجداول (FROM / JOIN / Views)
    # ============================
    tables = []

    from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'
    join_pattern = r'\bJOIN\s+([^\s\(\);]+)'
    view_pattern = r'Name\s*=\s*"([^"]+)"'

    # استخراج الجداول العامة من النص بالكامل
    for part in re.findall(from_pattern, text_clean, re.IGNORECASE):
        for t in part.split(','):
            name = t.split('#(lf)')[0].strip()
            if name and not name.startswith('('):
                tables.append(clean_table_name(name.split()[0]))

    for t in re.findall(join_pattern, text_clean, re.IGNORECASE):
        name = t.split('#(lf)')[0].strip()
        if name and not name.startswith('('):
            tables.append(clean_table_name(name.split()[0]))

    for v in re.findall(view_pattern, text_clean):
        tables.append(clean_table_name(v))

    # ============================
    # استخراج الجداول فقط من داخل query (لتمييزها)
    # ============================
    for qb in query_blocks:
        for part in re.findall(from_pattern, qb, re.IGNORECASE):
            for t in part.split(','):
                name = clean_table_name(t.split()[0])
                if name:
                    query_tables.append(name)

        for t in re.findall(join_pattern, qb, re.IGNORECASE):
            name = clean_table_name(t.split()[0])
            if name:
                query_tables.append(name)

    query_tables = list(dict.fromkeys(query_tables))

    # ============================
    # إزالة التكرار العام
    # ============================
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
    # عرض النتائج مع ترقيم
    # ============================
    st.success(f"✅ عدد الجداول الكلي: {len(tables_unique)}")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📝 جداول الإدارة")
        st.write(display_list_numbered(admin_tables) if admin_tables else "لا يوجد")

    with col2:
        st.subheader("📝 جداول المستودعات التقنية")
        st.write(display_list_numbered(dp_tables) if dp_tables else "لا يوجد")

    with col3:
        st.subheader("📝 جداول بدون سكيما")
        st.write(display_list_numbered(no_schema_tables) if no_schema_tables else "لا يوجد")

    st.subheader("📋 جميع الجداول")
    st.write(display_list_numbered(tables_unique) if tables_unique else "لا توجد نتائج")

    st.subheader("🧠 جداول مستخرجة من داخل query")
    st.write(display_list_numbered([f"[QUERY] {t}" for t in query_tables]) if query_tables else "لا يوجد")

    # ============================
    # تجهيز ملف TXT للتحميل مع ترقيم
    # ============================
    output_text += f"عدد الجداول الكلي: {len(tables_unique)}\n\n"
    output_text += add_numbered_section("جداول الإدارة:", admin_tables)
    output_text += add_numbered_section("جداول المستودعات التقنية:", dp_tables)
    output_text += add_numbered_section("جداول بدون سكيما:", no_schema_tables)
    output_text += add_numbered_section("جداول من داخل query:", query_tables, prefix="[QUERY] ")
    output_text += add_numbered_section("جميع الجداول:", tables_unique)

    st.download_button(
        label="⬇️ تحميل النتائج (TXT)",
        data=output_text,
        file_name="tables_list.txt",
        mime="text/plain"
    )

else:
    st.info("⬆️ الرجاء رفع ملف TXT للبدء")

# ============================
# مثال رسالة إضافية صحيحة
# ============================
st.info("🛸 Buy Spaceship")
st.write("Own today. Secure checkout and guided transfer support. No hidden fees.")
