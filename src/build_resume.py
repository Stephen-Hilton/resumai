import sys, dotenv, os, requests
from pathlib import Path

from langchain import chat_models
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.document_loaders import TextLoader

import openai
from docx import Document

sys.argv = [sys.argv[0], 'stephen.yaml', 'Apple_ Retail Store Analytics Director.md']

# load .env secrets
dotenv.load_dotenv('./.env')
llm_provider = str(os.getenv('LLM_MODEL_PROVIDER') )
llm_model    = str(os.getenv('LLM_MODEL'))
llm_apikey   = str(os.getenv('LLM_API_KEY'))
llm_apiurl   = str(os.getenv('LLM_API_URL'))


def build_prompt(person_filename:str, jobdesc_filename:str, extra_prompt:str='') -> str:

    # open files, and error if missing: 
    person_filepath  = Path(f'./people/{person_filename}').resolve()
    jobdesc_filepath =  Path(f'./jobs/{jobdesc_filename}').resolve()

    if person_filepath.exists() is False or jobdesc_filepath.exists() is False:
        print(f"""
                ERROR: missing file: 
                {person_filename} exists = {str(person_filepath.exists())} 
                {jobdesc_filename} exists = {str(jobdesc_filename.exists())} """)
        return None

    # load files to memory:
    with open(person_filepath, 'r') as f: person = str(f.read())
    with open(jobdesc_filepath, 'r') as f: jobdesc = str(f.read())
    with open(Path('./src/prompts/sys01_load_files.prompt'), 'r') as f: msg01 = str(f.read())
    with open(Path('./src/prompts/sys02_main_instructions.prompt'), 'r') as f: msg02 = str(f.read())
    with open(Path('./src/prompts/sys03_format.prompt'), 'r') as f: msg03 = str(f.read())
    msg01 = msg01.replace('{person}', person).replace('{jobdesc}', jobdesc)

    # build prompt list, and plain ol text:
    msgs = [
        {"role": "system", "content": msg01 },
        {"role": "system", "content": msg02 },
        {"role": "system", "content": msg03 },
        {"role": "user", "content": extra_prompt }
        ]
    text_prompt = '\n'.join([m['content'] for m in msgs])
    return (text_prompt, msgs)

   



################################ Generate two DOCX files
import requests
import os
from docx import Document

def generate_docx_files(model_name, api_key, prompt):
    # Set API endpoint and headers
    url = f"https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Set prompt and parameters
    data = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": 16000,
        "temperature": 0.7,
        "top_p": 1,
        "stop": None
    }

    # Make API call
    response = requests.post(url, headers=headers, json=data)

    # Check if response was successful
    if response.status_code == 200:
        # Get text from response
        text = response.json()["choices"][0]["text"]

        # Split text into two parts
        parts = text.split("###")  # Assuming ### is the separator

        # Create two DOCX files
        for i, part in enumerate(parts):
            document = Document()
            document.add_paragraph(part)
            filename = f"file_{i+1}.docx"
            document.save(filename)
            print(f"Saved {filename} to local directory")
    else:
        print(f"Error: {response.status_code}")


################################
 



if __name__ == "__main__":

    # if called from the command line, grab the two required CLI arguments
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <person_filename> <jobdesc_filename> <optional extra prompt text>")
    else:
        person_filename = sys.argv[1]
        jobdesc_filename = sys.argv[2]  
        extra_prompt = '' if len(sys.argv) < 4 else sys.argv[3]

        # build prompt:
        text_prompt, msgs = build_prompt(person_filename, jobdesc_filename, extra_prompt)
        response = generate_docx_files(llm_model, llm_apikey, text_prompt)

        print(text_prompt)
        

    pass