import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* الزر مربع */
.stButton > button {
    width: 90px;
    height: 90px;
    font-size: 38px;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.05);
    display: block;
    margin: auto;
}

/* النص */
.label {
    text-align: center;
    color: white;
    font-size: 14px;
    margin-top: 0px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    left, center, right = st.columns([1,2,1])

    with center:

        def icon(label, emoji, page):
            c1, c2, c3 = st.columns(3)
            with c2:
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
