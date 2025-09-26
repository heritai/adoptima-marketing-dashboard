"""
AdOptima - AI-Powered Marketing Campaign Optimizer
Main Streamlit dashboard application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from data_prep import MarketingDataProcessor
from campaign_model import MarketingCampaignModel
from visualization import MarketingVisualizer

# Page configuration
st.set_page_config(
    page_title="AdOptima - Marketing Campaign Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-card {
        background-color: rgba(31, 119, 180, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .insight-box {
        background-color: rgba(255, 127, 14, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
        background-color: rgba(128, 128, 128, 0.1);
        border-radius: 0.5rem;
        margin: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the marketing data."""
    data_path = 'sample_data/marketing_data.csv'
    processor = MarketingDataProcessor(data_path)
    data = processor.load_data()
    if data is not None:
        processed_data = processor.preprocess_data()
        return processor, processed_data
    return None, None

@st.cache_resource
def train_models(_processor):
    """Train and cache the ML models."""
    X_train, X_test, y_train, y_test = _processor.prepare_modeling_data()
    feature_names = _processor.get_feature_columns()
    
    model = MarketingCampaignModel()
    model.train_models(X_train, y_train, X_test, y_test)
    
    return model, feature_names

def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 AdOptima - AI-Powered Marketing Campaign Optimizer</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        Maximize your marketing ROI with AI-driven insights and optimization recommendations
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading marketing data..."):
        processor, processed_data = load_data()
    
    if processor is None or processed_data is None:
        st.error("Failed to load data. Please check if the data file exists.")
        return
    
    # Train models
    with st.spinner("Training AI models..."):
        model, feature_names = train_models(processor)
    
    # Initialize visualizer
    visualizer = MarketingVisualizer()
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Page selection
    page = st.sidebar.selectbox(
        "Select Dashboard Section",
        ["📈 Global Insights", "🎯 Campaign Optimizer", "🔮 Scenario Explorer", "📊 Model Performance"]
    )
    
    # Get summary statistics
    summary_stats = processor.get_summary_stats()
    
    if page == "📈 Global Insights":
        show_global_insights(processed_data, summary_stats, visualizer)
    elif page == "🎯 Campaign Optimizer":
        show_campaign_optimizer(processed_data, model, feature_names, visualizer)
    elif page == "🔮 Scenario Explorer":
        show_scenario_explorer(processed_data, model, feature_names, visualizer)
    elif page == "📊 Model Performance":
        show_model_performance(model, feature_names, visualizer)

