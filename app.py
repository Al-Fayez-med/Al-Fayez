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
/* زر المجموعة الرئيسي */
.category-btn {
    width: 100%;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 15px;
    text-align: right;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.category-btn:hover {
    background-color: #2563eb;
}
.category-code-small {
    font-size: 10px;
    color: #bfdbfe;
}
/* القائمة المنسدلة */
.dropdown-menu {
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
.action-btn {
    background-color: #1e3a8a;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 13px;
    cursor: pointer;
    min-width: 70px;
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
    cat_id = cat['id']
    
    # زر المجموعة الرئيسي
    if st.button(f"📁 {cat['name']}   <span class='category-code-small'>({cat['code']})</span>", key=f"cat_{cat_id}", use_container_width=True):
        if st.session_state.open_category == cat_id:
            st.session_state.open_category = None
        else:
            st.session_state.open_category = cat_id
        st.rerun()
    
    # القائمة المنسدلة (تظهر إذا كانت هذه المجموعة مفتوحة)
    if st.session_state.open_category == cat_id:
        st.markdown(f"""
        <div class="dropdown-menu">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #475569;">الكود: {cat['code']}</span>
            </div>
            <div class="action-buttons">
                <button class="action-btn" id="edit_{cat_id}">✏️ تعديل</button>
                <button class="action-btn delete-btn" id="delete_{cat_id}">🗑️ حذف</button>
                <button class="action-btn" id="view_{cat_id}">👁️ عرض</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # الأزرار المخفية (لربط HTML بوظائف Streamlit)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("edit", key=f"real_edit_{cat_id}", label_visibility="collapsed")
        with col2:
            st.button("delete", key=f"real_del_{cat_id}", label_visibility="collapsed")
        with col3:
            st.button("view", key=f"real_view_{cat_id}", label_visibility="collapsed")
        
        # ربط الأزرار
        st.markdown(f"""
        <script>
            const editBtn = document.getElementById('edit_{cat_id}');
            if (editBtn) editBtn.onclick = () => {{
                const realBtn = window.parent.document.querySelector('button[data-testid="baseButton-secondary"][key="real_edit_{cat_id}"]');
                if (realBtn) realBtn.click();
            }};
            const deleteBtn = document.getElementById('delete_{cat_id}');
            if (deleteBtn) deleteBtn.onclick = () => {{
                const realBtn = window.parent.document.querySelector('button[data-testid="baseButton-secondary"][key="real_del_{cat_id}"]');
                if (realBtn) realBtn.click();
            }};
            const viewBtn = document.getElementById('view_{cat_id}');
            if (viewBtn) viewBtn.onclick = () => {{
                const realBtn = window.parent.document.querySelector('button[data-testid="baseButton-secondary"][key="real_view_{cat_id}"]');
                if (realBtn) realBtn.click();
            }};
        </script>
        """, unsafe_allow_html=True)
        
        # معالجة الأزرار الفعلية
        if st.session_state.get(f"real_edit_{cat_id}"):
            st.session_state.edit_id = cat_id
            st.rerun()
        if st.session_state.get(f"real_del_{cat_id}"):
            st.session_state.delete_id = cat_id
            st.rerun()
        if st.session_state.get(f"real_view_{cat_id}"):
            st.session_state.view_id = cat_id
            st.rerun()
        
        # نوافذ التعديل والحذف والعرض
        if st.session_state.edit_id == cat_id:
            with st.container():
                st.markdown('<div style="background-color: #f1f5f9; border-radius: 8px; padding: 12px; margin-top: 8px;">', unsafe_allow_html=True)
                new_name = st.text_input("✏️ تعديل الاسم", value=cat['name'], key=f"edit_input_{cat_id}")
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
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.delete_id == cat_id:
            with st.container():
                st.markdown('<div style="background-color: #f1f5f9; border-radius: 8px; padding: 12px; margin-top: 8px;">', unsafe_allow_html=True)
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
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.view_id == cat_id:
            with st.container():
                st.markdown('<div style="background-color: #f1f5f9; border-radius: 8px; padding: 12px; margin-top: 8px;">', unsafe_allow_html=True)
                st.markdown(f"**📋 الاسم:** {cat['name']}")
                st.markdown(f"**🔢 الكود:** {cat['code']}")
                if st.button("🔙 إغلاق", key=f"close_view_{cat_id}"):
                    st.session_state.view_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
