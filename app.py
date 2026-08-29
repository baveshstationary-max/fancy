from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st
import urllib.parse

# 1. Streamlit Page Configuration & Professional High-Contrast Styling CSS
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
    iframe[title="streamlit_app.manage"] {display: none !important;}
    .manage-app {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none;}
    
    /* Completely hide header link icons next to section headers */
    .stHeadingWithAction > a, .markdown-text-container a.anchor-link, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
    label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
        color: var(--text-color) !important;
        font-weight: 500 !important;
    }
    
    input, textarea, div[data-baseweb="select"] > div {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1.5px solid #cbd5e1 !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        border-radius: 6px !important;
    }

    .brand-banner {
        background: linear-gradient(135deg, #e0f2fe 100%, #bae6fd 0%);
        padding: 14px 18px;
        border-radius: 8px;
        color: #0f172a !important;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
        border: 1.5px solid #7dd3fc;
    }
    .brand-title {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #0f172a !important;
        margin: 0;
    }

    div.stButton > button {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        border: 1.5px solid #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 6px !important;
        padding: 0.4rem 0.5rem !important;
        width: 100% !important;
        display: block !important;
    }
    div.stButton > button:hover {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        border: 1px solid #94a3b8 !important;
    }

    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 0rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Headset"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Login sheet error: {e}")

# Customer Login Screen
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 20px; margin-bottom: 10px;'>
            <h1 style='font-size: 26px; font-weight: 700; margin-bottom: 2px;'>HM MOBILES</h1>
            <p style='font-size: 13px; font-weight: 400;'>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.5, 1, 1.5])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 20px; border-radius: 10px; border: 1.5px solid #cbd5e1; box-shadow: 0 4px 12px -3px rgba(0,0,0,0.05); text-align: center;'>
                    <h3 style='margin-top: 0; margin-bottom: 12px; font-size: 16px; font-weight: 600;'>Customer Portal Login</h3>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("customer_direct_login_center"):
                cust_name = st.text_input("Your Name:")
                cust_phone = st.text_input("Mobile Number:", max_chars=10)
                login_btn = st.form_submit_button("Secure Login", use_container_width=True)

                if login_btn:
                    if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                        st.session_state.logged_in_user = cust_name.strip()
                        st.session_state.user_phone = cust_phone.strip()
                        st.session_state.user_role = "Customer"
                        st.session_state.selected_menu = "Headset"
                        
                        log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")
    st.stop()

# Header & Navigation
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_comm, top_space, top_c1, top_c2, top_c3 = st.columns([2.8, 1.4, 0.8, 0.8, 0.8], gap="small")
with top_comm:
    st.markdown(f"👋 Welcome, **{st.session_state.logged_in_user}**!")
with top_space:
    st.empty()
with top_c1:
    if st.button("Home", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c2:
    cart_count = len(st.session_state.cart)
    if st.button(f"Cart ({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with top_c3:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

@st.cache_data(ttl=2)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df
    except Exception as e:
        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")
        return pd.DataFrame()

inv_df = load_inventory_from_sheet()

product_records = []
if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            product_records.append({
                "id": str(row.iloc[0]),
                "name": str(row.iloc[1]),
                "category": str(row.iloc[2]),
                "stock": str(row.iloc[3]),
                "price": str(row.iloc[4]),
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })
    except Exception:
        product_records = []

def process_cart_checkout(address: str, secondary_phone: str, description: str) -> str:
    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."
    
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
    st.session_state.last_booked_item = cart_summary

    try:
        order_data = {
            "Type": "Order",
            "Timestamp": timestamp,
            "Customer_Name": customer_name,
            "Primary_Phone": primary_phone,
            "Items": cart_summary,
            "Address": address,
            "Secondary_Phone": secondary_phone,
            "Description": description
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception as e:
        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Order successful (TXN ID: {txn_id})."

if st.session_state.current_view == "Home":
    col_menu, col_items = st.columns([1, 2.5], gap="small")

    with col_menu:
        st.markdown("Menu")
        with st.container(height=520, border=True):
            categories = list(set([p['category'] for p in product_records])) if product_records else ["Headset"]
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"Products: {current_cat}")
        with st.container(height=520, border=True):
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                for idx, prod in enumerate(filtered_items):
                    item_id = str(prod.get('id', idx))
                    item_name = prod.get('name', 'Product')
                    price = prod.get('price', '0')
                    desc = prod.get('description', '')
                    
                    # Process image names from Google Sheet and map them directly to GitHub raw folder links
                    img_raw = prod.get("image", "")
                    img_list = []
                    if img_raw and img_raw.strip() != "":
                        for part in img_raw.replace('\\', ',').split(','):
                            c_name = part.strip()
                            if c_name:
                                if c_name.startswith("http"):
                                    img_list.append(c_name)
                                else:
                                    encoded_name = urllib.parse.quote(c_name)
                                    github_raw = f"https://raw.githubusercontent.com/baveshstationary-max/baveshstationary-max/main/images/{encoded_name}"
                                    img_list.append(github_raw)
                                
                    while len(img_list) < 6:
                        if len(img_list) > 0:
                            img_list.append(img_list[0])
                        else:
                            img_list.append("https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=300")

                    # Render 6 full-size images side-by-side alongside description, price, and add quantity buttons
                    cols = st.columns([1, 1, 1, 1, 1, 1, 1.8, 0.7, 1.1])
                    
                    for i in range(6):
                        with cols[i]:
                            try:
                                st.image(img_list[i], use_container_width=True)
                            except:
                                st.image("https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=300", use_container_width=True)
                            
                    with cols[6]:
                        st.markdown(f"**{item_name}**")
                        if desc:
                            st.markdown(f"<span style='color: #666; font-size: 10px;'>{desc}</span>", unsafe_allow_html=True)
                            
                    with cols[7]:
                        st.markdown(f"**₹{price}**")
                        
                    with cols[8]:
                        current_qty = 1.0
                        q_val = st.number_input("Qty", min_value=1.0, value=current_qty, step=1.0, key=f"qty_{item_id}_{idx}", label_visibility="collapsed")
                        if st.button("Add", key=f"add_btn_{item_id}_{idx}", use_container_width=True):
                            full_q_str = f"{int(q_val)} Units"
                            st.session_state.cart.append({"product": item_name, "quantity": full_q_str})
                            st.success("Added!")
                            st.rerun()
                                
                    st.markdown("<hr style='margin: 3px 0px;'>", unsafe_allow_html=True)
            else:
                st.info("No items found.")

else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove Item", key=f"rem_cart_view_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Secure Checkout Form")
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Product Specifications / Custom Description:")
            
            submit_checkout = st.form_submit_button("Complete Order")
            if submit_checkout:
                if checkout_address and secondary_phone:
                    result_msg = process_cart_checkout(
                        checkout_address, secondary_phone, product_desc
                    )
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")
    else:
        _, center_msg_col, _ = st.columns([1, 2, 1])
        with center_msg_col:
            st.info("Your cart is empty. Click **Home** above to browse and add products.")
