import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* ===== الترويسة ===== */
.header {
    height: 120px; /* 👈 مساحة فوق */
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
}

/* زر مربع */
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

/* النص */
.label {
    text-align: left;
    color: white;
    font-size: 14px;
    margin-top: 5px;
}

/* المسافة بين العناصر */
.icon-block {
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    # ===== الترويسة =====
    st.markdown('<div class="header">🏪 اسم المستودع</div>', unsafe_allow_html=True)

    def icon(label, emoji, page):
        st.markdown('<div class="icon-block">', unsafe_allow_html=True)

        if st.button(emoji, key=page):
            st.session_state.page = page
            st.rerun()

        st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ===== الأيقونات =====
    icon("ملفي الشخصي", "👤", "profile")
    icon("الضبط", "⚙️", "settings")
    icon("الصيدليات", "🏥", "pharmacy")
    icon("الأصناف", "📦", "products")
    icon("المجموعات", "🗂️", "categories")
    icon("المستودعات", "🏭", "warehouses")
    icon("الموردين", "👥", "suppliers")
    icon("السندات", "🧾", "receipts")
    icon("الصندوق", "💰", "cash")

# ===== PAGES =====
else:

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة قيد التطوير")
