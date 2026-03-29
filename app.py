import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from google.oauth2 import service_account
from google.cloud import firestore

# إعداد الصفحة
st.set_page_config(page_title="نظام إدارة المستودعات", page_icon="💊", layout="wide")

# ==================== إعداد الاتصال بـ Firebase ====================
def init_firebase():
    """تهيئة الاتصال بقاعدة البيانات"""
    key_path = "firebase-key.json"
    
    if not os.path.exists(key_path):
        st.error("❌ ملف المفتاح firebase-key.json غير موجود")
        return None
    
    try:
        with open(key_path, "r") as f:
            key_info = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_info(key_info)
        db = firestore.Client(credentials=credentials, project=key_info["project_id"])
        return db
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")
        return None

# تهيئة قاعدة البيانات
db = init_firebase()

# ==================== دوال مساعدة ====================
def load_products():
    """تحميل جميع المنتجات"""
    if db is None:
        return []
    
    try:
        products_ref = db.collection("products")
        docs = products_ref.stream()
        
        products = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            products.append(data)
        
        return products
    except Exception as e:
        st.error(f"خطأ في التحميل: {e}")
        return []

def save_product(product_data, product_id=None):
    """حفظ منتج"""
    if db is None:
        return False
    
    try:
        products_ref = db.collection("products")
        if product_id:
            products_ref.document(product_id).set(product_data, merge=True)
        else:
            products_ref.add(product_data)
        return True
    except Exception as e:
        st.error(f"خطأ في الحفظ: {e}")
        return False

def delete_product(product_id):
    """حذف منتج"""
    if db is None:
        return False
    
    try:
        db.collection("products").document(product_id).delete()
        return True
    except Exception as e:
        st.error(f"خطأ في الحذف: {e}")
        return False

def load_settings():
    """تحميل الإعدادات"""
    if db is None:
        return {"exchange_rate": 15000}
    
    try:
        settings_ref = db.collection("settings").document("general")
        doc = settings_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"exchange_rate": 15000}
    except:
        return {"exchange_rate": 15000}

def save_settings(settings):
    """حفظ الإعدادات"""
    if db is None:
        return False
    
    try:
        db.collection("settings").document("general").set(settings, merge=True)
        return True
    except:
        return False

def generate_code():
    """توليد كود تلقائي"""
    products = load_products()
    if not products:
        return "MED-001"
    
    codes = [p.get("code", "") for p in products if p.get("code", "").startswith("MED-")]
    numbers = []
    for code in codes:
        try:
            num = int(code.split("-")[1])
            numbers.append(num)
        except:
            pass
    
    if numbers:
        return f"MED-{str(max(numbers) + 1).zfill(3)}"
    return "MED-001"

def calculate_syp(price, currency, rate):
    """حساب السعر بالليرة"""
    if currency == "SYP":
        return price
    return price * rate

# ==================== تحميل البيانات الأولية ====================
settings = load_settings()
exchange_rate = settings.get("exchange_rate", 15000)
products = load_products()

# ==================== الواجهة الرئيسية ====================
st.title("💊 نظام إدارة المستودعات الطبية")
st.markdown("---")

# سعر الصرف
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 💱 سعر صرف الدولار")
        rate_col1, rate_col2 = st.columns([3, 1])
        with rate_col1:
            new_rate = st.number_input(
                "السعر",
                value=exchange_rate,
                step=100,
                format="%d",
                label_visibility="collapsed",
                key="rate_input"
            )
        with rate_col2:
            if st.button("تأكيد", key="confirm_rate_btn", use_container_width=True):
                save_settings({"exchange_rate": new_rate})
                st.success("✅ تم تحديث سعر الصرف")
                st.rerun()
st.markdown("---")

# أزرار التحكم
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ إضافة صنف جديد", key="add_product_btn", use_container_width=True, type="primary"):
        st.session_state.show_form = True
with col_btn2:
    if st.button("🔄 تحديث", key="refresh_btn", use_container_width=True):
        st.rerun()

# نموذج إضافة صنف جديد
if st.session_state.get("show_form", False):
    with st.expander("➕ إضافة صنف جديد", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("اسم الصنف", key="new_name")
            desc = st.text_area("الوصف", height=80, key="new_desc")
            category = st.text_input("المجموعة", key="new_category")
        
        with col2:
            price = st.number_input("السعر", min_value=0.0, step=0.5, format="%.2f", key="new_price")
            currency = st.selectbox("العملة", ["ليرة سورية", "دولار"], key="new_currency")
            currency_code = "SYP" if currency == "ليرة سورية" else "USD"
            quantity = st.number_input("الكمية", min_value=0, step=1, key="new_qty")
        
        # عرض السعر بالليرة
        current_rate = new_rate if 'new_rate' in locals() else exchange_rate
        syp_price = calculate_syp(price, currency_code, current_rate)
        st.text_input("السعر بالليرة السورية", value=f"{syp_price:,.0f} ل.س", disabled=True, key="new_syp")
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("💾 حفظ", key="save_new_btn", use_container_width=True):
                if name:
                    new_code = generate_code()
                    product_data = {
                        "code": new_code,
                        "name": name,
                        "description": desc,
                        "category": category,
                        "price": price,
                        "currency": currency_code,
                        "price_syp": syp_price,
                        "quantity": quantity,
                        "created_at": datetime.now().isoformat()
                    }
                    if save_product(product_data):
                        st.success(f"✅ تم إضافة {name}")
                        st.session_state.show_form = False
                        st.rerun()
                else:
                    st.warning("⚠️ يرجى إدخال اسم الصنف")
        
        with col_cancel:
            if st.button("إلغاء", key="cancel_new_btn", use_container_width=True):
                st.session_state.show_form = False
                st.rerun()

# عرض قائمة الأصناف
st.subheader("📋 قائمة الأصناف")

if not products:
    st.info("لا توجد أصناف. اضغط على إضافة صنف جديد")
else:
    for idx, product in enumerate(products):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{product.get('name', 'بدون اسم')}**")
                st.caption(f"الكود: {product.get('code', '')}")
                st.caption(f"المجموعة: {product.get('category', '')}")
            
            with col2:
                st.write(f"السعر: {product.get('price', 0)}")
                currency_display = "ليرة" if product.get('currency') == "SYP" else "دولار"
                st.write(f"العملة: {currency_display}")
                st.write(f"الكمية: {product.get('quantity', 0)}")
                st.write(f"السعر بالليرة: {product.get('price_syp', 0):,.0f} ل.س")
            
            with col3:
                if st.button("🗑️ حذف", key=f"del_btn_{product.get('id')}_{idx}", use_container_width=True):
                    if delete_product(product.get('id')):
                        st.success("تم الحذف")
                        st.rerun()
            
            st.markdown("---")

# تذييل
st.caption("© نظام إدارة المستودعات الطبية")
