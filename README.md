## 🚀 Getting Started.

### 1. One-Time Project Setup

1. Clone this repository
    ```bash
    git clone https://github.com/omargawdat/Gawdat_Django_Template.git
    ```
2. Replace `dars` with your `project name`
3. create 'media' folder
    ```bash
    mkdir assets/media
    touch assets/media/.gitkeep
    ```
4. move the `build_test` file to the workflow directory:
5. Initialize the Git repository:
   ```bash
   sudo rm -r .git
   git init
   git add .
   git commit -m "Initial commit"
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```
6. Share the project on GitHub

### 2. Local Development

1. install pre-commit hooks
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

2. Create `.env` file in the root directory:
    ```bash
    cp dummy.env .env
    ```

3. Build and run the application with Docker Compose:
   ```bash
   docker-compose -f docker-compose.local.yml up --build -d
   ```

4. Run Django management commands:
   ```bash
   docker compose -f docker-compose.local.yml run --rm django python manage.py [command]
   ```

### 3. Deployment

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
     "SENTRY_SDK_DSN": "MUST-BE-REPLACED",
     "DB_HOST": "MUST-BE-REPLACED",
     "DB_USER": "MUST-BE-REPLACED",
     "DB_PASSWORD": "MUST-BE-REPLACED",
     "DB_PORT": "5432",
     "DB_NAME": "MUST-BE-REPLACED",
     "DJANGO_SECRET_KEY": "MUST-BE-REPLACED",
     "DJANGO_SUPERUSER_USERNAME": "MUST-BE-REPLACED",
     "DJANGO_SUPERUSER_PASSWORD": "MUST-BE-REPLACED",
     "DJANGO_ADMIN_NAME": "MUST-BE-REPLACED",
     "DJANGO_ADMIN_EMAIL": "MUST-BE-REPLACED",
     "S3_BUCKET_NAME": "MUST-BE-REPLACED",
     "DOMAIN_NAME": "MUST-BE-REPLACED",
     "DJANGO_JWT_ACCESS_TOKEN_LIFETIME_MINUTES": "14400",
     "DJANGO_JWT_REFRESH_TOKEN_LIFETIME_MINUTES": "43200",
     "GOOGLE_APPLICATION_CREDENTIALS": "/app/credentials/google-service-account.json",
     "API_KEY": "api_key_example_ABC123XYZ",
     "TAPS_SECRET_KEY": "taps_secret_dummy_123456",
     "ENVIRONMENT": "development",
     "IS_TESTING_SMS": "true",
     "DJANGO_ADMIN_URL": "admin/",
     "OUR_SMS_API_KEY": "sms_api_key_987654321",
     "OUR_SMS_SENDER_NAME": "ExampleApp",
     "SMS_MISR_USERNAME": "sms-misr-user-id-abc123",
     "SMS_MISR_PASSWORD": "secure-sms-misr-pass-xyz789",
     "SMS_MISR_SENDER": "example_sms_sender_id",
     "GOOGLE_MAP_API_KEY": "MUST-BE-REPLACED",
     "GOOGLE_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "GOOGLE_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "FACEBOOK_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "FACEBOOK_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "APPLE_OAUTH2_CLIENT_ID": "MUST-BE-REPLACED",
     "APPLE_OAUTH2_CLIENT_SECRET": "MUST-BE-REPLACED",
     "KEY_ID": "MUST-BE-REPLACED",
     "TEAM_ID": "MUST-BE-REPLACED"
   }
   ```
    4. create app runner, port 5000 include permissions and write the secrets of the apprunner itself
