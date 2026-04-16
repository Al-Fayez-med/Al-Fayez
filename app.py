import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ==================== إعداد Firebase ====================
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# ==================== دوال مساعدة ====================
def load_categories():
    docs = db.collection("categories").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def generate_code():
    cats = load_categories()
    if not cats:
        return "001"
    max_code = max(int(c["code"]) for c in cats)
    return str(max_code + 1).zfill(3)

# ==================== CSS لإزالة المسافات ====================
st.markdown("""
<style>
/* إزالة كل المسافات الخارجية */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}
.element-container {
    margin-bottom: 0rem !important;
}
/* تقليل المسافات بين الأزرار */
.stButton > button {
    padding: 0px 4px !important;
    margin: 0px !important;
    height: 24px !important;
    font-size: 12px !important;
    background-color: #1e3a8a !important;
    color: white !important;
    border-radius: 4px !important;
}
/* إزالة المسافات بين الأسطر */
hr {
    margin: 2px 0px !important;
}
/* تقليل المسافات في النص */
.stMarkdown {
    margin-bottom: 0px !important;
}
/* تنسيق اسم المجموعة */
.category-name {
    font-size: 13px !important;
    font-weight: bold !important;
    margin-bottom: 0px !important;
    padding: 0px !important;
}
.category-code {
    font-size: 9px !important;
    color: #6b7280 !important;
    margin-bottom: 0px !important;
    padding: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== الواجهة ====================
st.markdown("### 🗂️ المجموعات")

# زر إضافة مجموعة
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat"):
        st.session_state.show_modal = True

# نافذة إضافة مجموعة
if st.session_state.get("show_modal", False):
    with st.form(key="add_category_form"):
        st.markdown("### ➕ إضافة مجموعة جديدة")
        name = st.text_input("اسم المجموعة")
        code = generate_code()
        st.text_input("الكود", value=code, disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 حفظ"):
                if name:
                    db.collection("categories").add({"name": name, "code": code})
                    st.session_state.show_modal = False
                    st.rerun()
                else:
                    st.error("الرجاء إدخال اسم المجموعة")
        with col2:
            if st.form_submit_button("❌ إلغاء"):
                st.session_state.show_modal = False
                st.rerun()

# عرض المجموعات
categories = load_categories()
for idx, cat in enumerate(categories):
    unique_key = f"cat_{idx}_{cat['id']}"
    
    # صف واحد: اسم المجموعة + الكود + الأيقونات
    col_name, col_code, col_edit, col_del, col_view = st.columns([3, 1.5, 0.8, 0.8, 0.8])
    
    with col_name:
        st.markdown(f'<div class="category-name">{cat["name"]}</div>', unsafe_allow_html=True)
    
    with col_code:
        st.markdown(f'<div class="category-code">{cat["code"]}</div>', unsafe_allow_html=True)
    
    with col_edit:
        if st.button("✏️", key=f"edit_{unique_key}", help="تعديل"):
            st.session_state.edit_id = cat['id']
    
    with col_del:
        if st.button("🗑️", key=f"del_{unique_key}", help="حذف"):
            st.session_state.delete_id = cat['id']
    
    with col_view:
        if st.button("👁️", key=f"view_{unique_key}", help="عرض"):
            st.session_state.view_id = cat['id']
    
    # نافذة تعديل (تظهر أسفل الصف)
    if st.session_state.get("edit_id") == cat['id']:
        new_name = st.text_input("اسم جديد", value=cat['name'], key=f"edit_input_{unique_key}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ", key=f"save_edit_{unique_key}"):
                db.collection("categories").document(cat['id']).update({"name": new_name})
                st.session_state.edit_id = None
                st.rerun()
        with col2:
            if st.button("❌ إلغاء", key=f"cancel_edit_{unique_key}"):
                st.session_state.edit_id = None
                st.rerun()
    
    # نافذة حذف (تظهر أسفل الصف)
    if st.session_state.get("delete_id") == cat['id']:
        st.warning(f"⚠️ حذف '{cat['name']}'؟")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ نعم", key=f"confirm_del_{unique_key}"):
                db.collection("categories").document(cat['id']).delete()
                st.session_state.delete_id = None
                st.rerun()
        with col2:
            if st.button("❌ لا", key=f"cancel_del_{unique_key}"):
                st.session_state.delete_id = None
                st.rerun()
    
    # نافذة عرض (تظهر أسفل الصف)
    if st.session_state.get("view_id") == cat['id']:
        st.markdown(f"**الاسم:** {cat['name']}  |  **الكود:** {cat['code']}")
        if st.button("🔙 إغلاق", key=f"close_view_{unique_key}"):
            st.session_state.view_id = None
            st.rerun()
    
    # فاصل رفيع جداً
    st.markdown("<hr>", unsafe_allow_html=True)
