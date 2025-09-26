"""
Machine learning models for marketing campaign optimization.
Implements Linear Regression and Random Forest models with optimization logic.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

class MarketingCampaignModel:
    """Marketing campaign optimization model with multiple algorithms."""
    
    def __init__(self):
        self.linear_model = LinearRegression()
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models = {
            'linear': self.linear_model,
            'random_forest': self.rf_model
        }
        self.is_trained = False
        self.feature_importance = None
        self.model_performance = {}
        
    def train_models(self, X_train, y_train, X_test, y_test):
        """Train both linear regression and random forest models."""
        print("Training marketing campaign models...")
        
        for name, model in self.models.items():
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Calculate metrics
            train_r2 = r2_score(y_train, y_pred_train)
            test_r2 = r2_score(y_test, y_pred_test)
            train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
            train_mae = mean_absolute_error(y_train, y_pred_train)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            
            self.model_performance[name] = {
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mae': train_mae,
                'test_mae': test_mae
            }
            
            print(f"{name.upper()} Model Performance:")
            print(f"  R² Score (Train): {train_r2:.3f}")
            print(f"  R² Score (Test): {test_r2:.3f}")
            print(f"  RMSE (Test): {test_rmse:.2f}")
            print(f"  MAE (Test): {test_mae:.2f}")
            print()
        
        # Get feature importance from Random Forest
        if hasattr(self.rf_model, 'feature_importances_'):
            self.feature_importance = self.rf_model.feature_importances_
        
        self.is_trained = True
        print("Model training completed!")
    
    def predict_revenue(self, X, model_name='random_forest'):
        """Predict revenue for given features."""
        if not self.is_trained:
            raise ValueError("Models must be trained before making predictions.")
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Available: {list(self.models.keys())}")
        
        model = self.models[model_name]
        predictions = model.predict(X)
        return predictions
    
    def get_feature_importance(self, feature_names):
        """Get feature importance from Random Forest model."""
        if not self.is_trained or self.feature_importance is None:
            return None
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def optimize_budget_allocation(self, current_allocation, total_budget, 
                                 feature_names, scenario='normal'):
        """
        Optimize budget allocation across marketing channels.
        
        Args:
            current_allocation: dict with current budget allocation
            total_budget: total budget available
            feature_names: list of feature names
            scenario: optimization scenario ('normal', 'holiday', 'competitor_high')
        """
        if not self.is_trained:
            raise ValueError("Models must be trained before optimization.")
        
        # Get baseline prediction
        baseline_features = self._prepare_optimization_features(
            current_allocation, feature_names, scenario
        )
        baseline_revenue = self.predict_revenue(baseline_features.reshape(1, -1))[0]
        
        # Define optimization ranges for each channel
        channels = ['social_media', 'search_ads', 'email', 'promotions']
        optimization_ranges = {
            'social_media': (0.1, 0.4),  # 10% to 40% of budget
            'search_ads': (0.2, 0.5),    # 20% to 50% of budget
            'email': (0.05, 0.2),        # 5% to 20% of budget
            'promotions': (0.1, 0.3)     # 10% to 30% of budget
        }
        
        # Grid search for optimal allocation
        best_allocation = current_allocation.copy()
        best_revenue = baseline_revenue
        best_roi = baseline_revenue / total_budget
        
        # Simple grid search (can be improved with more sophisticated optimization)
        step_size = 0.05
        for social_pct in np.arange(optimization_ranges['social_media'][0], 
                                  optimization_ranges['social_media'][1] + step_size, step_size):
            for search_pct in np.arange(optimization_ranges['search_ads'][0], 
                                      optimization_ranges['search_ads'][1] + step_size, step_size):
                for email_pct in np.arange(optimization_ranges['email'][0], 
                                         optimization_ranges['email'][1] + step_size, step_size):
                    promotions_pct = 1 - social_pct - search_pct - email_pct
                    
                    if (optimization_ranges['promotions'][0] <= promotions_pct <= 
                        optimization_ranges['promotions'][1]):
                        
                        test_allocation = {
                            'social_media': social_pct * total_budget,
                            'search_ads': search_pct * total_budget,
                            'email': email_pct * total_budget,
                            'promotions': promotions_pct * total_budget
                        }
                        
                        test_features = self._prepare_optimization_features(
                            test_allocation, feature_names, scenario
                        )
                        test_revenue = self.predict_revenue(test_features.reshape(1, -1))[0]
                        test_roi = test_revenue / total_budget
                        
                        if test_roi > best_roi:
                            best_roi = test_roi
                            best_revenue = test_revenue
                            best_allocation = test_allocation
        
        # Calculate improvement
        revenue_improvement = best_revenue - baseline_revenue
        roi_improvement = best_roi - (baseline_revenue / total_budget)
        
        return {
            'current_allocation': current_allocation,
            'optimized_allocation': best_allocation,
            'current_revenue': baseline_revenue,
            'optimized_revenue': best_revenue,
            'revenue_improvement': revenue_improvement,
            'current_roi': baseline_revenue / total_budget,
            'optimized_roi': best_roi,
            'roi_improvement': roi_improvement
        }
    
    def _prepare_optimization_features(self, allocation, feature_names, scenario):
        """Prepare features for optimization prediction."""
        # Create a feature vector based on allocation
        features = np.zeros(len(feature_names))
        
        # Map allocation to feature indices
        feature_mapping = {
            'Social_Media_Spend': allocation['social_media'],
            'Search_Ads_Spend': allocation['search_ads'],
            'Email_Spend': allocation['email'],
            'Promotions_Spend': allocation['promotions']
        }
        
        # Set spend features
        for i, feature in enumerate(feature_names):
            if feature in feature_mapping:
                features[i] = feature_mapping[feature]
            elif feature == 'Competitor_Activity_Index':
                features[i] = 60 if scenario == 'competitor_high' else 50
            elif feature == 'Month_Num':
                features[i] = 12 if scenario == 'holiday' else 6
            elif feature == 'Season_Encoded':
                features[i] = 0 if scenario == 'holiday' else 1
            elif 'Ratio' in feature:
                total = sum(allocation.values())
                if 'Social' in feature:
                    features[i] = allocation['social_media'] / total
                elif 'Search' in feature:
                    features[i] = allocation['search_ads'] / total
                elif 'Email' in feature:
                    features[i] = allocation['email'] / total
                elif 'Promotions' in feature:
                    features[i] = allocation['promotions'] / total
            else:
                # Use default values for other features
                features[i] = 0.5
        
        return features
    
    def get_channel_effectiveness(self, feature_names):
        """Analyze channel effectiveness based on feature importance."""
        if not self.is_trained or self.feature_importance is None:
            return None
        
        importance_df = self.get_feature_importance(feature_names)
        
        # Group by channel
        channel_importance = {}
        for _, row in importance_df.iterrows():
            feature = row['feature']
            importance = row['importance']
            
            if 'Social' in feature:
                channel = 'Social Media'
            elif 'Search' in feature:
                channel = 'Search Ads'
            elif 'Email' in feature:
                channel = 'Email'
            elif 'Promotions' in feature:
                channel = 'Promotions'
            else:
                continue
            
            if channel not in channel_importance:
                channel_importance[channel] = 0
            channel_importance[channel] += importance
        
        return channel_importance
    
    def save_model(self, filepath):
        """Save trained models to file."""
        if not self.is_trained:
            raise ValueError("Models must be trained before saving.")
        
        model_data = {
            'models': self.models,
            'feature_importance': self.feature_importance,
            'model_performance': self.model_performance,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load trained models from file."""
        model_data = joblib.load(filepath)
        
        self.models = model_data['models']
        self.feature_importance = model_data['feature_importance']
        self.model_performance = model_data['model_performance']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {filepath}")

