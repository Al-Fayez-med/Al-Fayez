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
    
    /* تنسيق زر المجموعة */
    .group-btn button {
        width: 100% !important;
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 5px 15px !important;
        text-align: right !important;
        font-size: 14px !important;
        cursor: pointer !important;
        height: 30px !important;
    }
    
    .group-btn button:hover {
        background-color: #2563eb !important;
    }
    
    /* تنسيق حقل الكود */
    .code-display {
        background-color: #1e3a8a;
        padding: 6px 12px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 14px;
        text-align: center;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* تنسيق أزرار الإجراءات */
    .action-btn {
        background-color: #1e40af;
        color: white;
        border: 1px solid #3b82f6;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 12px;
        cursor: pointer;
        width: 100%;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .action-btn:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* تنسيق الصفوف */
    .actions-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .code-item {
        flex: 2;
    }
    
    .action-item {
        flex: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== رجوع =====
    col_back, col_spacer = st.columns([1, 10])
    with col_back:
        if st.button("⬅️", key="back_to_home"):
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
    # ➕ إضافة مجموعة
    # =========================================
    col_add1, col_add2 = st.columns([1, 10])
    with col_add1:
        if st.button("➕", key="open_add_category"):
            st.session_state.add_mode = True

    # ===== نافذة إضافة مجموعة =====
    if st.session_state.add_mode:

        st.markdown("---")
        st.markdown("### ➕ إضافة مجموعة جديدة")
        
        col_name, col_code = st.columns([2, 1])
        
        with col_name:
            new_category_name = st.text_input("اسم المجموعة", key="add_category_name", placeholder="أدخل اسم المجموعة")
        
        with col_code:
            new_category_code = generate_category_code()
            st.markdown(f'<div class="code-display">الكود: {new_category_code}</div>', unsafe_allow_html=True)
        
        col_ok, col_cancel = st.columns(2)
        
        with col_ok:
            if st.button("✔️ موافق", key="confirm_add_category", use_container_width=True):
                if new_category_name:
                    db.collection("categories").add({
                        "name": new_category_name,
                        "code": new_category_code
                    })
                    st.session_state.add_mode = False
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.warning("⚠️ يرجى إدخال اسم المجموعة")
        
        with col_cancel:
            if st.button("❌ إلغاء", key="cancel_add_category", use_container_width=True):
                st.session_state.add_mode = False
                st.rerun()
        
        st.markdown("---")

    # =========================================
    # 📁 عرض المجموعات
    # =========================================
    for c in categories:

        # ===== زر المجموعة (مع div.group-btn) =====
        with st.container():
            st.markdown('<div class="group-btn">', unsafe_allow_html=True)
            if st.button(f"{c['name']}", key=f"group_{c['id']}"):
                if st.session_state.open == c["id"]:
                    st.session_state.open = None
                else:
                    st.session_state.open = c["id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ===== التفاصيل =====
        if st.session_state.open == c["id"]:

            # ===== صف واحد يحتوي على الكود والأزرار =====
            st.markdown(f"""
            <div class="actions-row">
                <div class="code-item">
                    <div class="code-display">الكود: {c['code']}</div>
                </div>
                <div class="action-item">
                    <button class="action-btn" onclick="alert('تعديل المجموعة {c["name"]}')">✏️ تعديل</button>
                </div>
                <div class="action-item">
                    <button class="action-btn" onclick="alert('حذف المجموعة {c["name"]}')">🗑️ حذف</button>
                </div>
                <div class="action-item">
                    <button class="action-btn" onclick="alert('عرض المجموعة {c["name"]}')">👁️ عرض</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # عرض عدد الأصناف
            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.caption(f"📊 عدد الأصناف: {count}")

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
