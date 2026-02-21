import streamlit as st
from src.core.data_provider import get_revenue_metrics, get_logistics_metrics
from src.ui.dashboard import render_kpi_cards, render_revenue_charts, render_executive_summary

# ST.SET_PAGE_CONFIG MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Olist Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚀 Olist E-Commerce Strategic Overview")
    st.markdown("---")
    
    # Load Data
    with st.spinner("Fetching data from PostgreSQL..."):
        df_trend, df_cat, df_state = get_revenue_metrics()
    
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/4e/Olist_logo.png", width=150)
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a Workspace", 
                                   ["Dashboard", "Raw Data Explorer", "Settings"])
    
    if app_mode == "Dashboard":
        # Tabs
        tab1, tab2, tab3 = st.tabs(["Analytics", "Visualizations", "Insights & Recommendations"])
        
        with tab1:
            st.header("Key Performance Indicators")
            render_kpi_cards(df_trend)
            st.markdown("---")
            st.dataframe(df_trend.sort_values("revenue_month", ascending=False), use_container_width=True)
            
        with tab2:
            st.header("Visual Analytics")
            render_revenue_charts(df_trend, df_cat, df_state)
            
        with tab3:
            render_executive_summary(df_trend, df_cat)
            
    elif app_mode == "Raw Data Explorer":
        st.header("Raw Data Inspection")
        if df_trend is not None:
            st.write("Monthly Revenue Data")
            st.dataframe(df_trend)
        if df_cat is not None:
            st.write("Category Performance")
            st.dataframe(df_cat)
            
    st.sidebar.markdown("---")
    st.sidebar.info("Olist Pipeline v2.0 - Built by Andrew Shwarts")

if __name__ == "__main__":
    main()
