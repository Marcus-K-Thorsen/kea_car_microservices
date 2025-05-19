import os
import logging

# Ensure log directory exists
log_dir = "var/log/auth_microservice"
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