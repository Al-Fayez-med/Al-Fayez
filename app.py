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

# ================= دوال =================
def load_products():
    docs = db.collection("products").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

def save_product(data):
    db.collection("products").add(data)

def update_product(product_id, data):
    db.collection("products").document(product_id).update(data)

def delete_product(product_id):
    db.collection("products").document(product_id).delete()

def load_settings():
    doc = db.collection("settings").document("general").get()
    return doc.to_dict() if doc.exists else {"exchange_rate": 15000}

def save_settings(data):
    db.collection("settings").document("general").set(data)

def calculate_syp(price, currency, rate):
    return price if currency == "SYP" else price * rate

# ================= بيانات =================
settings = load_settings()
exchange_rate = settings.get("exchange_rate", 15000)
products = load_products()

# ================= UI =================
st.title("💊 نظام إدارة المستودعات الطبية")
st.markdown("---")

# سعر الصرف
st.subheader("💱 سعر صرف الدولار")
col1, col2 = st.columns([3,1])

with col1:
    new_rate = st.number_input("السعر", value=exchange_rate, step=100)

with col2:
    if st.button("تأكيد"):
        save_settings({"exchange_rate": new_rate})
        st.success("تم تحديث السعر")
        st.rerun()

st.markdown("---")

# زر إضافة
if st.button("➕ إضافة صنف جديد"):
    st.session_state.edit_id = None
    st.session_state.show_form = True

# ================= نموذج =================
if st.session_state.get("show_form", False):

    editing = st.session_state.get("edit_id")

    if editing:
        product = next((p for p in products if p["id"] == editing), {})
        st.subheader("✏️ تعديل صنف")
    else:
        product = {}
        st.subheader("➕ إضافة صنف")

    name = st.text_input("اسم الصنف", value=product.get("name",""))
    desc = st.text_area("الوصف", value=product.get("description",""))
    category = st.text_input("المجموعة", value=product.get("category",""))

    price = st.number_input("السعر", min_value=0.0, value=float(product.get("price",0)))

    currency_map = {"SYP": "ليرة سورية", "USD": "دولار"}
    currency_reverse = {v:k for k,v in currency_map.items()}

    currency_display = currency_map.get(product.get("currency","SYP"), "ليرة سورية")
    currency = st.selectbox("العملة", ["ليرة سورية","دولار"], index=["ليرة سورية","دولار"].index(currency_display))
    currency_code = currency_reverse[currency]

    quantity = st.number_input("الكمية", min_value=0, value=int(product.get("quantity",0)))

    syp_price = calculate_syp(price, currency_code, new_rate)
    st.text_input("السعر بالليرة", value=f"{syp_price:,.0f}", disabled=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 حفظ"):
            if name:
                data = {
                    "name": name,
                    "description": desc,
                    "category": category,
                    "price": price,
                    "currency": currency_code,
                    "quantity": quantity,
                }

                if editing:
                    update_product(editing, data)
                    st.success("تم التعديل بنجاح ✅")
                else:
                    data["created_at"] = datetime.now().isoformat()
                    save_product(data)
                    st.success("تمت الإضافة بنجاح ✅")

                st.session_state.show_form = False
                st.session_state.edit_id = None
                st.rerun()
            else:
                st.warning("أدخل اسم الصنف")

    with col2:
        if st.button("❌ إلغاء"):
            st.session_state.show_form = False
            st.session_state.edit_id = None
            st.rerun()

# ================= عرض =================
st.subheader("📋 قائمة الأصناف")

for p in products:
    col1, col2, col3 = st.columns([2,2,2])

    currency = p.get("currency","SYP")
    price = p.get("price",0)
    quantity = p.get("quantity",0)
    syp_price = calculate_syp(price, currency, exchange_rate)

    with col1:
        st.markdown(f"**{p.get('name','')}**")
        st.caption(p.get("category",""))

    with col2:
        if currency == "USD":
            st.write(f"💵 {price} USD")
            st.markdown(f"<span style='color:gray'>≈ {syp_price:,.0f} ل.س</span>", unsafe_allow_html=True)
        else:
            st.write(f"{price:,.0f} ل.س")

        st.write(f"الكمية: {quantity}")

    with col3:
        if st.button("✏️ تعديل", key=f"edit_{p['id']}"):
            st.session_state.edit_id = p["id"]
            st.session_state.show_form = True

        if st.button("🗑️ حذف", key=f"del_{p['id']}"):
            st.session_state.delete_id = p["id"]

    if st.session_state.get("delete_id") == p["id"]:
        st.warning("تأكيد الحذف؟")
        c1,c2 = st.columns(2)

        with c1:
            if st.button("نعم", key=f"yes_{p['id']}"):
                delete_product(p["id"])
                st.session_state.delete_id = None
                st.rerun()

        with c2:
            if st.button("إلغاء", key=f"no_{p['id']}"):
                st.session_state.delete_id = None
                st.rerun()

    st.markdown("---")

st.caption("© نظام إدارة المستودعات")
