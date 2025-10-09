## 🚀 Getting Started

### Prerequisites

```bash
# Install required tools (macOS)
brew install uv just docker osv-scanner

# Note: No need to install pre-commit, ruff, mypy, or other dev tools globally
# They will be automatically managed per-project using 'uv tool run'
```

### 1. One-Time Project Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/omargawdat/Gawdat_Django_Template.git
    cd Gawdat_Django_Template
    ```

2. Install dependencies and setup pre-commit hooks:
    ```bash
    just install
    ```

3. Create media folder:
    ```bash
    mkdir -p assets/media
    touch assets/media/.gitkeep
    ```

4. Replace `projectname` with your `project name`

5. Initialize Git repository (optional):
   ```bash
   sudo rm -r .git
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. Share the project on GitHub

### 2. Local Development

1. Create `.env` file:
    ```bash
    cp dummy.env .env
    ```

2. Configure Firebase credentials (if using FCM/push notifications):
    ```bash
    # Download firebase.json from Firebase Console
    # https://console.firebase.google.com/ → Project Settings → Service Accounts
    just firebase-setup firebase.json
    ```

3. Start the application:
   ```bash
   just up
   ```

4. Access the application:
   - **Admin Panel**: http://localhost:8000/admin
   - **API**: http://localhost:8000/api
   - **API Docs**: http://localhost:8000/api/schema/swagger-ui

**Common commands:**
```bash
just up              # Start services
just down            # Stop services
just rebuild         # Rebuild containers
just migrate         # Run migrations
just makemigrations  # Create migrations
just shell           # Django shell
just test            # Run tests
just lint-all        # Fix code style
```

Run `just` to see all available commands.

### 3. Pre-commit Hooks

Pre-commit hooks are **automatically installed** when you run `just install`. They maintain code quality by running checks before each commit.

**How it works:**
- Hooks are installed automatically during project setup
- Run automatically on `git commit`
- Tools (ruff, mypy, etc.) are managed per-project via `uv tool run`
- Each project uses its own tool versions from `pyproject.toml`
- No conflicts between different projects with different tool versions

**Manual commands:**
```bash
# Run all hooks manually
uv tool run pre-commit run --all-files

# Run specific hook
uv tool run pre-commit run ruff-check --all-files

# Update hook versions
uv tool run pre-commit autoupdate
```

### 4. Deployment

This project uses GitHub Actions for CI/CD deployment to AWS. Follow these steps to set up your deployment environment:

1. Infrastructure Setup (in this order):

   a. Create AWS resources:
    - Create an Amazon ECR repository for storing Docker images
    - Set up AWS Secret Manager to store application secrets
    - Create an S3 bucket for static files and media storage, permissions and policies

   b. Create a database in your development RDS instance

   c. Create a Sentry project for error tracking and monitoring

2. Add the following secrets to your GitHub repository:

    - `AWS_ACCESS_KEY_ID` - AWS IAM user access key with appropriate permissions
    - `AWS_SECRET_ACCESS_KEY` - Corresponding secret for the IAM user
    - `AWS_REGION_NAME` - AWS region where your resources are located (e.g., us-east-1)
    - `AWS_SECRET_MANAGER_NAME` - Name of the AWS Secret Manager containing your application secrets
    - `ECR_REPOSITORY_NAME` - Name of your Amazon ECR repository for Docker images

3. Configure AWS Secret Manager with the following configuration values:

   ```json
   {
     "DJANGO_SECRET_KEY": "MUST-BE-REPLACED",
     "DJANGO_SUPERUSER_USERNAME": "MUST-BE-REPLACED",
     "DJANGO_SUPERUSER_PASSWORD": "MUST-BE-REPLACED",
     "DJANGO_ADMIN_NAME": "MUST-BE-REPLACED",
     "DJANGO_ADMIN_EMAIL": "MUST-BE-REPLACED",
     "DJANGO_ADMIN_URL": "admin/",
     "DJANGO_JWT_ACCESS_TOKEN_LIFETIME_MINUTES": "14400",
     "DJANGO_JWT_REFRESH_TOKEN_LIFETIME_MINUTES": "43200",
     "GOOGLE_APPLICATION_CREDENTIALS": "/app/credentials/google-service-account.json",
     "TAPS_SECRET_KEY": "taps_secret_dummy_123456",
     "PAYMENT_CONFIRMATION_KEY": "MUST-BE-REPLACED",

     "DATABASE_URL": "postgis://user:password@host:5432/dbname",

     "DOMAIN_NAME": "MUST-BE-REPLACED",
     "ENVIRONMENT": "development",
     "SENTRY_SDK_DSN": "MUST-BE-REPLACED",

     "AWS_REGION_NAME": "us-east-1",
     "S3_BUCKET_NAME": "MUST-BE-REPLACED",

     "FIREBASE_CREDENTIALS_B64": "MUST-BE-REPLACED",

     "GOOGLE_APPLICATION_CREDENTIALS": "/app/credentials/google-service-account.json",
     "GOOGLE_MAP_API_KEY": "MUST-BE-REPLACED",

     "TAPS_SECRET_KEY": "MUST-BE-REPLACED",

     "IS_TESTING_SMS": "true",
     "OUR_SMS_API_KEY": "MUST-BE-REPLACED",
     "OUR_SMS_SENDER_NAME": "YourApp",
     "SMS_MISR_USERNAME": "MUST-BE-REPLACED",
     "SMS_MISR_PASSWORD": "MUST-BE-REPLACED",
     "SMS_MISR_SENDER": "MUST-BE-REPLACED",

     "GOOGLE_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "GOOGLE_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "FACEBOOK_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "FACEBOOK_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "APPLE_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "APPLE_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "KEY_ID": "MUST-BE-REPLACED",
     "TEAM_ID": "MUST-BE-REPLACED",

     "EMAIL_HOST_USER": "MUST-BE-REPLACED",
     "EMAIL_HOST_PASSWORD": "MUST-BE-REPLACED",

     "API_KEY": "MUST-BE-REPLACED"
   }
   ```
    4. create app runner, port 5000 include permissions and write the secrets of the apprunner itself
