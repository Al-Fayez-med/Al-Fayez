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
if "open_popover" not in st.session_state:
    st.session_state.open_popover = None

# ==================== CSS بسيط ====================
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 1rem;
    margin-bottom: 1rem;
}
.category-name {
    font-size: 16px;
    font-weight: bold;
    color: white;
    background-color: #3b82f6;
    border: none;
    border-radius: 12px;
    padding: 8px 15px;
    margin-bottom: 5px;
    width: 100%;
    text-align: right;
    cursor: pointer;
}
.code-text {
    font-size: 11px;
    color: #6b7280;
    text-align: center;
    padding: 5px;
    background-color: #f3f4f6;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================== الواجهة ====================
st.markdown('<div class="main-header"><h2 style="color: white; margin: 0;">🗂️ المجموعات</h2></div>', unsafe_allow_html=True)

# زر إضافة مجموعة
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat_btn"):
        st.session_state.show_modal = True

# نافذة إضافة مجموعة (st.popover)
if st.session_state.show_modal:
    with st.popover("➕ إضافة مجموعة جديدة", use_container_width=True):
        name = st.text_input("اسم المجموعة", key="add_cat_name")
        code = generate_code()
        st.text_input("الكود", value=code, disabled=True, key="add_cat_code")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ", key="save_cat_btn"):
                if name:
                    db.collection("categories").add({"name": name, "code": code})
                    st.session_state.show_modal = False
                    st.rerun()
                else:
                    st.error("الرجاء إدخال اسم المجموعة")
        with col2:
            if st.button("❌ إلغاء", key="cancel_cat_btn"):
                st.session_state.show_modal = False
                st.rerun()

# عرض المجموعات
categories = load_categories()
for idx, cat in enumerate(categories):
    cat_id = cat['id']
    unique_key = f"cat_{idx}_{cat_id}"
    
    # زر اسم المجموعة (بدون أيقونة) - نستخدم st.popover
    with st.popover(f"{cat['name']}", use_container_width=True):
        # عرض الكود (نص باهت)
        st.markdown(f'<div class="code-text">📋 الكود: {cat["code"]}</div>', unsafe_allow_html=True)
        
        # أزرار الإجراءات
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ تعديل", key=f"edit_{unique_key}", use_container_width=True):
                # فتح نافذة تعديل منبثقة
                with st.popover("✏️ تعديل المجموعة"):
                    new_name = st.text_input("اسم جديد", value=cat['name'], key=f"edit_input_{unique_key}")
                    if st.button("💾 حفظ التعديل", key=f"save_edit_{unique_key}"):
                        db.collection("categories").document(cat_id).update({"name": new_name})
                        st.rerun()
        
        with col2:
            if st.button("🗑️ حذف", key=f"del_{unique_key}", use_container_width=True):
                # نافذة تأكيد الحذف العائمة
                with st.popover("🗑️ تأكيد الحذف"):
                    st.warning(f"⚠️ هل تريد حذف '{cat['name']}' نهائياً؟")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ نعم", key=f"confirm_del_{unique_key}"):
                            db.collection("categories").document(cat_id).delete()
                            st.rerun()
                    with col2:
                        if st.button("❌ لا", key=f"cancel_del_{unique_key}"):
                            st.rerun()
        
        with col3:
            if st.button("👁️ عرض", key=f"view_{unique_key}", use_container_width=True):
                # نافذة عرض معلومات
                with st.popover("👁️ عرض المجموعة"):
                    st.markdown(f"**الاسم:** {cat['name']}")
                    st.markdown(f"**الكود:** {cat['code']}")
                    if st.button("🔙 إغلاق", key=f"close_view_{unique_key}"):
                        st.rerun()
