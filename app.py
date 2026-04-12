# =========================================
# 📦 IMPORTS
# =========================================
import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json


# =========================================
# ⚙️ PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="نظام إدارة المستودعات",
    page_icon="💊",
    layout="wide"
)


# =========================================
# 🔥 FIREBASE (الاتصال)
# =========================================
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()


# =========================================
# 📦 DATA (تحميل البيانات)
# =========================================
@st.cache_data
def load_categories():
    docs = db.collection("categories").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


@st.cache_data
def load_products():
    docs = db.collection("products").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


def generate_category_code():
    cats = load_categories()
    if not cats:
        return "001"
    max_code = max(int(c["code"]) for c in cats)
    return str(max_code + 1).zfill(3)


# =========================================
# 🎨 STYLE (التصميم)
# =========================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
}

.header {
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stButton > button {
    width: 90px;
    height: 90px;
    font-size: 40px;
    border-radius: 20px;
}

.label {
    text-align: left;
    color: white;
    font-size: 14px;
    margin-top: 5px;
}

.icon-block {
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)


# =========================================
# 🔁 NAVIGATION (التنقل)
# =========================================
if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================
# 🧱 HEADER
# =========================================
def show_header():
    st.markdown(
        '<div class="header">🏪 اسم المستودع</div>',
        unsafe_allow_html=True
    )


# =========================================
# 🧩 ICON COMPONENT
# =========================================
def icon(label, emoji, page):
    if st.button(emoji, key=page):
        st.session_state.page = page
        st.rerun()

    st.markdown(
        f'<div class="label">{label}</div>',
        unsafe_allow_html=True
    )


# =========================================
# 🏠 HOME PAGE
# =========================================
def home_page():

    show_header()

    # ===== الأيقونات =====
    icon("الأصناف", "📦", "products")
    icon("المجموعات", "🗂️", "categories")


# =========================================
# 🗂️ CATEGORIES SECTION
# =========================================

def categories_section():

    # ===== CSS =====
    st.markdown("""
    <style>
    .group-btn button {
        width: 100% !important;
        height: 60px !important;
        text-align: right !important;
        font-size: 18px !important;
        border-radius: 12px !important;
    }

    .action-btn button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        padding: 0 !important;
    }

    .action-label {
        font-size: 12px;
        opacity: 0.5;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== رجوع =====
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ المجموعات")

    categories = load_categories()
    products = load_products()

    # ===== state =====
    if "open" not in st.session_state:
        st.session_state.open = None

    if "add_mode" not in st.session_state:
        st.session_state.add_mode = False

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # =========================================
    # ➕ إضافة
    # =========================================
    if st.button("➕ إضافة مجموعة"):
        st.session_state.add_mode = True

    # ===== form إضافة =====
    if st.session_state.add_mode:

        name = st.text_input("اسم المجموعة", key="add_name")
        code = generate_category_code()

        st.markdown(f"<span style='opacity:0.5'>الكود: {code}</span>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✔️"):
                if name:
                    db.collection("categories").add({
                        "name": name,
                        "code": code
                    })
                    st.session_state.add_mode = False
                    st.cache_data.clear()
                    st.rerun()

        with col2:
            if st.button("❌"):
                st.session_state.add_mode = False
                st.rerun()

    st.markdown("---")

    # =========================================
    # 📁 عرض
    # =========================================
    for c in categories:

        # ===== زر المجموعة =====
        with st.container():
            st.markdown('<div class="group-btn">', unsafe_allow_html=True)

            if st.button(f"📁 {c['name']}", key=f"group_{c['id']}"):
                if st.session_state.open == c["id"]:
                    st.session_state.open = None
                else:
                    st.session_state.open = c["id"]
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ===== التفاصيل =====
        if st.session_state.open == c["id"]:

            st.markdown(f"<span style='opacity:0.5'>الكود: {c['code']}</span>", unsafe_allow_html=True)

            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.write(f"عدد الأصناف: {count}")

            # ===== أزرار =====
            col1, col2, col3 = st.columns(3)

            # ===== تعديل =====
            with col1:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("✏️", key=f"edit_btn_{c['id']}"):
                    st.session_state.edit_id = c["id"]
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="action-label">تعديل</div>', unsafe_allow_html=True)

            # ===== حذف =====
            with col2:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_btn_{c['id']}"):
                    st.session_state.delete_id = c["id"]
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="action-label">حذف</div>', unsafe_allow_html=True)

            # ===== استعراض =====
            with col3:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("👁️", key=f"view_btn_{c['id']}"):
                    st.session_state.page = "products"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="action-label">استعراض</div>', unsafe_allow_html=True)

            # =========================================
            # ✏️ تعديل inline
            # =========================================
            if st.session_state.edit_id == c["id"]:

                new_name = st.text_input("اسم جديد", value=c["name"], key=f"edit_input_{c['id']}")

                colA, colB = st.columns(2)

                with colA:
                    if st.button("✔️", key=f"save_{c['id']}"):
                        db.collection("categories").document(c["id"]).update({
                            "name": new_name
                        })
                        st.session_state.edit_id = None
                        st.cache_data.clear()
                        st.rerun()

                with colB:
                    if st.button("❌", key=f"cancel_edit_{c['id']}"):
                        st.session_state.edit_id = None
                        st.rerun()

            # =========================================
            # 🗑️ حذف inline
            # =========================================
            if st.session_state.delete_id == c["id"]:

                st.warning(f"حذف {c['name']}؟")

                colA, colB = st.columns(2)

                with colA:
                    if st.button("✔️", key=f"confirm_del_{c['id']}"):
                        has_products = any(p.get("category_code") == c["code"] for p in products)

                        if has_products:
                            st.error("لا يمكن حذف مجموعة فيها أصناف")
                        else:
                            db.collection("categories").document(c["id"]).delete()
                            st.session_state.delete_id = None
                            st.cache_data.clear()
                            st.rerun()

                with colB:
                    if st.button("❌", key=f"cancel_del_{c['id']}"):
                        st.session_state.delete_id = None
                        st.rerun()

            st.markdown("---")
# =========================================
# 💊 PRODUCTS SECTION
# =========================================
def products_section():

    # ===== رجوع =====
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💊 الأصناف")

    products = load_products()

    for p in products:
        st.write(p["name"])


# =========================================
# 🚀 ROUTER (تحديد الصفحة)
# =========================================
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "categories":
    categories_section()

elif st.session_state.page == "products":
    products_section()
