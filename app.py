import streamlit as st
import requests
import pandas as pd
import urllib.parse

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="📚", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stHeadingWithAction > a, .markdown-text-container a.anchor-link, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
    /* Mobile App Shell Wrapper */
    .block-container { 
        padding-top: 0.5rem; 
        padding-bottom: 0.5rem; 
        max-width: 480px !important; 
        margin: auto;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Force images to display properly on mobile narrow screens */
    img {
        width: 100% !important;
        height: auto !important;
        max-height: 110px !important;
        object-fit: contain !important;
        background-color: #f8fafc;
        border-radius: 4px;
        display: block !important;
        visibility: visible !important;
    }
    
    h2 { margin-bottom: 0px; font-size: 1.3rem; }
    h3 { font-size: 1.1rem; }
    .stButton button { padding: 2px 4px; font-size: 11px; font-weight: 600; min-height: 28px; width: 100%; }
    div[data-testid="stHorizontalBlock"] { align-items: center; gap: 2px; }
    .element-container { margin-bottom: 0px !important; }
    hr { margin: 4px 0px !important; }
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

# MAIN APP SCREEN (Mobile Stacked Layout for Image Visibility)
else:
    head_col1, head_col2, head_col3, head_col4 = st.columns([2.2, 1, 1, 1])
    with head_col1:
        st.markdown("### 📚 BAVESH")
    with head_col2:
        if st.button("🏠", use_container_width=True, help="Home"):
            st.session_state.page = "home"
            st.rerun()
    with head_col3:
        cart_count = sum(st.session_state.cart.values())
        if st.button(f"🛒({cart_count})", use_container_width=True, help="Cart"):
            st.session_state.page = "cart"
            st.rerun()
    with head_col4:
        if st.button("🚪", use_container_width=True, help="Logout"):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()
            
    st.markdown("<hr style='margin: 2px 0px 4px 0px;'>", unsafe_allow_html=True)

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

                st.markdown("##### 📁 Categories")
                selected_cat = st.selectbox("Select Category", categories, index=categories.index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0, label_visibility="collapsed")
                if selected_cat != st.session_state.selected_category:
                    st.session_state.selected_category = selected_cat
                    st.rerun()

                st.markdown(f"##### Products: {st.session_state.selected_category}")
                
                filtered_df = df[df['CATEGORY'] == st.session_state.selected_category] if 'CATEGORY' in df.columns else df

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

                            # Mobile-optimized card layout using 3 vertical rows to prevent squeezing out images
                            
                            # Row 1: 3-column Image Carousel (Prev, Center, Next) with navigation buttons cleanly below/beside
                            img_cols = st.columns([1, 2.5, 1])
                            with img_cols[0]:
                                if st.button("◀ Prev", key=f"prev_{item_id}", use_container_width=True):
                                    st.session_state.image_indices[idx_key] = (st.session_state.image_indices[idx_key] + 1) % len(img_list)
                                    st.rerun()
                                st.image(img_list[prev_idx], use_container_width=True)
                            with img_cols[1]:
                                st.image(img_list[current_idx], use_container_width=True)
                            with img_cols[2]:
                                if st.button("Next ▶", key=f"next_{item_id}", use_container_width=True):
                                    st.session_state.image_indices[idx_key] = (st.session_state.image_indices[idx_key] - 1) % len(img_list)
                                    st.rerun()
                                st.image(img_list[next_idx], use_container_width=True)

                            # Row 2: Product Name, Description & Price
                            info_cols = st.columns([2.5, 1])
                            with info_cols[0]:
                                st.markdown(f"**{item_name}**")
                                if desc:
                                    st.markdown(f"<span style='color: #666; font-size: 10px;'>{desc}</span>", unsafe_allow_html=True)
                            with info_cols[1]:
                                st.markdown(f"**₹{price}**")

                            # Row 3: Quantity Counter & Add to Cart Button
                            cart_cols = st.columns([1.2, 1])
                            with cart_cols[0]:
                                current_qty = st.session_state.cart.get(str(item_id), 1)
                                qty = st.number_input("Qty", min_value=1, value=current_qty, key=f"qty_{item_id}", label_visibility="collapsed")
                            with cart_cols[1]:
                                if st.button("Add to Cart", key=f"add_{item_id}", use_container_width=True):
                                    st.session_state.cart[str(item_id)] = qty
                                    st.success(f"Added!")
                                    st.rerun()
                                    
                            st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)
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
            
            delivery_address = st.text_area("Delivery Address:", placeholder="Enter full address & pin code...")
            alt_contact = st.text_input("Alternative Contact Number:", placeholder="Secondary mobile number...")
            custom_desc = st.text_area("Product Specifications / Custom Description:", placeholder="Instructions or custom requirements...")
            
            if st.button("Complete Order", use_container_width=True):
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
