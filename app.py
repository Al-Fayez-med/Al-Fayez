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
    /* تنسيق زر إضافة مجموعة */
    div[data-testid="column"]:has(button[key="open_add_category"]) {
        display: flex;
        justify-content: flex-start;
    }
    button[key="open_add_category"] {
        width: 60px !important;
        height: 60px !important;
        border-radius: 15px !important;
        font-size: 30px !important;
        padding: 0 !important;
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
    }
    button[key="open_add_category"]:hover {
        background-color: #2563eb !important;
    }

    /* تنسيق أزرار المجموعات */
    .group-btn button {
        width: 100% !important;
        height: 60px !important;
        text-align: right !important;
        font-size: 18px !important;
        border-radius: 12px !important;
    }

    /* تنسيق أزرار الإجراءات */
    .action-btn button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        padding: 0 !important;
    }

    /* تنسيق حقل الكود */
    .code-display {
        background-color: #1e3a8a;
        padding: 12px 10px;
        border-radius: 10px;
        color: #94a3b8;
        font-size: 14px;
        text-align: center;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== رجوع =====
    col_back, _ = st.columns([1, 10])
    with col_back:
        if st.button("⬅️", key="back_to_home"):
            st.session_state.page = "home"
            st.rerun()

    st.title("🗂️ المجموعات")

    categories = load_categories()
    products = load_products()

    # ===== state =====
    if "open" not in st.session_state: st.session_state.open = None
    if "add_mode" not in st.session_state: st.session_state.add_mode = False
    if "edit_id" not in st.session_state: st.session_state.edit_id = None
    if "delete_id" not in st.session_state: st.session_state.delete_id = None

    # =========================================
    # ➕ إضافة مجموعة
    # =========================================
    col_add1, _ = st.columns([1, 10])
    with col_add1:
        if st.button("➕", key="open_add_category"):
            st.session_state.add_mode = True

    if st.session_state.add_mode:
        with st.expander("➕ إضافة مجموعة جديدة", expanded=True):
            col_name, col_code = st.columns([2, 1])
            with col_name:
                new_name = st.text_input("اسم المجموعة", key="add_category_name")
            with col_code:
                new_code = generate_category_code()
                st.markdown(f'<div class="code-display">الكود: {new_code}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✔️ موافق", key="confirm_add_category", use_container_width=True):
                    if new_name:
                        db.collection("categories").add({"name": new_name, "code": new_code})
                        st.session_state.add_mode = False
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.warning("⚠️ يرجى إدخال اسم المجموعة")
            with col2:
                if st.button("❌ إلغاء", key="cancel_add_category", use_container_width=True):
                    st.session_state.add_mode = False
                    st.rerun()
        st.markdown("---")

    # =========================================
    # 📁 عرض المجموعات
    # =========================================
    for c in categories:
        # زر المجموعة
        with st.container():
            st.markdown('<div class="group-btn">', unsafe_allow_html=True)
            if st.button(f"📁 {c['name']}", key=f"group_{c['id']}"):
                st.session_state.open = None if st.session_state.open == c["id"] else c["id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # التفاصيل (تظهر عند فتح المجموعة)
        if st.session_state.open == c["id"]:
            # صف واحد: الكود + الأزرار
            col_code, col_edit, col_del, col_view = st.columns([2, 1, 1, 1])
            with col_code:
                st.markdown(f'<div class="code-display">الكود: {c["code"]}</div>', unsafe_allow_html=True)
            with col_edit:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("✏️ تعديل", key=f"edit_btn_{c['id']}", use_container_width=True):
                    st.session_state.edit_id = c["id"]
                st.markdown('</div>', unsafe_allow_html=True)
            with col_del:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("🗑️ حذف", key=f"del_btn_{c['id']}", use_container_width=True):
                    st.session_state.delete_id = c["id"]
                st.markdown('</div>', unsafe_allow_html=True)
            with col_view:
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("👁️ استعراض", key=f"view_btn_{c['id']}", use_container_width=True):
                    st.session_state.page = "products"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # عرض عدد الأصناف
            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.caption(f"📊 عدد الأصناف: {count}")

            # =========================================
            # ✏️ تعديل inline
            # =========================================
            if st.session_state.edit_id == c["id"]:
                st.markdown("---")
                st.markdown("#### ✏️ تعديل المجموعة")
                new_name = st.text_input("اسم جديد", value=c["name"], key=f"edit_input_{c['id']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔️ حفظ", key=f"save_{c['id']}", use_container_width=True):
                        db.collection("categories").document(c["id"]).update({"name": new_name})
                        st.session_state.edit_id = None
                        st.cache_data.clear()
                        st.rerun()
                with col2:
                    if st.button("❌ إلغاء", key=f"cancel_edit_{c['id']}", use_container_width=True):
                        st.session_state.edit_id = None
                        st.rerun()

            # =========================================
            # 🗑️ حذف inline
            # =========================================
            if st.session_state.delete_id == c["id"]:
                st.markdown("---")
                st.warning(f"⚠️ هل أنت متأكد من حذف '{c['name']}'؟")
                has_products = any(p.get("category_code") == c["code"] for p in products)
                if has_products:
                    st.error("❌ لا يمكن حذف مجموعة فيها أصناف")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔️ نعم، احذف", key=f"confirm_del_{c['id']}", use_container_width=True, disabled=has_products):
                        db.collection("categories").document(c["id"]).delete()
                        st.session_state.delete_id = None
                        st.cache_data.clear()
                        st.rerun()
                with col2:
                    if st.button("❌ إلغاء", key=f"cancel_del_{c['id']}", use_container_width=True):
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
