import os
from dotenv import load_dotenv
import jobs_1_queue


def main():

    load_dotenv('.env')
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')

    jobs_1_queue.load(gmail_address=gmail_address, 
                       gmail_app_password=gmail_app_password)
    
    pass
          
if __name__ == '__main__':
    main()
