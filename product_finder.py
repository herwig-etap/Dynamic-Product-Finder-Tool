import streamlit as st
import pandas as pd

# Load product data
def load_data(refresh=False):
    # Force refresh logic
    if refresh:
        st.cache_data.clear()
    return pd.read_csv("products3.csv", delimiter=';')

# Filter products based on requirements
def filter_products(df, space_types, lighting_types, atex_certified, power_range, lumen_range):
    filtered = df[
        (df["Space Type"].isin(space_types)) &
        (df["Lighting Type"].isin(lighting_types)) &
        (df["Power (W)"] >= power_range[0]) &
        (df["Power (W)"] <= power_range[1]) &
        (df["Lumen Output"] >= lumen_range[0]) &
        (df["Lumen Output"] <= lumen_range[1])
    ]
    if atex_certified:
        filtered = filtered[filtered["ATEX Certified"] == "Yes"]
    return filtered

# Main Streamlit app
def main():
    st.title("Dynamic Product Finder Tool")
    st.write("Find the most suitable lighting products based on your requirements.")

    # Add a refresh button
    refresh = st.button("Refresh Data")  # Boolean indicating if refresh was clicked

    # Load data
    data = load_data(refresh=refresh)

    # Sidebar filters
    st.sidebar.header("Filter Products")

    # Multi-select for space types and lighting types
    space_types = st.sidebar.multiselect(
        "Select Space Types",
        options=data["Space Type"].unique(),
        default=data["Space Type"].unique()
    )

    lighting_types = st.sidebar.multiselect(
        "Select Lighting Types",
        options=data["Lighting Type"].unique(),
        default=data["Lighting Type"].unique()
    )

    # ATEX certification checkbox
    atex_certified = st.sidebar.checkbox("ATEX Certified (Explosion-proof)", value=False)

    # Power and lumen range sliders
    power_range = st.sidebar.slider(
        "Select Power Range (W)",
        min_value=int(data["Power (W)"].min()),
        max_value=int(data["Power (W)"].max()),
        value=(int(data["Power (W)"].min()), int(data["Power (W)"].max()))
    )

    lumen_range = st.sidebar.slider(
        "Select Lumen Output Range",
        min_value=int(data["Lumen Output"].min()),
        max_value=int(data["Lumen Output"].max()),
        value=(int(data["Lumen Output"].min()), int(data["Lumen Output"].max()))
    )

    # Filter data
    filtered_products = filter_products(data, space_types, lighting_types, atex_certified, power_range, lumen_range)

    # Display results
    st.header("Matched Products")
    if not filtered_products.empty:
        for _, row in filtered_products.iterrows():
            st.subheader(row["Product Name"])
            st.image(row["Image URL"], width=150)
            st.write(f"**Lighting Type**: {row['Lighting Type']}")
            st.write(f"**Space Type**: {row['Space Type']}")
            st.write(f"**ATEX Certified**: {row['ATEX Certified']}")
            st.write(f"**Power Consumption**: {row['Power (W)']} W")
            st.write(f"**Lumen Output**: {row['Lumen Output']} lm")
            st.write(f"[View Product]({row['Product Link']})")
            st.write("---")

        # Download results
        st.download_button(
            label="Download Matched Products as CSV",
            data=filtered_products.to_csv(index=False),
            file_name="matched_products.csv",
            mime="text/csv",
        )
    else:
        st.warning("No products match your requirements. Try adjusting your filters.")

if __name__ == "__main__":
    main()