def show_global_insights(data, summary_stats, visualizer):
    """Display global insights and KPIs."""
    
    st.header("📈 Global Marketing Insights")
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Marketing Spend",
            value=f"${summary_stats['total_spend']:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Sales Revenue",
            value=f"${summary_stats['total_revenue']:,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Average ROI",
            value=f"{summary_stats['avg_roi']:.2f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Avg Monthly Spend",
            value=f"${summary_stats['avg_monthly_spend']:,.0f}",
            delta=None
        )
    
    # Charts
    st.subheader("Marketing Performance Trends")
    
    # Spend vs Revenue Trend
    trend_fig = visualizer.create_spend_vs_revenue_trend(data)
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>📊 Trend Analysis:</strong> This chart shows how sales revenue responds to marketing spend over time. 
    Notice the correlation between spend and revenue, but also observe periods where increased spend doesn't 
    proportionally increase sales - indicating diminishing returns.
    </div>
    """, unsafe_allow_html=True)
    
    # Channel Effectiveness
    st.subheader("Channel Effectiveness Analysis")
    
    effectiveness_fig = visualizer.create_channel_effectiveness_chart(summary_stats)
    st.plotly_chart(effectiveness_fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>🎯 Channel Insights:</strong> Compare total spend vs ROI across channels. Channels with higher ROI 
    relative to their spend are more efficient. Look for opportunities to reallocate budget from low-ROI 
    channels to high-ROI channels.
    </div>
    """, unsafe_allow_html=True)
    
    # ROI Trend
    roi_fig = visualizer.create_roi_trend_chart(data)
    st.plotly_chart(roi_fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>📈 ROI Analysis:</strong> Track ROI performance over time. A declining trend may indicate 
    market saturation or increased competition. The dashed line shows the average ROI for reference.
    </div>
    """, unsafe_allow_html=True)

def show_campaign_optimizer(data, model, feature_names, visualizer):
    """Display campaign optimization interface."""
    
    st.header("🎯 Campaign Optimizer")
    st.markdown("Adjust your marketing budget allocation and see AI-powered predictions for revenue and ROI.")
    
    # Current allocation (based on latest data)
    latest_data = data.iloc[-1]
    current_total = latest_data['Total_Spend']
    
    st.subheader("Current Budget Allocation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Budget allocation sliders
        st.markdown("**Adjust Budget Allocation (in thousands $)**")
        
        col_social, col_search = st.columns(2)
        with col_social:
            social_budget = st.slider(
                "Social Media Spend",
                min_value=5.0,
                max_value=50.0,
                value=float(latest_data['Social_Media_Spend']),
                step=1.0,
                help="Social media advertising budget"
            )
            
            email_budget = st.slider(
                "Email Marketing Spend",
                min_value=2.0,
                max_value=20.0,
                value=float(latest_data['Email_Spend']),
                step=0.5,
                help="Email marketing and automation budget"
            )
        
        with col_search:
            search_budget = st.slider(
                "Search Ads Spend",
                min_value=10.0,
                max_value=60.0,
                value=float(latest_data['Search_Ads_Spend']),
                step=1.0,
                help="Search engine advertising budget"
            )
            
            promotions_budget = st.slider(
                "Promotions Spend",
                min_value=5.0,
                max_value=40.0,
                value=float(latest_data['Promotions_Spend']),
                step=1.0,
                help="Promotional campaigns and discounts budget"
            )
    
    with col2:
        # Current allocation summary
        total_budget = social_budget + search_budget + email_budget + promotions_budget
        
        st.markdown("**Current Allocation**")
        st.metric("Total Budget", f"${total_budget:,.0f}K")
        
        allocation = {
            'social_media': social_budget,
            'search_ads': search_budget,
            'email': email_budget,
            'promotions': promotions_budget
        }
        
        # Show allocation percentages
        for channel, amount in allocation.items():
            pct = (amount / total_budget) * 100
            st.write(f"{channel.replace('_', ' ').title()}: {pct:.1f}%")
    
    # Optimization
    st.subheader("AI-Powered Optimization")
    
    if st.button("🚀 Optimize Budget Allocation", type="primary"):
        with st.spinner("Running AI optimization..."):
            # Run optimization
            optimization_result = model.optimize_budget_allocation(
                allocation, total_budget, feature_names, 'normal'
            )
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Optimization Results**")
                
                # Revenue comparison
                st.metric(
                    "Predicted Revenue",
                    f"${optimization_result['optimized_revenue']:,.0f}",
                    delta=f"${optimization_result['revenue_improvement']:,.0f}"
                )
                
                st.metric(
                    "Predicted ROI",
                    f"{optimization_result['optimized_roi']:.3f}",
                    delta=f"{optimization_result['roi_improvement']:.3f}"
                )
            
            with col2:
                # Budget allocation comparison chart
                allocation_fig = visualizer.create_budget_allocation_chart(
                    allocation, optimization_result['optimized_allocation']
                )
                st.plotly_chart(allocation_fig, use_container_width=True)
            
            # Insights
            st.subheader("💡 AI Recommendations")
            insights = visualizer.create_optimization_insights(optimization_result)
            
            for insight in insights:
                st.markdown(f"• {insight}")
            
            # Detailed recommendations
            st.subheader("📋 Detailed Recommendations")
            
            current = optimization_result['current_allocation']
            optimized = optimization_result['optimized_allocation']
            
            rec_df = pd.DataFrame({
                'Channel': [ch.replace('_', ' ').title() for ch in current.keys()],
                'Current ($K)': list(current.values()),
                'Optimized ($K)': list(optimized.values()),
                'Change ($K)': [optimized[ch] - current[ch] for ch in current.keys()],
                'Change (%)': [((optimized[ch] - current[ch]) / current[ch] * 100) for ch in current.keys()]
            })
            
            st.dataframe(rec_df, use_container_width=True)

def show_scenario_explorer(data, model, feature_names, visualizer):
    """Display scenario exploration interface."""
    
    st.header("🔮 Scenario Explorer")
    st.markdown("Explore how different market conditions affect your marketing performance.")
    
    # Scenario selection
    st.subheader("Select Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox(
            "Choose Market Scenario",
            ["Normal Market", "Holiday Season", "High Competition", "Economic Downturn"],
            help="Select different market conditions to see their impact"
        )
    
    with col2:
        total_budget = st.number_input(
            "Total Marketing Budget ($K)",
            min_value=50.0,
            max_value=200.0,
            value=75.0,
            step=5.0,
            help="Set your total marketing budget"
        )
    
    # Default allocation
    default_allocation = {
        'social_media': total_budget * 0.25,
        'search_ads': total_budget * 0.35,
        'email': total_budget * 0.15,
        'promotions': total_budget * 0.25
    }
    
    # Map scenario to model parameter
    scenario_map = {
        "Normal Market": "normal",
        "Holiday Season": "holiday",
        "High Competition": "competitor_high",
        "Economic Downturn": "normal"  # Could be enhanced with specific downturn logic
    }
    
    if st.button("🔍 Analyze Scenario", type="primary"):
        with st.spinner("Analyzing scenario..."):
            # Run scenario analysis
            scenario_key = scenario_map[scenario]
            optimization_result = model.optimize_budget_allocation(
                default_allocation, total_budget, feature_names, scenario_key
            )
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{scenario} Analysis**")
                
                st.metric(
                    "Predicted Revenue",
                    f"${optimization_result['optimized_revenue']:,.0f}",
                    delta=f"${optimization_result['revenue_improvement']:,.0f}"
                )
                
                st.metric(
                    "Predicted ROI",
                    f"{optimization_result['optimized_roi']:.3f}",
                    delta=f"{optimization_result['roi_improvement']:.3f}"
                )
            
            with col2:
                # Scenario-specific insights
                st.markdown("**Scenario Insights**")
                
                if scenario == "Holiday Season":
                    st.info("🎄 Holiday season typically shows higher effectiveness for social media and promotions. Consider increasing these channels.")
                elif scenario == "High Competition":
                    st.warning("⚔️ High competition requires more aggressive spending on search ads and promotions to maintain market share.")
                elif scenario == "Economic Downturn":
                    st.error("📉 Economic downturn may require focusing on high-ROI channels like email marketing and reducing overall spend.")
                else:
                    st.success("📊 Normal market conditions allow for balanced allocation across all channels.")
            
            # Show scenario comparison
            st.subheader("📊 Scenario Comparison")
            
            # Run multiple scenarios for comparison
            scenarios = ["normal", "holiday", "competitor_high"]
            scenario_results = {}
            
            for sc in scenarios:
                result = model.optimize_budget_allocation(
                    default_allocation, total_budget, feature_names, sc
                )
                scenario_results[sc.replace('_', ' ').title()] = {
                    'revenue': result['optimized_revenue'],
                    'roi': result['optimized_roi']
                }
            
            # Create comparison chart
            comparison_fig = visualizer.create_scenario_comparison_chart(scenario_results)
            st.plotly_chart(comparison_fig, use_container_width=True)

def show_model_performance(model, feature_names, visualizer):
    """Display model performance metrics and feature importance."""
    
    st.header("📊 Model Performance & Insights")
    
    # Model performance metrics
    st.subheader("Model Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Linear Regression Model**")
        perf = model.model_performance['linear']
        st.metric("R² Score (Test)", f"{perf['test_r2']:.3f}")
        st.metric("RMSE (Test)", f"{perf['test_rmse']:.2f}")
        st.metric("MAE (Test)", f"{perf['test_mae']:.2f}")
    
    with col2:
        st.markdown("**Random Forest Model**")
        perf = model.model_performance['random_forest']
        st.metric("R² Score (Test)", f"{perf['test_r2']:.3f}")
        st.metric("RMSE (Test)", f"{perf['test_rmse']:.2f}")
        st.metric("MAE (Test)", f"{perf['test_mae']:.2f}")
    
    # Feature importance
    st.subheader("Feature Importance Analysis")
    
    importance_df = model.get_feature_importance(feature_names)
    
    if importance_df is not None:
        # Feature importance chart
        importance_fig = visualizer.create_feature_importance_chart(importance_df, top_n=10)
        if importance_fig:
            st.plotly_chart(importance_fig, use_container_width=True)
        
        # Feature importance table
        st.markdown("**Top 10 Most Important Features**")
        st.dataframe(importance_df.head(10), use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>🔍 Feature Importance Insights:</strong> This analysis shows which factors most strongly 
        influence sales revenue. Features with higher importance scores have greater impact on predictions. 
        Use this to understand what drives your marketing success.
        </div>
        """, unsafe_allow_html=True)
    
    # Channel effectiveness analysis
    st.subheader("Channel Effectiveness Analysis")
    
    channel_effectiveness = model.get_channel_effectiveness(feature_names)
    
    if channel_effectiveness:
        # Create channel effectiveness chart
        channels = list(channel_effectiveness.keys())
        importance_scores = list(channel_effectiveness.values())
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=channels,
            y=importance_scores,
            marker_color=visualizer.colors['channels'][:len(channels)],
            text=[f'{x:.3f}' for x in importance_scores],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Channel Effectiveness (Feature Importance)",
            xaxis_title="Marketing Channel",
            yaxis_title="Importance Score",
            plot_bgcolor=visualizer.colors['background'],
            paper_bgcolor=visualizer.colors['background']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 Channel Insights:</strong> This chart shows the relative importance of each marketing 
        channel based on the AI model's analysis. Channels with higher scores have greater impact on 
        sales revenue and should be prioritized in budget allocation.
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
