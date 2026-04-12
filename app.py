import streamlit as st

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# ================= Navigation =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= Style =================
st.markdown("""
<style>
body {
    direction: rtl;
}
.block-container {
    padding: 0;
}
.blue-bg {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
    height: 100vh;
    padding: 20px;
}
.card {
    text-align: center;
    padding: 20px;
}
.stButton>button {
    width: 110px;
    height: 110px;
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.6);
    background: transparent;
    color: white;
    font-size: 14px;
}
.stButton>button:active {
    transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

# ================= Home =================
if st.session_state.page == "home":

    st.markdown('<div class="blue-bg">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👤\nملفي الشخصي"):
            st.session_state.page = "profile"
            st.rerun()

        if st.button("🏥\nالصيدليات"):
            st.session_state.page = "pharmacy"
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

        if st.button("📦\nالأصناف"):
            st.session_state.page = "products"
            st.rerun()

        if st.button("🏭\nالمستودعات"):
            st.session_state.page = "warehouses"
            st.rerun()

        if st.button("🧾\nالسندات"):
            st.session_state.page = "receipts"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= Pages =================
else:

    st.markdown("""
    <div style="background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
    height:100vh; padding:20px; color:white;">
    """, unsafe_allow_html=True)

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فارغة")
    st.write("🚧 قيد التطوير")

    st.markdown("</div>", unsafe_allow_html=True)
