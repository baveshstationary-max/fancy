import streamlit as st
import requests
import pandas as pd
import urllib.parse

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stHeadingWithAction > a, .markdown-text-container a.anchor-link, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
    /* LIGHT MODE DEFAULT VARIABLES & STYLING */
    :root {
        --bg-color: linear-gradient(135deg, #f0f4ff 0%, #fdf2f8 100%);
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
        --card-shadow: 0 6px 15px rgba(99, 102, 241, 0.08);
        --text-main: #1e1b4b;
        --text-desc: #db2777;
        --price-color: #4f46e5;
        --image-bg: linear-gradient(135deg, #ffffff 0%, #f3e8ff 100%);
    }

    /* DARK MODE AUTOMATIC OVERRIDES */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: linear-gradient(135deg, #0f172a 100%, #1e1b4b 100%);
            --card-bg: #1e293b;
            --card-border: #334155;
            --card-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
            --text-main: #f8fafc;
            --text-desc: #f472b6;
            --price-color: #818cf8;
            --image-bg: linear-gradient(135deg, #0f172a 0%, #312e81 100%);
        }
    }

    .stApp {
        background: var(--bg-color);
    }
    
    .product-card {
        background: var(--card-bg);
        border: 2px solid var(--card-border);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease-in-out;
    }
    
    .product-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }
    
    /* Vibrant Headings */
    h3 {
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* 3D Product Carousel Container Perspective */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 8px;
    }
    
    /* Center Main Image */
    div[data-testid="column"]:nth-of-type(3) img {
        width: 100% !important;
        height: 110px !important;
        object-fit: contain !important;
        background: var(--image-bg);
        border-radius: 10px;
        border: 2px solid #ec4899 !important;
        display: block;
        margin: auto;
    }
    
    /* Left and Right Adjacent Images */
    div[data-testid="column"]:nth-of-type(2) img,
    div[data-testid="column"]:nth-of-type(4) img {
        width: 100% !important;
        height: 75px !important;
        object-fit: contain !important;
        background-color: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--card-border);
        opacity: 0.75;
        display: block;
        margin: auto;
    }

    /* Mobile Optimization Styles */
    @media (max-width: 768px) {
        .product-card {
            padding: 10px;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column;
            align-items: center;
        }
        .stButton button {
            min-height: 40px;
            font-size: 14px;
        }
    }
    
    .block-container { padding-top: 0.8rem; padding-bottom: 0.8rem; max-width: 100%; }
    .stButton button { padding: 6px 10px; font-size: 13px; font-weight: 600; min-height: 36px; width: 100%; border-radius: 8px; }
    .element-container { margin-bottom: 0px !important; }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "mobile" not in st.session_state:
    st.session_state.mobile = ""
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "image_indices" not in st.session_state:
    st.session_state.image_indices = {}

# LOGIN SCREEN
if not st.session_state.logged_in:
    st.markdown("## 🔐 Store Login")
    username = st.text_input("Username")
    mobile = st.text_input("Mobile Number", type="password")
    
    if st.button("Login"):
        if username and mobile:
            try:
                requests.get(f"{SCRIPT_URL}?action=login&user={username}&pass={mobile}")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.mobile = mobile
                st.rerun()
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.error("Please fill in both fields")

