"""
Data preparation utilities for AdOptima marketing dashboard.
Handles data loading, preprocessing, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class MarketingDataProcessor:
    """Handles data loading and preprocessing for marketing campaign data."""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.processed_data = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self):
        """Load marketing data from CSV file."""
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Data loaded successfully. Shape: {self.data.shape}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def preprocess_data(self):
        """Preprocess the marketing data for modeling."""
        if self.data is None:
            print("No data loaded. Please load data first.")
            return None
        
        df = self.data.copy()
        
        # Convert Month to datetime and extract features
        df['Month'] = pd.to_datetime(df['Month'])
        df['Year'] = df['Month'].dt.year
        df['Month_Num'] = df['Month'].dt.month
        
        # Encode categorical variables
        if 'Season' in df.columns:
            le_season = LabelEncoder()
            df['Season_Encoded'] = le_season.fit_transform(df['Season'])
            self.label_encoders['Season'] = le_season
        
        # Create additional features
        df['Total_Spend'] = (df['Social_Media_Spend'] + 
                            df['Search_Ads_Spend'] + 
                            df['Email_Spend'] + 
                            df['Promotions_Spend'])
        
        # Calculate spend ratios
        df['Social_Spend_Ratio'] = df['Social_Media_Spend'] / df['Total_Spend']
        df['Search_Spend_Ratio'] = df['Search_Ads_Spend'] / df['Total_Spend']
        df['Email_Spend_Ratio'] = df['Email_Spend'] / df['Total_Spend']
        df['Promotions_Spend_Ratio'] = df['Promotions_Spend'] / df['Total_Spend']
        
        # Calculate ROI for each channel
        df['Social_ROI'] = df['Sales_Revenue'] * df['Social_Spend_Ratio'] / df['Social_Media_Spend']
        df['Search_ROI'] = df['Sales_Revenue'] * df['Search_Spend_Ratio'] / df['Search_Ads_Spend']
        df['Email_ROI'] = df['Sales_Revenue'] * df['Email_Spend_Ratio'] / df['Email_Spend']
        df['Promotions_ROI'] = df['Sales_Revenue'] * df['Promotions_Spend_Ratio'] / df['Promotions_Spend']
        
        # Overall ROI
        df['Overall_ROI'] = df['Sales_Revenue'] / df['Total_Spend']
        
        # Lag features for time series patterns
        df['Sales_Revenue_Lag1'] = df['Sales_Revenue'].shift(1)
        df['Total_Spend_Lag1'] = df['Total_Spend'].shift(1)
        
        # Rolling averages
        df['Sales_Revenue_MA3'] = df['Sales_Revenue'].rolling(window=3, min_periods=1).mean()
        df['Total_Spend_MA3'] = df['Total_Spend'].rolling(window=3, min_periods=1).mean()
        
        # Fill NaN values
        df = df.fillna(method='bfill').fillna(method='ffill')
        
        self.processed_data = df
        return df
    
    def get_feature_columns(self):
        """Get list of feature columns for modeling."""
        if self.processed_data is None:
            print("No processed data available.")
            return []
        
        feature_cols = [
            'Social_Media_Spend', 'Search_Ads_Spend', 'Email_Spend', 'Promotions_Spend',
            'Competitor_Activity_Index', 'Month_Num', 'Season_Encoded',
            'Social_Spend_Ratio', 'Search_Spend_Ratio', 'Email_Spend_Ratio', 'Promotions_Spend_Ratio',
            'Sales_Revenue_Lag1', 'Total_Spend_Lag1', 'Sales_Revenue_MA3', 'Total_Spend_MA3'
        ]
        
        # Filter to only include columns that exist
        available_cols = [col for col in feature_cols if col in self.processed_data.columns]
        return available_cols
    
    def prepare_modeling_data(self, target_col='Sales_Revenue'):
        """Prepare data for machine learning modeling."""
        if self.processed_data is None:
            print("No processed data available. Please preprocess data first.")
            return None, None, None, None
        
        feature_cols = self.get_feature_columns()
        
        X = self.processed_data[feature_cols]
        y = self.processed_data[target_col]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def get_summary_stats(self):
        """Get summary statistics for the dataset."""
        if self.processed_data is None:
            print("No processed data available.")
            return None
        
        summary = {
            'total_months': len(self.processed_data),
            'total_spend': self.processed_data['Total_Spend'].sum(),
            'total_revenue': self.processed_data['Sales_Revenue'].sum(),
            'avg_roi': self.processed_data['Overall_ROI'].mean(),
            'avg_monthly_spend': self.processed_data['Total_Spend'].mean(),
            'avg_monthly_revenue': self.processed_data['Sales_Revenue'].mean(),
            'spend_by_channel': {
                'Social Media': self.processed_data['Social_Media_Spend'].sum(),
                'Search Ads': self.processed_data['Search_Ads_Spend'].sum(),
                'Email': self.processed_data['Email_Spend'].sum(),
                'Promotions': self.processed_data['Promotions_Spend'].sum()
            },
            'roi_by_channel': {
                'Social Media': self.processed_data['Social_ROI'].mean(),
                'Search Ads': self.processed_data['Search_ROI'].mean(),
                'Email': self.processed_data['Email_ROI'].mean(),
                'Promotions': self.processed_data['Promotions_ROI'].mean()
            }
        }
        
        return summary
    
    def get_optimization_data(self, budget_allocation):
        """Prepare data for budget optimization scenarios."""
        if self.processed_data is None:
            print("No processed data available.")
            return None
        
        # Get the latest data point as baseline
        latest_data = self.processed_data.iloc[-1:].copy()
        
        # Update with new budget allocation
        total_budget = sum(budget_allocation.values())
        latest_data['Social_Media_Spend'] = budget_allocation['social_media']
        latest_data['Search_Ads_Spend'] = budget_allocation['search_ads']
        latest_data['Email_Spend'] = budget_allocation['email']
        latest_data['Promotions_Spend'] = budget_allocation['promotions']
        latest_data['Total_Spend'] = total_budget
        
        # Recalculate ratios
        latest_data['Social_Spend_Ratio'] = latest_data['Social_Media_Spend'] / latest_data['Total_Spend']
        latest_data['Search_Spend_Ratio'] = latest_data['Search_Ads_Spend'] / latest_data['Total_Spend']
        latest_data['Email_Spend_Ratio'] = latest_data['Email_Spend'] / latest_data['Total_Spend']
        latest_data['Promotions_Spend_Ratio'] = latest_data['Promotions_Spend'] / latest_data['Total_Spend']
        
        # Prepare features for prediction
        feature_cols = self.get_feature_columns()
        X_optimization = latest_data[feature_cols]
        
        return X_optimization

def load_and_preprocess_data(data_path):
    """Convenience function to load and preprocess data."""
    processor = MarketingDataProcessor(data_path)
    data = processor.load_data()
    if data is not None:
        processed_data = processor.preprocess_data()
        return processor, processed_data
    return None, None

if __name__ == "__main__":
    # Test the data processor
    data_path = '/Users/youseftaheri/Downloads/AdOptima/sample_data/marketing_data.csv'
    processor, processed_data = load_and_preprocess_data(data_path)
    
    if processor is not None:
        print("Data preprocessing completed successfully!")
        print(f"Processed data shape: {processed_data.shape}")
        
        # Get summary stats
        summary = processor.get_summary_stats()
        print(f"\nSummary Statistics:")
        print(f"Total Spend: ${summary['total_spend']:,.2f}")
        print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
        print(f"Average ROI: {summary['avg_roi']:.2f}")
        
        # Test optimization data preparation
        test_allocation = {
            'social_media': 20,
            'search_ads': 30,
            'email': 10,
            'promotions': 15
        }
        opt_data = processor.get_optimization_data(test_allocation)
        print(f"\nOptimization data prepared. Shape: {opt_data.shape}")
