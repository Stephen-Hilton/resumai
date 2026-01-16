"""
Test script for Gmail job collection.

This script tests the get_gmail_linkedin event to fetch job alerts from Gmail.
"""

import asyncio
from pathlib import Path
from src.lib.types import EventContext
from src.events.event_bus import run_event
from dotenv import load_dotenv
import os


async def test_gmail_collection():
    """Test Gmail job collection."""
    
    # Load environment variables
    load_dotenv()
    
    print("=" * 60)
    print("Gmail Job Collection Test")
    print("=" * 60)
    
    # Verify credentials are loaded
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not username or not password:
        print("ERROR: Gmail credentials not found in .env file")
        print("Please ensure GMAIL_USERNAME and GMAIL_APP_PASSWORD are set")
        return
    
    print(f"Gmail Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    # Create context
    ctx = EventContext(
        jobs_root=Path("jobs"),
        resumes_root=Path("resumes"),
        default_resume="Stephen_Hilton.yaml",
        test_mode=False
    )
    
    print("Connecting to Gmail and searching for LinkedIn job alerts...")
    print("(This may take a minute)")
    print()
    
    # Run the event
    result = await run_event("get_gmail_linkedin", Path("placeholder"), ctx)
    
    print("=" * 60)
    print("Results:")
    print("=" * 60)
    
    if result.ok:
        print(f"✅ SUCCESS: {result.message}")
        if result.artifacts:
            print(f"\nCreated job folders:")
            for job_path in result.artifacts:
                print(f"  - {job_path}")
    else:
        print(f"❌ FAILED: {result.message}")
        if result.errors:
            print("\nErrors:")
            for error in result.errors:
                if isinstance(error, dict):
                    print(f"  - {error.get('message', str(error))}")
                    if error.get('details'):
                        details = error['details']
                        if isinstance(details, dict):
                            for key, value in details.items():
                                print(f"    {key}: {value}")
                        else:
                            print(f"    Details: {details}")
                else:
                    print(f"  - {error}")
    
    print()
    print("=" * 60)
    print("Check src/logs/ for detailed application logs")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_gmail_collection())
