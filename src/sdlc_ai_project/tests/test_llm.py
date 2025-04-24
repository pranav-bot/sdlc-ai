import os
import pytest
from crewai import LLM
from dotenv import load_dotenv

def test_gemini_llm_configuration():
    # Load environment variables
    load_dotenv()
    
    # Get the Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        pytest.skip("GEMINI_API_KEY not set in environment")
    
    # Configure the LLM
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=gemini_api_key
    )
    
    # Test a simple completion
    response = llm.call("What is 2+2?")
    
    # Basic assertions
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Test with a more complex prompt
    complex_prompt = """
    You are a software architect. Please provide a brief overview of 
    microservices architecture in 2-3 sentences.
    """
    response = llm.call(complex_prompt)
    
    # Basic assertions for complex response
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert "microservices" in response.lower() or "architecture" in response.lower()

def test_gemini_llm_error_handling():
    # Test with invalid API key
    with pytest.raises(Exception):
        llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key="invalid_key"
        )
        llm.call("Test prompt")
    
    # Test with invalid model name
    with pytest.raises(Exception):
        llm = LLM(
            model="invalid_model",
            api_key=os.getenv("GEMINI_API_KEY")
        )
        llm.call("Test prompt") 