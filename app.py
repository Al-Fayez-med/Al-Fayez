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
if "delete_id" not in st.session_state:
    st.session_state.delete_id = None

# ==================== الواجهة ====================
st.title("🗂️ المجموعات")

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
    with st.container():
        col1, col2, col3 = st.columns([6, 1, 1])
        
        with col1:
            st.write(f"**{cat['name']}**")
            st.caption(f"الكود: {cat['code']}")
        
        with col2:
            # زر تعديل (سيضاف لاحقاً)
            st.button("✏️", key=f"edit_{cat['id']}")
        
        with col3:
            # زر حذف
            if st.button("🗑️", key=f"del_{cat['id']}"):
                st.session_state.delete_id = cat['id']
        
        # نافذة تأكيد الحذف (تظهر أسفل الزر مباشرة)
        if st.session_state.delete_id == cat['id']:
            st.warning(f"⚠️ هل تريد حذف '{cat['name']}' نهائياً؟")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ نعم", key=f"confirm_{cat['id']}"):
                    db.collection("categories").document(cat['id']).delete()
                    st.session_state.delete_id = None
                    st.rerun()
            with col2:
                if st.button("❌ لا", key=f"cancel_{cat['id']}"):
                    st.session_state.delete_id = None
                    st.rerun()
        
        st.divider()
