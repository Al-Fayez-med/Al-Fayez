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

# ==================== تهيئة session_state ====================
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None
if "delete_id" not in st.session_state:
    st.session_state.delete_id = None
if "view_id" not in st.session_state:
    st.session_state.view_id = None
if "open_category" not in st.session_state:
    st.session_state.open_category = None

# ==================== CSS ====================
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 1rem;
    margin-bottom: 2rem;
}
.category-row {
    margin-bottom: 8px;
}
.category-header {
    width: 100%;
}
.category-header button {
    width: 100% !important;
    background-color: #3b82f6 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 15px !important;
    text-align: right !important;
    font-size: 16px !important;
    font-weight: bold !important;
    display: flex !important;
    justify-content: space-between !important;
}
.code-small {
    font-size: 10px;
    color: #bfdbfe;
}
.dropdown-box {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 12px;
    margin-top: 4px;
    margin-bottom: 8px;
    border-right: 4px solid #3b82f6;
}
.action-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-top: 8px;
}
.action-buttons button {
    background-color: #1e3a8a !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    flex: 1 !important;
}
.action-buttons button:first-child {
    background-color: #dc2626 !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== الواجهة ====================
st.markdown('<div class="main-header"><h1 class="text-4xl font-bold text-white">🗂️ المجموعات</h1></div>', unsafe_allow_html=True)

# زر إضافة مجموعة
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat"):
        st.session_state.show_modal = True

# نافذة إضافة مجموعة
if st.session_state.show_modal:
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
for cat in categories:
    cat_id = cat['id']
    
    # زر المجموعة الرئيسي
    with st.container():
        col1, col2 = st.columns([8, 1])
        with col1:
            if st.button(f"📁 {cat['name']}", key=f"cat_{cat_id}", use_container_width=True):
                if st.session_state.open_category == cat_id:
                    st.session_state.open_category = None
                else:
                    st.session_state.open_category = cat_id
                st.rerun()
        with col2:
            st.caption(cat['code'])
    
    # القائمة المنسدلة
    if st.session_state.open_category == cat_id:
        with st.container():
            st.markdown('<div class="dropdown-box">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ تعديل", key=f"edit_{cat_id}", use_container_width=True):
                    st.session_state.edit_id = cat_id
                    st.rerun()
            with col2:
                if st.button("🗑️ حذف", key=f"del_{cat_id}", use_container_width=True):
                    st.session_state.delete_id = cat_id
                    st.rerun()
            with col3:
                if st.button("👁️ عرض", key=f"view_{cat_id}", use_container_width=True):
                    st.session_state.view_id = cat_id
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # نافذة التعديل
    if st.session_state.edit_id == cat_id:
        new_name = st.text_input("اسم جديد", value=cat['name'], key=f"edit_input_{cat_id}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ", key=f"save_edit_{cat_id}"):
                db.collection("categories").document(cat_id).update({"name": new_name})
                st.session_state.edit_id = None
                st.rerun()
        with col2:
            if st.button("❌ إلغاء", key=f"cancel_edit_{cat_id}"):
                st.session_state.edit_id = None
                st.rerun()
    
    # نافذة الحذف
    if st.session_state.delete_id == cat_id:
        st.warning(f"⚠️ هل تريد حذف '{cat['name']}'؟")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ نعم", key=f"confirm_del_{cat_id}"):
                db.collection("categories").document(cat_id).delete()
                st.session_state.delete_id = None
                st.rerun()
        with col2:
            if st.button("❌ لا", key=f"cancel_del_{cat_id}"):
                st.session_state.delete_id = None
                st.rerun()
    
    # نافذة العرض
    if st.session_state.view_id == cat_id:
        st.markdown(f"""
        <div style="background-color: #f3f4f6; border-radius: 8px; padding: 12px; margin-top: 8px;">
            <p><strong>📋 تفاصيل المجموعة</strong></p>
            <p>الاسم: {cat['name']}</p>
            <p>الكود: {cat['code']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔙 إغلاق", key=f"close_view_{cat_id}"):
            st.session_state.view_id = None
            st.rerun()
    
    st.divider()
