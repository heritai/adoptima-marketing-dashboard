"""
Data generator for AdOptima marketing campaign dataset.
Creates realistic synthetic data with business patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_marketing_data(months=24):
    """
    Generate 2 years of monthly marketing campaign data with realistic patterns.
    
    Patterns simulated:
    - Social Media more effective in holidays
    - Promotions boost short-term sales but reduce margins
    - Email improves retention, not acquisition
    - Diminishing returns (more spend ≠ proportional sales growth)
    """
    
    np.random.seed(42)
    random.seed(42)
    
    # Generate base data
    data = []
    base_date = datetime(2022, 1, 1)
    
    # Seasonal patterns
    seasons = ['winter', 'spring', 'summer', 'fall']
    holiday_months = [11, 12, 1, 2]  # Holiday season
    back_to_school_months = [8, 9]   # Back to school
    
    for i in range(months):
        current_date = base_date + timedelta(days=30*i)
        month = current_date.month
        year = current_date.year
        
        # Determine season and special periods
        if month in [12, 1, 2]:
            season = 'winter'
            is_holiday = month in holiday_months
        elif month in [3, 4, 5]:
            season = 'spring'
            is_holiday = False
        elif month in [6, 7, 8]:
            season = 'summer'
            is_holiday = False
        else:
            season = 'fall'
            is_holiday = month in holiday_months
            
        is_back_to_school = month in back_to_school_months
        
        # Base spend amounts (in thousands)
        base_social = 15 + np.random.normal(0, 3)
        base_search = 25 + np.random.normal(0, 5)
        base_email = 8 + np.random.normal(0, 2)
        base_promotions = 12 + np.random.normal(0, 3)
        
        # Seasonal adjustments
        if is_holiday:
            base_social *= 1.4  # Social media more effective in holidays
            base_promotions *= 1.6  # More promotions during holidays
            base_search *= 1.2
        elif is_back_to_school:
            base_social *= 1.2
            base_search *= 1.3
            base_promotions *= 1.1
        
        # Add some random variation
        social_spend = max(5, base_social + np.random.normal(0, 2))
        search_spend = max(10, base_search + np.random.normal(0, 3))
        email_spend = max(3, base_email + np.random.normal(0, 1))
        promotions_spend = max(5, base_promotions + np.random.normal(0, 2))
        
        # Competitor activity (0-100 scale)
        competitor_activity = 50 + np.random.normal(0, 15)
        competitor_activity = max(0, min(100, competitor_activity))
        
        # Calculate sales revenue based on spend and patterns
        # Base conversion rates by channel
        social_conversion = 0.12 if is_holiday else 0.08
        search_conversion = 0.15
        email_conversion = 0.20  # High conversion but for retention
        promotions_conversion = 0.25  # High but with diminishing returns
        
        # Apply diminishing returns
        social_effectiveness = social_conversion * (1 - 0.1 * (social_spend - 15) / 15)
        search_effectiveness = search_conversion * (1 - 0.05 * (search_spend - 25) / 25)
        email_effectiveness = email_conversion  # Email doesn't have diminishing returns
        promotions_effectiveness = promotions_conversion * (1 - 0.15 * (promotions_spend - 12) / 12)
        
        # Calculate revenue from each channel
        social_revenue = social_spend * social_effectiveness * 1000  # Convert to actual revenue
        search_revenue = search_spend * search_effectiveness * 1000
        email_revenue = email_spend * email_effectiveness * 1000
        promotions_revenue = promotions_spend * promotions_effectiveness * 1000
        
        # Add some cross-channel effects and noise
        total_revenue = (social_revenue + search_revenue + email_revenue + promotions_revenue)
        
        # Competitor impact (reduces effectiveness)
        competitor_impact = 1 - (competitor_activity - 50) / 200
        total_revenue *= competitor_impact
        
        # Add some random noise
        total_revenue *= (1 + np.random.normal(0, 0.1))
        
        # Ensure positive revenue
        total_revenue = max(1000, total_revenue)
        
        # Create season description
        if is_holiday:
            season_desc = 'Holiday Season'
        elif is_back_to_school:
            season_desc = 'Back to School'
        elif month in [6, 7]:
            season_desc = 'Summer'
        else:
            season_desc = 'Regular'
        
        data.append({
            'Month': current_date.strftime('%Y-%m'),
            'Social_Media_Spend': round(social_spend, 2),
            'Search_Ads_Spend': round(search_spend, 2),
            'Email_Spend': round(email_spend, 2),
            'Promotions_Spend': round(promotions_spend, 2),
            'Competitor_Activity_Index': round(competitor_activity, 1),
            'Season': season_desc,
            'Sales_Revenue': round(total_revenue, 2)
        })
    
    return pd.DataFrame(data)

def save_dataset(df, filepath):
    """Save dataset to CSV file."""
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to {filepath}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

if __name__ == "__main__":
    # Generate and save the dataset
    df = generate_marketing_data(months=24)
    save_dataset(df, '/Users/youseftaheri/Downloads/AdOptima/sample_data/marketing_data.csv')
    
    # Display sample data
    print("\nSample data:")
    print(df.head())
    print(f"\nData summary:")
    print(df.describe())
