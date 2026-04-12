import streamlit as st

st.set_page_config(layout="wide")

# ===== STYLE =====
st.markdown("""
<style>

/* إزالة الهوامش */
.block-container {
    padding: 0 !important;
}

/* خلفية */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

/* توسيط كل شي */
.main {
    display: flex;
    justify-content: center;
}

/* زر بدون شكل */
.stButton > button {
    background: transparent;
    border: none;
    width: 100%;
}

/* العنصر */
.item {
    text-align: center;
    margin: 20px 0;
    cursor: pointer;
}

/* الأيقونة */
.icon {
    width: 80px;
    height: 80px;
    margin: auto;
    border: 2px solid rgba(255,255,255,0.7);
    border-radius: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    opacity: 0.7;
}

/* حركة الضغط */
.icon:active {
    transform: scale(1.1);
}

/* svg */
.icon svg {
    width: 40px;
    height: 40px;
    stroke: white;
    fill: none;
    stroke-width: 2;
}

/* النص */
.label {
    margin-top: 8px;
    color: white;
    font-size: 14px;
    opacity: 1;
}

</style>
""", unsafe_allow_html=True)

# ===== NAV =====
if "page" not in st.session_state:
    st.session_state.page = "home"

# ===== HOME =====
if st.session_state.page == "home":

    def item(label, icon_svg, page_name):
        if st.button(label, key=page_name):
            st.session_state.page = page_name
            st.rerun()

        st.markdown(f"""
        <div class="item">
            <div class="icon">
                {icon_svg}
            </div>
            <div class="label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    # ===== ICONS =====

    item("ملفي الشخصي", '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c2-4 14-4 16 0"/></svg>', "profile")

    item("الضبط", '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/></svg>', "settings")

    item("الصيدليات", '<svg viewBox="0 0 24 24"><path d="M12 2v20M2 12h20"/></svg>', "pharmacy")

    item("الأصناف", '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13"/></svg>', "products")

    item("الموردين", '<svg viewBox="0 0 24 24"><circle cx="9" cy="7" r="4"/></svg>', "suppliers")

    item("المستودعات", '<svg viewBox="0 0 24 24"><path d="M3 21V7l9-4 9 4v14"/></svg>', "warehouses")

    item("الصندوق", '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="2"/></svg>', "cash")

    item("السندات", '<svg viewBox="0 0 24 24"><path d="M6 2h12v20H6z"/></svg>', "receipts")

    item("المجموعات", '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/></svg>', "categories")

# ===== PAGES =====
else:

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("صفحة فاضية")
