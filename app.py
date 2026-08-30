import streamlit as st
import requests
import pandas as pd
import urllib.parse

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwO0yuuoGKlF6zAlA30OVjKxAHRE5wgl1xJ7uAr9DF5OFtnpesK5UD4C3pdnClWdKxQ/exec"

st.set_page_config(
    page_title="Bavesh Stationary",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# RESPONSIVE CSS & FORCED DESKTOP VIEWPORT WRAPPER
# ============================================================

st.markdown("""
<head>
    <meta name="viewport" content="width=1200, initial-scale=1.0">
</head>
<style>
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

.stHeadingWithAction > a,
.markdown-text-container a.anchor-link,
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}

/* Force overall page container to mimic desktop width with horizontal scrollability */
html, body {
    width: 100% !important;
    overflow-x: auto !important;
    background: #f8fafc !important;
}

/* Global desktop-width application shell */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewMain"], [data-testid="stMain"], section.main {
    width: 1200px !important;
    min-width: 1200px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.block-container {
    width: 1120px !important;
    min-width: 1120px !important;
    max-width: 1120px !important;
    padding-top: 0.45rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    margin: 0 auto !important;
}

.element-container {
    margin-bottom: 0 !important;
}

div[data-testid="stHorizontalBlock"] {
    align-items: center;
    gap: 5px;
    flex-wrap: nowrap !important;
}

.stButton button {
    min-height: 34px;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 600;
    width: 100%;
    border-radius: 7px;
}

hr {
    margin: 4px 0 !important;
}

/* Product images */
.product-main img {
    width: 100% !important;
    height: 120px !important;
    object-fit: contain !important;
    background: #f8fafc;
    border: 2px solid #ff4b4b;
    border-radius: 7px;
    box-shadow: 0 3px 7px rgba(0,0,0,.10);
}

.product-preview img {
    width: 100% !important;
    height: 75px !important;
    object-fit: contain !important;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    opacity: .75;
}

.product-card {
    border: 1px solid #e2e8f0;
    border-radius: 9px;
    padding: 7px 6px 4px 6px;
    margin: 3px 0;
    background: white;
}

.product-name {
    font-size: 14px;
    font-weight: 700;
    line-height: 1.25;
    word-break: break-word;
}

.product-desc {
    color: #666;
    font-size: 10px;
    line-height: 1.3;
    margin-top: 2px;
}

.product-price {
    font-size: 15px;
    font-weight: 700;
    white-space: nowrap;
}

/* =========================================================
   PROFESSIONAL COMPACT LOGIN
   ========================================================= */

.login-title {
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    color: #111827;
    margin: 4px 0 10px 0;
}

.login-card-host {
    width: 460px !important;
    max-width: 460px !important;
    margin: 0 auto !important;
}

.login-card-host [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #cbd5e1 !important;
    border-radius: 7px !important;
    box-shadow: none !important;
    background: #ffffff !important;
    padding: 16px 14px 12px 14px !important;
}

.login-card-host [data-testid="stTextInput"] label {
    font-size: 12px !important;
    color: #111827 !important;
    font-weight: 500 !important;
}

.login-card-host [data-testid="stTextInput"] input {
    height: 36px !important;
    min-height: 36px !important;
    padding: 6px 10px !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    background: #f8fafc !important;
    font-size: 13px !important;
}

.login-card-host [data-testid="stButton"] button {
    height: 36px !important;
    min-height: 36px !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    background: #ffffff !important;
    color: #111827 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    login_left, login_center, login_right = st.columns(
        [1, 1, 1],
        wrap=False
    )

    with login_center:

        st.markdown(
            "<div class='login-title'>Customer Portal Login</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='login-card-host'>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            username = st.text_input(
                "Your Name:",
                key="login_username"
            )

            mobile = st.text_input(
                "Mobile Number:",
                type="password",
                key="login_mobile"
            )

            if st.button(
                "Secure Login",
                use_container_width=True,
                key="login_button"
            ):

                if username and mobile:

                    try:
                        requests.get(
                            f"{SCRIPT_URL}?action=login"
                            f"&user={urllib.parse.quote(username)}"
                            f"&pass={urllib.parse.quote(mobile)}",
                            timeout=20
                        )

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.mobile = mobile

                        st.rerun()

                    except Exception as e:
                        st.error(f"Connection error: {e}")

                else:
                    st.error("Please fill in both fields")

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MAIN APPLICATION
# ============================================================

else:

    head_col1, head_col2, head_col3, head_col4 = st.columns(
        [3, 1, 1, 1],
        gap="small"
    )

    with head_col1:
        st.markdown("### 📚 BAVESH STATIONARY")

    with head_col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with head_col3:
        cart_count = sum(st.session_state.cart.values())

        if st.button(
            f"🛒 Cart ({cart_count})",
            use_container_width=True
        ):
            st.session_state.page = "cart"
            st.rerun()

    with head_col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.session_state.image_indices = {}
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)


    # ========================================================
    # HOME
    # ========================================================

    if st.session_state.page == "home":

        try:

            res = requests.get(
                f"{SCRIPT_URL}?action=getInventory",
                timeout=20
            )

            rows = res.json()

            if len(rows) <= 1:
                st.info("No products found in inventory.")

            else:

                headers = [
                    str(h).strip().upper()
                    for h in rows[0]
                ]

                df = pd.DataFrame(
                    rows[1:],
                    columns=headers
                )

                if "CATEGORY" in df.columns:
                    categories = (
                        df["CATEGORY"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )
                else:
                    categories = ["General"]

                if (
                    not st.session_state.selected_category
                    or
                    st.session_state.selected_category not in categories
                ):
                    if categories:
                        st.session_state.selected_category = categories[0]

                col_left, col_right = st.columns(
                    [1, 4],
                    gap="small"
                )

                # CATEGORY PANEL
                with col_left:

                    st.markdown("##### 📁 Categories")

                    with st.container(height=520):

                        for cat in categories:

                            is_active = (
                                cat ==
                                st.session_state.selected_category
                            )

                            if st.button(
                                str(cat),
                                use_container_width=True,
                                key=f"cat_{cat}",
                                type=(
                                    "primary"
                                    if is_active
                                    else "secondary"
                                )
                            ):

                                st.session_state.selected_category = cat
                                st.rerun()

                # PRODUCTS
                with col_right:

                    active_cat = (
                        st.session_state.selected_category
                    )

                    st.markdown(
                        f"##### 🛍️ Products: {active_cat}"
                    )

                    if "CATEGORY" in df.columns:
                        filtered_df = df[
                            df["CATEGORY"] == active_cat
                        ]
                    else:
                        filtered_df = df

                    if filtered_df.empty:

                        st.info(
                            "No products available in this category."
                        )

                    else:

                        with st.container(height=520):

                            grouped_df = filtered_df.groupby(
                                "ITEM ID",
                                sort=False
                            )

                            for item_id, group in grouped_df:

                                first_row = group.iloc[0]

                                item_name = first_row.get(
                                    "ITEM NAME",
                                    "Product"
                                )

                                price = first_row.get(
                                    "PRICE",
                                    "0"
                                )

                                desc = first_row.get(
                                    "DESCRIPTION",
                                    ""
                                )

                                raw_list = []

                                for _, r in group.iterrows():

                                    img_raw = str(
                                        r.get(
                                            "IMAGES",
                                            r.get(
                                                "IMAGE",
                                                ""
                                            )
                                        )
                                    )

                                    if (
                                        img_raw
                                        and
                                        img_raw.strip()
                                    ):

                                        for part in img_raw.replace(
                                            "\\",
                                            ","
                                        ).split(","):

                                            c_name = part.strip()

                                            if (
                                                c_name
                                                and
                                                not c_name.lower().endswith(
                                                    (
                                                        ".mp4",
                                                        ".mov",
                                                        ".avi"
                                                    )
                                                )
                                            ):

                                                raw_list.append(c_name)

                                img_list = []

                                for name in raw_list:

                                    if name.startswith("http"):

                                        img_list.append(name)

                                    else:

                                        encoded_name = (
                                            urllib.parse.quote(
                                                name
                                            )
                                        )

                                        github_raw = (
                                            "https://raw.githubusercontent.com/"
                                            "baveshstationary-max/fancy/"
                                            f"main/IMAGES/{encoded_name}"
                                        )

                                        img_list.append(
                                            github_raw
                                        )

                                if not img_list:

                                    img_list = [
                                        "https://images.unsplash.com/"
                                        "photo-1505740420928-5e560c06d30e"
                                        "?q=80&w=300"
                                    ]

                                idx_key = f"idx_{item_id}"

                                if (
                                    idx_key
                                    not in
                                    st.session_state.image_indices
                                ):
                                    st.session_state.image_indices[
                                        idx_key
                                    ] = 0

                                current_idx = (
                                    st.session_state
                                    .image_indices[idx_key]
                                    %
                                    len(img_list)
                                )

                                prev_idx = (
                                    current_idx - 1
                                ) % len(img_list)

                                next_idx = (
                                    current_idx + 1
                                ) % len(img_list)

                                st.markdown(
                                    "<div class='product-card'>",
                                    unsafe_allow_html=True
                                )

                                cols = st.columns([0.4, 0.9, 1.3, 0.9, 0.4, 2.2, 0.7, 1.0], wrap=False)

                                # PREVIOUS
                                with cols[0]:
                                    if st.button("◀", key=f"prev_{item_id}", use_container_width=True):
                                        st.session_state.image_indices[idx_key] = (
                                            st.session_state.image_indices[idx_key] + 1
                                        ) % len(img_list)
                                        st.rerun()

                                # LEFT PREVIEW
                                with cols[1]:
                                    st.markdown("<div class='product-preview'>", unsafe_allow_html=True)
                                    st.image(img_list[prev_idx], use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)

                                # MAIN IMAGE
                                with cols[2]:
                                    st.markdown("<div class='product-main'>", unsafe_allow_html=True)
                                    st.image(img_list[current_idx], use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)

                                # RIGHT PREVIEW
                                with cols[3]:
                                    st.markdown("<div class='product-preview'>", unsafe_allow_html=True)
                                    st.image(img_list[next_idx], use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)

                                # NEXT
                                with cols[4]:
                                    if st.button("▶", key=f"next_{item_id}", use_container_width=True):
                                        st.session_state.image_indices[idx_key] = (
                                            st.session_state.image_indices[idx_key] - 1
                                        ) % len(img_list)
                                        st.rerun()

                                # PRODUCT INFORMATION
                                with cols[5]:
                                    st.markdown(
                                        f"<div class='product-name'>{item_name}</div>",
                                        unsafe_allow_html=True
                                    )
                                    if desc:
                                        st.markdown(
                                            f"<div class='product-desc'>{desc}</div>",
                                            unsafe_allow_html=True
                                        )

                                # PRICE
                                with cols[6]:
                                    st.markdown(
                                        f"<div class='product-price'>₹{price}</div>",
                                        unsafe_allow_html=True
                                    )

                                # QUANTITY + ADD
                                with cols[7]:
                                    current_qty = st.session_state.cart.get(str(item_id), 1)
                                    qty = st.number_input(
                                        "Qty",
                                        min_value=1,
                                        value=current_qty,
                                        key=f"qty_{item_id}",
                                        label_visibility="collapsed"
                                    )
                                    if st.button(
                                        "Add",
                                        key=f"add_{item_id}",
                                        use_container_width=True
                                    ):
                                        st.session_state.cart[str(item_id)] = qty
                                        st.rerun()

                                st.markdown("<hr>", unsafe_allow_html=True)

        except Exception as e:
            st.error(
                f"Could not load catalog: {e}"
            )


    # ========================================================
    # CART
    # ========================================================

    elif st.session_state.page == "cart":

        st.markdown("#### 📌 Secure Checkout Form")

        if not st.session_state.cart:

            st.info(
                "Your cart is empty. Go back to Home to select products."
            )

        else:

            st.markdown("### 🛒 Your Cart")

            for item_id, qty in st.session_state.cart.items():

                st.markdown(
                    f"**Item ID:** {item_id}  \n"
                    f"**Quantity:** {qty}"
                )

            st.markdown("---")

            delivery_address = st.text_area(
                "Delivery Address:",
                placeholder=(
                    "Enter your full street address, "
                    "landmark, and pin code..."
                ),
                height=120
            )

            alt_contact = st.text_input(
                "Alternative Contact Number:",
                placeholder="Enter secondary mobile number..."
            )

            custom_desc = st.text_area(
                "Product Specifications / Custom Description:",
                placeholder=(
                    "Specify any specific instructions, "
                    "colors, or custom requirements..."
                ),
                height=120
            )

            if st.button(
                "✅ Complete Order",
                use_container_width=True
            ):

                if not delivery_address.strip():

                    st.error(
                        "Please enter a delivery address before completing your order."
                    )

                else:

                    try:

                        res = requests.get(
                            f"{SCRIPT_URL}?action=getInventory",
                            timeout=20
                        )

                        rows = res.json()

                        item_prices = {}

                        if len(rows) > 1:

                            headers = [
                                str(h).strip().upper()
                                for h in rows[0]
                            ]

                            inv_df = pd.DataFrame(
                                rows[1:],
                                columns=headers
                            )

                            if (
                                "ITEM ID" in inv_df.columns
                                and
                                "PRICE" in inv_df.columns
                            ):

                                for _, row in inv_df.iterrows():

                                    try:

                                        item_prices[
                                            str(row["ITEM ID"])
                                        ] = float(
                                            row["PRICE"]
                                        )

                                    except (ValueError, TypeError):

                                        item_prices[
                                            str(row["ITEM ID"])
                                        ] = 0.0

                        for item_id, qty in (
                            st.session_state.cart.items()
                        ):

                            unit_price = item_prices.get(
                                str(item_id),
                                0.0
                            )

                            total_cost = (
                                qty *
                                unit_price
                            )

                            order_data = {
                                "mobile":
                                    st.session_state.mobile,

                                "altContact":
                                    alt_contact,

                                "deliveryAddress":
                                    delivery_address,

                                "customDescription":
                                    custom_desc,

                                "itemId":
                                    item_id,

                                "itemName":
                                    f"Item {item_id}",

                                "quantity":
                                    qty,

                                "totalCost":
                                    total_cost
                            }

                            requests.post(
                                SCRIPT_URL,
                                json=order_data,
                                timeout=20
                            )

                        st.success(
                            "✅ Order successfully submitted to Google Sheets!"
                        )

                        st.session_state.cart = {}

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Error checking out: {e}"
                        )
