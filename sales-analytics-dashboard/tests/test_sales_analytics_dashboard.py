import os
import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import main as dashboard_main
from src.analyzer import SalesAnalyzer
from src.data_loader import generate_sample_data, load_and_preprocess_data
from src.visualizer import SalesVisualizer


@pytest.fixture
def raw_sales_data():
    return pd.DataFrame(
        [
            {
                "Date": "2026-01-15",
                "Product": "Laptop",
                "Region": "North",
                "Customer": "Customer_0001",
                "Quantity": 2,
                "Price": 1000.0,
            },
            {
                "Date": "2026-01-20",
                "Product": "Mouse",
                "Region": "South",
                "Customer": "Customer_0002",
                "Quantity": 5,
                "Price": 20.0,
            },
            {
                "Date": "2026-02-10",
                "Product": "Laptop",
                "Region": "North",
                "Customer": "Customer_0001",
                "Quantity": 1,
                "Price": 1000.0,
            },
            {
                "Date": "2026-02-11",
                "Product": "Keyboard",
                "Region": "West",
                "Customer": "Customer_0003",
                "Quantity": 3,
                "Price": 50.0,
            },
            {
                "Date": "2026-02-11",
                "Product": "Keyboard",
                "Region": "West",
                "Customer": "Customer_0003",
                "Quantity": 3,
                "Price": 50.0,
            },
            {
                "Date": "2026-03-01",
                "Product": "Monitor",
                "Region": "East",
                "Customer": "Customer_0004",
                "Quantity": None,
                "Price": 200.0,
            },
        ]
    )


@pytest.fixture
def processed_sales_data(raw_sales_data, tmp_path):
    csv_path = tmp_path / "sales.csv"
    raw_sales_data.to_csv(csv_path, index=False)
    return load_and_preprocess_data(csv_path)


def test_load_and_preprocess_data_cleans_and_enriches_sales(raw_sales_data, tmp_path):
    csv_path = tmp_path / "sales.csv"
    raw_sales_data.to_csv(csv_path, index=False)

    result = load_and_preprocess_data(csv_path)

    assert len(result) == 4
    assert list(result.columns) == [
        "Date",
        "Product",
        "Region",
        "Customer",
        "Quantity",
        "Price",
        "Revenue",
    ]
    assert pd.api.types.is_datetime64_any_dtype(result["Date"])
    assert result["Revenue"].tolist() == [2000.0, 100.0, 1000.0, 150.0]
    assert result["Date"].is_monotonic_increasing
    assert not result.isna().any().any()
    assert not result.duplicated().any()


def test_load_and_preprocess_data_generates_missing_file(tmp_path):
    csv_path = tmp_path / "data" / "sales_data.csv"

    result = load_and_preprocess_data(csv_path)

    assert csv_path.exists()
    assert len(result) == 1000
    assert {"Date", "Product", "Region", "Customer", "Quantity", "Price", "Revenue"} == set(
        result.columns
    )
    assert result["Revenue"].equals(result["Quantity"] * result["Price"])


def test_generate_sample_data_has_expected_shape_and_columns():
    result = generate_sample_data(num_records=25)

    assert len(result) == 25
    assert list(result.columns) == ["Date", "Product", "Region", "Customer", "Quantity", "Price"]
    assert result["Quantity"].between(1, 9).all()
    assert result["Price"].between(10, 2000).all()


def test_sales_analyzer_returns_summary_rankings_and_segments(processed_sales_data):
    analyzer = SalesAnalyzer(processed_sales_data)

    summary = analyzer.get_summary_statistics()
    top_products = analyzer.get_top_products(2)
    regional = analyzer.get_regional_performance()
    monthly = analyzer.get_monthly_trends()
    segments = analyzer.get_customer_segments()
    correlation = analyzer.get_product_correlation()

    assert summary == {
        "Total Revenue": "$3,250.00",
        "Total Orders": 4,
        "Average Order Value": "$812.50",
        "Unique Products": 3,
        "Unique Customers": 3,
    }
    assert top_products.to_dict("records") == [
        {"Product": "Laptop", "Revenue": 3000.0},
        {"Product": "Keyboard", "Revenue": 150.0},
    ]
    assert regional.to_dict("records") == [
        {"Region": "North", "Revenue": 3000.0, "Orders": 2},
        {"Region": "West", "Revenue": 150.0, "Orders": 1},
        {"Region": "South", "Revenue": 100.0, "Orders": 1},
    ]
    assert monthly["Revenue"].tolist() == [2100.0, 1150.0]
    assert monthly["Orders"].tolist() == [2, 2]
    assert segments.to_dict() == {"Premium": 1, "Low Value": 1, "High Value": 1}
    assert correlation.index.tolist() == ["Keyboard", "Laptop", "Mouse"]
    assert correlation.columns.tolist() == ["Keyboard", "Laptop", "Mouse"]


def test_sales_visualizer_writes_all_report_images(processed_sales_data, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("reports")
    visualizer = SalesVisualizer(processed_sales_data)

    visualizer.plot_sales_trend()
    visualizer.plot_product_performance()
    visualizer.plot_regional_distribution()
    visualizer.plot_customer_segments()
    visualizer.create_dashboard()

    expected_reports = [
        "sales_trend.png",
        "product_performance.png",
        "regional_distribution.png",
        "customer_segments.png",
        "dashboard.png",
    ]
    for report_name in expected_reports:
        report_path = tmp_path / "reports" / report_name
        assert report_path.exists()
        assert report_path.stat().st_size > 0


def test_main_runs_entire_program_and_creates_outputs(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    dashboard_main.main()

    captured = capsys.readouterr()
    assert "Sales Analytics Dashboard" in captured.out
    assert "Loaded 1000 records" in captured.out
    assert "Analysis complete!" in captured.out
    assert (tmp_path / "data" / "sales_data.csv").exists()

    expected_reports = [
        "sales_trend.png",
        "product_performance.png",
        "regional_distribution.png",
        "customer_segments.png",
        "dashboard.png",
    ]
    for report_name in expected_reports:
        report_path = tmp_path / "reports" / report_name
        assert report_path.exists()
        assert report_path.stat().st_size > 0
