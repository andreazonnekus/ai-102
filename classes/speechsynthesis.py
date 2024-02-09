from dotenv import load_dotenv

class SpeechSynthesis:
    def __init__(self):
        global training_client

        try:
            # Get Configuration Settings
            load_dotenv()

            training_endpoint = os.getenv('VISION_URL')
            training_key = os.getenv('VISION_KEY')
            project_id = os.getenv('PROJECT_ID')
            model_name = os.getenv('CLASSIFICATION_MODEL')

            # Get the Custom Vision project
            custom_vision_project = training_client.get_project(project_id)
            
            # Analyze image
            if len(sys.argv) > 0:

                if len(sys.argv) > 1:
                    search_term = sys.argv[2]
                # Train
                if sys.argv[1] == 'search':
                    
                    # Authenticate a client for the training API
                    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
                    training_client = CustomVisionTrainingClient(training_endpoint, credentials)

                    train(custom_vision_project, folder)
                elif sys.argv[1] == 'test':
                    img = os.path.join('static', 'test', sys.argv[3]) if sys.argv[3] and sys.argv[2] else os.path.join('static', 'test', 'image.jpg')
                    
                    # Authenticate a client for the training API
                    credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
                    prediction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)

                    test(model_name, custom_vision_project, img)
        except Exception as ex:
            print(ex)