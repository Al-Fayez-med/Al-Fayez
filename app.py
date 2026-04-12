import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# =========================================
# 🔥 FIREBASE
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
# 📦 DATA
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
# 🎨 STYLE
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
# 🔁 NAVIGATION
# =========================================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================================
# 🧱 HEADER
# =========================================
def show_header():
    st.markdown('<div class="header">🏪 اسم المستودع</div>', unsafe_allow_html=True)

# =========================================
# 🧩 ICON
# =========================================
def icon(label, emoji, page):
    if st.button(emoji, key=page):
        st.session_state.page = page
        st.rerun()
    st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)

# =========================================
# 🏠 HOME
# =========================================
def home_page():
    show_header()
    icon("الأصناف", "📦", "products")
    icon("المجموعات", "🗂️", "categories")

# =========================================
# 🗂️ CATEGORIES (🔥 الجديد)
# =========================================
def categories_section():

    # ===== رجوع =====
    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ المجموعات")

    categories = load_categories()
    products = load_products()

    if "open" not in st.session_state:
        st.session_state.open = None

    if "add_mode" not in st.session_state:
        st.session_state.add_mode = False

    if "edit" not in st.session_state:
        st.session_state.edit = None

    if "delete" not in st.session_state:
        st.session_state.delete = None

    # =========================================
    # ➕ زر الإضافة (فوق)
    # =========================================
    if st.button("➕ إضافة مجموعة"):
        st.session_state.add_mode = True

    st.markdown("---")

    # =========================================
    # 📁 عرض المجموعات
    # =========================================
    for c in categories:

        if st.button(f"📁 {c['name']}", key=c["id"]):

            if st.session_state.open == c["id"]:
                st.session_state.open = None
            else:
                st.session_state.open = c["id"]

            st.rerun()

        if st.session_state.open == c["id"]:

            st.markdown(
                f"<span style='color:gray'>الكود: {c['code']}</span>",
                unsafe_allow_html=True
            )

            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.write(f"عدد الأصناف: {count}")

            # ===== أزرار =====
            col1, col2, col3 = st.columns(3)

            with col1:
                btn = st.button("✏️", key="e"+c["id"])
                st.write("تعديل")
                if btn:
                    st.session_state.edit = c["id"]

            with col2:
                btn = st.button("🗑️", key="d"+c["id"])
                st.write("حذف")
                if btn:
                    st.session_state.delete = c["id"]

            with col3:
                btn = st.button("👁️", key="v"+c["id"])
                st.write("استعراض")
                if btn:
                    st.session_state.page = "products"
                    st.rerun()

            st.markdown("---")

    # =========================================
    # ➕ نافذة إضافة (Popup)
    # =========================================
    if st.session_state.add_mode:

        with st.modal("➕ إضافة مجموعة"):

            name = st.text_input("اسم المجموعة")
            code = generate_category_code()

            st.markdown(
                f"<span style='color:gray'>الكود: {code}</span>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            if col1.button("موافق"):
                if name:
                    db.collection("categories").add({
                        "name": name,
                        "code": code
                    })
                    st.session_state.add_mode = False
                    st.cache_data.clear()
                    st.rerun()

            if col2.button("إلغاء"):
                st.session_state.add_mode = False
                st.rerun()

    # =========================================
    # ✏️ تعديل (Popup)
    # =========================================
    if st.session_state.edit:

        cat = next((x for x in categories if x["id"] == st.session_state.edit), None)

        if cat:
            with st.modal("✏️ تعديل مجموعة"):

                new_name = st.text_input("اسم المجموعة", value=cat["name"])

                st.markdown(
                    f"<span style='color:gray'>الكود: {cat['code']}</span>",
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)

                if col1.button("موافق"):
                    db.collection("categories").document(cat["id"]).update({
                        "name": new_name
                    })
                    st.session_state.edit = None
                    st.cache_data.clear()
                    st.rerun()

                if col2.button("إلغاء"):
                    st.session_state.edit = None
                    st.rerun()

    # =========================================
    # 🗑️ حذف (Popup)
    # =========================================
    if st.session_state.delete:

        cat = next((x for x in categories if x["id"] == st.session_state.delete), None)

        if cat:
            with st.modal("⚠️ تأكيد الحذف"):

                st.warning(f"حذف {cat['name']}؟")

                has_products = any(p.get("category_code") == cat["code"] for p in products)

                if has_products:
                    st.error("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                else:
                    col1, col2 = st.columns(2)

                    if col1.button("إلغاء"):
                        st.session_state.delete = None
                        st.rerun()

                    if col2.button("تأكيد"):
                        db.collection("categories").document(cat["id"]).delete()
                        st.session_state.delete = None
                        st.cache_data.clear()
                        st.rerun()
    
# =========================================
# 💊 PRODUCTS
# =========================================
def products_section():

    if st.button("⬅️"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💊 الأصناف")

    products = load_products()

    for p in products:
        st.write(p["name"])

# =========================================
# 🚀 ROUTER
# =========================================
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "categories":
    categories_section()

elif st.session_state.page == "products":
    products_section()
