import streamlit as st
import pandas as pd
from datetime import datetime

# ====================== Page Configuration ======================
st.set_page_config(page_title="نظام إدارة المستودعات الطبية", page_icon="💊", layout="wide")

# ====================== Session State Initialization ======================
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame({
        'code': ['MED-001', 'MED-002'],
        'name': ['معقم كحولي', 'قفازات طبية'],
        'description': ['معقم كحولي 70% - 500 مل', 'قفازات لاتكس معقمة مقاس M'],
        'category': ['معقمات', 'مستلزمات تمريض'],
        'price': [5.00, 8.50],
        'currency': ['USD', 'USD'],
        'price_syp': [25000, 42500],
        'quantity': [50, 100],
        'image': ['', ''],
        'offer_text': ['', ''],
        'gift_product': ['', ''],
        'bundle_active': [False, False],
        'bundle_main_product': ['', ''],
        'bundle_ratio': ['', '']
    })

if 'exchange_rate' not in st.session_state:
    st.session_state.exchange_rate = 15000

if 'show_offer_modal' not in st.session_state:
    st.session_state.show_offer_modal = False

if 'show_bundle_modal' not in st.session_state:
    st.session_state.show_bundle_modal = False

if 'current_product_idx' not in st.session_state:
    st.session_state.current_product_idx = None

# ====================== Helper Functions ======================
def generate_product_code():
    """Generate a simple automatic product code"""
    codes = st.session_state.products['code'].tolist()
    if not codes:
        return "MED-001"
    numbers = [int(c.split('-')[1]) for c in codes if c.startswith('MED-')]
    last_num = max(numbers) if numbers else 0
    return f"MED-{str(last_num + 1).zfill(3)}"

def calculate_syp_price(price, currency, exchange_rate):
    """Calculate price in Syrian Pounds"""
    if currency == 'SYP':
        return price
    else:
        return price * exchange_rate

def add_new_product():
    """Add a new empty product row"""
    new_code = generate_product_code()
    new_row = pd.DataFrame({
        'code': [new_code],
        'name': [''],
        'description': [''],
        'category': [''],
        'price': [0.0],
        'currency': ['SYP'],
        'price_syp': [0.0],
        'quantity': [0],
        'image': [''],
        'offer_text': [''],
        'gift_product': [''],
        'bundle_active': [False],
        'bundle_main_product': [''],
        'bundle_ratio': ['']
    })
    st.session_state.products = pd.concat([st.session_state.products, new_row], ignore_index=True)

def save_product(index):
    """Save product data and update SYP price"""
    currency = st.session_state.products.at[index, 'currency']
    price = st.session_state.products.at[index, 'price']
    st.session_state.products.at[index, 'price_syp'] = calculate_syp_price(price, currency, st.session_state.exchange_rate)

def update_all_syp_prices():
    """Update all products SYP prices based on current exchange rate"""
    for idx in range(len(st.session_state.products)):
        curr = st.session_state.products.at[idx, 'currency']
        pr = st.session_state.products.at[idx, 'price']
        st.session_state.products.at[idx, 'price_syp'] = calculate_syp_price(pr, curr, st.session_state.exchange_rate)

# ====================== Page Header ======================
st.title("💊 نظام إدارة المستودعات الطبية")
st.markdown("#### إدارة الأصناف - الأكسسوارات الطبية والصيدلانية")
st.markdown("---")

# ====================== Exchange Rate Section (Top of Page) ======================
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 💱 سعر صرف الدولار مقابل الليرة السورية")
        rate_col1, rate_col2 = st.columns([3, 1])
        with rate_col1:
            new_rate = st.number_input(
                "سعر الصرف",
                min_value=1,
                value=st.session_state.exchange_rate,
                step=100,
                format="%d",
                label_visibility="collapsed"
            )
        with rate_col2:
            if st.button("تأكيد", key="confirm_rate_btn", use_container_width=True):
                st.session_state.exchange_rate = new_rate
                update_all_syp_prices()
                st.success("✅ تم تحديث سعر الصرف وجميع الأسعار")
        st.markdown("---")

# ====================== Main Action Buttons ======================
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])
with btn_col1:
    if st.button("➕ إضافة صنف جديد", use_container_width=True, type="primary"):
        add_new_product()
        st.rerun()
with btn_col2:
    if st.button("💾 حفظ جميع التغييرات", use_container_width=True):
        for idx in range(len(st.session_state.products)):
            save_product(idx)
        st.success("✅ تم حفظ جميع الأصناف")

st.markdown("---")

# ====================== Products Table (Editable) ======================
st.subheader("📋 قائمة الأصناف")

