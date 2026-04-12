import streamlit as st

st.set_page_config(layout="wide")

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    st.markdown("""
    <style>
    .grid {
        display: grid;
        grid-template-columns: repeat(2,1fr);
        gap: 15px;
        padding: 20px;
    }

    .item {
        text-align: center;
    }

    .box {
        width: 100%;
        height: 110px;
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.5);
        display:flex;
        align-items:center;
        justify-content:center;
        background: rgba(255,255,255,0.05);
        color:white;
        font-size:16px;
    }

    body {
        background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== GRID =====
    st.markdown('<div class="grid">', unsafe_allow_html=True)

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

    # زر بالنص
    if st.button("🗂️\nالمجموعات"):
        st.session_state.page = "categories"
        st.rerun()

# ===== PAGES =====
else:

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
