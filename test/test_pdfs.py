import sys, logging
from pathlib import Path

# Add src directory to path so we can import modules
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from step1_queue import get_all_ids
from step2_generate import print_pdf


ids = get_all_ids()

for id in [i for i in ids if i not in ['0000000000']][:3]: 
    logging.info(f'Starting manual PDF of ID: {id}')
    response = print_pdf(id)
    if response['success'] == False: break 

pass