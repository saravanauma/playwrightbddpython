# Playwright Python BDD Framework 🎭

A modern test automation framework combining Playwright, Pytest-BDD, and Allure for robust and maintainable end-to-end testing.

## ✨ Features

### 🎭 Core Testing
- **Playwright** automation
- **Page Object Model**
- **BDD-style** tests
- **Parallel** execution

### 📸 Auto-Recording
- Video capture
- Failure screenshots
- Execution logs
- Session recording

### 📊 Reports & Analysis
- Allure reports
- HTML results
- Visual evidence
- Test metrics

### �️ Configuration
- ENV-based setup
- Secure credentials
- Multi-environment
- Easy customization

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip
- Git

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd playwrightbddpython

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### First Test Run

```bash
# Verify setup with a basic test run
pytest tests/features/auth_login.feature -v

# Generate HTML report
pytest --html=reports/report.html
```

## 🌳 Project Structure

```
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Pytest settings and plugins
├── readme.md               # Project documentation
├── requirements.txt        # Python dependencies
└── tests/
    ├── api/               # API test modules
    ├── db/               
    │   └── fixtures.py    # Database fixtures
    ├── e2e/
    │   ├── pages/        # Page Object Models
    │   │   └── auth_loginpage.py
    │   └── steps/        # BDD step implementations
    │       └── test_auth_login_steps.py
    ├── features/         # Gherkin feature files
    │   └── auth_login.feature
    └── utils/
        └── config.py     # Configuration utilities
```

## 🔧 Environment Variables

Environment variables can be set in your `.env` file or system environment:

```bash
# Test Environment
ENV=pre_staging              # Environment (pre_staging/staging)
HEADLESS=false              # Run browsers in headless mode
SLOW_MO=50                  # Slow down Playwright operations (ms)
PAGE_TIMEOUT=30000          # Page load timeout (ms)

# Credentials (Use secure storage in production)
UI_USERNAME=user@email.com  # Default test username
UI_PASSWORD=password123     # Default test password

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=dbuser
DB_PASS=dbpass
DB_NAME=testdb
DB_SSL_DISABLED=true

# Report Configuration
REPORT_PATH=reports/        # Path to store test reports
```

## 📝 Writing Tests

### 1️⃣ Feature Files

```gherkin
# tests/features/auth_login.feature
Feature: Authentication
  Scenario: User login
    Given the user navigates to login
    When they enter valid credentials
    Then they should be logged in
```

### 2️⃣ Page Objects

```python
# tests/e2e/pages/auth_loginpage.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")

    def login(self, username=None, password=None):
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        self.username.fill(username)
        self.password.fill(password)
```

### 3️⃣ Step Definitions

```python
# tests/e2e/steps/test_auth_login_steps.py
@given("the user navigates to login")
def navigate_login(page):
    page.auth = LoginPage(page)
    page.auth.navigate()

@when("they enter valid credentials")
def enter_credentials(page):
    page.auth.login()  # Uses env credentials
```

## 🏃 Running Tests

### Parallel Execution

```bash
# Run tests in parallel
pytest -n auto             # Use all CPU cores
pytest -n 4                # Use specific number of workers

# Run specific test types
pytest -m "smoke"          # Run smoke tests
pytest -m "regression"     # Run regression tests
pytest tests/e2e/         # Run UI tests only
pytest tests/api/         # Run API tests only
pytest tests/db/            # Run DB tests
pytest
```

### Test Selection

```bash
# Run by pattern
pytest -k "login"         # Run tests containing "login"
pytest -k "not slow"      # Skip slow tests

# Run by markers
pytest -m "critical"      # Run critical tests
pytest -m "not flaky"     # Skip flaky tests
```

## 📊 Reports

### HTML Reports
```bash
pytest --html=reports/report.html
```

### Allure Reports
```bash
# Generate results
pytest --alluredir=reports/allure-results

# View report
allure serve reports/allure-results
```

### Screenshots and Videos
- Screenshots are captured automatically on test failure
- Videos are recorded for each test session
- Artifacts are saved in `reports/screenshots` and `reports/videos`

## 🔍 Debugging

### Visual Mode
```bash
# Run with browser visible
pytest --headed

# Slow down execution
pytest --slowmo 1000
```

### Debug Tools
```bash
# Enable verbose output
pytest -vv

# Show print statements
pytest -s

# Debug on failure
pytest --pdb
```
