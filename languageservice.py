from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


"""
LanguageService class provides methods to analyze text using Azure Text Analytics API.
Methods:
    __init__(self, endpoint, key):
        Initializes the LanguageService with the given endpoint and key.
    analyze_text(self, text):
        Analyzes the sentiment of the given text and extracts key phrases.
        Returns a dictionary with sentiment, severity, key phrases, and confidence scores.
        Parameters:
            text (str): The text to be analyzed.
        Returns:
            dict: A dictionary containing the sentiment, severity, key phrases, and confidence scores.
            In case of an error, returns an error message string.
Example usage:
        endpoint = "https://your-endpoint.cognitiveservices.azure.com/"
        key = "your-key"
        test_text = "Your text here."
""" 

class LanguageService:
    def __init__(self, endpoint, key):
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def analyze_text(self, text):
        try:
            response = self.client.analyze_sentiment(documents=[text])[0]
            sentiment = response.sentiment
            severity = "high" if response.confidence_scores.negative > 0.5 else "low"
            key_phrases = self.client.extract_key_phrases(documents=[text])[0].key_phrases
            return {
                "sentiment": sentiment,
                "severity": severity,
                "key_phrases": key_phrases,
                "scores": {
                    "positive": response.confidence_scores.positive,
                    "neutral": response.confidence_scores.neutral,
                    "negative": response.confidence_scores.negative
                }
            }
        except Exception as e:
            return f"Error in text analysis: {str(e)}"



    
 