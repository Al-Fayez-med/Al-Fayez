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

# ==================== CSS ====================
st.markdown("""
<style>
/* Tailwind CDN */
@import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');

/* تنسيق عام للصفحة */
.main-header {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 1rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ==================== الواجهة ====================
st.markdown('<div class="main-header"><h1 class="text-4xl font-bold text-white">🗂️ المجموعات</h1></div>', unsafe_allow_html=True)

# أزرار التحكم
col1, col2 = st.columns([1, 10])
with col1:
    if st.button("➕", key="add_cat", help="إضافة مجموعة"):
        st.session_state.show_add = True

# إضافة مجموعة (نافذة منبثقة باستخدام Tailwind)
if st.session_state.get("show_add", False):
    st.markdown("""
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" id="my-modal">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">إضافة مجموعة جديدة</h3>
          <div class="mt-2 px-7 py-3">
            <input type="text" id="cat_name" placeholder="اسم المجموعة" class="border rounded w-full py-2 px-3 text-gray-700">
            <div class="text-sm text-gray-500 mt-2">الكود: """ + generate_code() + """</div>
          </div>
          <div class="flex gap-3 mt-5">
            <button onclick="document.getElementById('my-modal').style.display='none'" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">حفظ</button>
            <button onclick="document.getElementById('my-modal').style.display='none'" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">إلغاء</button>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# عرض المجموعات
categories = load_categories()
for cat in categories:
    st.markdown(f"""
    <div class="bg-white shadow-md rounded-lg p-4 mb-4 border-r-4 border-blue-500">
        <div class="flex justify-between items-center">
            <div>
                <h3 class="text-xl font-bold text-gray-800">{cat['name']}</h3>
                <p class="text-sm text-gray-500">الكود: {cat['code']}</p>
            </div>
            <div class="flex gap-2">
                <button class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">✏️ تعديل</button>
                <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">🗑️ حذف</button>
                <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">👁️ عرض</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