def create_and_train_model(data_processor):
    """Convenience function to create and train a marketing model."""
    # Prepare data for modeling
    X_train, X_test, y_train, y_test = data_processor.prepare_modeling_data()
    feature_names = data_processor.get_feature_columns()
    
    # Create and train model
    model = MarketingCampaignModel()
    model.train_models(X_train, y_train, X_test, y_test)
    
    return model, feature_names

if __name__ == "__main__":
    # Test the model
    from data_prep import load_and_preprocess_data
    
    data_path = '/Users/youseftaheri/Downloads/AdOptima/sample_data/marketing_data.csv'
    processor, processed_data = load_and_preprocess_data(data_path)
    
    if processor is not None:
        model, feature_names = create_and_train_model(processor)
        
        # Test optimization
        test_allocation = {
            'social_media': 20,
            'search_ads': 30,
            'email': 10,
            'promotions': 15
        }
        
        optimization_result = model.optimize_budget_allocation(
            test_allocation, 75, feature_names, 'normal'
        )
        
        print("\nOptimization Results:")
        print(f"Current Revenue: ${optimization_result['current_revenue']:,.2f}")
        print(f"Optimized Revenue: ${optimization_result['optimized_revenue']:,.2f}")
        print(f"Revenue Improvement: ${optimization_result['revenue_improvement']:,.2f}")
        print(f"ROI Improvement: {optimization_result['roi_improvement']:.3f}")
