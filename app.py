import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# ================= Firebase =================
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# ================= Navigation =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= Home (الشاشة الزرقا) =================
if st.session_state.page == "home":

    st.components.v1.html("""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body {
      margin: 0;
      font-family: Arial;
      direction: rtl;
      background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
      color: white;
    }
    .container {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      height: 100vh;
      padding: 15px;
      gap: 15px;
    }
    .item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .icon-box {
      width: 110px;
      height: 110px;
      border: 2px solid rgba(255,255,255,0.6);
      border-radius: 25px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.15s ease-in-out, border-color 0.15s;
    }
    .icon-box:active {
      transform: scale(1.1);
      border-color: white;
    }
    .icon-box svg {
      width: 55px;
      height: 55px;
      stroke: rgba(255,255,255,0.75);
    }
    .label {
      margin-top: 10px;
      font-size: 15px;
    }
    </style>
    </head>

    <body>

    <div class="container">

      <div class="item" onclick="parent.postMessage('profile','*')">
        <div class="icon-box"><i data-lucide="user"></i></div>
        <div class="label">ملفي الشخصي</div>
      </div>

      <div class="item" onclick="parent.postMessage('settings','*')">
        <div class="icon-box"><i data-lucide="settings"></i></div>
        <div class="label">الضبط</div>
      </div>

      <div class="item" onclick="parent.postMessage('pharmacy','*')">
        <div class="icon-box"><i data-lucide="cross"></i></div>
        <div class="label">الصيدليات</div>
      </div>

      <div class="item" onclick="parent.postMessage('products','*')">
        <div class="icon-box"><i data-lucide="box"></i></div>
        <div class="label">الأصناف</div>
      </div>

      <div class="item" onclick="parent.postMessage('suppliers','*')">
        <div class="icon-box"><i data-lucide="users"></i></div>
        <div class="label">الموردين</div>
      </div>

      <div class="item" onclick="parent.postMessage('warehouses','*')">
        <div class="icon-box"><i data-lucide="warehouse"></i></div>
        <div class="label">المستودعات</div>
      </div>

      <div class="item" onclick="parent.postMessage('cash','*')">
        <div class="icon-box"><i data-lucide="banknote"></i></div>
        <div class="label">الصندوق</div>
      </div>

      <div class="item" onclick="parent.postMessage('receipts','*')">
        <div class="icon-box"><i data-lucide="receipt"></i></div>
        <div class="label">السندات</div>
      </div>

    </div>

    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>

    </body>
    </html>
    """, height=800)

    # استقبال الضغطات
    page = st.experimental_get_query_params().get("page")

# ================= صفحات فاضية =================
else:

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <style>
    body {
      background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
      color:white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("صفحة جديدة")
    st.info("🚧 صفحة قيد التطوير")
