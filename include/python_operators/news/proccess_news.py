## DQ Cheks + Process News


analyze_news_sentiment_task = PythonOperator( ## Read json from s3, analyze news, save to s3
    task_id=f"analyze_news_sentiment_{keyword_naming}",
    python_callable=analyze_news_sentiment,
    op_args=[keyword],
)