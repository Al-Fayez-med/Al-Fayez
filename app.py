
import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

/* إزالة الهوامش */
.block-container {
    padding: 0 !important;
}

/* خلفية زرقا */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* توسيط المحتوى */
.main {
    display: flex;
    justify-content: center;
}

/* الأزرار */
.stButton > button {
    width: 250px;
    height: 70px;
    margin: 10px auto;
    display: block;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.6);
    background: transparent;
    color: white;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    st.markdown("##", unsafe_allow_html=True)

    if st.button("👤 ملفي الشخصي"):
        st.session_state.page = "profile"
        st.rerun()

    if st.button("⚙️ الضبط"):
        st.session_state.page = "settings"
        st.rerun()

    if st.button("🏥 الصيدليات"):
        st.session_state.page = "pharmacy"
        st.rerun()

    if st.button("📦 الأصناف"):
        st.session_state.page = "products"
        st.rerun()

    if st.button("👥 الموردين"):
        st.session_state.page = "suppliers"
        st.rerun()

    if st.button("🏭 المستودعات"):
        st.session_state.page = "warehouses"
        st.rerun()

    if st.button("💰 الصندوق"):
        st.session_state.page = "cash"
        st.rerun()

    if st.button("🧾 السندات"):
        st.session_state.page = "receipts"
        st.rerun()

    if st.button("🗂️ المجموعات"):
        st.session_state.page = "categories"
        st.rerun()

# ===== PAGES =====
else:

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
