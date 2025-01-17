# from pathlib import Path
#
# from django.conf import settings
# from django.core.checks import Error
# from django.core.checks import register
#
# REQUIRED_FILES = [
#     "firebase_cred.json",
# ]
#
#
# def get_required_vars_from_env_example():
#     env_example_path = Path(settings.BASE_DIR) / ".env.example"
#     required_vars = []
#
#     with open(env_example_path) as f:
#         for line in f:
#             line = line.strip()
#             if line and not line.startswith("#"):
#                 var_name = line.split("=")[0].strip()
#                 required_vars.append(var_name)
#
#     return required_vars
#
#
# @register()
# def check_critical_env_vars_and_files(app_configs, **kwargs):
#     errors = []
#
#     # Check environment variables
#     required_vars = get_required_vars_from_env_example()
#     for var in required_vars:
#         if not hasattr(settings, var):
#             errors.append(
#                 Error(
#                     f'Required environment variable "{var}" is not set',
#                     hint=f"Please set the {var} environment variable (defined in .env.example)",
#                     obj=settings,
#                     id="myapp.E001",
#                 )
#             )
#
#     # Check required files
#     for file_name in REQUIRED_FILES:
#         file_path = Path(settings.BASE_DIR) / file_name
#         if not file_path.exists():
#             errors.append(
#                 Error(
#                     f'Required file "{file_name}" is missing',
#                     hint=f"Please ensure {file_name} exists in the project root directory",
#                     obj=settings,
#                     id="myapp.E002",
#                 )
#             )
#
#     return errors
