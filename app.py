import streamlit as st
from datetime import datetime
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

def category_has_products(code):
    products = load_products()
    return any(p.get("category_code") == code for p in products)

# ================= Navigation =================
page = st.sidebar.radio("📂 التنقل", ["📦 الأصناف", "🗂️ المجموعات"])

# ================= Categories Page =================
if page == "🗂️ المجموعات":

    st.title("🗂️ إدارة المجموعات")

    # Add category
    st.subheader("➕ إضافة مجموعة")
    name = st.text_input("اسم المجموعة")

    if st.button("حفظ المجموعة"):
        if name:
            code = generate_category_code()
            db.collection("categories").add({
                "name": name,
                "code": code
            })
            st.cache_data.clear()
            st.success(f"تمت الإضافة بالكود {code}")
            st.rerun()

    st.markdown("---")

    categories = load_categories()

    for c in categories:
        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(f"{c['code']} - {c['name']}")

        with col2:
            if st.button("✏️ تعديل", key=f"edit_{c['id']}"):
                st.session_state.edit_cat = c["id"]
                st.rerun()

        with col3:
            if st.button("🗑️ حذف", key=f"del_{c['id']}"):
                if category_has_products(c["code"]):
                    st.warning("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                else:
                    db.collection("categories").document(c["id"]).delete()
                    st.cache_data.clear()
                    st.rerun()

    # Edit form
    if st.session_state.get("edit_cat"):
        cat_id = st.session_state.edit_cat
        cat = next((x for x in categories if x["id"] == cat_id), None)

        if cat:
            st.markdown("---")
            st.subheader("✏️ تعديل مجموعة")

            new_name = st.text_input("اسم المجموعة", value=cat["name"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 حفظ"):
                    db.collection("categories").document(cat_id).update({
                        "name": new_name
                    })
                    st.cache_data.clear()
                    st.session_state.edit_cat = None
                    st.success("تم التعديل")
                    st.rerun()

            with col2:
                if st.button("❌ إلغاء"):
                    st.session_state.edit_cat = None
                    st.rerun()

# ================= Products Page =================
if page == "📦 الأصناف":

    st.title("💊 إدارة الأصناف")

    categories = load_categories()
    products = load_products()

    # Exchange rate
    settings = db.collection("settings").document("general").get()
    exchange_rate = settings.to_dict().get("exchange_rate",15000) if settings.exists else 15000

    new_rate = st.number_input("سعر الصرف", value=exchange_rate)

    if st.button("تحديث السعر"):
        db.collection("settings").document("general").set({"exchange_rate": new_rate})
        st.rerun()

    st.markdown("---")

    # Add product
    if st.button("➕ إضافة صنف"):
        st.session_state.add_product = True
        st.rerun()

    if st.session_state.get("add_product"):

        st.subheader("➕ إضافة صنف")

        name = st.text_input("الاسم")
        desc = st.text_area("الوصف")

        if not categories:
            st.warning("❌ أضف مجموعة أولاً")
            st.stop()

        cat_names = [f"{c['code']} - {c['name']}" for c in categories]
        selected = st.selectbox("المجموعة", cat_names)

        category_code = selected.split(" - ")[0]

        price = st.number_input("السعر", min_value=0.0)
        currency = st.selectbox("العملة", ["SYP","USD"])
        quantity = st.number_input("الكمية", min_value=0)

        if st.button("💾 حفظ الصنف"):
            code = generate_product_code(category_code)

            db.collection("products").add({
                "name": name,
                "description": desc,
                "category_code": category_code,
                "code": code,
                "price": price,
                "currency": currency,
                "quantity": quantity,
                "created_at": datetime.now().isoformat()
            })

            st.cache_data.clear()
            st.session_state.add_product = False
            st.success(f"تم الحفظ بالكود {code}")
            st.rerun()

    st.markdown("---")

    # Display products (FULL DATA VIEW)
    for p in products:
        st.markdown("### 📦 صنف")

        st.write("🆔 الكود:", p.get("code"))
        st.write("📛 الاسم:", p.get("name"))
        st.write("📝 الوصف:", p.get("description"))
        st.write("📂 كود المجموعة:", p.get("category_code"))
        st.write("💰 السعر:", p.get("price"), p.get("currency"))
        st.write("📦 الكمية:", p.get("quantity"))
        st.write("⏱️ تاريخ الإنشاء:", p.get("created_at"))

        st.markdown("---")

st.caption("© نظام إدارة المستودعات")
