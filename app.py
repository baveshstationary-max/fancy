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

# MAIN APP SCREEN (Two-Column Layout matching your new design)
else:
    # Stable Top Header
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

    # HOME PAGE: Split layout (Categories on Left | Products on Right)
    if st.session_state.page == "home":
        try:
            res = requests.get(f"{SCRIPT_URL}?action=getInventory")
            rows = res.json()
            if len(rows) > 1:
                headers = rows[0] 
                df = pd.DataFrame(rows[1:], columns=headers)
                
                # Get unique categories from data
                categories = df['CATEGORY'].dropna().unique().tolist() if 'CATEGORY' in df.columns else ["General"]
                if not st.session_state.selected_category and categories:
                    st.session_state.selected_category = categories[0]

                # TWO COLUMN MASTER-DETAIL LAYOUT (Left: Categories sidebar, Right: Product catalog)
                col_left, col_right = st.columns([1, 3])

                with col_left:
                    st.markdown("### Category")
                    st.markdown("---")
                    for cat in categories:
                        if st.button(f"📁 {cat}", use_container_width=True, key=f"cat_{cat}"):
                            st.session_state.selected_category = cat
                            st.rerun()

                with col_right:
                    active_cat = st.session_state.selected_category
                    st.markdown(f"### Products in: {active_cat}")
                    st.markdown("---")

                    # Filter products by selected category
                    filtered_df = df[df['CATEGORY'] == active_cat] if 'CATEGORY' in df.columns else df

                    if filtered_df.empty:
                        st.info("No products available in this category.")
                    else:
                        with st.container(height=550):
                            for index, row in filtered_df.iterrows():
                                item_id = str(row.get('ITEM ID', index))
                                item_name = row.get('ITEM NAME', 'Product')
                                price = row.get('PRICE', '0')
                                img_url = row.get("IMAGES") if row.get("IMAGES") else "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?q=80&w=500"
                                
                                p_col1, p_col2, p_col3 = st.columns([2, 2, 1.2])
                                
                                with p_col1:
                                    st.markdown(f"**Product NAME**")
                                    st.markdown(f"### {item_name}")
                                    st.markdown(f"PRICE")
                                    st.markdown(f"**Rs. {price}**")
                                    
                                with p_col2:
                                    st.markdown("**Product Image**")
                                    st.image(img_url, use_container_width=True)
                                    
                                with p_col3:
                                    st.markdown("**Qty / Add**")
                                    current_qty = st.session_state.cart.get(item_id, 0)
                                    st.markdown(f"Qty: {current_qty}")
                                    
                                    if st.button("➕ Add", key=f"add_{item_id}_{index}", use_container_width=True):
                                        st.session_state.cart[item_id] = current_qty + 1
                                        st.rerun()
                                    if current_qty > 0:
                                        if st.button("➖ Remove", key=f"sub_{item_id}_{index}", use_container_width=True):
                                            st.session_state.cart[item_id] = current_qty - 1
                                            if st.session_state.cart[item_id] == 0:
                                                del st.session_state.cart[item_id]
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
