# Capstone Project: AI-Driven Stock Market Analysis

## Overview
This project aims to build an AI-powered analytics pipeline for stock market data using cloud-based infrastructure and modern data engineering tools. The goal is to collect financial news and stock market data, analyze sentiment, detect anomalies, and predict potential trends based on historical data.

## Architecture
The system consists of the following components:
- **PostgreSQL Database (Amazon RDS):** Stores historical stock price data, sentiment scores, and anomaly detection insights.
- **S3 Data Lake:** Serves as a storage layer for raw and processed data.
- **Terraform:** Manages infrastructure as code for database and storage provisioning.
- **Apache Airflow:** Orchestrates data ingestion workflows.
- **DBT (Data Build Tool):** Transforms and models data for analytical processing.
- **AI Sentiment and Impact Analysis:** Uses OpenAI’s models to assess both the sentiment and business impact of news articles.
- **Power BI:** Creates dashboards to visualize analytical patterns from the database.
- **SQLAlchemy & Alembic:** Handles ORM (Object-Relational Mapping) and database migrations.
- **GitHub Actions:** Automates migrations and schema changes upon pull request (PR) merges.

## Data Sources
- **News APIs:**
  - [Yahoo News](https://developer.yahoo.com/api/)
  - [News API](https://newsapi.org/)
- **Stock Market Data:**
  - [Polygon](https://polygon.io/)
- **Sentiment and Impact Analysis:**
  - [OpenAI](https://openai.com/)

## Key Features
- **News Aggregation:** Retrieves financial news from multiple sources.
- **Sentiment and Impact Analysis:** Uses AI models to classify news articles based on sentiment (positive, neutral, negative) and impact level (low, medium, high) on the given business.
- **Stock Price Variance Tracking:** Records the daily variance of closing prices for different stocks.
- **Anomaly Detection:** Identifies unusual stock price movements.
- **Predictive Analytics:** Forecasts potential market trends based on historical patterns.
- **Correlation Analysis:** Computes correlation coefficients between sentiment, stock price movements, and external factors.
- **Interactive Dashboards:** Power BI visualizes trends, anomalies, and key insights.
- **Automated Database Migrations:** SQLAlchemy and Alembic streamline database version control.
- **CI/CD Pipeline:** GitHub Actions ensure automated database schema changes on pull requests.
- **RAG-Enhanced Sentiment and Impact Analysis:** The GPT model is integrated with a Retrieval-Augmented Generation (RAG) system that provides useful contextual information about each analyzed ticker, enhancing the accuracy and relevance of sentiment and impact insights.

## Goals
- Populate the database with data from the last 1 year.
- Implement a scalable cloud-based data pipeline.
- Automate data ingestion, transformation, and analysis.
- Apply AI-driven insights to enhance stock market predictions.
- Compute correlation coefficients between market variables.
- Build an analytical platform to track and evaluate market behavior trends.
- Ensure seamless and version-controlled database migrations with CI/CD practices.
