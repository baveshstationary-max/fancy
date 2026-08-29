```python
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
# RESPONSIVE / MOBILE CSS
# ============================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stHeadingWithAction > a,
.markdown-text-container a.anchor-link,
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}

/* -----------------------------------------------------------
   GENERAL
----------------------------------------------------------- */

.block-container {
    padding-top: 0.4rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

.element-container {
    margin-bottom: 0 !important;
}

hr {
    margin: 4px 0 !important;
}

.stButton button {
    min-height: 36px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 7px;
}

div[data-testid="stHorizontalBlock"] {
    align-items: center;
    gap: 6px;
}

/* -----------------------------------------------------------
   LOGIN
----------------------------------------------------------- */

.login-box {
    max-width: 500px;
    margin: 50px auto;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
}

/* -----------------------------------------------------------
   PRODUCT IMAGES
----------------------------------------------------------- */

/* Main image */
.product-main-image img {
    width: 100% !important;
    height: 120px !important;
    object-fit: contain !important;
    background-color: #f8fafc;
    border-radius: 8px;
    border: 2px solid #ff4b4b;
    box-shadow: 0 3px 8px rgba(0,0,0,0.10);
    display: block;
    margin: auto;
}

/* Preview images */
.product-preview-image img {
    width: 100% !important;
    height: 75px !important;
    object-fit: contain !important;
    background-color: #f8fafc;
    border-radius: 7px;
    border: 1px solid #cbd5e1;
    opacity: 0.75;
    display: block;
    margin: auto;
}

/* -----------------------------------------------------------
   PRODUCT CARD
----------------------------------------------------------- */

.product-card {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 8px;
    margin: 4px 0;
    background: white;
}

.product-name {
    font-size: 15px;
    font-weight: 700;
    line-height: 1.2;
}

.product-description {
    color: #666;
    font-size: 11px;
    line-height: 1.3;
}

.product-price {
    font-size: 16px;
    font-weight: 700;
}

/* -----------------------------------------------------------
   CATEGORY CONTAINER
----------------------------------------------------------- */

.category-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 5px;
}

/* -----------------------------------------------------------
   MOBILE
----------------------------------------------------------- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
        padding-top: 5px !important;
    }

    /* Header becomes compact */
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
    }

    /* Smaller headings */
    h1 {
        font-size: 22px !important;
    }

    h2 {
        font-size: 19px !important;
    }

    h3 {
        font-size: 17px !important;
    }

    h4, h5 {
        font-size: 15px !important;
    }

    /* Header buttons */
    .stButton button {
        min-height: 34px !important;
        font-size: 12px !important;
        padding: 4px 5px !important;
    }

    /* Make horizontal blocks wrap on small screens */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }

    /* Category section full width */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
    }

    /* Product images smaller on mobile */
    .product-main-image img {
        height: 180px !important;
        border-width: 2px;
    }

    .product-preview-image img {
        height: 85px !important;
    }

    /* Product name */
    .product-name {
        font-size: 16px;
    }

    .product-description {
        font-size: 12px;
    }

    .product-price {
        font-size: 18px;
    }

    /* Mobile number input */
    input {
        font-size: 16px !important;
    }

    textarea {
        font-size: 15px !important;
    }

}

/* -----------------------------------------------------------
   VERY SMALL PHONES
----------------------------------------------------------- */

@media (max-width: 480px) {

    .block-container {
        padding-left: 5px !important;
        padding-right: 5px !important;
    }

    .product-main-image img {
        height: 160px !important;
    }

    .product-preview-image img {
        height: 65px !important;
    }

    .stButton button {
        min-height: 36px !important;
        font-size: 11px !important;
    }

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
# LOGIN SCREEN
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="login-box">
            <h2 style="text-align:center;">🔐 Store Login</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    mobile = st.text_input(
        "Mobile Number",
        type="password",
        placeholder="Enter mobile number"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        if username and mobile:

            try:

                requests.get(
                    f"{SCRIPT_URL}?action=login&user={urllib.parse.quote(username)}&pass={urllib.parse.quote(mobile)}",
                    timeout=15
                )

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.mobile = mobile

                st.rerun()

            except Exception as e:

                st.error(
                    f"Connection error: {e}"
                )

        else:

            st.error(
                "Please fill in both fields"
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

else:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    head_col1, head_col2, head_col3, head_col4 = st.columns(
        [3, 1, 1, 1]
    )

    with head_col1:

        st.markdown(
            "### 📚 BAVESH STATIONARY"
        )

    with head_col2:

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.session_state.page = "home"
            st.rerun()

    with head_col3:

        cart_count = sum(
            st.session_state.cart.values()
        )

        if st.button(
            f"🛒 Cart ({cart_count})",
            use_container_width=True
        ):

            st.session_state.page = "cart"
            st.rerun()

    with head_col4:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.session_state.image_indices = {}

            st.rerun()

    st.markdown(
        "<hr>",
        unsafe_allow_html=True
    )


    # ========================================================
    # HOME PAGE
    # ========================================================

    if st.session_state.page == "home":

        try:

            res = requests.get(
                f"{SCRIPT_URL}?action=getInventory",
                timeout=20
            )

            rows = res.json()

            if len(rows) > 1:

                headers = [
                    str(h).strip().upper()
                    for h in rows[0]
                ]

                df = pd.DataFrame(
                    rows[1:],
                    columns=headers
                )


                # ------------------------------------------------
                # CATEGORIES
                # ------------------------------------------------

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
                    and categories
                ):

                    st.session_state.selected_category = categories[0]


                # ------------------------------------------------
                # DESKTOP / TABLET CATEGORY + PRODUCTS
                # ------------------------------------------------

                col_left, col_right = st.columns(
                    [1, 4],
                    gap="small"
                )


                # =================================================
                # CATEGORY PANEL
                # =================================================

                with col_left:

                    st.markdown(
                        "##### 📁 Categories"
                    )

                    with st.container(height=520):

                        for cat in categories:

                            is_active = (
                                cat ==
                                st.session_state.selected_category
                            )

                            btn_type = (
                                "primary"
                                if is_active
                                else "secondary"
                            )

                            if st.button(
                                str(cat),
                                use_container_width=True,
                                key=f"cat_{cat}",
                                type=btn_type
                            ):

                                st.session_state.selected_category = cat

                                st.rerun()


                # =================================================
                # PRODUCT PANEL
                # =================================================

                with col_right:

                    active_cat = (
                        st.session_state.selected_category
                    )

                    st.markdown(
                        f"##### 🛍️ Products: {active_cat}"
                    )

                    if "CATEGORY" in df.columns:

                        filtered_df = df[
                            df["CATEGORY"] ==
                            active_cat
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


                            # =====================================
                            # PRODUCT LOOP
                            # =====================================

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


                                # ---------------------------------
                                # IMAGE LIST
                                # ---------------------------------

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
                                        img_raw.strip() != ""
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

                                                raw_list.append(
                                                    c_name
                                                )


                                # ---------------------------------
                                # CONVERT IMAGE NAMES TO URL
                                # ---------------------------------

                                img_list = []

                                for name in raw_list:

                                    if name.startswith(
                                        "http"
                                    ):

                                        img_list.append(
                                            name
                                        )

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


                                # ---------------------------------
                                # FALLBACK IMAGE
                                # ---------------------------------

                                placeholder_url = (
                                    "https://images.unsplash.com/"
                                    "photo-1505740420928-5e560c06d30e"
                                    "?q=80&w=300"
                                )


                                if not img_list:

                                    img_list = [
                                        placeholder_url
                                    ]


                                # ---------------------------------
                                # IMAGE INDEX
                                # ---------------------------------

                                idx_key = (
                                    f"idx_{item_id}"
                                )

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
                                )

                                # Safety if image count changes
                                current_idx = (
                                    current_idx %
                                    len(img_list)
                                )

                                prev_idx = (
                                    current_idx - 1
                                ) % len(img_list)

                                next_idx = (
                                    current_idx + 1
                                ) % len(img_list)


                                # =================================
                                # PRODUCT CARD
                                # =================================

                                st.markdown(
                                    "<div class='product-card'>",
                                    unsafe_allow_html=True
                                )


                                # ---------------------------------
                                # IMAGE / PRODUCT INFO
                                # ---------------------------------

                                image_col1, image_col2, image_col3, info_col, price_col, action_col = st.columns(
                                    [0.35, 0.75, 1.25, 2.2, 0.8, 1.1],
                                    gap="small"
                                )


                                # PREVIOUS IMAGE
                                with image_col1:

                                    if st.button(
                                        "◀",
                                        key=f"prev_{item_id}",
                                        use_container_width=True
                                    ):

                                        st.session_state.image_indices[
                                            idx_key
                                        ] = next_idx

                                        st.rerun()


                                # PREVIEW IMAGE
                                with image_col2:

                                    st.markdown(
                                        "<div class='product-preview-image'>",
                                        unsafe_allow_html=True
                                    )

                                    st.image(
                                        img_list[prev_idx],
                                        use_container_width=True
                                    )

                                    st.markdown(
                                        "</div>",
                                        unsafe_allow_html=True
                                    )


                                # MAIN IMAGE
                                with image_col3:

                                    st.markdown(
                                        "<div class='product-main-image'>",
                                        unsafe_allow_html=True
                                    )

                                    st.image(
                                        img_list[current_idx],
                                        use_container_width=True
                                    )

                                    st.markdown(
                                        "</div>",
                                        unsafe_allow_html=True
                                    )


                                # PRODUCT INFORMATION
                                with info_col:

                                    st.markdown(
                                        f"""
                                        <div class="product-name">
                                            {item_name}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                                    if desc:

                                        st.markdown(
                                            f"""
                                            <div class="product-description">
                                                {desc}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )


                                # PRICE
                                with price_col:

                                    st.markdown(
                                        f"""
                                        <div class="product-price">
                                            ₹{price}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )


                                # QUANTITY + ADD
                                with action_col:

                                    current_qty = (
                                        st.session_state.cart.get(
                                            str(item_id),
                                            1
                                        )
                                    )

                                    qty = st.number_input(
                                        "Qty",
                                        min_value=1,
                                        value=current_qty,
                                        key=f"qty_{item_id}",
                                        label_visibility="collapsed"
                                    )

                                    if st.button(
                                        "🛒 Add",
                                        key=f"add_{item_id}",
                                        use_container_width=True
                                    ):

                                        st.session_state.cart[
                                            str(item_id)
                                        ] = qty

                                        st.rerun()


                                # NEXT IMAGE
                                # Kept below the main content on mobile-friendly layout
                                with image_col3:

                                    if st.button(
                                        "▶",
                                        key=f"next_{item_id}",
                                        use_container_width=True
                                    ):

                                        st.session_state.image_indices[
                                            idx_key
                                        ] = next_idx

                                        st.rerun()


                                st.markdown(
                                    "</div>",
                                    unsafe_allow_html=True
                                )

                                st.markdown(
                                    "<hr>",
                                    unsafe_allow_html=True
                                )


            else:

                st.info(
                    "No products found in inventory."
                )


        except Exception as e:

            st.error(
                f"Could not load catalog: {e}"
            )


    # ========================================================
    # CART PAGE
    # ========================================================

    elif st.session_state.page == "cart":

        st.markdown(
            "#### 📌 Secure Checkout Form"
        )


        if not st.session_state.cart:

            st.info(
                "Your cart is empty. Go back to Home to select products."
            )


        else:

            # -----------------------------------------------
            # CART ITEMS
            # -----------------------------------------------

            st.markdown(
                "### 🛒 Your Cart"
            )

            for item_id, qty in st.session_state.cart.items():

                st.markdown(
                    f"""
                    **Item ID:** {item_id}
                    
                    **Quantity:** {qty}
                    """
                )


            st.markdown("---")


            # -----------------------------------------------
            # CHECKOUT FORM
            # -----------------------------------------------

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

                        # ---------------------------------------
                        # GET CURRENT INVENTORY
                        # ---------------------------------------

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
                                            str(
                                                row["ITEM ID"]
                                            )
                                        ] = float(
                                            row["PRICE"]
                                        )

                                    except:

                                        item_prices[
                                            str(
                                                row["ITEM ID"]
                                            )
                                        ] = 0.0


                        # ---------------------------------------
                        # SUBMIT ORDERS
                        # ---------------------------------------

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
```
