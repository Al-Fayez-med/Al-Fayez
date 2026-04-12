import streamlit as st

st.set_page_config(layout="wide")

# خلفية زرقا
st.markdown("""
<style>
body {
    direction: rtl;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}
.stButton>button {
    width: 120px;
    height: 120px;
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.6);
    background: transparent;
    color: white;
    font-size: 16px;
}
.stButton>button:hover {
    border-color: white;
}
</style>
""", unsafe_allow_html=True)

# navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# الصفحة الرئيسية
if st.session_state.page == "home":

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👤\nملفي"):
            st.session_state.page = "profile"
            st.rerun()

        if st.button("📦\nالأصناف"):
            st.session_state.page = "products"
            st.rerun()

        if st.button("👥\nالموردين"):
            st.session_state.page = "suppliers"
            st.rerun()

        if st.button("💰\nالصندوق"):
            st.session_state.page = "cash"
            st.rerun()

    with col2:
        if st.button("⚙️\nالضبط"):
            st.session_state.page = "settings"
            st.rerun()

        if st.button("🏥\nالصيدليات"):
            st.session_state.page = "pharmacy"
            st.rerun()

        if st.button("🏭\nالمستودعات"):
            st.session_state.page = "warehouses"
            st.rerun()

        if st.button("🧾\nالسندات"):
            st.session_state.page = "receipts"
            st.rerun()

# الصفحات
else:
    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
