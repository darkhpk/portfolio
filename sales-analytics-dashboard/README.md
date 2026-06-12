# Sales Analytics Dashboard

A comprehensive data analytics project that analyzes sales data and creates interactive visualizations using Python, pandas, matplotlib, and seaborn.

## Features

- **Data Analysis**: Comprehensive sales data analysis with statistical insights
- **Visualizations**: Interactive charts and graphs including:
  - Sales trends over time
  - Product performance analysis
  - Regional sales distribution
  - Customer segmentation
- **Export Reports**: Generate PDF and HTML reports
- **Data Cleaning**: Automated data preprocessing and validation

## Technologies Used

- Python 3.8+
- pandas - Data manipulation and analysis
- matplotlib - Data visualization
- seaborn - Statistical data visualization
- numpy - Numerical computing
- jupyter - Interactive notebooks

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the main analysis:
```bash
python main.py
```

### Open Jupyter Notebook for interactive analysis:
```bash
jupyter notebook analysis.ipynb
```

## Project Structure

- `main.py` - Main analysis script
- `analysis.ipynb` - Interactive Jupyter notebook
- `data/` - Sample sales data
- `reports/` - Generated reports and visualizations
- `src/` - Source code modules
  - `data_loader.py` - Data loading and preprocessing
  - `analyzer.py` - Analysis functions
  - `visualizer.py` - Visualization functions

## Sample Insights

The dashboard provides insights such as:
- Top performing products and regions
- Seasonal sales trends
- Customer buying patterns
- Revenue forecasts
- Product correlation analysis

## Future Enhancements

- Real-time data integration
- Machine learning predictions
- Interactive web dashboard with Plotly Dash
- Database integration
