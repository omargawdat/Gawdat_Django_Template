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
    cp dummy.env .env
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
