import os
from dotenv import load_dotenv
import step1_queue, step2_generate
import logging_setup


def main():
    # Set up logging first
    logger = logging_setup.setup_logging()
    
    try:
        logger.info("Loading environment variables")
        load_dotenv('.env')
        gmail_address = os.getenv('GMAIL_ADDRESS')
        gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_address or not gmail_app_password:
            logger.warning("Gmail credentials not found in environment variables")
        else:
            logger.info(f"Gmail address configured: {gmail_address}")
        
        logger.info("Starting job queue loading process")
        step1_queue.load(gmail_address=gmail_address, 
                         gmail_app_password=gmail_app_password)
        
        logger.info("Starting custom resume generation")
        step2_generate.generate(force=False)

        logger.info("Main process completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}", exc_info=True)
        raise
          
if __name__ == '__main__':
    main()
