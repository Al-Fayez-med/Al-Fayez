import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

.stButton > button {
    width: 100%;
    height: 80px;
    margin: 10px 0;
    border-radius: 16px;
    border: none;
    background-color: rgba(255,255,255,0.1);
    color: white;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    # 👇 هذا هو السر الحقيقي
    left, center, right = st.columns([1,2,1])

    with center:

        st.title("📱 القائمة الرئيسية")

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

    st.title("صفحة قيد التطوير")