# Display each product row
for idx, row in st.session_state.products.iterrows():
    with st.container():
        st.markdown(f"##### 🔹 الصنف رقم {idx + 1} - الكود: `{row['code']}`")
        
        # Create columns for better layout
        col_left, col_mid, col_right = st.columns([2, 2, 1])
        
        with col_left:
            # Product Name
            new_name = st.text_input(
                "اسم الصنف",
                value=row['name'],
                key=f"name_{idx}",
                placeholder="أدخل اسم المنتج"
            )
            
            # Description
            new_desc = st.text_area(
                "الوصف",
                value=row['description'],
                key=f"desc_{idx}",
                height=80,
                placeholder="وصف تفصيلي للمنتج..."
            )
            
            # Category
            new_category = st.text_input(
                "المجموعة",
                value=row['category'],
                key=f"cat_{idx}",
                placeholder="مثال: معقمات / أدوات جراحية / مستلزمات تمريض"
            )
        
        with col_mid:
            # Price and Currency
            price_col, currency_col = st.columns(2)
            with price_col:
                new_price = st.number_input(
                    "السعر",
                    value=float(row['price']),
                    step=0.5,
                    format="%.2f",
                    key=f"price_{idx}"
                )
            with currency_col:
                currency_options = {'ليرة سورية': 'SYP', 'دولار أمريكي': 'USD'}
                currency_labels = ['ليرة سورية', 'دولار أمريكي']
                current_currency_label = [k for k, v in currency_options.items() if v == row['currency']]
                current_idx = 0 if current_currency_label[0] == 'ليرة سورية' else 1 if current_currency_label else 0
                new_currency_label = st.selectbox(
                    "العملة",
                    options=currency_labels,
                    index=current_idx,
                    key=f"curr_{idx}"
                )
                new_currency = currency_options[new_currency_label]
            
            # SYP Price Display
            calculated_syp = calculate_syp_price(new_price, new_currency, st.session_state.exchange_rate)
            if new_currency == 'SYP':
                st.text_input(
                    "السعر بالليرة السورية",
                    value=f"{calculated_syp:,.0f} ل.س",
                    key=f"syp_{idx}",
                    disabled=True
                )
                st.caption("🔒 السعر بالليرة السورية (ثابت - اللون الباهت يشير إلى عدم التغيير)")
            else:
                st.text_input(
                    "السعر بالليرة السورية",
                    value=f"{calculated_syp:,.0f} ل.س",
                    key=f"syp_calc_{idx}",
                    disabled=True
                )
                st.caption("💱 تم الحساب تلقائياً حسب سعر الصرف")
            
            # Quantity
            new_qty = st.number_input(
                "الكمية المتوفرة",
                value=int(row['quantity']),
                step=1,
                key=f"qty_{idx}"
            )
        
        with col_right:
            # Image Preview
            st.markdown("**🖼️ معاينة الصورة**")
            uploaded_image = st.file_uploader(
                "رفع صورة المنتج",
                type=["png", "jpg", "jpeg", "webp"],
                key=f"img_{idx}",
                label_visibility="collapsed"
            )
            if uploaded_image is not None:
                st.image(uploaded_image, width=120, caption="معاينة")
                st.caption("✅ تم رفع الصورة")
            elif row['image']:
                st.info("صورة موجودة مسبقاً")
            else:
                st.caption("📷 لم يتم رفع صورة بعد")
        
        # Buttons for Offers and Bundles
        st.markdown("---")
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
        
        with btn_col1:
            if st.button("🎯 عروض", key=f"offer_btn_{idx}", use_container_width=True):
                st.session_state.show_offer_modal = True
                st.session_state.current_product_idx = idx
        
        with btn_col2:
            if st.button("📦 تحميل", key=f"bundle_btn_{idx}", use_container_width=True):
                st.session_state.show_bundle_modal = True
                st.session_state.current_product_idx = idx
        
        with btn_col3:
            if st.button("💾 حفظ هذا الصنف", key=f"save_{idx}", use_container_width=True):
                # Update DataFrame with current values
                st.session_state.products.at[idx, 'name'] = new_name
                st.session_state.products.at[idx, 'description'] = new_desc
                st.session_state.products.at[idx, 'category'] = new_category
                st.session_state.products.at[idx, 'price'] = new_price
                st.session_state.products.at[idx, 'currency'] = new_currency
                st.session_state.products.at[idx, 'quantity'] = new_qty
                save_product(idx)
                st.success(f"✅ تم حفظ {new_name or 'الصنف'} بنجاح")
                st.rerun()
        
        st.markdown("---")

