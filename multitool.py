import argparse
from ai_search import Search
from vision_analysis import VisionAnalysis
from vision_detection import VisionDetection
from text_analysis import TextAnalysis
from translation import Translation
from conversational_model import ConversationalModel
from openai_cmd import OpenAI
from ocr import OCR
from document_intelligence import DocumentIntelligence
from video_processing import VideoProcessing
from speech_synthesis import SpeechSynthesis

class MULTITOOL:
    def __init__(self):
        self.actions = {
            'search': Search,
            'vision analysis': VisionAnalysis,
            'vision detection': VisionDetection,
            'text analysis': TextAnalysis,
            'translate': Translation,
            'conversation model': ConversationalModel,
            'open AI': OpenAI,
            'ocr': OCR,
            'document intelligence': DocumentIntelligence,
            'video processing': VideoProcessing,
            'speech synthesis': SpeechSynthesis,
        }
        self.parser = argparse.ArgumentParser(description='Welcome to the multitool')
        self.parser.add_argument('action', choices=list(self.actions.keys()) + [str(i) for i in range(1, len(self.actions)+1)], help='Choose an action by name or number')
        self.parser.add_argument('--function', type=str, help='Choose a function within the action class')
        self.parser.add_argument('--param1', type=int, help='Parameter 1')
        self.parser.add_argument('--param2', type=str, help='Parameter 2')

    def run(self):
        args = self.parser.parse_args()

        if args.action.isdigit():
            # User provided a number
            action_num = int(args.action)
            if 1 <= action_num <= 5:
                action_name = f'action{action_num}'
        else:
            action_name = args.action

        if action_name in self.actions:
            # User provided action name
            action_instance = self.actions[action_name]()
            if args.function:
                self._execute_function(action_instance, args.function, args.param1, args.param2)
            else:
                self._list_functions(action_instance)
        else:
            print("Invalid action. Please choose a valid action name or number.")

    def _list_functions(self, action_instance):
        functions = [func for func in dir(action_instance) if callable(getattr(action_instance, func)) and not func.startswith("__")]
        print(f"Functions available in {action_instance.__class__.__name__}: {', '.join(functions)}")

    def _execute_function(self, action_instance, function_name, param1, param2):
        if hasattr(action_instance, function_name):
            # Check if the action class has the specified function
            function_to_call = getattr(action_instance, function_name)
            function_to_call(param1, param2)
        else:
            print(f"Invalid function '{function_name}' for the chosen action.")

if __name__ == "__main__":
    multiool = MULTITOOL()
    multiool.run()