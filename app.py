import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* الزر */
.stButton > button {
    width: 100%;
    height: 100px;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.05);
    color: white;
    font-size: 16px;
}

/* تقليل المسافات */
.block-container {
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    st.markdown("## 📱")

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

    # صف 5 (واحدة بالنص)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🗂️\nالمجموعات"):
            st.session_state.page = "categories"
            st.rerun()

# ===== PAGES =====
else:

    col1, col2 = st.columns([1,5])

    with col1:
        if st.button("⬅️"):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        st.title("صفحة فاضية")

    st.write("🚧 قيد البناء")
