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
# ======= 🗂️ قسم المجموعات (HTML) =========
# =========================================

def generate_category_code():
    categories = st.session_state.get("categories_data", [])
    if not categories:
        return "001"
    max_code = max(int(c["code"]) for c in categories)
    return str(max_code + 1).zfill(3)


def categories_section():

    # ====== بيانات ======
    if "categories_data" not in st.session_state:
        st.session_state.categories_data = []

    if "search_text" not in st.session_state:
        st.session_state.search_text = ""

    if "show_add" not in st.session_state:
        st.session_state.show_add = False

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # ===== رجوع =====
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("## 🗂️ إدارة المجموعات")

    # ===== بحث =====
    st.session_state.search_text = st.text_input("🔍", label_visibility="collapsed")

    # ===== فلترة =====
    filtered = [
        c for c in st.session_state.categories_data
        if st.session_state.search_text.lower() in c["name"].lower()
    ]

    # =========================================
    # ======= 🎨 HTML + CSS ===================
    # =========================================

    html = """
    <style>
    .top-bar {
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:20px;
    }

    .btn {
        width:60px;
        height:60px;
        border-radius:12px;
        border:1px solid rgba(255,255,255,0.3);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:22px;
        cursor:pointer;
    }

    .btn:hover {
        background:rgba(255,255,255,0.1);
    }

    .table {
        width:100%;
    }

    .row {
        display:flex;
        align-items:center;
        padding:10px 5px;
        border-bottom:1px solid rgba(255,255,255,0.1);
    }

    .header {
        font-weight:bold;
        border-bottom:2px solid rgba(255,255,255,0.3);
    }

    .cell {
        flex:1;
        text-align:left;
    }

    .actions {
        display:flex;
        gap:10px;
    }

    .code {
        color:rgba(255,255,255,0.5);
    }
    </style>

    <div class="top-bar">
        <div class="btn">➕</div>
        <div>🔍</div>
    </div>

    <div class="table">

        <div class="row header">
            <div class="cell">الاسم</div>
            <div class="cell">الكود</div>
            <div class="cell">عدد</div>
            <div class="cell">إجراءات</div>
        </div>
    """

    for i, c in enumerate(filtered):
        html += f"""
        <div class="row">
            <div class="cell">{c['name']}</div>
            <div class="cell code">{c['code']}</div>
            <div class="cell">0</div>
            <div class="cell">
                <div class="actions">
                    <span>✏️</span>
                    <span>🗑️</span>
                </div>
            </div>
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    # =========================================
    # ======= ➕ إضافة ========================
    # =========================================

    if st.button("➕ إضافة مجموعة"):
        st.session_state.show_add = True

    if st.session_state.show_add:

        name = st.text_input("اسم المجموعة")
        code = generate_category_code()

        st.markdown(f"الكود: <span style='color:gray'>{code}</span>", unsafe_allow_html=True)

        if st.button("موافق"):
            if name:
                st.session_state.categories_data.append({
                    "name": name,
                    "code": code
                })
                st.session_state.show_add = False
                st.rerun()

        if st.button("إلغاء"):
            st.session_state.show_add = False
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
