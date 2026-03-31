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

def calculate_syp(price, currency, rate):
    return price if currency == "SYP" else price * rate

# ================= Navigation =================
page = st.sidebar.radio("📂 التنقل", ["📦 الأصناف", "🗂️ المجموعات"])

# ================= Categories =================
if page == "🗂️ المجموعات":

    st.title("🗂️ إدارة المجموعات")

    name = st.text_input("اسم المجموعة")

    if st.button("➕ إضافة مجموعة"):
        if name:
            code = generate_category_code()
            db.collection("categories").add({"name": name, "code": code})
            st.cache_data.clear()
            st.success(f"تمت الإضافة ({code})")
            st.rerun()

    st.markdown("---")

    categories = load_categories()

    for c in categories:
        col1, col2, col3 = st.columns([3,1,1])

        with col1:
            st.write(f"{c['code']} - {c['name']}")

        with col2:
            if st.button("✏️", key=f"edit_{c['id']}"):
                st.session_state.edit_cat = c["id"]
                st.rerun()

        with col3:
            if st.button("🗑️", key=f"del_{c['id']}"):
                if category_has_products(c["code"]):
                    st.warning("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                else:
                    db.collection("categories").document(c["id"]).delete()
                    st.cache_data.clear()
                    st.rerun()

# ================= Products =================
if page == "📦 الأصناف":

    st.title("💊 إدارة الأصناف")

    categories = load_categories()
    products = load_products()

    # سعر الصرف
    settings = db.collection("settings").document("general").get()
    exchange_rate = settings.to_dict().get("exchange_rate",15000) if settings.exists else 15000

    new_rate = st.number_input("سعر الصرف", value=exchange_rate)

    if st.button("💱 تحديث السعر"):
        db.collection("settings").document("general").set({"exchange_rate": new_rate})
        st.rerun()

    st.markdown("---")

    # إضافة صنف
    if st.button("➕ إضافة صنف"):
        st.session_state.add_product = True
        st.session_state.edit_product = None
        st.rerun()

    # ================= نموذج إضافة/تعديل =================
    if st.session_state.get("add_product") or st.session_state.get("edit_product"):

        editing = st.session_state.get("edit_product")
        product = next((p for p in products if p["id"] == editing), {}) if editing else {}

        st.subheader("✏️ تعديل صنف" if editing else "➕ إضافة صنف")

        name = st.text_input("الاسم", value=product.get("name",""))
        desc = st.text_area("الوصف", value=product.get("description",""))

        if not categories:
            st.warning("❌ أضف مجموعة أولاً")
            st.stop()

        cat_names = [f"{c['code']} - {c['name']}" for c in categories]
        selected = st.selectbox("المجموعة", cat_names)

        category_code = selected.split(" - ")[0]

        price = st.number_input("السعر", min_value=0.0, value=float(product.get("price",0)))
        currency = st.selectbox("العملة", ["SYP","USD"])
        quantity = st.number_input("الكمية", min_value=0, value=int(product.get("quantity",0)))

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 حفظ"):
                data = {
                    "name": name,
                    "description": desc,
                    "category_code": category_code,
                    "price": price,
                    "currency": currency,
                    "quantity": quantity,
                }

                if editing:
                    db.collection("products").document(editing).update(data)
                else:
                    code = generate_product_code(category_code)
                    data["code"] = code
                    data["created_at"] = datetime.now().isoformat()
                    db.collection("products").add(data)

                st.cache_data.clear()
                st.session_state.add_product = False
                st.session_state.edit_product = None
                st.rerun()

        with col2:
            if st.button("❌ إلغاء"):
                st.session_state.add_product = False
                st.session_state.edit_product = None
                st.rerun()

    st.markdown("---")

    # ================= عرض الأصناف =================
    for p in products:
        col1, col2, col3 = st.columns([3,2,1])

        syp_price = calculate_syp(p.get("price",0), p.get("currency","SYP"), exchange_rate)

        with col1:
            st.markdown(f"### {p.get('name')}")
            st.caption(f"🆔 {p.get('code')}")

        with col2:
            if p.get("currency") == "USD":
                st.write(f"💵 {p.get('price')} USD")
                st.markdown(f"<span style='color:gray'>≈ {syp_price:,.0f} ل.س</span>", unsafe_allow_html=True)
            else:
                st.write(f"{p.get('price'):,.0f} ل.س")

            st.write(f"📦 الكمية: {p.get('quantity')}")

        with col3:
            if st.button("✏️", key=f"edit_{p['id']}"):
                st.session_state.edit_product = p["id"]
                st.session_state.add_product = True
                st.rerun()

            if st.button("🗑️", key=f"del_{p['id']}"):
                db.collection("products").document(p["id"]).delete()
                st.cache_data.clear()
                st.rerun()

        # تاريخ (باهت)
        st.markdown(
            f"<small style='color:gray'>تمت الإضافة: {p.get('created_at','')}</small>",
            unsafe_allow_html=True
        )

        st.markdown("---")

st.caption("© نظام إدارة المستودعات")
