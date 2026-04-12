import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* زر الإيموجي */
.stButton > button {
    width: 100%;
    height: 90px;
    font-size: 40px; /* 👈 كبرنا الأيقونة */
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.05);
}

/* النص */
.label {
    text-align: center;
    color: white;
    margin-top: -5px;
    margin-bottom: 10px;
    font-size: 14px;
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

        if st.button("📦"):
            st.session_state.page = "products"
            st.rerun()
        st.markdown('<div class="label">الأصناف</div>', unsafe_allow_html=True)

        if st.button("🗂️"):
            st.session_state.page = "categories"
            st.rerun()
        st.markdown('<div class="label">المجموعات</div>', unsafe_allow_html=True)

        if st.button("👥"):
            st.session_state.page = "suppliers"
            st.rerun()
        st.markdown('<div class="label">الموردين</div>', unsafe_allow_html=True)

# ===== PAGES =====
else:

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة")
