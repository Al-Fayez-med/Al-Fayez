import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

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

# ==================== واجهة المجموعات ====================
st.title("🗂️ المجموعات")

# أزرار التحكم
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat"):
        st.session_state.show_add = True

# إضافة مجموعة
if st.session_state.get("show_add", False):
    with st.form(key="add_form"):
        name = st.text_input("اسم المجموعة")
        code = generate_code()
        st.text_input("الكود", value=code, disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("✔️ حفظ"):
                if name:
                    db.collection("categories").add({"name": name, "code": code})
                    st.session_state.show_add = False
                    st.rerun()
        with col2:
            if st.form_submit_button("❌ إلغاء"):
                st.session_state.show_add = False
                st.rerun()

# عرض المجموعات
categories = load_categories()
for cat in categories:
    with st.container():
        st.markdown(f"**📁 {cat['name']}**")
        st.caption(f"الكود: {cat['code']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ تعديل", key=f"edit_{cat['id']}"):
                st.session_state.edit_id = cat['id']
        with col2:
            if st.button("🗑️ حذف", key=f"del_{cat['id']}"):
                st.session_state.delete_id = cat['id']
        with col3:
            if st.button("👁️ عرض", key=f"view_{cat['id']}"):
                st.info("سيتم الانتقال إلى صفحة الأصناف")
        
        # تعديل
        if st.session_state.get("edit_id") == cat['id']:
            new_name = st.text_input("اسم جديد", value=cat['name'], key=f"new_name_{cat['id']}")
            if st.button("💾 حفظ التعديل", key=f"save_{cat['id']}"):
                db.collection("categories").document(cat['id']).update({"name": new_name})
                st.session_state.edit_id = None
                st.rerun()
        
        # حذف
        if st.session_state.get("delete_id") == cat['id']:
            st.warning(f"هل تريد حذف {cat['name']}؟")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("نعم", key=f"yes_{cat['id']}"):
                    db.collection("categories").document(cat['id']).delete()
                    st.session_state.delete_id = None
                    st.rerun()
            with col2:
                if st.button("لا", key=f"no_{cat['id']}"):
                    st.session_state.delete_id = None
                    st.rerun()
        
        st.divider()
