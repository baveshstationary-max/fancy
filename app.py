import streamlit as st
import requests
import pandas as pd
import urllib.parse

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stHeadingWithAction > a, .markdown-text-container a.anchor-link, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
    /* 3D Product Carousel Container Perspective */
    div[data-testid="stHorizontalBlock"] {
        perspective: 1000px !important;
        align-items: center;
        gap: 4px;
    }
    
    /* Center Main Image (3D Pop-out Highlight) */
    div[data-testid="column"]:nth-of-type(3) img {
        width: 100% !important;
        height: 120px !important;
        object-fit: contain !important;
        background-color: #f8fafc;
        border-radius: 6px;
        border: 2px solid #ff4b4b !important;
        transform: translateZ(50px) scale(1.05) !important;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        box-shadow: 0 15px 25px rgba(0,0,0,0.25) !important;
        display: block;
        margin: auto;
        z-index: 10;
    }
    
    /* Left Adjacent Image (3D Rotated Left) */
    div[data-testid="column"]:nth-of-type(2) img {
        width: 100% !important;
        height: 85px !important;
        object-fit: contain !important;
        background-color: #f8fafc;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        transform: rotateY(25deg) translateZ(-20px) scale(0.9) !important;
        transition: transform 0.4s ease;
        opacity: 0.7;
        display: block;
        margin: auto;
    }
    
    /* Right Adjacent Image (3D Rotated Right) */
    div[data-testid="column"]:nth-of-type(4) img {
        width: 100% !important;
        height: 85px !important;
        object-fit: contain !important;
        background-color: #f8fafc;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        transform: rotateY(-25deg) translateZ(-20px) scale(0.9) !important;
        transition: transform 0.4s ease;
        opacity: 0.7;
        display: block;
        margin: auto;
    }
    
    .block-container { padding-top: 0.4rem; padding-bottom: 0.4rem; max-width: 100%; }
    h2 { margin-bottom: 0px; }
    .stButton button { padding: 2px 4px; font-size: 12px; font-weight: 600; min-height: 28px; width: 100%; }
    .element-container { margin-bottom: 0px !important; }
    hr { margin: 3px 0px !important; }
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
        st.markdown("### 📚 BAVESH STATIONARY")
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
            
    st.markdown("<hr style='margin: 2px 0px 6px 0px;'>", unsafe_allow_html=True)

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

                                cols = st.columns([0.4, 1.0, 1.2, 1.0, 0.4, 2.2, 0.7, 1.0])
                                
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
                                    st.markdown(f"**{item_name}**")
                                    if desc:
                                        st.markdown(f"<span style='color: #666; font-size: 10px;'>{desc}</span>", unsafe_allow_html=True)
                                        
                                with cols[6]:
                                    st.markdown(f"**₹{price}**")
                                    
                                with cols[7]:
                                    current_qty = st.session_state.cart.get(str(item_id), 1)
                                    qty = st.number_input("Qty", min_value=1, value=current_qty, key=f"qty_{item_id}", label_visibility="collapsed")
                                    if st.button("Add", key=f"add_{item_id}", use_container_width=True):
                                        st.session_state.cart[str(item_id)] = qty
                                        st.rerun()
                                        
                                st.markdown("<hr style='margin: 3px 0px;'>", unsafe_allow_html=True)
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
            custom_desc = st.text_area("Product Specifications / Custom Description:", placeholder="Specify any specific instructions
