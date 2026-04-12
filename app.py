import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* زر مربع */
.stButton > button {
    width: 90px;
    height: 90px;
    font-size: 60px; /* 👈 كبرنا الإيموجي */
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.7); /* 👈 شفافية 70% */
    display: block;
}

/* النص */
.label {
    text-align: left;
    color: white;
    font-size: 14px;
    margin-top: 5px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    def icon(label, emoji, page):
        if st.button(emoji, key=page):
            st.session_state.page = page
            st.rerun()
        st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)

    # ===== كل الأيقونات =====
    icon("ملفي الشخصي", "👤", "profile")
    icon("الضبط", "⚙️", "settings")
    icon("الصيدليات", "🏥", "pharmacy")
    icon("الأصناف", "📦", "products")
    icon("الموردين", "👥", "suppliers")
    icon("المستودعات", "🏭", "warehouses")
    icon("الصندوق", "💰", "cash")
    icon("السندات", "🧾", "receipts")
    icon("المجموعات", "🗂️", "categories")

# ===== PAGES =====
else:

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة")
