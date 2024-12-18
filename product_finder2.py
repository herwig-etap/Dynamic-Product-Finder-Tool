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
            # Create columns for the grid
            cols = st.columns(3)

            # Loop through the rows and distribute them across columns
            for index, row in filtered_data.iterrows():
                # Place content in one of the 3 columns using modulo operator
                with cols[index % 3]:
                    st.image(row["Image URL"], width=130)  # Set a smaller image size
                    st.markdown(f"""
                        <div style="text-align: center; font-size: 14px; font-weight: bold; margin-bottom: 15px;border-radius: 8px;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);background-color: #f9f9f9;padding: 10px;">
                        {row["Product Name"]}
                        </div>
                        <div style="font-size: 12px; line-height: 1.4; margin-bottom: 10px;">
                            <b>Lighting Type:</b> {row['Lighting Type']}<br>
                            <b>Space Type:</b> {row['Space Type']}<br>
                            <b>Power:</b> {row['Power (W)']} W<br>
                            <b>Lumen Output:</b> {row['Lumen Output']} lm
                        </div>
                    <a href="{row['Product Link']}" target="_blank" style="font-size: 12px; color: blue;">View Product</a>
                    <hr style="border: 0.5px solid #ddd; margin-top: 10px;">
                """, unsafe_allow_html=True)  # Render HTML for better styling

    else:
        st.info("Please choose your filters in the sidebar and click 'Apply Filters' to see results.")

if __name__ == "__main__":
    main()
