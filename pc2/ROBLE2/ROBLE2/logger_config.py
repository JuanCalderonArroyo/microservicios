# logger_config.py
import logging

logging.basicConfig(
    filename='microservices.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("microservice_manager")
