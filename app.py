import streamlit as st

st.set_page_config(layout="wide")

# NAV
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    st.markdown("""
    <style>
    body {
        margin:0;
        direction: rtl;
    }

    .grid {
        display:grid;
        grid-template-columns: repeat(2,1fr);
        gap:15px;
        padding:20px;
        height:100vh;
        background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
    }

    .item {
        text-align:center;
    }

    button.custom {
        width:100%;
        height:110px;
        border-radius:25px;
        border:2px solid rgba(255,255,255,0.6);
        background:transparent;
        color:white;
        font-size:14px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 👇 شبكة حقيقية
    st.markdown('<div class="grid">', unsafe_allow_html=True)

    if st.button("👤\nملفي الشخصي"):
        st.session_state.page = "profile"
        st.rerun()

    if st.button("⚙️\nالضبط"):
        st.session_state.page = "settings"
        st.rerun()

    if st.button("🏥\nالصيدليات"):
        st.session_state.page = "pharmacy"
        st.rerun()

    if st.button("📦\nالأصناف"):
        st.session_state.page = "products"
        st.rerun()

    if st.button("👥\nالموردين"):
        st.session_state.page = "suppliers"
        st.rerun()

    if st.button("🏭\nالمستودعات"):
        st.session_state.page = "warehouses"
        st.rerun()

    if st.button("💰\nالصندوق"):
        st.session_state.page = "cash"
        st.rerun()

    if st.button("🧾\nالسندات"):
        st.session_state.page = "receipts"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ===== PAGES =====
else:
    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
