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

.stHeadingWithAction > a,
.markdown-text-container a.anchor-link,
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}

.block-container {
    padding-top: 0.4rem !important;
    padding-bottom: 0.4rem !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    max-width: 100% !important;
}

.element-container {
    margin-bottom: 0 !important;
}

hr {
    margin: 4px 0 !important;
}

.stButton button {
    padding: 3px 5px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    min-height: 32px !important;
    width: 100% !important;
    border-radius: 7px !important;
}

.desktop-only {
    display: block !important;
}

.mobile-only {
    display: none !important;
}

/* ============================================================
   DESKTOP PRODUCT VIEW
   ============================================================ */

.desktop-product-row {
    display: block !important;
}

.desktop-main-image img {
    width: 100% !important;
    height: 120px !important;
    object-fit: contain !important;
    background: #f8fafc !important;
    border: 2px solid #ff4b4b !important;
    border-radius: 7px !important;
    box-shadow: 0 3px 7px rgba(0,0,0,.10) !important;
}

.desktop-preview-image img {
    width: 100% !important;
    height: 75px !important;
    object-fit: contain !important;
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 7px !important;
    opacity: .75 !important;
}

/* ============================================================
   MOBILE PRODUCT VIEW
   ============================================================ */

.mobile-product-card {
    display: none !important;
}

.mobile-main-image img {
    width: 100% !important;
    height: 180px !important;
    object-fit: contain !important;
    background: #f8fafc !important;
    border: 2px solid #ff4b4b !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 7px rgba(0,0,0,.10) !important;
}

.mobile-preview-image img {
    width: 100% !important;
    height: 88px !important;
    object-fit: contain !important;
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 7px !important;
    opacity: .75 !important;
}

