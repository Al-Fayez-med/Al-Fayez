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

    # ===== رجوع =====
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ المجموعات")

    categories = load_categories()
    products = load_products()

    # ===== حالات =====
    if "open" not in st.session_state:
        st.session_state.open = None

    if "add_mode" not in st.session_state:
        st.session_state.add_mode = False

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # =========================================
    # ➕ إضافة مجموعة
    # =========================================
    if st.button("➕ إضافة مجموعة"):
        st.session_state.add_mode = True

    # ===== نموذج الإضافة =====
    if st.session_state.add_mode:

        name = st.text_input("اسم المجموعة")
        code = generate_category_code()

        st.markdown(f"<span style='color:gray'>الكود: {code}</span>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,1])

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
    # 📁 عرض المجموعات
    # =========================================
    for c in categories:

        # ===== زر المجموعة (أفقي) =====
        if st.button(f"📁 {c['name']}", key=c["id"]):

            if st.session_state.open == c["id"]:
                st.session_state.open = None
            else:
                st.session_state.open = c["id"]

            st.rerun()

        # =========================================
        # 📂 تفاصيل المجموعة
        # =========================================
        if st.session_state.open == c["id"]:

            st.markdown(f"<span style='color:gray'>الكود: {c['code']}</span>", unsafe_allow_html=True)

            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.write(f"عدد الأصناف: {count}")

            # ===== أزرار العمليات =====
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("✏️", key="e"+c["id"]):
                    st.session_state.edit_id = c["id"]
                st.markdown("<small style='opacity:0.5'>تعديل</small>", unsafe_allow_html=True)

            with col2:
                if st.button("🗑️", key="d"+c["id"]):
                    st.session_state.delete_id = c["id"]
                st.markdown("<small style='opacity:0.5'>حذف</small>", unsafe_allow_html=True)

            with col3:
                if st.button("👁️", key="v"+c["id"]):
                    st.session_state.page = "products"
                    st.rerun()
                st.markdown("<small style='opacity:0.5'>استعراض</small>", unsafe_allow_html=True)

            # =========================================
            # ✏️ تعديل
            # =========================================
            if st.session_state.edit_id == c["id"]:

                new_name = st.text_input("تعديل الاسم", value=c["name"], key="edit_name")

                st.markdown(f"<span style='color:gray'>الكود: {c['code']}</span>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✔️", key="save"+c["id"]):
                        db.collection("categories").document(c["id"]).update({
                            "name": new_name
                        })
                        st.session_state.edit_id = None
                        st.cache_data.clear()
                        st.rerun()

                with col2:
                    if st.button("❌", key="cancel_edit"+c["id"]):
                        st.session_state.edit_id = None
                        st.rerun()

            # =========================================
            # 🗑️ حذف
            # =========================================
            if st.session_state.delete_id == c["id"]:

                st.warning(f"هل أنت متأكد من حذف {c['name']} ؟")

                has_products = any(p.get("category_code") == c["code"] for p in products)

                if has_products:
                    st.error("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                else:
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("✔️", key="confirm"+c["id"]):
                            db.collection("categories").document(c["id"]).delete()
                            st.session_state.delete_id = None
                            st.cache_data.clear()
                            st.rerun()

                    with col2:
                        if st.button("❌", key="cancel_del"+c["id"]):
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
