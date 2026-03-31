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

# ================= Load =================
@st.cache_data
def load_products():
    docs = db.collection("products").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

@st.cache_data
def load_categories():
    docs = db.collection("categories").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

# ================= Helpers =================
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
    cats = load_categories()
    for c in cats:
        if c["code"] == code:
            return c["name"]
    return "غير معروف"

def category_has_products(code):
    products = load_products()
    return any(p.get("category_code") == code for p in products)

# ================= Navigation =================
page = st.sidebar.radio("📂 التنقل", ["📦 الأصناف", "🗂️ المجموعات"])

# ================= Categories =================
if page == "🗂️ المجموعات":

    st.title("🗂️ إدارة المجموعات")

    name = st.text_input("اسم المجموعة")

    if st.button("➕ إضافة"):
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
                if category_has_products(c["code"]):
                    st.warning("❌ لا يمكن حذف مجموعة تحتوي على أصناف")
                else:
                    db.collection("categories").document(c["id"]).delete()
                    st.cache_data.clear()
                    st.rerun()

    # ===== تعديل =====
    if st.session_state.get("edit_cat"):
        cat_id = st.session_state.edit_cat
        cat = next((x for x in categories if x["id"] == cat_id), None)

        if cat:
            st.subheader("✏️ تعديل مجموعة")
            new_name = st.text_input("اسم جديد", value=cat["name"])

            if st.button("💾 حفظ التعديل"):
                db.collection("categories").document(cat_id).update({
                    "name": new_name
                })
                st.cache_data.clear()
                st.session_state.edit_cat = None
                st.rerun()

# ================= Products =================
if page == "📦 الأصناف":

    st.title("💊 إدارة الأصناف")

    categories = load_categories()
    products = load_products()

    # إضافة
    if st.button("➕ إضافة صنف"):
        st.session_state.add = True
        st.session_state.edit = None
        st.rerun()

    # ===== نموذج =====
    if st.session_state.get("add"):

        editing = st.session_state.get("edit")
        product = next((p for p in products if p["id"] == editing), {}) if editing else {}

        name = st.text_input("الاسم", value=product.get("name",""))
        desc = st.text_area("الوصف", value=product.get("description",""))

        cat_names = [f"{c['code']} - {c['name']}" for c in categories]
        selected = st.selectbox("المجموعة", cat_names)

        new_category_code = selected.split(" - ")[0]

        price = st.number_input("السعر", min_value=0.0, value=float(product.get("price",0)))
        currency = st.selectbox("العملة", ["SYP","USD"])
        quantity = st.number_input("الكمية", min_value=0, value=int(product.get("quantity",0)))

        if st.button("💾 حفظ"):
            if editing:
                old_code = product.get("code")
                movement = product.get("movement_count", 0)

                if new_category_code != product.get("category_code"):
                    new_code = generate_product_code(new_category_code)

                    # إعادة استخدام الكود القديم
                    if movement == 0:
                        pass  # ممكن نستخدمه لاحقاً (جاهزين للفكرة)

                else:
                    new_code = old_code

                db.collection("products").document(editing).update({
                    "name": name,
                    "description": desc,
                    "category_code": new_category_code,
                    "code": new_code,
                    "price": price,
                    "currency": currency,
                    "quantity": quantity
                })

            else:
                code = generate_product_code(new_category_code)

                db.collection("products").add({
                    "name": name,
                    "description": desc,
                    "category_code": new_category_code,
                    "code": code,
                    "price": price,
                    "currency": currency,
                    "quantity": quantity,
                    "movement_count": 0,
                    "created_at": datetime.now().isoformat()
                })

            st.cache_data.clear()
            st.session_state.add = False
            st.session_state.edit = None
            st.rerun()

    st.markdown("---")

    # ===== عرض =====
    for p in products:
        col1, col2, col3 = st.columns([3,2,1])

        with col1:
            st.markdown(f"### {p.get('name')}")
            st.caption(f"🆔 {p.get('code')}")
            st.write(f"📂 {get_category_name(p.get('category_code'))}")

        with col2:
            st.write(f"{p.get('price')} {p.get('currency')}")
            st.write(f"📦 {p.get('quantity')}")

        with col3:
            if st.button("✏️", key=f"edit_{p['id']}"):
                st.session_state.edit = p["id"]
                st.session_state.add = True
                st.rerun()

            if st.button("🗑️", key=f"del_{p['id']}"):
                db.collection("products").document(p["id"]).delete()
                st.cache_data.clear()
                st.rerun()

        st.markdown("---")
