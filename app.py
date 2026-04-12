import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
body {
    direction: rtl;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* نخلي الأعمدة ما تنهار على الجوال */
@media (max-width: 768px) {
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
    }
}

/* الأزرار */
.stButton>button {
    width: 100%;
    height: 110px;
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.6);
    background: transparent;
    color: white;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    # صف 1
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤\nملفي الشخصي"):
            st.session_state.page = "profile"
            st.rerun()
    with col2:
        if st.button("⚙️\nالضبط"):
            st.session_state.page = "settings"
            st.rerun()

    # صف 2
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏥\nالصيدليات"):
            st.session_state.page = "pharmacy"
            st.rerun()
    with col2:
        if st.button("📦\nالأصناف"):
            st.session_state.page = "products"
            st.rerun()

    # صف 3
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥\nالموردين"):
            st.session_state.page = "suppliers"
            st.rerun()
    with col2:
        if st.button("🏭\nالمستودعات"):
            st.session_state.page = "warehouses"
            st.rerun()

    # صف 4
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰\nالصندوق"):
            st.session_state.page = "cash"
            st.rerun()
    with col2:
        if st.button("🧾\nالسندات"):
            st.session_state.page = "receipts"
            st.rerun()

    # صف 5 (الأيقونة الناقصة)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗂️\nالمجموعات"):
            st.session_state.page = "categories"
            st.rerun()

# ===== PAGES =====
else:

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
