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

# ==================== CSS ====================
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');

.main-header {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 1rem;
    margin-bottom: 2rem;
}

/* تنسيق زر المجموعة */
.category-btn {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 5px 15px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    width: auto !important;
    min-width: 150px !important;
    text-align: center !important;
}

/* تنسيق أزرار الإجراءات */
.action-btn {
    background-color: #1e3a8a !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 5px 12px !important;
    font-size: 12px !important;
    height: 30px !important;
    width: auto !important;
    min-width: 60px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    border: none !important;
    cursor: pointer !important;
}

.action-btn:hover {
    background-color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== الواجهة ====================
st.markdown('<div class="main-header"><h1 class="text-4xl font-bold text-white">🗂️ المجموعات</h1></div>', unsafe_allow_html=True)

# حالة النافذة المنبثقة
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

# زر إضافة مجموعة
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat"):
        st.session_state.show_modal = True

# النافذة المنبثقة
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
        # زر المجموعة (أزرق)
        st.markdown(f"""
        <button class="category-btn" onclick="alert('تم فتح {cat['name']}')">
            📁 {cat['name']}
        </button>
        <div style="margin-top: 10px; margin-bottom: 10px;">
            <span style="background-color: #1e3a8a; color: #94a3b8; padding: 5px 12px; border-radius: 8px; font-size: 12px;">الكود: {cat['code']}</span>
        </div>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <button class="action-btn" onclick="alert('تعديل {cat['name']}')">✏️ تعديل</button>
            <button class="action-btn" onclick="alert('حذف {cat['name']}')">🗑️ حذف</button>
            <button class="action-btn" onclick="alert('عرض {cat['name']}')">👁️ عرض</button>
        </div>
        """, unsafe_allow_html=True)
