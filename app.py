import streamlit as st
import requests
import pandas as pd

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="📚", layout="wide")

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

# MAIN APP SCREEN (Matching your exact horizontal layout: Categories on Left | Images / Description / Pricing & Add on Right)
else:
    st.markdown("<h2 style='text-align: center;'>BAVESH STATIONARY</h2>", unsafe_allow_html=True)
    
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("HOME", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with nav2:
        cart_count = sum(st.session_state.cart.values())
        if st.button(f"CART ({cart_count})", use_container_width=True):
            st.session_state.page = "cart"
            st.rerun()
    with nav3:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()
            
    st.markdown("---")

    # HOME PAGE
    if st.session_state.page == "home":
        try:
            res = requests.get(f"{SCRIPT_URL}?action=getInventory")
            rows = res.json()
            if len(rows) > 1:
                headers = rows[0] 
                df = pd.DataFrame(rows[1:], columns=headers)
                
                categories = df['CATEGORY'].dropna().unique().tolist() if 'CATEGORY' in df.columns else ["General"]
                if not st.session_state.selected_category and categories:
                    st.session_state.selected_category = categories[0]

                # Two-column layout: Left = Categories, Right = Products horizontal row layout
                col_left, col_right = st.columns([1, 4])

                with col_left:
                    st.markdown("### Category")
                    st.markdown("---")
                    for cat in categories:
                        if st.button(f"📁 {cat}", use_container_width=True, key=f"cat_{cat}"):
                            st.session_state.selected_category = cat
                            st.rerun()

                with col_right:
                    active_cat = st.session_state.selected_category
                    st.markdown(f"### Category: {active_cat}")
                    st.markdown("---")

                    filtered_df = df[df['CATEGORY'] == active_cat] if 'CATEGORY' in df.columns else df

                    if filtered_df.empty:
                        st.info("No products available in this category.")
                    else:
                        with st.container(height=600):
                            for index, row in filtered_df.iterrows():
                                item_id = str(row.get('ITEM ID', index))
                                item_name = row.get('ITEM NAME', 'Product')
                                price = row.get('PRICE', '0')
                                desc = row.get('DESCRIPTION', 'No description available.')
                                img_url = row.get("IMAGES") if row.get("IMAGES") else "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=500"
                                
                                # Exact horizontal breakdown matching your UI sample image
                                img_col, desc_col, buy_col = st.columns([1.5, 2, 2])
                                
                                with img_col:
                                    st.image(img_url, use_container_width=True)
                                    
                                with desc_col:
                                    st.markdown("**Description:**")
                                    st.markdown(f"<p style='color: gray; font-size: 14px;'>{desc}</p>", unsafe_allow_html=True)
                                    
                                with buy_col:
                                    st.markdown(f"**{item_name}**")
                                    st.markdown(f"### ₹{price}")
                                    
                                    current_qty = st.session_state.cart.get(item_id, 1)
                                    
                                    qty_col, add_col = st.columns([1, 1.5])
                                    with qty_col:
                                        qty = st.number_input("Qty", min_value=1, value=current_qty, key=f"qty_{item_id}_{index}", label_visibility="collapsed")
                                    with add_col:
                                        if st.button("Add", key=f"add_{item_id}_{index}", use_container_width=True):
                                            st.session_state.cart[item_id] = qty
                                            st.success(f"Added {qty} item(s)")
                                            st.rerun()
                                            
                                st.markdown("---")
            else:
                st.info("No products found in inventory.")
        except Exception as e:
            st.error(f"Could not load catalog: {e}")

    # CART PAGE
    elif st.session_state.page == "cart":
        st.markdown("#### 🛒 Your Shopping Cart")
        if not st.session_state.cart:
            st.info("Your cart is empty. Go back to HOME to select products.")
        else:
            for item_id, qty in st.session_state.cart.items():
                st.markdown(f"**Item ID:** {item_id} | **Quantity:** {qty}")
            
            st.markdown("---")
            if st.button("Checkout & Submit Order to Sheet", use_container_width=True):
                try:
                    for item_id, qty in st.session_state.cart.items():
                        order_data = {
                            "mobile": st.session_state.mobile,
                            "itemId": item_id,
                            "itemName": f"Item {item_id}",
                            "quantity": qty,
                            "totalCost": qty * 500
                        }
                        requests.post(SCRIPT_URL, json=order_data)
                    
                    st.success("Order successfully sent to Google Sheets!")
                    st.session_state.cart = {}
                except Exception as e:
                    st.error(f"Error checking out: {e}")
