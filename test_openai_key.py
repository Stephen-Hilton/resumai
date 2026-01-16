#!/usr/bin/env python3
"""
Test script to verify OpenAI API key is configured correctly.

This script will:
1. Check if the API key is set in environment
2. Make a simple API call to verify the key works
3. Display quota and model information
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test the OpenAI API key configuration."""
    
    print("=" * 60)
    print("OpenAI API Key Test")
    print("=" * 60)
    print()
    
    # Check environment variables
    print("1. Checking environment variables...")
    print("-" * 60)
    
    llm_provider = os.getenv('LLM_PROVIDER')
    llm_model = os.getenv('LLM_MODEL')
    llm_api_key = os.getenv('LLM_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    print(f"LLM_PROVIDER: {llm_provider or '(not set)'}")
    print(f"LLM_MODEL: {llm_model or '(not set)'}")
    print(f"LLM_API_KEY: {'***' + llm_api_key[-4:] if llm_api_key and len(llm_api_key) > 4 else '(not set)'}")
    print(f"OPENAI_API_KEY: {'***' + openai_api_key[-4:] if openai_api_key and len(openai_api_key) > 4 else '(not set)'}")
    print()
    
    if not llm_api_key and not openai_api_key:
        print("❌ ERROR: No API key found!")
        print()
        print("Please set LLM_API_KEY in your .env file:")
        print("  export LLM_API_KEY=\"sk-...\"")
        print()
        return False
    
    # Use LLM_API_KEY if set, otherwise fall back to OPENAI_API_KEY
    api_key = llm_api_key or openai_api_key
    
    if not llm_provider:
        print("⚠️  WARNING: LLM_PROVIDER not set, assuming 'openai'")
        llm_provider = "openai"
    
    if not llm_model:
        print("⚠️  WARNING: LLM_MODEL not set, assuming 'gpt-4o-mini'")
        llm_model = "gpt-4o-mini"
    
    print()
    
    # Test API connection
    print("2. Testing API connection...")
    print("-" * 60)
    
    try:
        if llm_provider.lower() == "openai":
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            # Make a simple API call
            print(f"Making test API call with model: {llm_model}")
            
            # Use max_completion_tokens (works with all modern models)
            # Note: Some models like gpt-5-mini only support default temperature
            response = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'API key is working!' in exactly 5 words."}
                ],
                max_completion_tokens=20
            )
            
            result = response.choices[0].message.content
            print(f"✅ API Response: {result}")
            print()
            
            # Display usage information
            print("3. API Usage Information")
            print("-" * 60)
            print(f"Model: {response.model}")
            print(f"Tokens used: {response.usage.total_tokens}")
            print(f"  - Prompt tokens: {response.usage.prompt_tokens}")
            print(f"  - Completion tokens: {response.usage.completion_tokens}")
            print()
            
            print("=" * 60)
            print("✅ SUCCESS: OpenAI API key is configured correctly!")
            print("=" * 60)
            return True
            
        else:
            print(f"❌ ERROR: Unsupported LLM provider: {llm_provider}")
            print("Currently only 'openai' is supported.")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: API call failed!")
        print()
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()
        
        # Provide helpful error messages
        error_str = str(e).lower()
        if "401" in error_str or "invalid" in error_str or "incorrect" in error_str:
            print("This looks like an authentication error.")
            print()
            print("Possible causes:")
            print("  1. API key is incorrect or expired")
            print("  2. API key format is wrong (should start with 'sk-')")
            print("  3. Environment variable contains placeholder text like '$LLM_API_KEY'")
            print()
            print("To fix:")
            print("  1. Get your API key from: https://platform.openai.com/api-keys")
            print("  2. Update your .env file:")
            print("     export LLM_API_KEY=\"sk-your-actual-key-here\"")
            print("  3. Restart your terminal or run: source .env")
            print()
        elif "429" in error_str or "rate" in error_str:
            print("This looks like a rate limit error.")
            print()
            print("Possible causes:")
            print("  1. You've exceeded your API quota")
            print("  2. Too many requests in a short time")
            print()
            print("To fix:")
            print("  1. Check your usage at: https://platform.openai.com/usage")
            print("  2. Wait a few minutes and try again")
            print("  3. Consider upgrading your plan if needed")
            print()
        elif "model" in error_str:
            print("This looks like a model access error.")
            print()
            print("Possible causes:")
            print("  1. The model name is incorrect")
            print("  2. You don't have access to this model")
            print()
            print("To fix:")
            print("  1. Check available models at: https://platform.openai.com/docs/models")
            print("  2. Update LLM_MODEL in your .env file")
            print()
        
        return False


if __name__ == '__main__':
    success = test_openai_key()
    sys.exit(0 if success else 1)
