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
