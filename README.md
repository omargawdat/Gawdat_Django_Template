## 1. Initial Project Configuration

1. **Rename Project**  
   Replace `project_name` with the actual name of your project to better reflect its identity.

2. **Domain Configuration**  
   - Update any instance of `domain.com` into real domain.
   - make sure the domain is pointing into the instance IP.
3. **Fill the `.envs/.production/.django` file**
4. **Optional: Replace Postgis with POSTGRES**
    - If your project does not use PostGIS, you may remove `libgdal` from the Django Docker files.
    - Replace the PostGIS image with a standard PostgreSQL image to match your project's database needs.
    - Update the `DATABASE_URL` in the `entry point` file to "postgres".
5. **Optional: Using S3**
   - Remove white noise from `[middle ware + package]`
   - Write the s3 configurations in the productions settings. 
6. **Try the Local Development**
  ```
  docker compose -f local.yml up --build
  docker compose -f local.yml exec django python manage.py makemigrations
  docker compose -f local.yml exec django python manage.py migrate
  ```

## 2. Git Repository Setup
1. **Uncomment the `.gitignore` File**
2. **Uncomment the `ci.yml` and `dependabot.yml`Files**
3. **Initialize the Git Repository**
   ```
   sudo rm -r .git
   git init
   pre-commit install
   git add .
   git commit -m "Initial commit"
   ```
4. **Share the project on GitHub**


## 3. Server Ready Configuration
1. **Create Ec2 instance with  IAM Role (S3) if using s3**
2. **Install Needed Packages Using DNF (Amazon Linux 2023)**
   ```
   sudo dnf install git 
   sudo dnf install docker
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ec2-user
   newgrp docker
   sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) -o /usr/bin/docker-compose && sudo chmod 755 /usr/bin/docker-compose && docker-compose --version. 
   ```
3. **Clone the repository to your server.**
    ```
      git clone repo_url
    ```
4. **Upload the .envs files into the server**
    ```
      mkdir .envs/.production/
    ```
    ```
       nano .envs/.production/.django
    ```
    ```
       nano .envs/.production/.postgres
    ```
    ```
       python3 merge_production_dotenvs_in_dotenv.py
    ```
5. Run the docker container
   ```
    sudo docker-compose -f production.yml up --build
   ```
   