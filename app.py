import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# ==================== Firebase ====================
@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            key_dict = json.loads(st.secrets["firebase_key"])
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")
        return None

db = init_firebase()

# ==================== دوال ====================
def load_products():
    try:
        docs = db.collection("products").stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
    except:
        return []

def save_product(data):
    try:
        db.collection("products").add(data)
        return True
    except:
        return False

def delete_product(product_id):
    try:
        db.collection("products").document(product_id).delete()
        return True
    except:
        return False

def load_settings():
    doc = db.collection("settings").document("general").get()
    return doc.to_dict() if doc.exists else {"exchange_rate": 15000}

def save_settings(data):
    db.collection("settings").document("general").set(data)

def calculate_syp(price, currency, rate):
    return price if currency == "SYP" else price * rate

# ==================== بيانات ====================
settings = load_settings()
exchange_rate = settings.get("exchange_rate", 15000)
products = load_products()

# ==================== UI ====================
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
    st.session_state.show_form = True

# ==================== نموذج ====================
if st.session_state.get("show_form", False):

    st.subheader("إضافة صنف")

    name = st.text_input("اسم الصنف")
    desc = st.text_area("الوصف")
    category = st.text_input("المجموعة")

    price = st.number_input("السعر", min_value=0.0)
    currency = st.selectbox("العملة", ["ليرة سورية", "دولار"])
    currency_code = "SYP" if currency == "ليرة سورية" else "USD"

    quantity = st.number_input("الكمية", min_value=0)

    syp_price = calculate_syp(price, currency_code, new_rate)
    st.text_input("السعر بالليرة", value=f"{syp_price:,.0f}", disabled=True)

    col_save, col_cancel = st.columns(2)

    with col_save:
        if st.button("💾 حفظ"):
            if name:
                data = {
                    "name": name,
                    "description": desc,
                    "category": category,
                    "price": price,
                    "currency": currency_code,
                    "price_syp": syp_price,
                    "quantity": quantity,
                    "created_at": datetime.now().isoformat()
                }

                if save_product(data):
                    st.success("تم الحفظ")
                    st.session_state.show_form = False
                    st.rerun()
            else:
                st.warning("أدخل اسم الصنف")

    with col_cancel:
        if st.button("❌ إلغاء"):
            st.session_state.show_form = False
            st.rerun()

# ==================== عرض ====================
st.subheader("📋 قائمة الأصناف")

if not products:
    st.info("لا يوجد أصناف")
else:
    for p in products:
        col1, col2, col3 = st.columns([2,2,1])

        with col1:
            st.markdown(f"**{p.get('name','')}**")
            st.caption(p.get("category",""))

        with col2:
            st.write(f"السعر: {p.get('price',0)}")
            st.write(f"الكمية: {p.get('quantity',0)}")
            st.write(f"بالليرة: {p.get('price_syp',0):,.0f}")

        with col3:
            if st.button("🗑️ حذف", key=p["id"]):
                st.session_state[f"confirm_{p['id']}"] = True

        if st.session_state.get(f"confirm_{p['id']}", False):
            st.warning("هل أنت متأكد من الحذف؟")
            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("نعم", key=f"yes_{p['id']}"):
                    delete_product(p["id"])
                    st.rerun()

            with col_no:
                if st.button("إلغاء", key=f"no_{p['id']}"):
                    st.session_state[f"confirm_{p['id']}"] = False

        st.markdown("---")

st.caption("© نظام إدارة المستودعات")
