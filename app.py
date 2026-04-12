import streamlit as st

st.set_page_config(layout="wide")

# =========================================
# ======= 🎨 STYLE (CSS) ==================
# =========================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* ===== HEADER ===== */
.header {
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ===== ICON BUTTON ===== */
.stButton > button {
    width: 90px;
    height: 90px;
    font-size: 40px;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* تكبير الإيموجي */
.stButton > button span {
    display: inline-block;
    transform: scale(2.5);
}

/* ===== TEXT ===== */
.label {
    text-align: left;
    color: white;
    font-size: 14px;
    margin-top: 5px;
}

/* ===== SPACING ===== */
.icon-block {
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# ======= 🔁 NAVIGATION ====================
# =========================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================================
# ======= 🧱 HEADER ========================
# =========================================

def show_header():
    st.markdown(
        '<div class="header">🏪 اسم المستودع</div>',
        unsafe_allow_html=True
    )

# =========================================
# ======= 🧩 ICON COMPONENT ===============
# =========================================

def icon(label, emoji, page):
    st.markdown('<div class="icon-block">', unsafe_allow_html=True)

    if st.button(emoji, key=page):
        st.session_state.page = page
        st.rerun()

    st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# ======= 🏠 الصفحة الرئيسية ===============
# =========================================

def home_page():

    show_header()

    icon("ملفي الشخصي", "👤", "profile")
    icon("الضبط", "⚙️", "settings")
    icon("الصيدليات", "🏥", "pharmacy")
    icon("الأصناف", "📦", "products")
    icon("المجموعات", "🗂️", "categories")
    icon("المستودعات", "🏭", "warehouses")
    icon("الموردين", "👥", "suppliers")
    icon("السندات", "🧾", "receipts")
    icon("الصندوق", "💰", "cash")

# =========================================
# ======= 💊 قسم الأصناف ==================
# =========================================

def products_section():

    # -------- 📄 الصفحة الرئيسية للأصناف --------
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💊 الأصناف")

    st.write("هنا رح نبني نظام الأصناف لاحقًا")

# =========================================
# ======= 🗂️ قسم المجموعات ================
# =========================================
# =========================================
# ======= 🗂️ قسم المجموعات ================
# =========================================

def generate_category_code():
    categories = st.session_state.get("categories_data", [])
    if not categories:
        return "001"
    max_code = max(int(c["code"]) for c in categories)
    return str(max_code + 1).zfill(3)


def categories_section():

    # ====== بيانات مؤقتة ======
    if "categories_data" not in st.session_state:
        st.session_state.categories_data = []

    if "show_add" not in st.session_state:
        st.session_state.show_add = False

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # ====== رجوع ======
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ إدارة المجموعات")

    # ====== زر إضافة ======
    if st.button("➕ إضافة مجموعة"):
        st.session_state.show_add = True

    st.markdown("---")

    # =========================================
    # ======= 🎨 جدول HTML ====================
    # =========================================

    st.markdown("""
    <style>
    .table { width:100%; color:white; font-size:14px; }
    .row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:10px 5px;
        border-bottom:1px solid rgba(255,255,255,0.1);
    }
    .header {
        font-weight:bold;
        border-bottom:2px solid rgba(255,255,255,0.3);
    }
    .cell { flex:1; text-align:left; }
    .code { color:rgba(255,255,255,0.5); }
    </style>
    """, unsafe_allow_html=True)

    # ===== Header =====
    st.markdown("""
    <div class="row header">
        <div class="cell">الاسم</div>
        <div class="cell">الكود</div>
        <div class="cell">عدد الأصناف</div>
        <div class="cell">تعديل</div>
        <div class="cell">حذف</div>
    </div>
    """, unsafe_allow_html=True)

    # ===== Rows =====
    for i, c in enumerate(st.session_state.categories_data):

        cols = st.columns([3,1,1,1,1])

        cols[0].write(c["name"])
        cols[1].markdown(f"<span class='code'>{c['code']}</span>", unsafe_allow_html=True)
        cols[2].write("0")

        if cols[3].button("✏️", key=f"edit_{i}"):
            st.session_state.edit_id = i

        if cols[4].button("🗑️", key=f"del_{i}"):
            st.session_state.delete_id = i

    # =========================================
    # ======= ➕ إضافة ========================
    # =========================================

    if st.session_state.show_add:

        st.markdown("### ➕ إضافة مجموعة")

        name = st.text_input("اسم المجموعة")

        code = generate_category_code()

        st.markdown(f"الكود: <span style='color:gray'>{code}</span>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        if col1.button("موافق"):
            if name:
                st.session_state.categories_data.append({
                    "name": name,
                    "code": code
                })
                st.session_state.show_add = False
                st.rerun()

        if col2.button("إلغاء"):
            st.session_state.show_add = False
            st.rerun()

    # =========================================
    # ======= ✏️ تعديل ========================
    # =========================================

    if st.session_state.edit_id is not None:

        c = st.session_state.categories_data[st.session_state.edit_id]

        st.markdown("### ✏️ تعديل مجموعة")

        new_name = st.text_input("اسم المجموعة", value=c["name"])

        st.markdown(f"الكود: <span style='color:gray'>{c['code']}</span>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        if col1.button("موافق"):
            if new_name:
                c["name"] = new_name
                st.session_state.edit_id = None
                st.rerun()

        if col2.button("إلغاء"):
            st.session_state.edit_id = None
            st.rerun()

    # =========================================
    # ======= 🗑️ حذف =========================
    # =========================================

    if st.session_state.delete_id is not None:

        c = st.session_state.categories_data[st.session_state.delete_id]

        st.warning(f"⚠️ حذف المجموعة: {c['name']} ؟")

        col1, col2 = st.columns(2)

        if col1.button("إلغاء"):
            st.session_state.delete_id = None
            st.rerun()

        if col2.button("تأكيد"):
            st.session_state.categories_data.pop(st.session_state.delete_id)
            st.session_state.delete_id = None
            st.rerun()
# =========================================
# ======= 👥 قسم الموردين =================
# =========================================

def suppliers_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("👥 الموردين")

# =========================================
# ======= 🏭 قسم المستودعات ===============
# =========================================

def warehouses_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🏭 المستودعات")

# =========================================
# ======= 💰 قسم الصندوق ==================
# =========================================

def cash_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💰 الصندوق")

# =========================================
# ======= 🧾 قسم السندات ==================
# =========================================

def receipts_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🧾 السندات")

# =========================================
# ======= 🏥 قسم الصيدليات ================
# =========================================

def pharmacy_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🏥 الصيدليات")

# =========================================
# ======= ⚙️ قسم الضبط ====================
# =========================================

def settings_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("⚙️ الضبط")

# =========================================
# ======= 👤 الملف الشخصي =================
# =========================================

def profile_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("👤 ملفي الشخصي")

# =========================================
# ======= 🚀 ROUTER =======================
# =========================================

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "products":
    products_section()

elif st.session_state.page == "categories":
    categories_section()

elif st.session_state.page == "suppliers":
    suppliers_section()

elif st.session_state.page == "warehouses":
    warehouses_section()

elif st.session_state.page == "cash":
    cash_section()

elif st.session_state.page == "receipts":
    receipts_section()

elif st.session_state.page == "pharmacy":
    pharmacy_section()

elif st.session_state.page == "settings":
    settings_section()

elif st.session_state.page == "profile":
    profile_section()
