import streamlit as st
import requests
import pandas as pd

# CONFIG & SETUP
SCRIPT_URL = "YOUR_GOOGLE_APPS_SCRIPT_URL"

st.set_page_config(page_title="Fancy Earrings Store", page_icon="✨", layout="centered")

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

# LOGIN SCREEN
if not st.session_state.logged_in:
    st.markdown("## 🔐 Store Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            res = requests.get(f"{SCRIPT_URL}?action=login&user={username}&pass={password}")
            data = res.json()
            if data.get("success"):
                st.session_state.logged_in = True
                st.session_state.role = data.get("role")
                st.rerun()
            else:
                st.error("Invalid login credentials")
        except Exception as e:
            st.error(f"Connection error: {e}")

# MAIN APP SCREEN
else:
    st.markdown("# ✨ Fancy Earrings Store")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛍️ Inventory Catalog (From Google Sheet)")

    # Fetch Inventory
    try:
        res = requests.get(f"{SCRIPT_URL}?action=getInventory")
        rows = res.json()
        if len(rows) > 1:
            headers = rows[0]
            df = pd.DataFrame(rows[1:], columns=headers)
            
            # Display items in a grid layout
            cols = st.columns(2)
            for index, row in df.iterrows():
                with cols[index % 2]:
                    img_url = row.get("images") or "https://images.unsplash.com/photo-1630019852942-f89202989a59?q=80&w=500"
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"**{row.get('Item_Name')}**")
                    st.markdown(f"Price: ₹{row.get('Price_INR')}")
                    st.markdown("---")
        else:
            st.info("No items found in inventory sheet.")
    except Exception as e:
        st.error(f"Could not load inventory: {e}")

    # PLACE ORDER FORM
    st.markdown("### 📦 Place an Order")
    with st.form("order_form"):
        cust_name = st.text_input("Customer Name")
        item_name = st.text_input("Earring Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        submit_btn = st.form_submit_button("Submit Order to Sheet")
        
        if submit_btn:
            order_data = {
                "orderId": "ORD-" + str(int(pd.Timestamp.now().timestamp())),
                "customer": cust_name,
                "itemName": item_name,
                "quantity": quantity
            }
            try:
                post_res = requests.post(SCRIPT_URL, json=order_data)
                if post_res.status_code == 200:
                    st.success("Order successfully recorded in Google Sheets!")
                else:
                    st.error("Failed to submit order.")
            except Exception as e:
                st.error(f"Error submitting order: {e}")
