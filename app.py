from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Professional High-Contrast Styling CSS
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Apply Professional Font Family Globally */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Hide Streamlit default top header, menu, share, github, and floating badges/links */
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
        a.stMarkdownHeaderLink {display: none !important;}
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {display: none !important;}
        
        /* Automatically adapt text color based on Streamlit's active theme (Dark/Light Mode) */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 600 !important;
        }
        
        /* Input boxes styling supporting both modes */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
        }

        /* Professional Neutral Dark/Slate Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #1e293b 100%, #334155 0%);
            padding: 14px 18px;
            border-radius: 8px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 12px;
        }
        .brand-title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }

        /* Compact, Full-Width Buttons tightly fitted inside columns */
        div.stButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 750 !important;
            font-size: 16px !important;
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

        /* ============================================================
           LOGIN SCREEN - RESPONSIVE WITHOUT COLUMNS
           ============================================================ */

        .hm-login-wrapper {
            width: min(430px, 100%) !important;
            max-width: 430px !important;
            margin: 10px auto 0 auto !important;
            box-sizing: border-box !important;
        }

        .hm-login-card {
            width: 100% !important;
            box-sizing: border-box !important;
            padding: 16px 14px 3px 14px !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px 10px 0 0 !important;
            text-align: center !important;
        }

        .hm-login-card h3 {
            margin: 0 0 8px 0 !important;
            font-size: 16px !important;
            font-weight: 750 !important;
        }

        .hm-login-wrapper [data-testid="stForm"] {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            padding: 8px 14px 14px 14px !important;
            border: 1.5px solid #cbd5e1 !important;
            border-top: 0 !important;
            border-radius: 0 0 10px 10px !important;
        }

        .hm-login-wrapper input,
        .hm-login-wrapper button {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* ============================================================
           RESPONSIVE LAYOUT
           Same structure on desktop AND mobile:
           HEADER
           Welcome | Home | Cart | Logout
           MENU    | PRODUCT
           Image   | Description | Price
           ============================================================ */

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }

        .block-container {
            padding-top: 0.8rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* Never let Streamlit columns wrap into a second line. */
        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            flex-wrap: nowrap !important;
            box-sizing: border-box !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }

        /* Header navigation */
        .hm-top-nav {
            width: 100% !important;
            max-width: 100% !important;
        }

        .hm-top-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }

        .hm-top-nav div.stButton > button {
            width: 100% !important;
            min-width: 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            font-size: clamp(10px, 2.2vw, 16px) !important;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }

        /* Main MENU | PRODUCT layout */
        .hm-main-layout,
        .hm-main-layout > div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        .hm-main-layout div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
        }

        /* Product IMAGE | DESCRIPTION | PRICE row */
        .hm-product-row {
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        .hm-product-row div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
            flex-wrap: nowrap !important;
        }

        .hm-product-row div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
            overflow: hidden !important;
        }

        .hm-product-row img {
            max-width: 100% !important;
            height: auto !important;
            object-fit: contain !important;
        }

        .hm-product-row p,
        .hm-product-row span {
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        @media (max-width: 600px) {
            .hm-login-wrapper {
                width: 100% !important;
                max-width: 100% !important;
                margin-top: 5px !important;
            }

            .hm-login-card {
                padding: 12px 9px 2px 9px !important;
            }

            .hm-login-wrapper [data-testid="stForm"] {
                padding: 6px 9px 10px 9px !important;
            }

            .hm-login-heading h1 {
                font-size: 23px !important;
                line-height: 1.15 !important;
            }

            .hm-login-heading p {
                font-size: 11px !important;
                line-height: 1.25 !important;
                overflow-wrap: anywhere !important;
            }

            .block-container {
                padding-left: 3px !important;
                padding-right: 3px !important;
            }

            .brand-banner {
                padding: 8px 4px !important;
                margin-bottom: 5px !important;
            }

            .brand-title {
                font-size: clamp(13px, 4vw, 20px) !important;
                letter-spacing: 0 !important;
            }

            .hm-top-nav div.stButton > button {
                font-size: 10px !important;
                padding: 0.25rem 1px !important;
            }

            .hm-product-row div.stButton > button {
                font-size: 10px !important;
                padding: 0.25rem 1px !important;
            }

            .hm-product-row div[data-testid="stImage"] img {
                max-width: 100% !important;
            }
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

# Google Apps Script Web App Endpoint URL Updated
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"


# Function to log customer login into the "LOGIN" tab
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


# 2. Responsive Customer Login Screen (Before Login)
if not st.session_state.logged_in_user:
    st.markdown("""
        <div class='hm-login-heading' style='text-align: center; margin-top: 20px; margin-bottom: 10px;'>
            <h1 style='font-size: 26px; font-weight: 800; margin-bottom: 2px;'>HM MOBILES</h1>
            <p style='font-size: 13px; font-weight: 500;'>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)

    # IMPORTANT: no st.columns() here.
    # The previous [1.5, 1, 1.5] columns were squeezing the login form on phones.
    st.markdown('<div class="hm-login-wrapper">', unsafe_allow_html=True)

    st.markdown("""
        <div class='hm-login-card'>
            <h3>Customer Portal Login</h3>
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

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# --- AFTER LOGIN: COMPACT PROFESSIONAL HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

# Commercial banner area on the left and right-aligned navigation buttons on the right
st.markdown('<div class="hm-top-nav">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")


# Load Inventory Directly from Google Sheets CSV Link with Short TTL Cache
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


# Load Product Records from Google Sheet Data dynamically with correct index mapping (Description is Column F -> Index 5, Image is Column G -> Index 6)
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

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "images/Headset 1 1.jpg \\ images/Headset 1 2.jpg \\ images/Headset 1 3.jpg", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
    ]


def process_cart_checkout(address: str, secondary_phone: str, description: str, payment_method: str, location_link: str) -> str:
    """Checkout all items currently in the cart with delivery and payment details, and send to Google Sheet 'HM Mobiles Orders'."""
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
            "Description": description,
            "Live_Location": location_link
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception as e:
        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description", "Live Location"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description, location_link])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Payment via {payment_method} successful (TXN ID: {txn_id})."


# View Switching: Home View vs Cart/Checkout View
if st.session_state.current_view == "Home":
    st.markdown('<div class="hm-main-layout">', unsafe_allow_html=True)
    col_menu, col_items = st.columns([1, 2.5], gap="small")

    # --- SECTION 1: MENU ---
    with col_menu:
        st.markdown("Menu")
        with st.container(height=480, border=True):
            categories = list(set([p['category'] for p in product_records]))
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.rerun()

    # --- SECTION 2: ITEMS ---
    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"{current_cat}")
        with st.container(height=480, border=True):
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                for idx, prod in enumerate(filtered_items):
                    slide_key = f"slide_{current_cat}_{idx}"
                    
                    if slide_key not in st.session_state:
                        st.session_state[slide_key] = 0

                    # Same product structure on desktop and mobile:
                    # IMAGE | DESCRIPTION | PRICE / QTY / ADD
                    st.markdown('<div class="hm-product-row">', unsafe_allow_html=True)
                    p_img_col, p_desc_col, p_details_col = st.columns([1.35, 1.25, 1], gap="small")

                    with p_img_col:
                        raw_img = prod.get("image", "")
                        if raw_img:
                            img_paths = [img.strip() for img in raw_img.replace("\\", ",").split(",") if img.strip()]
                            valid_paths = [p for p in img_paths if os.path.exists(p)]
                            if valid_paths:
                                total_imgs = len(valid_paths)
                                current_idx = st.session_state[slide_key]
                                
                                l_btn, img_display, r_btn = st.columns([0.45, 3.1, 0.45], gap="small")
                                
                                with l_btn:
                                    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                                    if st.button("‹", key=f"prev_{current_cat}_{idx}"):
                                        if st.session_state[slide_key] > 0:
                                            st.session_state[slide_key] -= 1
                                        else:
                                            st.session_state[slide_key] = total_imgs - 1
                                        st.rerun()
                                        
                                with img_display:
                                    if total_imgs >= 2:
                                        sub_col1, sub_col2 = st.columns(2, gap="small")
                                        with sub_col1:
                                            _, center_sub1, _ = st.columns([1, 4, 1])
                                            with center_sub1:
                                                st.image(valid_paths[current_idx], width=95)
                                        with sub_col2:
                                            _, center_sub2, _ = st.columns([1, 4, 1])
                                            with center_sub2:
                                                next_idx = (current_idx + 1) % total_imgs
                                                st.image(valid_paths[next_idx], width=95)
                                    else:
                                        _, center_img_col, _ = st.columns([1, 4, 1])
                                        with center_img_col:
                                            st.image(valid_paths[0], width=95)
                                        
                                with r_btn:
                                    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                                    if st.button("›", key=f"next_{current_cat}_{idx}"):
                                        if st.session_state[slide_key] + 1 < total_imgs:
                                            st.session_state[slide_key] += 1
                                        else:
                                            st.session_state[slide_key] = 0
                                        st.rerun()
                            else:
                                st.caption("No Image")
                        else:
                            st.caption("No Image")
                            
                    with p_desc_col:
                        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                        st.markdown("**Description:**")
                        st.caption(prod.get('description', ''))

                    with p_details_col:
                        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"**{prod['name']}**")
                        st.markdown(f"₹{prod['price']}")
                        
                        q_col, b_col = st.columns([1, 1], gap="small")
                        with q_col:
                            q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                        with b_col:
                            if st.button("Add", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                                full_q_str = f"{int(q_val)} Units"
                                st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                                st.success(f"Added!")
                                st.rerun()
                                    
                    st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px; border: none; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No items found.")

    st.markdown('</div>', unsafe_allow_html=True)

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
            payment_method = st.selectbox("Payment Method", ["UPI / GPay", "Credit/Debit Card", "Cash on Delivery"])
            live_location = st.text_input("Live Location Link (Google Maps Share URL):")
            
            submit_checkout = st.form_submit_button("Complete Order & Pay")
            if submit_checkout:
                if checkout_address and secondary_phone:
                    result_msg = process_cart_checkout(
                        checkout_address, secondary_phone, product_desc, payment_method, live_location
                    )
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")
    else:
        st.info("Your cart is empty. Click **Home** above to browse and add products.")
