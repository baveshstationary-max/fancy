import streamlit as st
import requests
import pandas as pd

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(page_title="Bavesh Stationary", page_icon="📚", layout="wide")

# Custom CSS to force 6 images side-by-side in a single row and maximize screen space
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 0.3rem; padding-bottom: 0.3rem; max-width: 100%; }
    h2 { margin-bottom: 0px; }
    .stButton button { padding: 2px 4px; font-size: 11px; font-weight: 500; min-height: 24px; }
    div[data-testid="stHorizontalBlock"] { align-items: center; gap: 4px; }
    .element-container { margin-bottom: 0px !important; }
    hr { margin: 2px 0px !important; }
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
            
    st.markdown("<hr style='margin: 2px 0px 4px 0px;'>", unsafe_allow_html=True)

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

                col_left, col_right = st.columns([1, 5])

                with col_left:
                    st.markdown("##### 📁 Categories")
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
                            for index, row in filtered_df.iterrows():
                                item_id = str(row.get('ITEM ID', index))
                                item_name = row.get('ITEM NAME', 'Product')
                                price = row.get('PRICE', '0')
                                
                                # Fetch up to 6 image columns or fall back to comma-separated images/defaults
                                img_list = []
                                for col_name in ['IMAGE1', 'IMAGE2', 'IMAGE3', 'IMAGE4', 'IMAGE5', 'IMAGE6']:
                                    if col_name in row and row[col_name]:
                                        img_list.append(row[col_name])
                                
                                if not img_list and 'IMAGES' in row and row['IMAGES']:
                                    img_list = [img.strip() for img in str(row['IMAGES']).split(',')]

                                # Ensure we have 6 image slots to display side-by-side in a single row
                                while len(img_list) < 6:
                                    img_list.append("https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=150")

                                # Render exactly 6 images in a single row alongside product details and add button
                                cols = st.columns([1, 1, 1, 1, 1, 1, 2, 1, 1.2])
                                
                                for i in range(6):
                                    with cols[i]:
                                        st.image(img_list[i], width=50)
                                        
                                with cols[6]:
                                    st.markdown(f"**{item_name}**")
                                    st.markdown(f"<span style='color: #666; font-size: 10px;'>₹{price}</span>", unsafe_allow_html=True)
                                    
                                with cols[7]:
                                    current_qty = st.session_state.cart.get(item_id, 1)
                                    qty = st.number_input("Qty", min_value=1, value=current_qty, key=f"qty_{item_id}_{index}", label_visibility="collapsed")
                                    
                                with cols[8]:
                                    if st.button("Add", key=f"add_{item_id}_{index}", use_container_width=True):
                                        st.session_state.cart[item_id] = qty
                                        st.rerun()
                                            
                                st.markdown("<hr style='margin: 2px 0px;'>", unsafe_allow_html=True)
            else:
                st.info("No products found in inventory.")
        except Exception as e:
            st.error(f"Could not load catalog: {e}")

    # CART PAGE
    elif st.session_state.page == "cart":
        st.markdown("#### 🛒 Your Shopping Cart")
        if not st.session_state.cart:
            st.info("Your cart is empty. Go back to Home to select products.")
        else:
            for item_id, qty in st.session_state.cart.items():
                st.markdown(f"- **Item ID:** {item_id} | **Quantity:** {qty}")
            
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
                    
                    st.success("Order successfully submitted to Google Sheets!")
                    st.session_state.cart = {}
                except Exception as e:
                    st.error(f"Error checking out: {e}")
