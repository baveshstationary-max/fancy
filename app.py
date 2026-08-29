import streamlit as st
import requests
import pandas as pd

SCRIPT_URL = "YOUR_GOOGLE_APPS_SCRIPT_URL"

st.set_page_config(page_title="Fancy Earrings Store", page_icon="✨", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# LOGIN SCREEN
if not st.session_state.logged_in:
    st.markdown("## 🔐 Store Login")
    username = st.text_input("Username")
    mobile = st.text_input("Mobile Number", type="password")
    
    if st.button("Login"):
        try:
            res = requests.get(f"{SCRIPT_URL}?action=login&user={username}&pass={mobile}")
            data = res.json()
            if data.get("success"):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.mobile = mobile
                st.rerun()
            else:
                st.error("Invalid Username or Mobile Number")
        except Exception as e:
            st.error(f"Connection error: {e}")

# MAIN APP SCREEN
else:
    st.markdown(f"# ✨ Welcome, {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛍️ Product Catalog")

    # Fetch Inventory from PRODUCT UPLOAD sheet
    try:
        res = requests.get(f"{SCRIPT_URL}?action=getInventory")
        rows = res.json()
        if len(rows) > 1:
            headers = rows[0] # ITEM ID, ITEM NAME, CATEGORY, STOCK, PRICE, DESCRIPTION, IMAGES
            df = pd.DataFrame(rows[1:], columns=headers)
            
            cols = st.columns(2)
            for index, row in df.iterrows():
                with cols[index % 2]:
                    img_url = row.get("IMAGES") if row.get("IMAGES") else "https://images.unsplash.com/photo-1630019852942-f89202989a59?q=80&w=500"
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"**{row.get('ITEM NAME')}** (ID: {row.get('ITEM ID')})")
                    st.markdown(f"Price: ₹{row.get('PRICE')}")
                    st.markdown(f"Stock: {row.get('STOCK')}")
                    st.markdown("---")
        else:
            st.info("No products found in inventory.")
    except Exception as e:
        st.error(f"Could not load catalog: {e}")

    # PLACE ORDER FORM (matches ORDERS sheet columns)
    st.markdown("### 📦 Place an Order")
    with st.form("order_form"):
        item_id = st.text_input("Item ID")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        price_per_item = st.number_input("Price per Item (₹)", min_value=0.0, value=0.0)
        
        submit_btn = st.form_submit_button("Submit Order")
        
        if submit_btn:
            total_cost = quantity * price_per_item
            order_data = {
                "mobile": st.session_state.mobile,
                "itemId": item_id,
                "itemName": item_name,
                "quantity": quantity,
                "totalCost": total_cost
            }
            try:
                post_res = requests.post(SCRIPT_URL, json=order_data)
                if post_res.status_code == 200:
                    st.success("Order successfully sent to your Google Sheet!")
                else:
                    st.error("Failed to submit order.")
            except Exception as e:
                st.error(f"Error submitting order: {e}")
