import streamlit as st
import pandas as pd

# Load product data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

# Filter products based on customer requirements
def filter_products(df, space_type, lighting_type, atex_certified):
    filtered = df[
        (df["Space Type"] == space_type) &
        (df["Lighting Type"] == lighting_type) &
        ((df["ATEX Certified"] == "Yes") if atex_certified else True)
    ]
    return filtered

# Main Streamlit app
def main():
    st.title("Dynamic Product Finder Tool")
    st.write("Find the most suitable lighting products based on your requirements.")

    # Load product data
    data = load_data()

    # Input Form
    st.sidebar.header("Enter Your Requirements")
    space_type = st.sidebar.selectbox("Space Type", options=data["Space Type"].unique())
    lighting_type = st.sidebar.selectbox("Lighting Type", options=data["Lighting Type"].unique())
    atex_certified = st.sidebar.checkbox("ATEX Certified (Explosion-proof)", value=False)

    # Filter products
    filtered_products = filter_products(data, space_type, lighting_type, atex_certified)

    # Display Results
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

        # Download Results
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
