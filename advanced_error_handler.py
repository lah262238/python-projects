import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom error for API failures"""
    pass

class ValidationError(Exception):
    """Custom error for invalid input"""
    pass

class APIClient:
    """Handle API calls with advanced error handling"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_KEY")
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
        
        if not self.api_key:
            logger.error("API key not found in environment variables")
            raise ValidationError("Missing API key. Check .env file")
    
    def validate_input(self, text, min_length=1, max_length=5000):
        """Validate input before sending to API"""
        if not text:
            raise ValidationError("Input text cannot be empty")
        if len(text) < min_length:
            raise ValidationError(f"Text too short. Minimum {min_length} characters")
        if len(text) > max_length:
            raise ValidationError(f"Text too long. Maximum {max_length} characters")
        return True
    
    def call_api(self, messages, timeout=30):
        """Call API with error handling"""
        import requests
        
        try:
            logger.info("Calling API with model: " + self.model)
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + self.api_key},
                json={
                    "model": self.model,
                    "messages": messages
                },
                timeout=timeout
            )
            
            # Check for HTTP errors
            if response.status_code != 200:
                logger.error(f"API returned status {response.status_code}")
                raise APIError(f"API Error: Status {response.status_code}")
            
            data = response.json()
            
            # Check for API errors in response
            if "error" in data:
                logger.error(f"API error: {data['error']['message']}")
                raise APIError(f"API Error: {data['error']['message']}")
            
            logger.info("API call successful")
            return data["choices"][0]["message"]["content"]
        
        except requests.Timeout:
            logger.error("API request timed out")
            raise APIError("Request timed out. Please try again")
        
        except requests.ConnectionError:
            logger.error("Connection error to API")
            raise APIError("Connection error. Check internet connection")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise APIError(f"Unexpected error: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        client = APIClient()
        logger.info("API client initialized successfully")
        
        # Test with valid input
        text = "Hello, this is a test message"
        client.validate_input(text)
        
        messages = [{"role": "user", "content": text}]
        response = client.call_api(messages)
        
        print(f"Response: {response}")
        logger.info("Test completed successfully")
    
    except ValidationError as e:
        print(f"Validation Error: {str(e)}")
        logger.error(f"Validation error: {str(e)}")
    
    except APIError as e:
        print(f"API Error: {str(e)}")
        logger.error(f"API error: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
