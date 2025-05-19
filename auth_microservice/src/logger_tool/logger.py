import os
import logging

# Get the absolute path to the parent directory of auth_microservice
current_dir = os.path.dirname(os.path.abspath(__file__))
auth_microservice_dir = os.path.dirname(current_dir)
log_dir = os.path.join(auth_microservice_dir, "var", "log", "auth_microservice")
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add file handler to log to a file as well
file_handler = logging.FileHandler(os.path.join(log_dir, "auth_microservice.log"))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)