# MAIN APP SCREEN
else:
    head_col1, head_col2, head_col3, head_col4 = st.columns([3, 1, 1, 1])
    with head_col1:
        st.markdown("### BAVESH STATIONARY")
    with head_col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with head_col3:
        cart_count = sum(st.session_state.cart.values())
        if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
            st.session_state.page = "cart"
            st.rerun()
    with head_col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()
            
    st.markdown("<hr style='margin: 4px 0px 10px 0px; border-color: var(--card-border);'>", unsafe_allow_html=True)

    # HOME PAGE
    if st.session_state.page == "home":
        try:
            res = requests.get(f"{SCRIPT_URL}?action=getInventory")
            rows = res.json()
            if len(rows) > 1:
                headers = [str(h).strip().upper() for h in rows[0]]
                df = pd.DataFrame(rows[1:], columns=headers)
                
                categories = df['CATEGORY'].dropna().unique().tolist() if 'CATEGORY' in df.columns else ["General"]
                if not st.session_state.selected_category and categories:
                    st.session_state.selected_category = categories[0]

                col_left, col_right = st.columns([1, 4])

                with col_left:
                    st.markdown("##### 📁 Categories")
                    with st.container(height=520):
                        for cat in categories:
                            is_active = (cat == st.session_state.selected_category)
                            btn_type = "primary" if is_active else "secondary"
                            if st.button(cat, use_container_width=True, key=f"cat_{cat}", type=btn_type):
                                st.session_state.selected_category = cat
                                st.rerun()

                with col_right:
                    active_cat = st.session_state.selected_category
                    st.markdown(f"##### Products: {active_cat}")
                    
                    filtered_df = df[df['CATEGORY'] == active_cat] if 'CATEGORY' in df.columns else df

                    if filtered_df.empty:
                        st.info("No products available in this category.")
                    else:
                        with st.container(height=520):
                            grouped_df = filtered_df.groupby('ITEM ID', sort=False)
                            
                            for item_id, group in grouped_df:
                                first_row = group.iloc[0]
                                item_name = first_row.get('ITEM NAME', 'Product')
                                price = first_row.get('PRICE', '0')
                                desc = first_row.get('DESCRIPTION', '')
                                
                                raw_list = []
                                for _, r in group.iterrows():
                                    img_raw = str(r.get('IMAGES', r.get('IMAGE', '')))
                                    if img_raw and img_raw.strip() != "":
                                        for part in img_raw.replace('\\', ',').split(','):
                                            c_name = part.strip()
                                            if c_name and not c_name.lower().endswith(('.mp4', '.mov', '.avi')):
                                                raw_list.append(c_name)

                                img_list = []
                                for name in raw_list:
                                    if name.startswith("http"):
                                        img_list.append(name)
                                    else:
                                        encoded_name = urllib.parse.quote(name)
                                        github_raw = f"https://raw.githubusercontent.com/baveshstationary-max/fancy/main/IMAGES/{encoded_name}"
                                        img_list.append(github_raw)
                                        
                                placeholder_url = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=300"
                                if not img_list:
                                    img_list = [placeholder_url]

                                idx_key = f"idx_{item_id}"
                                if idx_key not in st.session_state.image_indices:
                                    st.session_state.image_indices[idx_key] = 0

                                current_idx = st.session_state.image_indices[idx_key]
                                prev_idx = (current_idx - 1) % len(img_list)
                                next_idx = (current_idx + 1) % len(img_list)

                                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                                cols = st.columns([0.4, 0.9, 1.2, 0.9, 0.4, 2.2, 0.8, 1.1])
                                
                                with cols[0]:
                                    if st.button("◀", key=f"prev_{item_id}", use_container_width=True):
                                        st.session_state.image_indices[idx_key] = (st.session_state.image_indices[idx_key] + 1) % len(img_list)
                                        st.rerun()

                                with cols[1]:
                                    st.image(img_list[prev_idx], use_container_width=True)

                                with cols[2]:
                                    st.image(img_list[current_idx], use_container_width=True)

                                with cols[3]:
                                    st.image(img_list[next_idx], use_container_width=True)

                                with cols[4]:
                                    if st.button("▶", key=f"next_{item_id}", use_container_width=True):
                                        st.session_state.image_indices[idx_key] = (st.session_state.image_indices[idx_key] - 1) % len(img_list)
                                        st.rerun()
                                        
                                with cols[5]:
                                    st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: var(--text-main);'>{item_name}</div>", unsafe_allow_html=True)
                                    if desc:
                                        st.markdown(f"<div style='color: var(--text-desc); font-size: 11px; margin-top: 2px; font-weight: 500;'>{desc}</div>", unsafe_allow_html=True)
                                        
                                with cols[6]:
                                    st.markdown(f"<div style='font-size: 16px; font-weight: 800; color: var(--price-color); margin-top: 6px;'>₹{price}</div>", unsafe_allow_html=True)
                                    
                                with cols[7]:
                                    current_qty = st.session_state.cart.get(str(item_id), 1)
                                    qty = st.number_input("Qty", min_value=1, value=current_qty, key=f"qty_{item_id}", label_visibility="collapsed")
                                    if st.button("Add to Cart", key=f"add_{item_id}", use_container_width=True):
                                        st.session_state.cart[str(item_id)] = qty
                                        st.rerun()
                                        
                                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No products found in inventory.")
        except Exception as e:
            st.error(f"Could not load catalog: {e}")

    # CART PAGE
    elif st.session_state.page == "cart":
        st.markdown("#### 📌 Secure Checkout Form")
        if not st.session_state.cart:
            st.info("Your cart is empty. Go back to Home to select products.")
        else:
            for item_id, qty in st.session_state.cart.items():
                st.markdown(f"- **Item ID:** {item_id} | **Quantity:** {qty}")
            
            st.markdown("---")
            
            delivery_address = st.text_area("Delivery Address:", placeholder="Enter your full street address, landmark, and pin code...")
            alt_contact = st.text_input("Alternative Contact Number:", placeholder="Enter secondary mobile number...")
            custom_desc = st.text_area("Product Specifications / Custom Description:", placeholder="Specify any specific instructions, colors, or custom requirements...")
            
            if st.button("Complete Order", use_container_width=False):
                if not delivery_address.strip():
                    st.error("Please enter a delivery address before completing your order.")
                else:
                    try:
                        res = requests.get(f"{SCRIPT_URL}?action=getInventory")
                        rows = res.json()
                        item_prices = {}
                        if len(rows) > 1:
                            headers = [str(h).strip().upper() for h in rows[0]]
                            inv_df = pd.DataFrame(rows[1:], columns=headers)
                            if 'ITEM ID' in inv_df.columns and 'PRICE' in inv_df.columns:
                                for _, row in inv_df.iterrows():
                                    item_prices[str(row['ITEM ID'])] = float(row['PRICE'])

                        for item_id, qty in st.session_state.cart.items():
                            unit_price = item_prices.get(str(item_id), 0.0)
                            total_cost = qty * unit_price
                            
                            order_data = {
                                "mobile": st.session_state.mobile,
                                "altContact": alt_contact,
                                "deliveryAddress": delivery_address,
                                "customDescription": custom_desc,
                                "itemId": item_id,
                                "itemName": f"Item {item_id}",
                                "quantity": qty,
                                "totalCost": total_cost
                            }
                            requests.post(SCRIPT_URL, json=order_data)
                        
                        st.success("Order successfully submitted to Google Sheets!")
                        st.session_state.cart = {}
                    except Exception as e:
                        st.error(f"Error checking out: {e}")
