import streamlit as st
import requests
import pandas as pd

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="📚", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.mobile = ""
    st.session_state.page = "home"
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

# MAIN APP SCREEN (Sticky Header + Scrollable Body)
else:
    # STABLE / STICKY HEADER (Stays fixed at the top)
    st.markdown("### BAVESH STATIONARY")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("HOME", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        cart_count = sum(st.session_state.cart.values())
        if st.button(f"CART ({cart_count})", use_container_width=True):
            st.session_state.page = "cart"
            st.rerun()
    with col3:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()
            
    st.markdown("---")

    # SCROLLABLE CONTENT AREA
    if st.session_state.page == "home":
        st.markdown("#### Category: Products")
        
        try:
            res = requests.get(f"{SCRIPT_URL}?action=getInventory")
            rows = res.json()
            if len(rows) > 1:
                headers = rows[0] 
                df = pd.DataFrame(rows[1:], columns=headers)
                
                # Scrollable container for product list
                with st.container(height=500):
                    for index, row in df.iterrows():
                        item_id = row.get('ITEM ID', str(index))
                        item_name = row.get('ITEM NAME', 'Product')
                        price = row.get('PRICE', '0')
                        img_url = row.get("IMAGES") if row.get("IMAGES") else "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?q=80&w=500"
                        
                        # Product Layout mimicking your sketch
                        col_info, col_img, col_action = st.columns([2, 2, 1])
                        
                        with col_info:
                            st.markdown(f"**{item_name}**")
                            st.markdown(f"PRICE")
                            st.markdown(f"**Rs. {price}**")
                            
                        with col_img:
                            st.image(img_url, use_container_width=True)
                            
                        with col_action:
                            current_qty = st.session_state.cart.get(item_id, 0)
                            st.markdown(f"Qty: {current_qty}")
                            if st.button("➕ Add", key=f"add_{item_id}"):
                                st.session_state.cart[item_id] = current_qty + 1
                                st.rerun()
                            if current_qty > 0:
                                if st.button("➖ Remove", key=f"sub_{item_id}"):
                                    st.session_state.cart[item_id] = current_qty - 1
                                    if st.session_state.cart[item_id] == 0:
                                        del st.session_state.cart[item_id]
                                    st.rerun()
                                    
                        st.markdown("---")
            else:
                st.info("No products found in inventory.")
        except Exception as e:
            st.error(f"Could not load catalog: {e}")

    elif st.session_state.page == "cart":
        st.markdown("#### 🛒 Your Shopping Cart")
        if not st.session_state.cart:
            st.info("Your cart is empty.")
        else:
            total_bill = 0
            for item_id, qty in st.session_state.cart.items():
                st.markdown(f"- Item ID: {item_id} | Quantity: {qty}")
            
            if st.button("Checkout & Send Order to Sheet"):
                try:
                    for item_id, qty in st.session_state.cart.items():
                        order_data = {
                            "mobile": st.session_state.mobile,
                            "itemId": item_id,
                            "itemName": f"Item {item_id}",
                            "quantity": qty,
                            "totalCost": qty * 500 # Adjust price calculation as needed
                        }
                        requests.post(SCRIPT_URL, json=order_data)
                    
                    st.success("Orders successfully placed and saved to Google Sheets!")
                    st.session_state.cart = {}
                except Exception as e:
                    st.error(f"Error checking out: {e}")
