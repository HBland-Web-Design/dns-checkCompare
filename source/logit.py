import logging
from datetime import datetime
import os

def getDate():
    return datetime.now().date()

logit = logging.getLogger(__name__)

if os.getenv('HB_RUNTIME') == 'DOCKER':
    pass
else:
    fileHandler = logging.FileHandler('{}.log'.format(getDate()))
streamHandler = logging.StreamHandler()

streamHandler.setLevel(logging.INFO)
fileHandler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
streamFormat = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
fileFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(streamFormat)
fileHandler.setFormatter(fileFormat)

# Add handlers to the logger
logit.addHandler(streamHandler)
logit.addHandler(fileHandler)