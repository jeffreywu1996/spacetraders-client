import sys
sys.path.append('.')
sys.path.append('backend')
import logging

from backend.controllers import agent

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
    payload, _ = agent.agent()
    for k,v in payload['data'].items():
        logger.info(f'{k}: {v}')
