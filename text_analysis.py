import os, sys
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

class TextAnalysis:
    def __init__(self):
        global language_client
        
        load_dotenv()
        
        try:
            url = os.getenv('LANGUAGE_URL')
            key = os.getenv('LANGUAGE_KEY')

            language_client = TextAnalyticsClient(url, AzureKeyCredential(key))

            if len(sys.argv) > 1:
                if len(sys.argv) > 2:
                    input_text = sys.argv[2]
                else:
                    input_text = None
            
                # Analyze image
                if sys.argv[1] == 'detect':
                    detect_language(input_text)
                elif sys.argv[1] == 'extract':
                    extract_keyphrase(input_text)
                elif sys.argv[1] == 'sentiment':
                    detect_sentiment(input_text)
                elif sys.argv[1] == 'recognise':
                    recognise_entities(input_text)
                elif sys.argv[1] == 'link':
                    link_entities(input_text)
        except Exception as ex:
            print(ex)
        
    def detect_language(text = None):
        while text == None:
            text = input("What text do you want to determine the primary language of?\n")
        detectedLanguage = language_client.detect_language(documents=[text])[0]

        print('\nThe primary language was determined to be {} at {}% confidence'.format(
            detectedLanguage.primary_language.name, 
            int(detectedLanguage.primary_language.confidence_score*100)))

    def extract_keyphrase(text = None):
        while text == None:
            text = input("What text do you want to extract key phrases from?\n")
        extractedPhrases = language_client.extract_key_phrases(documents = [text])[0]
        
        print('\nKey phrases include: {}'.format(
            ', '.join(extractedPhrases.key_phrases)))

    def detect_sentiment(text = None):
        while text == None:
            text = input("What do you want to analyse the sentiment of?\n")
        detectedSentiment = language_client.analyze_sentiment(documents=[text])[0]

        print('\nThere is a {}% percent chance the phrase \n\t\"{}\"\nis {}\n'.format(
            int(detectedSentiment.confidence_scores[detectedSentiment.sentiment] * 100),
            ' '.join([x.text for x in detectedSentiment.sentences]),
            detectedSentiment.sentiment))

    def recognise_entities(text = None):
        while text == None:
            text = input("What sentence do you want to detect the entities in?\n")
        recognisesdEntities = language_client.recognize_entities(documents=[text])[0]

        print('\nThese are the detected entities: \"{}\" with confidence scores of\n\t{}% respectively\n'.format(
            ', '.join([x.text for x in recognisesdEntities.entities]),
            '%, '.join([str(int(x.confidence_score * 100)) for x in recognisesdEntities.entities])))

    def link_entities(text = None):
        while text == None:
            text = input("What sentence do you want to detect the entities in?\n")
        recognisesdLinkedEntities = language_client.recognize_linked_entities(documents=[text])[0].entities
        processedLinkedEntities = [[x.name, int(x.matches[0].confidence_score * 100), x.url] for x in recognisesdLinkedEntities]

        for entity in processedLinkedEntities:
            print('\n\"{}\" (Found at {}) with confidence scores of {}%'.format(
                entity[0],
                entity[2],
                entity[1]))