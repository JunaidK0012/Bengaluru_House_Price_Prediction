import os
import sys
import logging
from datetime import datetime

LOGS_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
Log_path = os.path.join(os.getcwd(),'logs',LOGS_FILE)

os.makedirs(Log_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_FILE,Log_path)

logging.basicConfig(
    name = LOG_FILE_PATH,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

logging.info('Logging has started')