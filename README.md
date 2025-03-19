## 🚀 Getting Started

### 1. One-Time Project Setup

1. Clone this repository
    ```bash
    git clone https://github.com/omargawdat/Gawdat_Django_Template.git
    ```
2. Replace `temp_project` with your `project name`
3. create 'media' folder
    ```bash
    mkdir assets/media
    touch assets/media/.gitkeep
    ```
4. Initialize the Git repository:
   ```bash
   sudo rm -r .git
   git init
   git add .
   git commit -m "Initial commit"
   ```
5. Share the project on GitHub

### 2. Local Development

1. Install pre-commit hooks:
   ```bash
   pip3 install pre-commit
   pre-commit install --hook-type commit-msg
   ```

2. Create `.env` file in the root directory:
    ```bash
    touch .env
    ```
    ```
    # Django Settings
    DJANGO_SECRET_KEY=your-secure-secret-key-here
    DJANGO_SUPERUSER_USERNAME=omar
    DJANGO_SUPERUSER_PASSWORD=123
    DJANGO_ADMIN_NAME=Admin User
    DJANGO_ADMIN_EMAIL=admin@example.com
    DJANGO_JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
    DJANGO_JWT_REFRESH_TOKEN_LIFETIME_MINUTES=1440

    # Configurations
    COMPOSE_BAKE=true

    # AWS Settings
    AWS_STORAGE_BUCKET_NAME=local-development-bucket
    AWS_REGION_NAME=eu-central-1

    # External Services
    GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json
    API_KEY=dummy-api-key-for-local-development
    TAPS_SECRET_KEY=dummy-taps-secret-key

    # Environment
    DOMAIN_NAME=localhost
    ENVIRONMENT=local
    SENTRY_SDK_DSN=https://dummy@sentry.example.com/123
    S3_BUCKET_NAME=local-development-bucket
    ```

3. Build and run the application with Docker Compose:
   ```bash
   docker-compose -f docker-compose.local.yml up --build -d
   ```

4. Run Django management commands:
   ```bash
   docker-compose -f docker-compose.local.yml exec django python manage.py [command]
   ```

## todo:

1. mention how the deployment will work and the needed setups for envs
2. consider making scripts to automate the process
