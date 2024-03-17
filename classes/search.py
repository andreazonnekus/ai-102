import os, sys, requests
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

class Search:
    def __init__(self) -> None:
        # Get Configuration Settings
        load_dotenv()

        url = os.getenv('SEARCH_URL')
        key = os.getenv('SEARCH_KEY')
        index = os.getenv('SEARCH_INDEX_NAME')

        self.search_client = SearchClient(url, index, AzureKeyCredential(key))
        
    def main(self):
        try:
            # Analyze image
            if len(sys.argv) > 1:
                if len(sys.argv) > 2:
                    search_input = sys.argv[2]

                # Train
                if sys.argv[1] == 'search':
                    self.search(search_input)

        except Exception as ex:
            print(ex)

    def search(search_text = None):
        while search_text == None:
            search_text = input("What do you want to search\n")
        
        # Submit search query
        results =  self.search_client.search(search_text,
                                        # search_mode="all",
                                        include_total_count=True,
                                        # filter=filter_by,
                                        # order_by=sort_order,
                                        # facets=['metadata_author'],
                                        # highlight_fields='merged_content-3,imageCaption-3',
                                        # select = "keyphrases, text, translated_text, merged_content, imageTags, imageCaption")
                                        select = "text")
        print(results.get_answers())