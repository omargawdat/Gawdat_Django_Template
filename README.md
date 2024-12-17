## 1. Initial Project Configuration

1. **Rename Project**
   Replace `temp_project` with the actual name of your project to better reflect its identity.

2. **Domain Configuration**
    - Update any instance of `example.com` into real domain.
    - make sure the domain is pointing into the instance IP.
3. **Fill the `.envs/.prod/.django` file**
4. **Try the Local Development**
5. create `dev` branch
6. database in pycharm

  ```
  docker compose -f docker-compose.local.yml up --build -d
  ```

## 2. Git Repository Setup

1. **Uncomment the `.gitignore`, `ci.yml`, `dependabot`  Files**
2. **Initialize the Git Repository**
   ```
   brew install hadolint
   sudo rm -r .git
   git init
   pre-commit install
   pre-commit install --hook-type commit-msg
   git add .
   git commit -m "Initial commit"
   ```
3. **Share the project on GitHub**
4.

## 3. Server Ready Configuration

1. **Create Ec2 instance using AMI image with IAM Role Full access**
2. **Create S3 Bucket**
3. **Clone the repository to your server.**
    ```
      git clone repo_url
    ```
4. **Upload the .envs files into the server**
    ```
      mkdir .envs/.prod/
    ```
    ```
       nano .envs/.prod/.django
    ```
    ```
       nano .envs/.prod/.postgres
    ```
5. Run the docker container
   ```
    sudo docker-compose -f docker-compose.prod.yml up --build
   ```
