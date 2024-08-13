## 1. Initial Project Configuration

1. **Rename Project**
   Replace `newproject` with the actual name of your project to better reflect its identity.

2. **Domain Configuration**
    - Update any instance of `domain.com` into real domain.
    - make sure the domain is pointing into the instance IP.
3. **Fill the `.envs/.production/.django` file**
4. **Try the Local Development**

  ```
  docker compose -f docker-compose.local.yml up --build -d
  ```

## 2. Git Repository Setup

1. **Uncomment the `.gitignore`, `ci.yml`, `dependabot`  Files**
2. **Initialize the Git Repository**
   ```
   sudo rm -r .git
   git init
   pre-commit install
   git add .
   git commit -m "Initial commit"
   ```
3. **Share the project on GitHub**

## 3. Server Ready Configuration

1. **Create Ec2 instance using AMI image with IAM Role Full access**
2. **Create S3 Bucket**
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
    sudo docker-compose -f docker-compose.production.yml up --build
   ```

TODO:

- validations and exceptions
- permissions (owner-rules?)
