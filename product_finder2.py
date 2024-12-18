import streamlit as st
import pandas as pd

# Load product data
@st.cache_data
def load_data():
    try:
        # Load and clean the data
        data = pd.read_csv("products3.csv", delimiter=';')
        data["Power (W)"] = pd.to_numeric(data["Power (W)"], errors="coerce")
        data["Lumen Output"] = pd.to_numeric(data["Lumen Output"], errors="coerce")
        data = data.dropna(subset=["Power (W)", "Lumen Output"])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Main function
def main():
    st.title("Dynamic Product Finder Tool")
    st.write("Choose filters to find the most suitable luminaires.")

    # Load data
    data = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Products")

    # Space Types and Lighting Types
    space_types = st.sidebar.multiselect(
        "Select Space Types",
        options=data["Space Type"].dropna().unique(),
        default=[]
    )

    lighting_types = st.sidebar.multiselect(
        "Select Lighting Types",
        options=data["Lighting Type"].dropna().unique(),
        default=[]
    )

    # ATEX Certification checkbox
    atex_certified = st.sidebar.checkbox("ATEX Certified (Explosion-proof)", value=False)

    # Power and Lumen range sliders
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

    # Apply Filters button
    if st.sidebar.button("Apply Filters"):
        st.session_state.show_results = True

    # Check if filters have been applied
    if st.session_state.get("show_results", False):
        # Filter the data based on user inputs
        filtered_data = data[
            (data["Space Type"].isin(space_types)) &
            (data["Lighting Type"].isin(lighting_types)) &
            (data["Power (W)"] >= power_range[0]) &
            (data["Power (W)"] <= power_range[1]) &
            (data["Lumen Output"] >= lumen_range[0]) &
            (data["Lumen Output"] <= lumen_range[1])
        ]

        if atex_certified:
            filtered_data = filtered_data[filtered_data["ATEX Certified"] == "Yes"]

        # Display filtered results
        st.header("Matched Products")
        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                st.subheader(row["Product Name"])
                st.image(row["Image URL"], width=150)
                st.write(f"**Lighting Type**: {row['Lighting Type']}")
                st.write(f"**Space Type**: {row['Space Type']}")
                st.write(f"**ATEX Certified**: {row['ATEX Certified']}")
                st.write(f"**Power Consumption**: {row['Power (W)']} W")
                st.write(f"**Lumen Output**: {row['Lumen Output']} lm")
                st.write(f"[View Product]({row['Product Link']})")
                st.write("---")
        else:
            st.warning("No products match your filters. Please adjust your selections.")

    else:
        st.info("Please choose your filters in the sidebar and click 'Apply Filters' to see results.")

if __name__ == "__main__":
    main()
