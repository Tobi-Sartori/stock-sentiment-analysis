## Capstone Project: AI-Driven Stock Market Analysis - Task Checklist

This checklist breaks down the project into actionable tasks, organized by category.  Use this to track your progress and ensure you cover all necessary aspects.

**I. Infrastructure & Setup:**

* [ ] **Database (PostgreSQL on RDS):**
    * [x] Provision RDS instance.
    * [x] Configure database security (firewall rules, access control).
    * [ ] Design database schema (tables for stock data, sentiment scores, anomalies, etc.).
* [ ] **S3 Data Lake:**
    * [x] Create S3 buckets for raw data, processed data, and model artifacts.
    * [ ] Configure S3 lifecycle policies for data archiving and deletion.
* [ ] **Terraform:**
    * [ ] Write Terraform code to manage RDS and S3.
    * [ ] Implement Terraform state management.
* [ ] **Airflow:**
    * [x] Install and configure Airflow.
    * [ ] Set up Airflow connections to RDS, S3, and APIs.
* [ ] **DBT:**
    * [ ] Install and configure DBT.
    * [ ] Define DBT models for data transformation and aggregation.
* [ ] **Power BI:**
    * [ ] Set up Power BI connection to RDS.
    * [ ] Design and develop dashboards for visualization.
* [ ] **SQLAlchemy & Alembic:**
    * [x] Set up SQLAlchemy for database interaction.
    * [x] Configure Alembic for database migrations.
* [ ] **GitHub Actions:**
    * [ ] Create GitHub Actions workflow for automated database migrations on PR merge.
    * [ ] Set up CI/CD pipeline for code deployment and testing.
* [ ] **Project Setup:**
    * [x] Create project repository on GitHub.
    * [x] Set up development environment.

**II. Data Ingestion & Processing:**

* [ ] **News APIs (Yahoo News, News API):**
    * [ ] Implement API clients for each news source.
    * [ ] Handle API rate limits and errors.
    * [ ] Implement data extraction and parsing for relevant information (title, date, content, ticker).
    * [ ] Store raw news data in S3.
* [ ] **Stock Market Data (Polygon):**
    * [ ] Implement Polygon API client.
    * [ ] Retrieve historical stock price data (daily open, high, low, close, volume).
    * [ ] Store raw stock data in S3.
* [ ] **Data Pipeline (Airflow):**
    * [ ] Create Airflow DAGs to orchestrate data ingestion from APIs.
    * [ ] Implement data quality checks and validation.
    * [ ] Schedule DAGs for regular execution.
* [ ] **Data Transformation (DBT):**
    * [ ] Create DBT models to clean, transform, and aggregate data.
    * [ ] Implement calculations for stock price variance.
    * [ ] Load processed data into the PostgreSQL database.

**III. AI & Analysis:**

* [ ] **Sentiment & Impact Analysis (OpenAI & RAG):**
    * [x] Implement OpenAI API integration.
    * [ ] Develop RAG system:
        * [ ] Create a knowledge base with relevant ticker information.
        * [ ] Implement context retrieval based on ticker symbols in news articles.
    * [ ] Implement sentiment analysis using OpenAI models, enhanced by retrieved context.
    * [ ] Implement impact analysis (low, medium, high) using OpenAI models.
    * [ ] Store sentiment scores and impact ratings in the database.
* [ ] **Anomaly Detection:**
    * [ ] Choose and implement anomaly detection algorithm(s) (e.g., statistical methods, time series analysis).
    * [ ] Train and evaluate anomaly detection model.
    * [ ] Store anomaly detection results in the database.
* [ ] **Predictive Analytics:**
    * [ ] Choose and implement predictive modeling technique(s) (e.g., time series analysis, regression).
    * [ ] Train and evaluate predictive model.  Use a backtesting framework.
    * [ ] Store predictions in the database.
* [ ] **Correlation Analysis:**
    * [ ] Implement correlation analysis between sentiment, stock price movements, and other factors.
    * [ ] Store correlation coefficients in the database.

**IV. Visualization & Reporting:**

* [ ] **Power BI Dashboards:**
    * [ ] Create interactive dashboards to visualize:
        * [ ] Stock price trends.
        * [ ] Sentiment scores over time.
        * [ ] Anomaly detection results.
        * [ ] Correlation analysis findings.
        * [ ] Predictive model outputs.
    * [ ] Implement data filtering and drill-down capabilities.

**V. Testing & Deployment:**

* [ ] **Unit Tests:**
    * [ ] Write unit tests for all code components.
* [ ] **Integration Tests:**
    * [ ] Implement integration tests to verify interactions between different components.
* [ ] **End-to-End Tests:**
    * [ ] Test the entire data pipeline from data ingestion to visualization.
* [ ] **Documentation:**
    * [ ] Write comprehensive documentation for the project, including architecture, data pipeline, analysis methods, and usage instructions.
* [ ] **Deployment:**
    * [ ] Deploy the Airflow DAGs and other components to a production environment.
    * [ ] Set up monitoring and logging.

**VI. Project Management:**

* [ ] **Define Metrics:**
    * [ ] Establish clear metrics to measure project success (e.g., sentiment analysis accuracy, prediction performance).
* [ ] **Scope Management:**
    * [ ] Prioritize features and manage project scope.
* [ ] **Regular Reviews:**
    * [ ] Conduct regular project reviews to track progress and identify potential issues.