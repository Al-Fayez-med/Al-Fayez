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

    /* تنسيق أزرار الإجراءات (تعديل، حذف، استعراض) */
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
        text-align: center;
    }
    
    /* تنسيق حقل الكود غير القابل للتعديل */
    .code-display {
        background-color: #1e3a8a;
        padding: 8px 12px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 14px;
        text-align: center;
    }
    
    /* تنسيق صف الإجراءات */
    .actions-row {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
        flex-wrap: wrap;
    }
    
    .code-item {
        flex: 2;
        min-width: 100px;
    }
    
    .action-item {
        flex: 1;
        min-width: 70px;
        text-align: center;
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
    # ➕ إضافة مجموعة (زر صغير 60x60)
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

            # ===== صف واحد يحتوي على الكود والأزرار =====
            st.markdown(f"""
            <div class="actions-row">
                <div class="code-item">
                    <div class="code-display">الكود: {c['code']}</div>
                </div>
                <div class="action-item">
                    <div class="action-btn" id="edit_btn_{c['id']}"></div>
                    <div class="action-label">تعديل</div>
                </div>
                <div class="action-item">
                    <div class="action-btn" id="del_btn_{c['id']}"></div>
                    <div class="action-label">حذف</div>
                </div>
                <div class="action-item">
                    <div class="action-btn" id="view_btn_{c['id']}"></div>
                    <div class="action-label">استعراض</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # الأزرار الفعلية (مخفية لكنها تعمل)
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("✏️", key=f"edit_btn_{c['id']}", help="تعديل"):
                    st.session_state.edit_id = c["id"]
                    st.rerun()
            with col_btn2:
                if st.button("🗑️", key=f"del_btn_{c['id']}", help="حذف"):
                    st.session_state.delete_id = c["id"]
                    st.rerun()
            with col_btn3:
                if st.button("👁️", key=f"view_btn_{c['id']}", help="استعراض الأصناف"):
                    st.session_state.page = "products"
                    st.rerun()

            # عرض عدد الأصناف
            count = sum(1 for p in products if p.get("category_code") == c["code"])
            st.caption(f"📊 عدد الأصناف: {count}")

            # =========================================
            # ✏️ تعديل inline
            # =========================================
            if st.session_state.edit_id == c["id"]:

                st.markdown("---")
                st.markdown("#### ✏️ تعديل المجموعة")
                
                col_edit_name, col_edit_spacer = st.columns([2, 1])
                
                with col_edit_name:
                    new_name = st.text_input("اسم جديد", value=c["name"], key=f"edit_input_{c['id']}")
                
                st.markdown(f'<div class="code-display">الكود: {c["code"]}</div>', unsafe_allow_html=True)

                colA, colB = st.columns(2)

                with colA:
                    if st.button("✔️ حفظ", key=f"save_{c['id']}", use_container_width=True):
                        db.collection("categories").document(c["id"]).update({
                            "name": new_name
                        })
                        st.session_state.edit_id = None
                        st.cache_data.clear()
                        st.rerun()

                with colB:
                    if st.button("❌ إلغاء", key=f"cancel_edit_{c['id']}", use_container_width=True):
                        st.session_state.edit_id = None
                        st.rerun()

            # =========================================
            # 🗑️ حذف inline
            # =========================================
            if st.session_state.delete_id == c["id"]:

                st.markdown("---")
                st.warning(f"⚠️ هل أنت متأكد من حذف مجموعة '{c['name']}'؟")

                has_products = any(p.get("category_code") == c["code"] for p in products)

                if has_products:
                    st.error("❌ لا يمكن حذف مجموعة تحتوي على أصناف. قم بحذف الأصناف أولاً.")

                colA, colB = st.columns(2)

                with colA:
                    if st.button("✔️ نعم، احذف", key=f"confirm_del_{c['id']}", use_container_width=True, disabled=has_products):
                        db.collection("categories").document(c["id"]).delete()
                        st.session_state.delete_id = None
                        st.cache_data.clear()
                        st.rerun()

                with colB:
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
