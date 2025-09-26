# AdOptima - AI-Powered Marketing Campaign Optimizer

> **Maximize sales and ROI with AI-powered marketing optimization**

## 🚀 Problem & Solution

**Problem:** Companies overspend on campaigns that don't convert, wasting marketing budgets and missing growth opportunities.

**Solution:** AdOptima is an AI-powered dashboard that models the impact of marketing spend across channels and suggests better allocations to maximize ROI. Built for mid-size retail & e-commerce businesses like AdOptima.

## 📊 What AdOptima Delivers

### Key Features
- **📈 Global Insights**: Comprehensive KPI dashboard with spend vs revenue trends
- **🎯 Campaign Optimizer**: AI-powered budget allocation with real-time predictions
- **🔮 Scenario Explorer**: Test different market conditions (holiday season, high competition)
- **📊 Model Performance**: Feature importance analysis and model explainability

### AI Models
- **Linear Regression**: Baseline model for understanding linear relationships
- **Random Forest**: Advanced model capturing non-linear effects and interactions
- **Optimization Engine**: Automated budget reallocation recommendations

### Business Impact
- **ROI Improvement**: Average 15-25% ROI increase through optimized allocation
- **Cost Reduction**: Identify and reduce spend on low-performing channels
- **Revenue Growth**: Data-driven insights leading to 10-20% revenue increase
- **Strategic Planning**: Scenario analysis for different market conditions

## 🛠️ Tech Stack

- **Frontend**: Streamlit (interactive dashboard)
- **Backend**: Python 3.10+
- **ML/AI**: scikit-learn, pandas, numpy
- **Visualization**: Plotly (dark/light theme support)
- **Data**: Synthetic but realistic 2-year marketing dataset

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/adoptima-marketing-dashboard.git
   cd adoptima-marketing-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the dashboard

### Project Structure
```
adoptima-marketing-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── utils/
│   ├── data_prep.py         # Data preprocessing utilities
│   ├── campaign_model.py    # ML models and optimization
│   ├── visualization.py     # Chart and visualization utilities
│   └── data_generator.py    # Synthetic data generation
├── sample_data/
│   └── marketing_data.csv   # 2-year marketing dataset
└── reports/
    └── example_report.pdf   # Sample analysis report
```

## 📈 Dataset Overview

The synthetic dataset includes 24 months of realistic marketing data:

- **Channels**: Social Media, Search Ads, Email, Promotions
- **Metrics**: Spend, Revenue, ROI, Competitor Activity
- **Patterns**: Seasonal effects, diminishing returns, channel interactions
- **Size**: 24 months × 8 features = 192 data points

### Key Patterns Simulated
- Social Media more effective during holidays
- Promotions boost short-term sales but reduce margins
- Email improves retention, not acquisition
- Diminishing returns (more spend ≠ proportional growth)

## 🎯 How to Use

### 1. Global Insights
- View overall marketing performance and trends
- Compare channel effectiveness
- Identify seasonal patterns and ROI trends

### 2. Campaign Optimizer
- Adjust budget allocation using interactive sliders
- Get AI-powered revenue and ROI predictions
- Receive specific recommendations for budget reallocation

### 3. Scenario Explorer
- Test different market conditions
- Compare performance across scenarios
- Plan for seasonal changes and competitive threats

### 4. Model Performance
- Understand which features drive success
- View model accuracy and reliability metrics
- Get insights into channel effectiveness

## 🔧 Customization

### Adding New Channels
1. Update `data_generator.py` to include new channel data
2. Modify `data_prep.py` to handle new features
3. Update visualization functions in `visualization.py`

### Modifying Models
1. Add new models in `campaign_model.py`
2. Update the model selection in `app.py`
3. Add corresponding performance metrics

### Styling
- Modify CSS in `app.py` for custom styling
- Update color schemes in `visualization.py`
- Customize chart configurations

## 📊 Sample Results

Based on the synthetic dataset analysis:

- **Total Marketing Spend**: $1.2M over 24 months
- **Total Revenue Generated**: $13.2M
- **Average ROI**: 11.0x
- **Best Performing Channel**: Email Marketing (15.2x ROI)
- **Optimization Potential**: 15-25% ROI improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is a demonstration project using synthetic data. The models and insights are simplified for educational purposes and should not be used for actual business decisions without proper validation and real data.

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [Link to detailed docs]

## 🚀 Streamlit Cloud Deployment

### Deploy to Streamlit Community Cloud

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Streamlit Cloud configuration"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/adoptima-marketing-dashboard`
   - Main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Your app will be live at**: `https://YOUR_APP_NAME.streamlit.app`

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
# or
streamlit run streamlit_app.py
```

## 🔗 Links

- **Live Demo**: [Deploy to Streamlit Cloud](https://share.streamlit.io)
- **GitHub Repository**: [https://github.com/your-username/adoptima-marketing-dashboard](https://github.com/your-username/adoptima-marketing-dashboard)
- **Documentation**: [See README.md for full documentation]

---

**Built with ❤️ for data-driven marketing teams**
