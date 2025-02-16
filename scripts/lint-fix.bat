@echo off
:: Running black
poetry run black .
if %errorlevel% neq 0 (
    echo Failed to run black
    exit /b %errorlevel%
)

:: Running isort
poetry run isort .
if %errorlevel% neq 0 (
    echo Failed to run isort
    exit /b %errorlevel%
)

:: Running toml-sort
poetry run toml-sort pyproject.toml
if %errorlevel% neq 0 (
    echo Failed to run toml-sort
    exit /b %errorlevel%
)

echo Script completed successfully.
