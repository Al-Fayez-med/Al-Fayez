import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":

    st.components.v1.html("""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body {
      margin:0;
      background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
      direction: rtl;
      font-family: Arial;
      color:white;
    }

    .container {
      display:grid;
      grid-template-columns: repeat(2,1fr);
      gap:30px;
      padding:25px;
    }

    .item {
      text-align:center;
    }

    .icon-box {
      width:85px;
      height:85px;
      margin:auto;
      border:2px solid rgba(255,255,255,0.6);
      border-radius:22px;

      display:flex;
      align-items:center;
      justify-content:center;

      transition:0.15s;
    }

    .icon-box:active {
      transform:scale(1.1);
    }

    .icon-box svg {
      width:42px;
      height:42px;
      stroke:rgba(255,255,255,0.75);
    }

    .label {
      margin-top:10px;
      font-size:14px;
    }
    </style>
    </head>

    <body>

    <div class="container">

      <div class="item">
        <div class="icon-box"><i data-lucide="user"></i></div>
        <div class="label">ملفي</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="settings"></i></div>
        <div class="label">الضبط</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="cross"></i></div>
        <div class="label">الصيدليات</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="box"></i></div>
        <div class="label">الأصناف</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="layers"></i></div>
        <div class="label">المجموعات</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="users"></i></div>
        <div class="label">الموردين</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="warehouse"></i></div>
        <div class="label">المستودعات</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="banknote"></i></div>
        <div class="label">الصندوق</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="receipt"></i></div>
        <div class="label">السندات</div>
      </div>

    </div>

    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
    lucide.createIcons();
    </script>

    </body>
    </html>
    """, height=700)

    st.stop()
# ================= Firebase =================
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# ================= Data =================
@st.cache_data
def load_products():
    docs = db.collection("products").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

@st.cache_data
def load_categories():
    docs = db.collection("categories").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def generate_category_code():
    cats = load_categories()
    if not cats:
        return "001"
    max_code = max(int(c["code"]) for c in cats)
    return str(max_code + 1).zfill(3)

def generate_product_code(category_code):
    products = load_products()
    same = [p for p in products if p.get("category_code") == category_code]
    if not same:
        return f"{category_code}001"
    max_code = max(int(p["code"][-3:]) for p in same)
    return f"{category_code}{str(max_code + 1).zfill(3)}"

def get_category_name(code):
    for c in load_categories():
        if c["code"] == code:
            return c["name"]
    return ""

def category_has_products(code):
    for p in load_products():
        if p.get("category_code") == code:
            return True
    return False

# ================= Navigation =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= Dashboard =================
if st.session_state.page == "home":

    st.components.v1.html("""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body {
      margin:0;
      background: radial-gradient(circle at center, #3b82f6 0%, #1e3a8a 70%);
      direction: rtl;
      font-family: Arial;
      color:white;
    }
    .container {
      display:grid;
      grid-template-columns: repeat(2,1fr);
      gap:25px;
      padding:20px;
    }
    .item {
      text-align:center;
    }
    .icon-box {
      width:90px;
      height:90px;
      margin:auto;
      border:2px solid rgba(255,255,255,0.6);
      border-radius:20px;
      display:flex;
      align-items:center;
      justify-content:center;
      transition:0.15s;
    }
    .icon-box:active {
      transform:scale(1.1);
    }
    .icon-box svg {
      width:45px;
      height:45px;
      stroke:rgba(255,255,255,0.75);
    }
    .label {
      margin-top:8px;
      font-size:14px;
    }
    </style>
    </head>
    <body>

    <div class="container">

      <div class="item">
        <div class="icon-box"><i data-lucide="box"></i></div>
        <div class="label">الأصناف</div>
      </div>

      <div class="item">
        <div class="icon-box"><i data-lucide="layers"></i></div>
        <div class="label">المجموعات</div>
      </div>

    </div>

    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>

    </body>
    </html>
    """, height=500)

    st.markdown("### اختر القسم")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📦 الأصناف"):
            st.session_state.page = "products"
            st.rerun()

    with col2:
        if st.button("🗂️ المجموعات"):
            st.session_state.page = "categories"
            st.rerun()

# ================= Categories =================
elif st.session_state.page == "categories":

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🗂️ إدارة المجموعات")

    name = st.text_input("اسم المجموعة")

    if st.button("➕ إضافة مجموعة"):
        if name:
            code = generate_category_code()
            db.collection("categories").add({"name": name, "code": code})
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    categories = load_categories()

    for c in categories:
        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(f"{c['code']} - {c['name']}")

        with col2:
            if st.button("✏️", key=f"edit_cat_{c['id']}"):
                st.session_state.edit_cat = c["id"]
                st.rerun()

        with col3:
            if st.button("🗑️", key=f"del_cat_{c['id']}"):
                st.session_state.delete_cat = c["id"]

    # ✅ رجعت حذف المجموعات
    if st.session_state.get("delete_cat"):
        cat = next((x for x in categories if x["id"] == st.session_state.delete_cat), None)

        if cat:
            st.warning(f"⚠️ حذف المجموعة: {cat['name']} ؟")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("❌ إلغاء"):
                    st.session_state.delete_cat = None
                    st.rerun()

            with col2:
                if st.button("🗑️ تأكيد"):
                    if category_has_products(cat["code"]):
                        st.error("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                    else:
                        db.collection("categories").document(cat["id"]).delete()
                        st.session_state.delete_cat = None
                        st.cache_data.clear()
                        st.rerun()

# ================= Products =================
elif st.session_state.page == "products":

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💊 إدارة الأصناف")

    categories = load_categories()
    products = load_products()

    st.write("هنا كودك كما هو بدون تعديل")

st.caption("© نظام إدارة المستودعات")
