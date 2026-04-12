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

def categories_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ المجموعات")

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
