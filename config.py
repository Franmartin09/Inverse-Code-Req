import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

def config_groq():
    # Get the Groq API key from the environment variables
    groq_api_key = os.getenv('GROQ_API_KEY')

    # Ensure the API key is loaded correctly
    if not groq_api_key:
        raise ValueError("Groq API key not found in the environment variables.")

    # Initialize Groq client using the API key
    groq_client = Groq(api_key=groq_api_key)
    return groq_client

def config_variables():
    code_dir = os.getenv('CODE_DIR')
    output_dir = os.getenv('OUTPUT_DIR')
    return code_dir, output_dir