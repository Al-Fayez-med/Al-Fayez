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

# ==================== دوال الأزرار ====================
def handle_edit(cat_id):
    st.session_state.edit_id = cat_id
    st.session_state.delete_id = None
    st.session_state.view_id = None

def handle_delete(cat_id):
    st.session_state.delete_id = cat_id
    st.session_state.edit_id = None
    st.session_state.view_id = None

def handle_view(cat_id):
    st.session_state.view_id = cat_id
    st.session_state.edit_id = None
    st.session_state.delete_id = None

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
.category-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: white;
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    flex-wrap: wrap;
}
.category-info {
    flex: 2;
    text-align: right;
}
.category-name {
    font-size: 16px;
    font-weight: bold;
    color: #1f2937;
}
.category-code {
    font-size: 10px;
    color: #6b7280;
}
.actions-group {
    display: flex;
    gap: 6px;
    flex-wrap: nowrap;
    justify-content: flex-end;
}
.action-btn {
    background-color: #1e3a8a;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    cursor: pointer;
    min-width: 55px;
    text-align: center;
}
.action-btn:hover {
    background-color: #2563eb;
}
.delete-btn {
    background-color: #dc2626;
}
.delete-btn:hover {
    background-color: #b91c1c;
}
@media (max-width: 600px) {
    .category-card {
        flex-direction: column;
        align-items: stretch;
    }
    .category-info {
        text-align: center;
        margin-bottom: 8px;
    }
    .actions-group {
        justify-content: center;
    }
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

# النافذة المنبثقة للإضافة
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
    # عرض بطاقة المجموعة
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="category-info">
                <div class="category-name">{cat['name']}</div>
                <div class="category-code">الكود: {cat['code']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✏️ تعديل", key=f"edit_{cat['id']}", use_container_width=True):
                handle_edit(cat['id'])
                st.rerun()
        
        with col3:
            if st.button("🗑️ حذف", key=f"del_{cat['id']}", use_container_width=True):
                handle_delete(cat['id'])
                st.rerun()
        
        # زر العرض في صف منفصل على الجوال
        if st.button("👁️ عرض", key=f"view_{cat['id']}", use_container_width=True):
            handle_view(cat['id'])
            st.rerun()
    
    # تعديل
    if st.session_state.edit_id == cat['id']:
        new_name = st.text_input("اسم جديد", value=cat['name'], key=f"edit_input_{cat['id']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ", key=f"save_edit_{cat['id']}"):
                db.collection("categories").document(cat['id']).update({"name": new_name})
                st.session_state.edit_id = None
                st.rerun()
        with col2:
            if st.button("❌ إلغاء", key=f"cancel_edit_{cat['id']}"):
                st.session_state.edit_id = None
                st.rerun()
    
    # حذف
    if st.session_state.delete_id == cat['id']:
        st.warning(f"⚠️ هل تريد حذف '{cat['name']}'؟")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ نعم", key=f"confirm_del_{cat['id']}"):
                db.collection("categories").document(cat['id']).delete()
                st.session_state.delete_id = None
                st.rerun()
        with col2:
            if st.button("❌ لا", key=f"cancel_del_{cat['id']}"):
                st.session_state.delete_id = None
                st.rerun()
    
    # عرض
    if st.session_state.view_id == cat['id']:
        st.markdown(f"""
        <div style="background-color: #f3f4f6; border-radius: 8px; padding: 12px; margin-top: 8px;">
            <p><strong>📋 تفاصيل المجموعة</strong></p>
            <p>الاسم: {cat['name']}</p>
            <p>الكود: {cat['code']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔙 إغلاق", key=f"close_view_{cat['id']}"):
            st.session_state.view_id = None
            st.rerun()
    
    st.divider()