.mobile-product-name {
    font-size: 15px !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

.mobile-product-desc {
    color: #666 !important;
    font-size: 11px !important;
    line-height: 1.3 !important;
}

.mobile-product-price {
    font-size: 17px !important;
    font-weight: 700 !important;
}

.mobile-product-card [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 9px !important;
    padding: 7px !important;
    background: #ffffff !important;
}

/* ============================================================
   MOBILE PHONE
   ============================================================ */

@media screen and (max-width: 768px) {

    .block-container {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        padding: 0.35rem 6px !important;
    }

    .desktop-only,
    .desktop-product-row {
        display: none !important;
    }

    .mobile-only,
    .mobile-product-card {
        display: block !important;
    }

    .mobile-product-card .stButton button {
        min-height: 38px !important;
        font-size: 11px !important;
    }

    .mobile-product-card input {
        min-height: 38px !important;
        font-size: 16px !important;
    }

    /* Header automatically fits */
    .mobile-safe-row {
        width: 100% !important;
        max-width: 100% !important;
    }

    h1, h2, h3 {
        max-width: 100% !important;
    }
}

@media screen and (max-width: 480px) {

    .mobile-main-image img {
        height: 155px !important;
    }

    .mobile-preview-image img {
        height: 70px !important;
    }

    .mobile-product-name {
        font-size: 14px !important;
    }

    .mobile-product-desc {
        font-size: 10px !important;
    }

    .mobile-product-price {
        font-size: 16px !important;
    }
}
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
            res = requests.get(f"{SCRIPT_URL}?action=getInventory", timeout=20)
            rows = res.json()

            if len(rows) > 1:
                headers = [str(h).strip().upper() for h in rows[0]]
                df = pd.DataFrame(rows[1:], columns=headers)

                categories = (
                    df["CATEGORY"].dropna().astype(str).unique().tolist()
                    if "CATEGORY" in df.columns
                    else ["General"]
                )

                if (
                    not st.session_state.selected_category
                    or st.session_state.selected_category not in categories
                ) and categories:
                    st.session_state.selected_category = categories[0]

                # ====================================================
                # DESKTOP CATEGORY + PRODUCT AREA
                # ====================================================
                desktop_left, desktop_right = st.columns([1, 4])

                with desktop_left:
                    st.markdown("##### 📁 Categories")

                    with st.container(height=520):
                        for cat in categories:
                            is_active = cat == st.session_state.selected_category

                            if st.button(
                                str(cat),
                                use_container_width=True,
                                key=f"desktop_cat_{cat}",
                                type="primary" if is_active else "secondary"
                            ):
                                st.session_state.selected_category = cat
                                st.rerun()

                with desktop_right:
                    active_cat = st.session_state.selected_category
                    st.markdown(f"##### Products: {active_cat}")

                    filtered_df = (
                        df[df["CATEGORY"] == active_cat]
                        if "CATEGORY" in df.columns
                        else df
                    )

                    if filtered_df.empty:
                        st.info("No products available in this category.")
                    else:
                        with st.container(height=520):
                            grouped_df = filtered_df.groupby("ITEM ID", sort=False)

                            for item_id, group in grouped_df:
                                first_row = group.iloc[0]
                                item_name = first_row.get("ITEM NAME", "Product")
                                price = first_row.get("PRICE", "0")
                                desc = first_row.get("DESCRIPTION", "")

                                raw_list = []

                                for _, r in group.iterrows():
                                    img_raw = str(
                                        r.get("IMAGES", r.get("IMAGE", ""))
                                    )

                                    if img_raw.strip():
                                        for part in img_raw.replace("\\", ",").split(","):
                                            c_name = part.strip()
                                            if (
                                                c_name
                                                and not c_name.lower().endswith(
                                                    (".mp4", ".mov", ".avi")
                                                )
                                            ):
                                                raw_list.append(c_name)

                                img_list = []

                                for name in raw_list:
                                    if name.startswith("http"):
                                        img_list.append(name)
                                    else:
                                        encoded_name = urllib.parse.quote(name)
                                        img_list.append(
                                            "https://raw.githubusercontent.com/"
                                            "baveshstationary-max/fancy/main/IMAGES/"
                                            f"{encoded_name}"
                                        )

                                if not img_list:
                                    img_list = [
                                        "https://images.unsplash.com/"
                                        "photo-1505740420928-5e560c06d30e"
                                        "?q=80&w=300"
                                    ]

                                idx_key = f"idx_{item_id}"

                                if idx_key not in st.session_state.image_indices:
                                    st.session_state.image_indices[idx_key] = 0

                                current_idx = (
                                    st.session_state.image_indices[idx_key]
                                    % len(img_list)
                                )
                                prev_idx = (current_idx - 1) % len(img_list)
                                next_idx = (current_idx + 1) % len(img_list)

                                st.markdown(
                                    "<div class='desktop-only desktop-product-row'>",
                                    unsafe_allow_html=True
                                )

                                cols = st.columns(
                                    [0.4, 0.9, 1.3, 0.9, 0.4, 2.2, 0.7, 1.0]
                                )

                                with cols[0]:
                                    if st.button(
                                        "◀",
                                        key=f"desktop_prev_{item_id}",
                                        use_container_width=True
                                    ):
                                        st.session_state.image_indices[idx_key] = next_idx
                                        st.rerun()

                                with cols[1]:
                                    st.markdown(
                                        "<div class='desktop-preview-image'>",
                                        unsafe_allow_html=True
                                    )
                                    st.image(
                                        img_list[prev_idx],
                                        use_container_width=True
                                    )
                                    st.markdown("</div>", unsafe_allow_html=True)

                                with cols[2]:
                                    st.markdown(
                                        "<div class='desktop-main-image'>",
                                        unsafe_allow_html=True
                                    )
                                    st.image(
                                        img_list[current_idx],
                                        use_container_width=True
                                    )
                                    st.markdown("</div>", unsafe_allow_html=True)

                                with cols[3]:
                                    st.markdown(
                                        "<div class='desktop-preview-image'>",
                                        unsafe_allow_html=True
                                    )
                                    st.image(
                                        img_list[next_idx],
                                        use_container_width=True
                                    )
                                    st.markdown("</div>", unsafe_allow_html=True)

                                with cols[4]:
                                    if st.button(
                                        "▶",
                                        key=f"desktop_next_{item_id}",
                                        use_container_width=True
                                    ):
                                        st.session_state.image_indices[idx_key] = prev_idx
                                        st.rerun()

                                with cols[5]:
                                    st.markdown(f"**{item_name}**")
                                    if desc:
                                        st.markdown(
                                            f"<span style='color:#666;font-size:10px'>{desc}</span>",
                                            unsafe_allow_html=True
                                        )

                                with cols[6]:
                                    st.markdown(f"**₹{price}**")

                                with cols[7]:
                                    current_qty = st.session_state.cart.get(
                                        str(item_id), 1
                                    )
                                    qty = st.number_input(
                                        "Qty",
                                        min_value=1,
                                        value=current_qty,
                                        key=f"desktop_qty_{item_id}",
                                        label_visibility="collapsed"
                                    )

                                    if st.button(
                                        "Add",
                                        key=f"desktop_add_{item_id}",
                                        use_container_width=True
                                    ):
                                        st.session_state.cart[str(item_id)] = qty
                                        st.rerun()

                                st.markdown("</div>", unsafe_allow_html=True)
                                st.markdown("<hr>", unsafe_allow_html=True)

                # ====================================================
                # MOBILE CATEGORY + PRODUCT AREA
                # ====================================================
                st.markdown(
                    "<div class='mobile-only'>",
                    unsafe_allow_html=True
                )

                st.markdown("##### 📁 Categories")

                mobile_category_cols = st.columns(
                    min(4, max(1, len(categories)))
                )

                # Show first categories across the available mobile width.
                # Extra categories remain in a compact second line.
                for i, cat in enumerate(categories):
                    with mobile_category_cols[i % len(mobile_category_cols)]:
                        is_active = cat == st.session_state.selected_category

                        if st.button(
                            str(cat),
                            use_container_width=True,
                            key=f"mobile_cat_{cat}",
                            type="primary" if is_active else "secondary"
                        ):
                            st.session_state.selected_category = cat
                            st.rerun()

                active_cat = st.session_state.selected_category

                st.markdown(
                    f"##### 🛍️ Products: {active_cat}"
                )

                filtered_df = (
                    df[df["CATEGORY"] == active_cat]
                    if "CATEGORY" in df.columns
                    else df
                )

                if filtered_df.empty:
                    st.info("No products available in this category.")
                else:
                    for item_id, group in filtered_df.groupby(
                        "ITEM ID", sort=False
                    ):
                        first_row = group.iloc[0]
                        item_name = first_row.get("ITEM NAME", "Product")
                        price = first_row.get("PRICE", "0")
                        desc = first_row.get("DESCRIPTION", "")

                        raw_list = []

                        for _, r in group.iterrows():
                            img_raw = str(
                                r.get("IMAGES", r.get("IMAGE", ""))
                            )

                            if img_raw.strip():
                                for part in img_raw.replace("\\", ",").split(","):
                                    c_name = part.strip()

                                    if (
                                        c_name
                                        and not c_name.lower().endswith(
                                            (".mp4", ".mov", ".avi")
                                        )
                                    ):
                                        raw_list.append(c_name)

                        img_list = []

                        for name in raw_list:
                            if name.startswith("http"):
                                img_list.append(name)
                            else:
                                encoded_name = urllib.parse.quote(name)
                                img_list.append(
                                    "https://raw.githubusercontent.com/"
                                    "baveshstationary-max/fancy/main/IMAGES/"
                                    f"{encoded_name}"
                                )

                        if not img_list:
                            img_list = [
                                "https://images.unsplash.com/"
                                "photo-1505740420928-5e560c06d30e"
                                "?q=80&w=300"
                            ]

                        idx_key = f"idx_{item_id}"

                        if idx_key not in st.session_state.image_indices:
                            st.session_state.image_indices[idx_key] = 0

                        current_idx = (
                            st.session_state.image_indices[idx_key]
                            % len(img_list)
                        )
                        prev_idx = (current_idx - 1) % len(img_list)
                        next_idx = (current_idx + 1) % len(img_list)

                        # Native Streamlit container gives us a reliable
                        # DOM boundary for the mobile card.
                        with st.container(
                            border=True,
                            key=f"mobile_product_{item_id}"
                        ):

                            st.markdown(
                                "<div class='mobile-product-card'>",
                                unsafe_allow_html=True
                            )

                            image_cols = st.columns([0.22, 0.56, 0.22])

                            with image_cols[0]:
                                if st.button(
                                    "◀",
                                    key=f"mobile_prev_{item_id}",
                                    use_container_width=True
                                ):
                                    st.session_state.image_indices[idx_key] = prev_idx
                                    st.rerun()

                            with image_cols[1]:
                                st.markdown(
                                    "<div class='mobile-main-image'>",
                                    unsafe_allow_html=True
                                )
                                st.image(
                                    img_list[current_idx],
                                    use_container_width=True
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                            with image_cols[2]:
                                if st.button(
                                    "▶",
                                    key=f"mobile_next_{item_id}",
                                    use_container_width=True
                                ):
                                    st.session_state.image_indices[idx_key] = next_idx
                                    st.rerun()

                            preview_cols = st.columns([0.25, 0.5, 0.25])

                            with preview_cols[0]:
                                st.markdown(
                                    "<div class='mobile-preview-image'>",
                                    unsafe_allow_html=True
                                )
                                st.image(
                                    img_list[prev_idx],
                                    use_container_width=True
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                            with preview_cols[1]:
                                st.markdown(
                                    "<div style='text-align:center;font-size:10px;color:#64748b'>"
                                    f"{current_idx + 1} / {len(img_list)}"
                                    "</div>",
                                    unsafe_allow_html=True
                                )

                            with preview_cols[2]:
                                st.markdown(
                                    "<div class='mobile-preview-image'>",
                                    unsafe_allow_html=True
                                )
                                st.image(
                                    img_list[next_idx],
                                    use_container_width=True
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                            st.markdown(
                                f"<div class='mobile-product-name'>{item_name}</div>",
                                unsafe_allow_html=True
                            )

                            if desc:
                                st.markdown(
                                    f"<div class='mobile-product-desc'>{desc}</div>",
                                    unsafe_allow_html=True
                                )

                            price_qty_cols = st.columns([1, 1])

                            with price_qty_cols[0]:
                                st.markdown(
                                    f"<div class='mobile-product-price'>₹{price}</div>",
                                    unsafe_allow_html=True
                                )

                            with price_qty_cols[1]:
                                current_qty = st.session_state.cart.get(
                                    str(item_id), 1
                                )

                                qty = st.number_input(
                                    "Qty",
                                    min_value=1,
                                    value=current_qty,
                                    key=f"mobile_qty_{item_id}",
                                    label_visibility="collapsed"
                                )

                            if st.button(
                                "🛒 Add to Cart",
                                key=f"mobile_add_{item_id}",
                                use_container_width=True
                            ):
                                st.session_state.cart[str(item_id)] = qty
                                st.rerun()

                            st.markdown(
                                "</div>",
                                unsafe_allow_html=True
                            )

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
