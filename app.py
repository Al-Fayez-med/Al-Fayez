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
if "open_action" not in st.session_state:
    st.session_state.open_action = None

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
    flex-wrap: wrap;
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
    # عرض بطاقة المجموعة باستخدام HTML
    st.markdown(f"""
    <div class="category-card">
        <div class="category-info">
            <div class="category-name">{cat['name']}</div>
            <div class="category-code">الكود: {cat['code']}</div>
        </div>
        <div class="actions-group">
            <button class="action-btn" onclick="alert('تعديل {cat['name']}')">✏️ تعديل</button>
            <button class="action-btn delete-btn" onclick="alert('حذف {cat['name']}')">🗑️ حذف</button>
            <button class="action-btn" onclick="alert('عرض {cat['name']}')">👁️ عرض</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
