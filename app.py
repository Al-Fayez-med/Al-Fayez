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

# ==================== معالجة الإجراءات ====================
action = st.query_params.get("action", None)
cat_id = st.query_params.get("id", None)

if action == "edit" and cat_id:
    st.session_state.edit_id = cat_id
    # مسح parameters بعد القراءة
    st.query_params.clear()

if action == "delete" and cat_id:
    st.session_state.delete_id = cat_id
    st.query_params.clear()

if action == "view" and cat_id:
    st.session_state.view_cat = cat_id
    st.query_params.clear()

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
    background-color: white;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}
.category-info {
    flex: 2;
    min-width: 150px;
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
    gap: 8px;
    flex-wrap: wrap;
}
.action-btn {
    background-color: #1e3a8a;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
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

# حالة النافذة المنبثقة
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None

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
    # بناء روابط الأزرار
    edit_link = f"?action=edit&id={cat['id']}"
    delete_link = f"?action=delete&id={cat['id']}"
    view_link = f"?action=view&id={cat['id']}"
    
    st.markdown(f"""
    <div class="category-card">
        <div class="category-info">
            <div class="category-name">{cat['name']}</div>
            <div class="category-code">الكود: {cat['code']}</div>
        </div>
        <div class="actions-group">
            <a href="{edit_link}" class="action-btn" target="_self">✏️ تعديل</a>
            <a href="{delete_link}" class="action-btn delete-btn" target="_self">🗑️ حذف</a>
            <a href="{view_link}" class="action-btn" target="_self">👁️ عرض</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== معالجة التعديل ====================
if st.session_state.edit_id:
    cat_to_edit = next((c for c in categories if c["id"] == st.session_state.edit_id), None)
    if cat_to_edit:
        st.markdown("---")
        st.markdown("### ✏️ تعديل المجموعة")
        new_name = st.text_input("اسم جديد", value=cat_to_edit["name"], key="edit_input")
        if st.button("💾 حفظ التعديل", key="save_edit"):
            db.collection("categories").document(cat_to_edit["id"]).update({"name": new_name})
            st.session_state.edit_id = None
            st.rerun()
        if st.button("❌ إلغاء", key="cancel_edit"):
            st.session_state.edit_id = None
            st.rerun()

# ==================== معالجة الحذف ====================
if st.session_state.delete_id:
    cat_to_delete = next((c for c in categories if c["id"] == st.session_state.delete_id), None)
    if cat_to_delete:
        st.markdown("---")
        st.warning(f"⚠️ هل تريد حذف '{cat_to_delete['name']}' نهائياً؟")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ نعم، احذف", key="confirm_delete"):
                db.collection("categories").document(cat_to_delete["id"]).delete()
                st.session_state.delete_id = None
                st.rerun()
        with col2:
            if st.button("❌ إلغاء", key="cancel_delete"):
                st.session_state.delete_id = None
                st.rerun()

# ==================== معالجة العرض ====================
if st.session_state.get("view_cat"):
    cat_to_view = next((c for c in categories if c["id"] == st.session_state.view_cat), None)
    if cat_to_view:
        st.markdown("---")
        st.markdown(f"### 👁️ عرض المجموعة: {cat_to_view['name']}")
        st.write(f"**الاسم:** {cat_to_view['name']}")
        st.write(f"**الكود:** {cat_to_view['code']}")
        if st.button("🔙 رجوع"):
            st.session_state.view_cat = None
            st.rerun()