# ====================== Offer Modal (Popup) ======================
if st.session_state.show_offer_modal and st.session_state.current_product_idx is not None:
    idx = st.session_state.current_product_idx
    product_name = st.session_state.products.at[idx, 'name'] or "هذا الصنف"
    
    with st.expander(f"🎯 إعداد العرض لـ {product_name}", expanded=True):
        st.markdown("### إضافة عرض أو هدية")
        
        offer_text = st.text_area(
            "نص العرض",
            value=st.session_state.products.at[idx, 'offer_text'],
            key="offer_text_input",
            placeholder="مثال: اشتري 4 قطع واحصل على قطعة مجانية",
            height=80
        )
        
        st.markdown("#### 🎁 إرفاق منتج هدية (اختياري)")
        
        # Get list of other products for gift
        other_products = []
        for i, row in st.session_state.products.iterrows():
            if i != idx and row['name']:
                other_products.append(f"{row['code']} - {row['name']}")
        
        gift_product = st.selectbox(
            "اختر المنتج الهدية",
            options=["لا يوجد"] + other_products,
            key="gift_select"
        )
        
        col_ok, col_cancel = st.columns(2)
        with col_ok:
            if st.button("✅ تأكيد العرض", use_container_width=True):
                st.session_state.products.at[idx, 'offer_text'] = offer_text
                if gift_product != "لا يوجد":
                    st.session_state.products.at[idx, 'gift_product'] = gift_product
                else:
                    st.session_state.products.at[idx, 'gift_product'] = ''
                st.success("✅ تم حفظ العرض بنجاح")
                st.session_state.show_offer_modal = False
                st.session_state.current_product_idx = None
                st.rerun()
        
        with col_cancel:
            if st.button("❌ إلغاء", use_container_width=True):
                st.session_state.show_offer_modal = False
                st.session_state.current_product_idx = None
                st.rerun()

# ====================== Bundle Modal (Popup) ======================
if st.session_state.show_bundle_modal and st.session_state.current_product_idx is not None:
    idx = st.session_state.current_product_idx
    product_name = st.session_state.products.at[idx, 'name'] or "هذا الصنف"
    
    with st.expander(f"📦 إعداد التحميل (ربط منتج كاسد) لـ {product_name}", expanded=True):
        st.markdown("### ربط منتج كاسد بمنتج رائج")
        
        # First field: ratio from current product
        st.markdown("#### من هذا المنتج (الرائج)")
        bundle_ratio = st.text_input(
            "العدد المطلوب من هذا المنتج",
            value=st.session_state.products.at[idx, 'bundle_ratio'],
            key="bundle_ratio_input",
            placeholder="مثال: 4 (يعني كل 4 قطع من هذا المنتج)",
            help="أدخل العدد المطلوب من هذا المنتج لتفعيل التحميل"
        )
        
        st.markdown("#### المنتج المحمَّل (الكاسد)")
        
        # Get list of other products for bundle
        other_products = []
        for i, row in st.session_state.products.iterrows():
            if i != idx and row['name']:
                other_products.append(f"{row['code']} - {row['name']}")
        
        bundle_product = st.selectbox(
            "اختر المنتج المحمَّل",
            options=["لا يوجد"] + other_products,
            key="bundle_select",
            help="المنتج الذي سيتم إضافته إجبارياً للفاتورة"
        )
        
        st.markdown("#### كمية المنتج المحمَّل")
        bundle_qty = st.number_input(
            "الكمية التي تضاف للفاتورة",
            min_value=1,
            value=1,
            step=1,
            key="bundle_qty",
            help="مثال: 1 (يعني تضاف وحدة واحدة من المنتج الكاسد)"
        )
        
        col_ok, col_cancel = st.columns(2)
        with col_ok:
            if st.button("✅ تأكيد التحميل", use_container_width=True):
                if bundle_product != "لا يوجد" and bundle_ratio:
                    st.session_state.products.at[idx, 'bundle_active'] = True
                    st.session_state.products.at[idx, 'bundle_main_product'] = bundle_product
                    st.session_state.products.at[idx, 'bundle_ratio'] = bundle_ratio
                    st.session_state.products.at[idx, 'bundle_qty'] = bundle_qty
                    st.success(f"✅ تم ربط {product_name} بـ {bundle_product} بنسبة {bundle_ratio}:{bundle_qty}")
                else:
                    st.warning("⚠️ يرجى اختيار المنتج المحمَّل وتحديد النسبة")
                    st.stop()
                st.session_state.show_bundle_modal = False
                st.session_state.current_product_idx = None
                st.rerun()
        
        with col_cancel:
            if st.button("❌ إلغاء", use_container_width=True):
                st.session_state.show_bundle_modal = False
                st.session_state.current_product_idx = None
                st.rerun()

# ====================== Footer ======================
st.markdown("---")
st.caption("© نظام إدارة المستودعات الطبية | جميع الحقوق محفوظة")