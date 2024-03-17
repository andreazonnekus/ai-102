import os, sys
from dotenv import load_dotenv

class ConversationalModel:
    def __init__(self) -> None:
        # Get Configuration Settings
        load_dotenv()

        training_endpoint = os.getenv('VISION_URL')
        training_key = os.getenv('VISION_KEY')
        project_id = os.getenv('PROJECT_ID')
        model_name = os.getenv('CLASSIFICATION_MODEL')

        # Get the Custom Vision project
        custom_vision_project = conversational_client.get_project(project_id)

    def main(self):
        try: 
            if len(sys.argv) > 0:

                if len(sys.argv) > 1:
                    search_term = sys.argv[2]
                # Converse
                if sys.argv[1] == 'converse':
                    
                    self.converse()
        except Exception as ex:
            print(ex)

    def converse(self):
        # TODO: do something
        pass