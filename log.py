import logging
import logging.config
import time
from pythonjsonlogger import jsonlogger
import sys
from datetime import datetime;

while(True):
    time.sleep(2)
    handler = logging.StreamHandler(sys.stdout)
    class ElkJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
            log_record['@timestamp'] = datetime.now().isoformat()
            log_record['level'] = record.levelname
            log_record['logger'] = record.name

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger("MainLogger")
    logging.info('Application running!')
    logger.addHandler(handler)