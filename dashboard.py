
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DataVision Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #f8fafc;
}

[data-testid="stMetric"] {
    background-color: #172238;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #27364f;
}

h1, h2, h3 {
    color: #60a5fa;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER AND SIDEBAR
# ==========================================

st.title("📊 DataVision Analytics Dashboard")

st.write(
    "Transform your data into meaningful insights."
)

st.sidebar.title("DataVision")
st.sidebar.write("Interactive Analytics Platform")

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

# ==========================================
# 4. READ DATASET
# ==========================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            original_df = pd.read_csv(uploaded_file)
        else:
            original_df = pd.read_excel(uploaded_file)

        if original_df.empty:
            st.warning("The uploaded file has no data.")

        else:

            st.success("Dataset uploaded successfully!")

            # ==========================================
            # 5. DATASET OVERVIEW
            # ==========================================

            st.header("📁 Dataset Overview")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Rows",
                original_df.shape[0]
            )

            col2.metric(
                "Total Columns",
                original_df.shape[1]
            )

            col3.metric(
                "Missing Values",
                int(original_df.isnull().sum().sum())
            )

            col4.metric(
                "Duplicate Rows",
                int(original_df.duplicated().sum())
            )

            # ==========================================
            # 6. DATASET PREVIEW
            # ==========================================

            st.header("📋 Dataset Preview")

            st.dataframe(
                original_df,
                use_container_width=True
            )

            # ==========================================
            # 7. COLUMN INFORMATION
            # ==========================================

            st.header("🔍 Column Information")

            column_info = pd.DataFrame({
                "Column Name": original_df.columns,
                "Data Type": original_df.dtypes.astype(str).values,
                "Missing Values": original_df.isnull().sum().values,
                "Unique Values": original_df.nunique().values
            })

            st.dataframe(
                column_info,
                use_container_width=True
            )

            # ==========================================
            # 8. STATISTICAL SUMMARY
            # ==========================================

            st.header("📈 Statistical Summary")

            st.dataframe(
                original_df.describe(include="all").fillna(""),
                use_container_width=True
            )

            # ==========================================
            # 9. DATA CLEANING
            # ==========================================

            st.header("🧹 Data Cleaning")

            cleaned_df = original_df.copy()

            with st.expander("Open Data Cleaning Options"):

                st.write("Choose how you want to clean your dataset.")

                missing_option = st.selectbox(
                    "Handle missing values",
                    [
                        "Keep missing values",
                        "Drop rows with missing values",
                        "Fill numeric with median and text with mode"
                    ]
                )

                remove_duplicates = st.checkbox(
                    "Remove duplicate rows"
                )

                if st.button("Apply Data Cleaning"):

                    if missing_option == "Drop rows with missing values":
                        cleaned_df = cleaned_df.dropna()

                    elif missing_option == "Fill numeric with median and text with mode":

                        for col in cleaned_df.columns:

                            if pd.api.types.is_numeric_dtype(cleaned_df[col]):

                                median_value = cleaned_df[col].median()

                                if pd.notna(median_value):
                                    cleaned_df[col] = cleaned_df[col].fillna(
                                        median_value
                                    )

                            else:

                                mode_values = cleaned_df[col].mode(
                                    dropna=True
                                )

                                if not mode_values.empty:
                                    cleaned_df[col] = cleaned_df[col].fillna(
                                        mode_values.iloc[0]
                                    )

                    if remove_duplicates:
                        cleaned_df = cleaned_df.drop_duplicates()

                    st.session_state["cleaned_df"] = cleaned_df

                    st.success("Data cleaning completed!")

            # Reuse the cleaned dataset after cleaning
            if "cleaned_df" in st.session_state:
                cleaned_df = st.session_state["cleaned_df"].copy()

            st.write("Cleaned Dataset Preview")

            st.dataframe(
                cleaned_df,
                use_container_width=True
            )

            # ==========================================
            # 10. FILTER DATA
            # ==========================================

            st.header("🔎 Interactive Data Filters")

            filter_column = st.selectbox(
                "Choose a column to filter",
                ["None"] + cleaned_df.columns.tolist()
            )

            filtered_df = cleaned_df.copy()

            if filter_column != "None":

                if pd.api.types.is_numeric_dtype(
                    cleaned_df[filter_column]
                ):

                    valid_values = cleaned_df[filter_column].dropna()

                    if not valid_values.empty:

                        minimum = float(valid_values.min())
                        maximum = float(valid_values.max())

                        if minimum < maximum:

                            selected_range = st.slider(
                                "Select value range",
                                min_value=minimum,
                                max_value=maximum,
                                value=(minimum, maximum)
                            )

                            filtered_df = cleaned_df[
                                cleaned_df[filter_column].between(
                                    selected_range[0],
                                    selected_range[1]
                                )
                            ]

                else:

                    options = (
                        cleaned_df[filter_column]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    selected_values = st.multiselect(
                        "Select values",
                        options
                    )

                    if selected_values:

                        filtered_df = cleaned_df[
                            cleaned_df[filter_column]
                            .astype(str)
                            .isin(selected_values)
                        ]

            st.write(
                f"Filtered Records: {len(filtered_df)}"
            )

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

            # ==========================================
            # 11. IDENTIFY COLUMN TYPES
            # ==========================================

            numeric_columns = filtered_df.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_columns = filtered_df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns.tolist()

            all_columns = filtered_df.columns.tolist()

            # ==========================================
            # 12. BAR CHART
            # ==========================================

            st.header("📊 Bar Chart")

            if categorical_columns and numeric_columns:

                col1, col2 = st.columns(2)

                with col1:
                    bar_x = st.selectbox(
                        "Select category",
                        categorical_columns,
                        key="bar_x"
                    )

                with col2:
                    bar_y = st.selectbox(
                        "Select numeric column",
                        numeric_columns,
                        key="bar_y"
                    )

                bar_data = (
                    filtered_df.groupby(
                        bar_x,
                        dropna=False
                    )[bar_y]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    bar_data,
                    x=bar_x,
                    y=bar_y,
                    title=f"{bar_y} by {bar_x}",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info(
                    "Bar chart requires a categorical and numeric column."
                )

            # ==========================================
            # 13. PIE CHART
            # ==========================================

            st.header("🥧 Pie Chart")

            if categorical_columns:

                pie_column = st.selectbox(
                    "Choose a category",
                    categorical_columns,
                    key="pie_column"
                )

                pie_data = (
                    filtered_df[pie_column]
                    .fillna("Missing")
                    .astype(str)
                    .value_counts()
                    .reset_index()
                )

                pie_data.columns = [
                    pie_column,
                    "Count"
                ]

                fig = px.pie(
                    pie_data,
                    names=pie_column,
                    values="Count",
                    title=f"Distribution of {pie_column}",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("Pie chart requires a categorical column.")

            # ==========================================
            # 14. HISTOGRAM
            # ==========================================

            st.header("📈 Histogram")

            if numeric_columns:

                histogram_column = st.selectbox(
                    "Choose numeric column",
                    numeric_columns,
                    key="histogram"
                )

                fig = px.histogram(
                    filtered_df,
                    x=histogram_column,
                    title=f"Distribution of {histogram_column}",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("Histogram requires a numeric column.")

            # ==========================================
            # 15. LINE CHART / TREND ANALYSIS
            # ==========================================

            st.header("📉 Trend Analysis")

            if len(all_columns) >= 2 and numeric_columns:

                col1, col2 = st.columns(2)

                with col1:
                    line_x = st.selectbox(
                        "Select X-axis",
                        all_columns,
                        key="line_x"
                    )

                with col2:
                    line_y = st.selectbox(
                        "Select Y-axis",
                        numeric_columns,
                        key="line_y"
                    )

                if line_x != line_y:

                    fig = px.line(
                        filtered_df,
                        x=line_x,
                        y=line_y,
                        markers=True,
                        title=f"{line_y} Trend",
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:
                    st.info("Choose different columns for both axes.")

            else:
                st.info("Trend analysis requires two columns, including one numeric column.")

            # ==========================================
            # 16. SCATTER PLOT
            # ==========================================

            st.header("🔵 Scatter Plot")

            if len(numeric_columns) >= 2:

                col1, col2 = st.columns(2)

                with col1:
                    scatter_x = st.selectbox(
                        "Select X-axis",
                        numeric_columns,
                        key="scatter_x"
                    )

                with col2:
                    scatter_y = st.selectbox(
                        "Select Y-axis",
                        numeric_columns,
                        key="scatter_y"
                    )

                if scatter_x != scatter_y:

                    fig = px.scatter(
                        filtered_df,
                        x=scatter_x,
                        y=scatter_y,
                        title=f"{scatter_x} vs {scatter_y}",
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:
                    st.info("Choose two different numeric columns.")

            else:
                st.info("Scatter plot requires at least two numeric columns.")

            # ==========================================
            # 17. CORRELATION HEATMAP
            # ==========================================

            st.header("🔥 Correlation Heatmap")

            if len(numeric_columns) >= 2:

                correlation = filtered_df[
                    numeric_columns
                ].corr()

                fig = px.imshow(
                    correlation,
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Between Numeric Columns",
                    color_continuous_scale="RdBu",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("Heatmap requires at least two numeric columns.")

            # ==========================================
            # 18. MISSING VALUES ANALYSIS
            # ==========================================

            st.header("🧹 Missing Values Analysis")

            missing_data = pd.DataFrame({
                "Column": original_df.columns,
                "Missing Values": original_df.isnull().sum().values
            })

            st.dataframe(
                missing_data,
                use_container_width=True
            )

            # ==========================================
            # 19. DUPLICATE ANALYSIS
            # ==========================================

            st.header("🔁 Duplicate Records")

            duplicate_count = int(
                original_df.duplicated().sum()
            )

            if duplicate_count > 0:

                st.warning(
                    f"Found {duplicate_count} duplicate rows."
                )

            else:

                st.success("No duplicate rows found!")

            # ==========================================
            # 20. SMART DATA INSIGHTS
            # ==========================================

            st.header("🧠 Smart Data Insights")

            insights = []

            insights.append(
                f"Your dataset contains {original_df.shape[0]} rows "
                f"and {original_df.shape[1]} columns."
            )

            total_missing = int(
                original_df.isnull().sum().sum()
            )

            insights.append(
                f"Your dataset contains {total_missing} missing values."
            )

            insights.append(
                f"Your dataset contains {duplicate_count} duplicate rows."
            )

            for col in numeric_columns:

                values = filtered_df[col].dropna()

                if not values.empty:

                    insights.append(
                        f"{col}: Highest value is {values.max():.2f}, "
                        f"lowest value is {values.min():.2f}, "
                        f"and average value is {values.mean():.2f}."
                    )

            for col in categorical_columns:

                counts = filtered_df[col].dropna().value_counts()

                if not counts.empty:

                    insights.append(
                        f"In {col}, '{counts.index[0]}' appears most often "
                        f"({counts.iloc[0]} times)."
                    )

            for insight in insights:

                st.info("💡 " + insight)

            # ==========================================
            # 21. DOWNLOAD DATA
            # ==========================================

            st.header("⬇️ Download Your Data")

            col1, col2 = st.columns(2)

            with col1:

                filtered_csv = filtered_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "Download Filtered Dataset",
                    data=filtered_csv,
                    file_name="datavision_filtered.csv",
                    mime="text/csv"
                )

            with col2:

                cleaned_csv = cleaned_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "Download Cleaned Dataset",
                    data=cleaned_csv,
                    file_name="datavision_cleaned.csv",
                    mime="text/csv"
                )

            # ==========================================
            # 22. EXPORT ANALYSIS REPORT
            # ==========================================

            st.header("📄 Download Analysis Report")

            report = [
                "DATAVISION - DATA ANALYSIS REPORT",
                "===================================",
                f"Total Rows: {original_df.shape[0]}",
                f"Total Columns: {original_df.shape[1]}",
                f"Missing Values: {total_missing}",
                f"Duplicate Rows: {duplicate_count}",
                "",
                "SMART DATA INSIGHTS",
                "-------------------"
            ]

            report.extend(insights)

            report_text = "\n".join(report)

            st.download_button(
                "Download Analysis Report",
                data=report_text,
                file_name="datavision_analysis_report.txt",
                mime="text/plain"
            )

    except Exception as e:

        st.error(f"Something went wrong: {e}")

else:

    st.info(
        "👈 Upload a CSV or Excel dataset using the sidebar to get started."
    )

    st.markdown("""
    ## Explore DataVision

    - 📁 CSV and Excel upload
    - 📊 Interactive charts
    - 🔎 Data filtering
    - 🧹 Data cleaning
    - 🔥 Correlation heatmap
    - 🧠 Smart Data Insights
    - 📄 Download analysis reports
    """)
