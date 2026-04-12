import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# ================= Firebase =================
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# ================= Data =================
@st.cache_data
def load_products():
    docs = db.collection("products").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

@st.cache_data
def load_categories():
    docs = db.collection("categories").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def generate_category_code():
    cats = load_categories()
    if not cats:
        return "001"
    max_code = max(int(c["code"]) for c in cats)
    return str(max_code + 1).zfill(3)

def category_has_products(code):
    for p in load_products():
        if p.get("category_code") == code:
            return True
    return False

# ================= Navigation =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= Home =================
if st.session_state.page == "home":

    st.markdown("## 📱 الشاشة الرئيسية")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📦 الأصناف", use_container_width=True):
            st.session_state.page = "products"
            st.rerun()

    with col2:
        if st.button("🗂️ المجموعات", use_container_width=True):
            st.session_state.page = "categories"
            st.rerun()

# ================= Categories =================
elif st.session_state.page == "categories":

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ إدارة المجموعات")

    name = st.text_input("اسم المجموعة")

    if st.button("➕ إضافة مجموعة"):
        if name:
            code = generate_category_code()
            db.collection("categories").add({"name": name, "code": code})
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    categories = load_categories()

    for c in categories:
        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(f"{c['code']} - {c['name']}")

        with col2:
            if st.button("✏️", key=f"edit_cat_{c['id']}"):
                pass

        with col3:
            if st.button("🗑️", key=f"del_cat_{c['id']}"):
                st.session_state.delete_cat = c["id"]

    if st.session_state.get("delete_cat"):
        cat = next((x for x in categories if x["id"] == st.session_state.delete_cat), None)

        if cat:
            st.warning(f"⚠️ حذف المجموعة: {cat['name']} ؟")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("❌ إلغاء"):
                    st.session_state.delete_cat = None
                    st.rerun()

            with col2:
                if st.button("🗑️ تأكيد"):
                    if category_has_products(cat["code"]):
                        st.error("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                    else:
                        db.collection("categories").document(cat["id"]).delete()
                        st.session_state.delete_cat = None
                        st.cache_data.clear()
                        st.rerun()

# ================= Products =================
elif st.session_state.page == "products":

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💊 إدارة الأصناف")

    st.info("🚧 سيتم تطوير هذا القسم في الخطوة القادمة")

st.caption("© نظام إدارة المستودعات")
