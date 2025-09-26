"""
Visualization utilities for AdOptima marketing dashboard.
Provides charts that work well in both dark and light Streamlit themes.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

class MarketingVisualizer:
    """Handles all visualizations for the marketing dashboard."""
    
    def __init__(self):
        # Color palettes that work well in both dark and light themes
        self.colors = {
            'primary': '#1f77b4',      # Blue
            'secondary': '#ff7f0e',     # Orange
            'success': '#2ca02c',       # Green
            'warning': '#d62728',       # Red
            'info': '#9467bd',          # Purple
            'light': '#17becf',         # Cyan
            'channels': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'background': 'rgba(0,0,0,0)',
            'grid': 'rgba(128,128,128,0.2)'
        }
        
        # Chart configuration
        self.config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'adoptima_chart',
                'height': 500,
                'width': 700,
                'scale': 2
            }
        }
    
    def create_spend_vs_revenue_trend(self, data):
        """Create spend vs revenue trend chart over time."""
        fig = go.Figure()
        
        # Add revenue line
        fig.add_trace(go.Scatter(
            x=data['Month'],
            y=data['Sales_Revenue'],
            mode='lines+markers',
            name='Sales Revenue',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=6)
        ))
        
        # Add total spend line
        fig.add_trace(go.Scatter(
            x=data['Month'],
            y=data['Total_Spend'],
            mode='lines+markers',
            name='Total Marketing Spend',
            line=dict(color=self.colors['secondary'], width=3),
            marker=dict(size=6),
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Marketing Spend vs Sales Revenue Over Time',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title='Month',
            yaxis_title='Sales Revenue ($)',
            yaxis2=dict(
                title='Marketing Spend ($)',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        return fig
    
    def create_channel_effectiveness_chart(self, summary_stats):
        """Create channel effectiveness comparison chart."""
        channels = list(summary_stats['spend_by_channel'].keys())
        spend_values = list(summary_stats['spend_by_channel'].values())
        roi_values = list(summary_stats['roi_by_channel'].values())
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Marketing Spend by Channel', 'ROI by Channel'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Spend bar chart
        fig.add_trace(
            go.Bar(
                x=channels,
                y=spend_values,
                name='Total Spend',
                marker_color=self.colors['channels'],
                text=[f'${x:,.0f}' for x in spend_values],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # ROI bar chart
        fig.add_trace(
            go.Bar(
                x=channels,
                y=roi_values,
                name='Average ROI',
                marker_color=self.colors['channels'],
                text=[f'{x:.2f}' for x in roi_values],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Channel Effectiveness Analysis',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            showlegend=False,
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text="Spend ($)", row=1, col=1)
        fig.update_yaxes(title_text="ROI", row=1, col=2)
        
        return fig
    
    def create_roi_trend_chart(self, data):
        """Create ROI trend chart over time."""
        fig = go.Figure()
        
        # Calculate monthly ROI
        monthly_roi = data['Sales_Revenue'] / data['Total_Spend']
        
        fig.add_trace(go.Scatter(
            x=data['Month'],
            y=monthly_roi,
            mode='lines+markers',
            name='Monthly ROI',
            line=dict(color=self.colors['success'], width=3),
            marker=dict(size=6),
            fill='tonexty'
        ))
        
        # Add average ROI line
        avg_roi = monthly_roi.mean()
        fig.add_hline(
            y=avg_roi,
            line_dash="dash",
            line_color=self.colors['warning'],
            annotation_text=f"Average ROI: {avg_roi:.2f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title={
                'text': 'Return on Investment (ROI) Over Time',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title='Month',
            yaxis_title='ROI',
            hovermode='x unified',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        return fig
    
    def create_budget_allocation_chart(self, current_allocation, optimized_allocation):
        """Create budget allocation comparison chart."""
        channels = list(current_allocation.keys())
        current_values = list(current_allocation.values())
        optimized_values = list(optimized_allocation.values())
        
        fig = go.Figure()
        
        # Current allocation
        fig.add_trace(go.Bar(
            name='Current Allocation',
            x=channels,
            y=current_values,
            marker_color=self.colors['primary'],
            text=[f'${x:,.0f}' for x in current_values],
            textposition='auto'
        ))
        
        # Optimized allocation
        fig.add_trace(go.Bar(
            name='Optimized Allocation',
            x=channels,
            y=optimized_values,
            marker_color=self.colors['secondary'],
            text=[f'${x:,.0f}' for x in optimized_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title={
                'text': 'Budget Allocation: Current vs Optimized',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title='Marketing Channel',
            yaxis_title='Budget Allocation ($)',
            barmode='group',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def create_feature_importance_chart(self, importance_df, top_n=10):
        """Create feature importance chart."""
        if importance_df is None or len(importance_df) == 0:
            return None
        
        # Get top N features
        top_features = importance_df.head(top_n)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=top_features['importance'],
            y=top_features['feature'],
            orientation='h',
            marker_color=self.colors['info'],
            text=[f'{x:.3f}' for x in top_features['importance']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title={
                'text': f'Top {top_n} Feature Importance',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title='Importance Score',
            yaxis_title='Feature',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        return fig
    
    def create_scenario_comparison_chart(self, scenario_results):
        """Create scenario comparison chart."""
        scenarios = list(scenario_results.keys())
        revenues = [scenario_results[s]['revenue'] for s in scenarios]
        rois = [scenario_results[s]['roi'] for s in scenarios]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Revenue by Scenario', 'ROI by Scenario'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Revenue bars
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=revenues,
                name='Revenue',
                marker_color=self.colors['channels'][:len(scenarios)],
                text=[f'${x:,.0f}' for x in revenues],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # ROI bars
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=rois,
                name='ROI',
                marker_color=self.colors['channels'][:len(scenarios)],
                text=[f'{x:.2f}' for x in rois],
                textposition='auto'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title={
                'text': 'Scenario Analysis Comparison',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            showlegend=False,
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(size=12)
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="ROI", row=1, col=2)
        
        return fig
    
    def create_kpi_cards(self, summary_stats):
        """Create KPI cards for the dashboard."""
        kpis = {
            'Total Spend': f"${summary_stats['total_spend']:,.0f}",
            'Total Revenue': f"${summary_stats['total_revenue']:,.0f}",
            'Average ROI': f"{summary_stats['avg_roi']:.2f}",
            'Avg Monthly Spend': f"${summary_stats['avg_monthly_spend']:,.0f}"
        }
        
        return kpis
    
    def create_optimization_insights(self, optimization_result):
        """Create insights text for optimization results."""
        insights = []
        
        # Revenue improvement
        if optimization_result['revenue_improvement'] > 0:
            insights.append(
                f"💰 **Revenue Boost**: Optimized allocation could increase revenue by "
                f"${optimization_result['revenue_improvement']:,.0f} "
                f"({optimization_result['revenue_improvement']/optimization_result['current_revenue']*100:.1f}%)"
            )
        else:
            insights.append(
                f"📉 **Revenue Impact**: Current allocation is already well-optimized. "
                f"Minimal change expected: ${optimization_result['revenue_improvement']:,.0f}"
            )
        
        # ROI improvement
        if optimization_result['roi_improvement'] > 0:
            insights.append(
                f"📈 **ROI Improvement**: Expected ROI increase of "
                f"{optimization_result['roi_improvement']:.3f} "
                f"({optimization_result['roi_improvement']/optimization_result['current_roi']*100:.1f}%)"
            )
        else:
            insights.append(
                f"📊 **ROI Status**: Current ROI is already optimal. "
                f"Change: {optimization_result['roi_improvement']:.3f}"
            )
        
        # Channel recommendations
        current = optimization_result['current_allocation']
        optimized = optimization_result['optimized_allocation']
        
        recommendations = []
        for channel in current.keys():
            current_val = current[channel]
            optimized_val = optimized[channel]
            change_pct = (optimized_val - current_val) / current_val * 100
            
            if abs(change_pct) > 5:  # Only show significant changes
                if change_pct > 0:
                    recommendations.append(
                        f"📈 **{channel.replace('_', ' ').title()}**: Increase by {change_pct:.1f}% "
                        f"(${optimized_val - current_val:,.0f})"
                    )
                else:
                    recommendations.append(
                        f"📉 **{channel.replace('_', ' ').title()}**: Decrease by {abs(change_pct):.1f}% "
                        f"(${current_val - optimized_val:,.0f})"
                    )
        
        if recommendations:
            insights.extend(recommendations)
        
        return insights

def get_theme_colors():
    """Get colors that work well with Streamlit themes."""
    return {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'warning': '#d62728',
        'info': '#9467bd',
        'light': '#17becf',
        'channels': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    }

if __name__ == "__main__":
    # Test the visualizer
    from data_prep import load_and_preprocess_data
    
    data_path = '/Users/youseftaheri/Downloads/AdOptima/sample_data/marketing_data.csv'
    processor, processed_data = load_and_preprocess_data(data_path)
    
    if processor is not None:
        visualizer = MarketingVisualizer()
        summary_stats = processor.get_summary_stats()
        
        # Test trend chart
        trend_fig = visualizer.create_spend_vs_revenue_trend(processed_data)
        print("Trend chart created successfully!")
        
        # Test effectiveness chart
        effectiveness_fig = visualizer.create_channel_effectiveness_chart(summary_stats)
        print("Effectiveness chart created successfully!")
        
        # Test KPI cards
        kpis = visualizer.create_kpi_cards(summary_stats)
        print("KPI cards created successfully!")
        print(kpis)
