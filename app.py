from datetime import datetime
import csv
import os

import pandas as pd
import requests
import streamlit as st


# ============================================================
# HM MOBILES THIRUVERKADU
# ONE RESPONSIVE LAYOUT FOR DESKTOP + MOBILE
# ============================================================

st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# RESPONSIVE CSS
# ============================================================

st.markdown(
    """
    <style>
    /* ============================================================
       HM MOBILES
       One fixed responsive design for desktop + mobile.
       The page NEVER changes MENU|PRODUCT into stacked blocks.
       ============================================================ */

    * {
        box-sizing: border-box !important;
    }

    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 8px 10px 12px 10px !important;
        margin: 0 auto !important;
    }

    /* Streamlit columns: never wrap on a phone. */
    div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
        gap: 5px !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* Remove Streamlit browser chrome. */
    #MainMenu,
    header,
    footer,
    div[data-testid="stToolbar"],
    section[data-testid="stStatusWidget"],
    div[data-testid="stDecoration"],
    div[class*="viewerBadge"] {
        display: none !important;
    }

    /* ============================================================
       LOGIN
       ============================================================ */

    .hm-login-title {
        width: 100% !important;
        text-align: center !important;
        margin: 7px auto 10px auto !important;
    }

    .hm-login-title h1 {
        margin: 0 !important;
        font-size: 28px !important;
        line-height: 1.15 !important;
        font-weight: 800 !important;
    }

    .hm-login-title p {
        margin: 4px 0 0 0 !important;
        font-size: 13px !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stForm"] {
        width: min(430px, 100%) !important;
        max-width: 430px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    input,
    textarea,
    div[data-baseweb="select"] > div {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }

    /* ============================================================
       BRAND
       ============================================================ */

    .hm-brand {
        width: 100% !important;
        padding: 10px 7px !important;
        margin: 0 0 5px 0 !important;
        background: #1e293b !important;
        border-radius: 7px !important;
        text-align: center !important;
    }

    .hm-brand-title {
        margin: 0 !important;
        color: #ffffff !important;
        font-size: 20px !important;
        line-height: 1.2 !important;
        font-weight: 800 !important;
        overflow-wrap: anywhere !important;
    }

    /* ============================================================
       NAVIGATION
       Welcome | Home | Cart | Logout
       ============================================================ */

    .hm-nav {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    .hm-nav div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
        align-items: center !important;
    }

    .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        overflow: hidden !important;
    }

    .hm-nav p {
        margin: 0 !important;
        font-size: 14px !important;
        line-height: 1.3 !important;
        overflow-wrap: anywhere !important;
    }

    .hm-nav div.stButton > button {
        width: 100% !important;
        min-width: 0 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        padding: 5px 4px !important;
    }

    /* ============================================================
       MAIN
       Menu | Product
       ============================================================ */

    .hm-main {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    .hm-main > div[data-testid="stHorizontalBlock"] {
        gap: 6px !important;
    }

    .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        overflow: hidden !important;
    }

    .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 0 0 24% !important;
        width: 24% !important;
    }

    .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        flex: 0 0 76% !important;
        width: 76% !important;
    }

    .hm-main h3 {
        margin: 2px 0 6px 0 !important;
        font-size: 18px !important;
    }

    .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child div.stButton > button {
        width: 100% !important;
        min-width: 0 !important;
        padding: 6px 4px !important;
        font-size: 13px !important;
        line-height: 1.15 !important;
    }

    /* ============================================================
       PRODUCT
       Image | Description | Price
       ============================================================ */

    .hm-product {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    .hm-product > div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        gap: 5px !important;
        align-items: flex-start !important;
    }

    .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
        flex: 0 0 31% !important;
        width: 31% !important;
    }

    .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        flex: 0 0 41% !important;
        width: 41% !important;
    }

    .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
        flex: 0 0 28% !important;
        width: 28% !important;
    }

    .hm-product p,
    .hm-product span,
    .hm-product label {
        max-width: 100% !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        line-height: 1.3 !important;
    }

    .hm-product img {
        display: block !important;
        max-width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
    }

    .hm-product hr {
        margin: 7px 0 !important;
    }

    .hm-product div.stButton > button,
    .hm-product input {
        min-width: 0 !important;
        max-width: 100% !important;
    }

    /* ============================================================
       CART
       ============================================================ */

    .hm-cart {
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* ============================================================
       MOBILE - purpose-built spacing
       ============================================================ */

    @media (max-width: 600px) {

        .block-container {
            padding: 3px 3px 7px 3px !important;
        }

        /* LOGIN */
        .hm-login-title {
            margin: 2px auto 6px auto !important;
        }

        .hm-login-title h1 {
            font-size: 23px !important;
        }

        .hm-login-title p {
            font-size: 10px !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stForm"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* BRAND */
        .hm-brand {
            padding: 7px 3px !important;
            margin-bottom: 3px !important;
            border-radius: 6px !important;
        }

        .hm-brand-title {
            font-size: 13px !important;
        }

        /* NAV - carefully sized for a phone */
        .hm-nav div[data-testid="stHorizontalBlock"] {
            gap: 2px !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 40% !important;
            width: 40% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 19% !important;
            width: 19% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 21% !important;
            width: 21% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 20% !important;
            width: 20% !important;
        }

        .hm-nav p {
            font-size: 10px !important;
            line-height: 1.2 !important;
        }

        .hm-nav div.stButton > button {
            min-height: 29px !important;
            font-size: 9px !important;
            padding: 3px 1px !important;
        }

        /* MAIN MENU | PRODUCT */
        .hm-main > div[data-testid="stHorizontalBlock"] {
            gap: 3px !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
            flex-basis: 25% !important;
            width: 25% !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
            flex-basis: 75% !important;
            width: 75% !important;
        }

        .hm-main h3 {
            font-size: 13px !important;
            line-height: 1.15 !important;
            margin: 1px 0 4px 0 !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child div.stButton > button {
            min-height: 28px !important;
            font-size: 9px !important;
            padding: 3px 1px !important;
        }

        /* PRODUCT IMAGE | DESCRIPTION | PRICE */
        .hm-product > div[data-testid="stHorizontalBlock"] {
            gap: 2px !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex-basis: 30% !important;
            width: 30% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex-basis: 43% !important;
            width: 43% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex-basis: 27% !important;
            width: 27% !important;
        }

        .hm-product p,
        .hm-product span,
        .hm-product label {
            font-size: 9px !important;
            line-height: 1.2 !important;
        }

        .hm-product h3 {
            font-size: 12px !important;
            line-height: 1.1 !important;
            margin: 0 !important;
        }

        .hm-product h4 {
            font-size: 10px !important;
            line-height: 1.1 !important;
        }

        .hm-product img {
            max-height: 82px !important;
        }

        .hm-product div.stButton > button {
            min-height: 26px !important;
            font-size: 8px !important;
            padding: 2px 1px !important;
        }

        .hm-product input {
            min-height: 26px !important;
            font-size: 9px !important;
            padding: 2px !important;
        }

        /* CART */
        .hm-cart div[data-testid="stHorizontalBlock"] {
            gap: 3px !important;
        }
    }

    /* ============================================================
       PORTRAIT PHONE
       <= 600px wide AND taller than wide.

       This is intentionally different from landscape.
       The goal is to make a 320-430px portrait screen usable without
       collapsing MENU above PRODUCT or creating horizontal scrolling.
       ============================================================ */

    @media (max-width: 600px) and (orientation: portrait) {

        html, body,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }

        .block-container {
            width: 100% !important;
            max-width: 100% !important;
            padding: 2px 2px 6px 2px !important;
        }

        /* ---------- LOGIN ---------- */
        .hm-login-title {
            margin: 1px auto 5px auto !important;
        }

        .hm-login-title h1 {
            font-size: 21px !important;
        }

        .hm-login-title p {
            font-size: 9px !important;
        }

        div[data-testid="stForm"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* ---------- BRAND ---------- */
        .hm-brand {
            padding: 6px 2px !important;
            margin-bottom: 2px !important;
        }

        .hm-brand-title {
            font-size: 12px !important;
            line-height: 1.15 !important;
        }

        /* ---------- HEADER ----------
           36% Welcome | 20% Home | 22% Cart | 22% Logout */
        .hm-nav div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            gap: 1px !important;
            flex-wrap: nowrap !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 36% !important;
            width: 36% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 20% !important;
            width: 20% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 22% !important;
            width: 22% !important;
        }

        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 22% !important;
            width: 22% !important;
        }

        .hm-nav p {
            font-size: 9px !important;
            line-height: 1.1 !important;
            white-space: nowrap !important;
        }

        .hm-nav div.stButton > button {
            width: 100% !important;
            min-height: 27px !important;
            height: 27px !important;
            font-size: 8px !important;
            line-height: 1 !important;
            padding: 2px 0 !important;
        }

        /* ---------- MAIN ----------
           20% MENU | 80% PRODUCT */
        .hm-main > div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            gap: 2px !important;
            flex-wrap: nowrap !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
            flex: 0 0 20% !important;
            width: 20% !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
            flex: 0 0 80% !important;
            width: 80% !important;
        }

        .hm-main h3 {
            font-size: 12px !important;
            line-height: 1.1 !important;
            margin: 1px 0 3px 0 !important;
        }

        /* Menu buttons fit the narrow left rail. */
        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child div.stButton > button {
            width: 100% !important;
            min-height: 27px !important;
            height: 27px !important;
            font-size: 7px !important;
            line-height: 1 !important;
            padding: 2px 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* ---------- PRODUCT ----------
           28% IMAGE | 45% DESCRIPTION | 27% PRICE */
        .hm-product > div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            gap: 1px !important;
            flex-wrap: nowrap !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 28% !important;
            width: 28% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 45% !important;
            width: 45% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 27% !important;
            width: 27% !important;
        }

        .hm-product p,
        .hm-product span,
        .hm-product label {
            font-size: 8px !important;
            line-height: 1.15 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .hm-product h3 {
            font-size: 11px !important;
            line-height: 1.05 !important;
            margin: 0 !important;
        }

        .hm-product h4 {
            font-size: 9px !important;
            line-height: 1.05 !important;
            margin: 1px 0 !important;
        }

        .hm-product img {
            width: 100% !important;
            max-width: 100% !important;
            max-height: 68px !important;
            object-fit: contain !important;
        }

        .hm-product div.stButton > button {
            width: 100% !important;
            min-height: 25px !important;
            height: 25px !important;
            font-size: 7px !important;
            line-height: 1 !important;
            padding: 2px 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        .hm-product input {
            width: 100% !important;
            min-height: 25px !important;
            height: 25px !important;
            font-size: 8px !important;
            padding: 1px !important;
        }

        .hm-product hr {
            margin: 4px 0 !important;
        }

        /* ---------- CART ----------
           Cart controls stay inside the portrait viewport. */
        .hm-cart,
        .hm-cart div[data-testid="stHorizontalBlock"],
        .hm-cart div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        .hm-cart div[data-testid="stHorizontalBlock"] {
            gap: 2px !important;
            flex-wrap: nowrap !important;
        }
    }

    /* Very narrow portrait phones: 320px-ish screens. */
    @media (max-width: 360px) and (orientation: portrait) {

        .block-container {
            padding-left: 1px !important;
            padding-right: 1px !important;
        }

        .hm-brand-title {
            font-size: 11px !important;
        }

        .hm-nav p {
            font-size: 8px !important;
        }

        .hm-nav div.stButton > button {
            font-size: 7px !important;
        }

        /* Keep Menu usable but give Product the majority of the width. */
        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
            flex-basis: 19% !important;
            width: 19% !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
            flex-basis: 81% !important;
            width: 81% !important;
        }

        .hm-main > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child div.stButton > button {
            font-size: 6px !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex-basis: 27% !important;
            width: 27% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex-basis: 46% !important;
            width: 46% !important;
        }

        .hm-product > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex-basis: 27% !important;
            width: 27% !important;
        }

        .hm-product p,
        .hm-product span,
        .hm-product label {
            font-size: 7px !important;
        }

        .hm-product h3 {
            font-size: 10px !important;
        }

        .hm-product h4 {
            font-size: 8px !important;
        }

        .hm-product div.stButton > button {
            font-size: 6px !important;
        }
    }
    </style>

    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "user_phone" not in st.session_state:
    st.session_state.user_phone = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "cart" not in st.session_state:
    st.session_state.cart = []

if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"

if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Headset"


# ============================================================
# GOOGLE APPS SCRIPT
# ============================================================

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT"
    "/exec"
)


def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone,
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
    except Exception as e:
        print(f"Login sheet error: {e}")


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in_user:

    st.markdown(
        """
        <div class="hm-login-title">
            <h1>HM MOBILES</h1>
            <p>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # NO st.columns() here.
    # The form automatically centers on desktop and fills the phone width.
    with st.form("customer_direct_login_center", border=True):

        st.markdown(
            "<h3 style='text-align:center; margin:0 0 10px 0;'>"
            "Customer Portal Login</h3>",
            unsafe_allow_html=True,
        )

        cust_name = st.text_input("Your Name:")

        cust_phone = st.text_input(
            "Mobile Number:",
            max_chars=10,
        )

        login_btn = st.form_submit_button(
            "Secure Login",
            use_container_width=True,
        )

        if login_btn:

            if (
                cust_name.strip()
                and len(cust_phone.strip()) == 10
                and cust_phone.strip().isdigit()
            ):
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                st.session_state.user_role = "Customer"
                st.session_state.selected_menu = "Headset"
                st.session_state.current_view = "Home"

                log_login_to_sheet(
                    cust_name.strip(),
                    cust_phone.strip(),
                )

                st.rerun()

            else:
                st.warning(
                    "⚠️ Please provide a valid name and 10-digit mobile number."
                )

    st.stop()


# ============================================================
# AFTER LOGIN - HEADER
# ============================================================

st.markdown(
    """
    <div class="hm-brand">
        <div class="hm-brand-title">HM MOBILES THIRUVERKADU</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER NAVIGATION
# SAME HORIZONTAL ROW ON DESKTOP + MOBILE
# ============================================================

st.markdown('<div class="hm-nav">', unsafe_allow_html=True)

top_comm, top_home, top_cart, top_logout = st.columns(
    [2.4, 0.8, 0.9, 0.9],
    gap="small",
)

with top_comm:
    st.markdown(
        f"👋 Welcome, **{st.session_state.logged_in_user}**!"
    )

with top_home:
    if st.button(
        "Home",
        key="nav_home",
        use_container_width=True,
    ):
        st.session_state.current_view = "Home"
        st.rerun()

with top_cart:
    cart_count = len(st.session_state.cart)

    if st.button(
        f"Cart ({cart_count})",
        key="nav_cart",
        use_container_width=True,
    ):
        st.session_state.current_view = "Cart"
        st.rerun()

with top_logout:
    if st.button(
        "Logout",
        key="nav_logout",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ============================================================
# LOAD INVENTORY
# ============================================================

@st.cache_data(ttl=2)
def load_inventory_from_sheet():

    sheet_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ"
        "/export?format=csv"
    )

    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df

    except Exception as e:

        print(f"Inventory error: {e}")

        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")

        return pd.DataFrame()


inv_df = load_inventory_from_sheet()


# ============================================================
# PRODUCT RECORDS
# ============================================================

product_records = []

if not inv_df.empty:

    try:

        for _, row in inv_df.iterrows():

            product_records.append(
                {
                    "id": str(row.iloc[0]),
                    "name": str(row.iloc[1]),
                    "category": str(row.iloc[2]),
                    "stock": str(row.iloc[3]),
                    "price": str(row.iloc[4]),
                    "description": (
                        str(row.iloc[5]).strip()
                        if len(row) > 5 and pd.notna(row.iloc[5])
                        else ""
                    ),
                    "image": (
                        str(row.iloc[6]).strip()
                        if len(row) > 6 and pd.notna(row.iloc[6])
                        else ""
                    ),
                }
            )

    except Exception as e:

        print(f"Product parsing error: {e}")
        product_records = []


# ============================================================
# FALLBACK PRODUCTS
# ============================================================

if not product_records:

    product_records = [
        {
            "id": "ITM001",
            "name": "Bluetooth Wireless Headset",
            "price": "1200",
            "stock": "50",
            "category": "Headset",
            "image": (
                "images/Headset 1 1.jpg \\ "
                "images/Headset 1 2.jpg \\ "
                "images/Headset 1 3.jpg"
            ),
            "description": "Premium Bluetooth wireless headset.",
        },
        {
            "id": "ITM002",
            "name": "Over-Ear Gaming Headset",
            "price": "1800",
            "stock": "40",
            "category": "Headset",
            "image": "",
            "description": "Comfortable over-ear gaming headset.",
        },
        {
            "id": "ITM003",
            "name": "Fast Type-C Charger 33W",
            "price": "650",
            "stock": "120",
            "category": "Charger",
            "image": "",
            "description": "33W fast Type-C wall charger.",
        },
        {
            "id": "ITM004",
            "name": "Dual Port Fast Wall Charger",
            "price": "500",
            "stock": "90",
            "category": "Charger",
            "image": "",
            "description": "Dual-port fast charging adapter.",
        },
        {
            "id": "ITM005",
            "name": "Braided Micro USB Cable",
            "price": "250",
            "stock": "200",
            "category": "Cable",
            "image": "",
            "description": "Durable braided Micro USB cable.",
        },
        {
            "id": "ITM006",
            "name": "Type-C Fast Charging Cable",
            "price": "300",
            "stock": "150",
            "category": "Cable",
            "image": "",
            "description": "Fast charging Type-C cable.",
        },
        {
            "id": "ITM007",
            "name": "Professional Studio Mic",
            "price": "2500",
            "stock": "30",
            "category": "Mic",
            "image": "",
            "description": "Professional studio microphone.",
        },
        {
            "id": "ITM008",
            "name": "Mini Lavalier Clip-on Mic",
            "price": "450",
            "stock": "80",
            "category": "Mic",
            "image": "",
            "description": "Compact clip-on microphone.",
        },
        {
            "id": "ITM009",
            "name": "Lithium Mobile Replacement Battery",
            "price": "800",
            "stock": "45",
            "category": "Battery",
            "image": "",
            "description": "Mobile replacement battery.",
        },
        {
            "id": "ITM010",
            "name": "Edge-to-Edge Tempered Glass",
            "price": "200",
            "stock": "300",
            "category": "Tempered",
            "image": "",
            "description": "Full edge-to-edge tempered glass.",
        },
        {
            "id": "ITM011",
            "name": "Wireless Bluetooth Ear Pods",
            "price": "1500",
            "stock": "75",
            "category": "Ear pod",
            "image": "",
            "description": "Wireless Bluetooth ear pods.",
        },
    ]


# ============================================================
# CHECKOUT
# ============================================================

def process_cart_checkout(
    address: str,
    secondary_phone: str,
    description: str,
    payment_method: str,
    location_link: str,
) -> str:

    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."

    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    txn_id = (
        "TXN"
        + datetime.now().strftime("%Y%m%d%H%M%S")
    )

    cart_summary = ", ".join(
        [
            f"{item['quantity']} of {item['product']}"
            for item in st.session_state.cart
        ]
    )

    st.session_state.last_booked_item = cart_summary

    try:

        order_data = {
            "Type": "Order",
            "Timestamp": timestamp,
            "Customer_Name": customer_name,
            "Primary_Phone": primary_phone,
            "Items": cart_summary,
            "Address": address,
            "Secondary_Phone": secondary_phone,
            "Description": description,
            "Live_Location": location_link,
        }

        requests.post(
            GOOGLE_SCRIPT_URL,
            json=order_data,
            timeout=15,
        )

    except Exception as e:

        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")

    with open(
        "orders.csv",
        mode="a",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "Timestamp",
                    "Customer Name",
                    "Primary Phone",
                    "Items",
                    "Address",
                    "Secondary Phone",
                    "Description",
                    "Live Location",
                ]
            )

        writer.writerow(
            [
                timestamp,
                customer_name,
                primary_phone,
                cart_summary,
                address,
                secondary_phone,
                description,
                location_link,
            ]
        )

    st.session_state.cart = []

    return (
        f"Checkout complete! Order placed for: "
        f"{cart_summary}. Payment via "
        f"{payment_method} successful "
        f"(TXN ID: {txn_id})."
    )


# ============================================================
# HOME
# ============================================================

if st.session_state.current_view == "Home":

    st.markdown('<div class="hm-main">', unsafe_allow_html=True)

    # IMPORTANT:
    # This is ALWAYS MENU | PRODUCT.
    # It does not change to vertical on mobile.
    col_menu, col_items = st.columns(
        [1, 3],
        gap="small",
    )

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    with col_menu:

        st.markdown("### Menu")

        with st.container(
            height=480,
            border=True,
        ):

            # Keep original category behavior.
            categories = list(
                dict.fromkeys(
                    [
                        p["category"]
                        for p in product_records
                    ]
                )
            )

            for cat in categories:

                if st.button(
                    cat,
                    key=f"menu_btn_{cat}",
                    use_container_width=True,
                ):
                    st.session_state.selected_menu = cat
                    st.rerun()

    # --------------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------------

    with col_items:

        current_cat = st.session_state.get(
            "selected_menu",
            "Headset",
        )

        st.markdown(f"### {current_cat}")

        with st.container(
            height=480,
            border=True,
        ):

            filtered_items = [
                p
                for p in product_records
                if p["category"] == current_cat
            ]

            if filtered_items:

                for idx, prod in enumerate(filtered_items):

                    slide_key = (
                        f"slide_{current_cat}_{idx}"
                    )

                    if slide_key not in st.session_state:
                        st.session_state[slide_key] = 0

                    # IMPORTANT:
                    # Every product is ALWAYS:
                    # IMAGE | DESCRIPTION | PRICE
                    st.markdown(
                        '<div class="hm-product">',
                        unsafe_allow_html=True,
                    )

                    p_img_col, p_desc_col, p_details_col = st.columns(
                        [1.25, 1.45, 1],
                        gap="small",
                    )

                    # ------------------------------------------------
                    # IMAGE
                    # ------------------------------------------------

                    with p_img_col:

                        raw_img = prod.get(
                            "image",
                            "",
                        )

                        if raw_img:

                            img_paths = [
                                img.strip()
                                for img in raw_img.replace(
                                    "\\",
                                    ",",
                                ).split(",")
                                if img.strip()
                            ]

                            valid_paths = [
                                p
                                for p in img_paths
                                if os.path.exists(p)
                            ]

                            if valid_paths:

                                total_imgs = len(
                                    valid_paths
                                )

                                current_idx = (
                                    st.session_state[
                                        slide_key
                                    ]
                                )

                                if total_imgs >= 2:

                                    left_col, image_col, right_col = st.columns(
                                        [0.45, 3.1, 0.45],
                                        gap="small",
                                    )

                                    with left_col:

                                        if st.button(
                                            "‹",
                                            key=(
                                                f"prev_"
                                                f"{current_cat}_"
                                                f"{idx}"
                                            ),
                                        ):

                                            if (
                                                st.session_state[
                                                    slide_key
                                                ]
                                                > 0
                                            ):
                                                st.session_state[
                                                    slide_key
                                                ] -= 1
                                            else:
                                                st.session_state[
                                                    slide_key
                                                ] = (
                                                    total_imgs
                                                    - 1
                                                )

                                            st.rerun()

                                    with image_col:

                                        st.image(
                                            valid_paths[
                                                current_idx
                                            ],
                                            width=95,
                                        )

                                    with right_col:

                                        if st.button(
                                            "›",
                                            key=(
                                                f"next_"
                                                f"{current_cat}_"
                                                f"{idx}"
                                            ),
                                        ):

                                            if (
                                                st.session_state[
                                                    slide_key
                                                ]
                                                + 1
                                                < total_imgs
                                            ):
                                                st.session_state[
                                                    slide_key
                                                ] += 1
                                            else:
                                                st.session_state[
                                                    slide_key
                                                ] = 0

                                            st.rerun()

                                else:

                                    st.image(
                                        valid_paths[0],
                                        width=95,
                                    )

                            else:
                                st.caption("No Image")

                        else:
                            st.caption("No Image")

                    # ------------------------------------------------
                    # DESCRIPTION
                    # ------------------------------------------------

                    with p_desc_col:

                        st.markdown(
                            "**Description:**"
                        )

                        description = prod.get(
                            "description",
                            "",
                        )

                        if description:
                            st.caption(
                                description
                            )
                        else:
                            st.caption(
                                "No description available."
                            )

                    # ------------------------------------------------
                    # PRICE / PRODUCT / QUANTITY / ADD
                    # ------------------------------------------------

                    with p_details_col:

                        st.markdown(
                            f"**{prod['name']}**"
                        )

                        st.markdown(
                            f"### ₹{prod['price']}"
                        )

                        q_val = st.number_input(
                            "Qty",
                            min_value=1.0,
                            value=1.0,
                            step=1.0,
                            key=(
                                f"qty_"
                                f"{current_cat}_"
                                f"{idx}"
                            ),
                        )

                        if st.button(
                            "Add",
                            key=(
                                f"add_btn_"
                                f"{current_cat}_"
                                f"{idx}"
                            ),
                            use_container_width=True,
                        ):

                            full_q_str = (
                                f"{int(q_val)} Units"
                            )

                            st.session_state.cart.append(
                                {
                                    "product": prod[
                                        "name"
                                    ],
                                    "quantity": full_q_str,
                                }
                            )

                            st.success("Added!")
                            st.rerun()

                    st.markdown(
                        "<hr>",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True,
                    )

            else:
                st.info("No items found.")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CART / CHECKOUT
# ============================================================

else:

    st.subheader(
        "🛒 Your Shopping Cart & Checkout"
    )

    if st.session_state.cart:

        for c_idx, item in enumerate(
            st.session_state.cart
        ):

            cc1, cc2 = st.columns(
                [4, 1],
                gap="small",
            )

            with cc1:
                st.markdown(
                    f"- **{item['product']}** "
                    f"({item['quantity']})"
                )

            with cc2:

                if st.button(
                    "Remove",
                    key=f"rem_cart_view_{c_idx}",
                    use_container_width=True,
                ):

                    st.session_state.cart.pop(
                        c_idx
                    )

                    st.rerun()

        st.markdown("---")

        st.subheader(
            "📍 Secure Checkout Form"
        )

        with st.form(
            "checkout_form_main_view",
            border=True,
        ):

            checkout_address = st.text_area(
                "Delivery Address:"
            )

            secondary_phone = st.text_input(
                "Alternative Contact Number:",
                max_chars=10,
            )

            product_desc = st.text_area(
                "Product Specifications / "
                "Custom Description:"
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "UPI / GPay",
                    "Credit/Debit Card",
                    "Cash on Delivery",
                ],
            )

            live_location = st.text_input(
                "Live Location Link "
                "(Google Maps Share URL):"
            )

            submit_checkout = (
                st.form_submit_button(
                    "Complete Order & Pay"
                )
            )

            if submit_checkout:

                if (
                    checkout_address.strip()
                    and secondary_phone.strip()
                ):

                    result_msg = (
                        process_cart_checkout(
                            checkout_address,
                            secondary_phone,
                            product_desc,
                            payment_method,
                            live_location,
                        )
                    )

                    st.success(result_msg)

                    st.session_state.current_view = (
                        "Home"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Please provide delivery "
                        "address and secondary contact "
                        "number."
                    )

    else:

        st.info(
            "Your cart is empty. Click **Home** "
            "above to browse and add products."
        )
