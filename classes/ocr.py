import os, sys, requests
from dotenv import load_dotenv
import azure.ai.vision as sdk
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

from utils import *

class OCR:
    def __init__(self):
        global vision_client

        load_dotenv()

        # Set the values of your computer vision endpoint and computer vision key as environment variables:
        try:
            url = os.environ.get("VISION_URL")
            key = os.environ.get("VISION_KEY")
        except KeyError:
            print("Missing environment variable 'VISION_URL' or 'VISION_KEY'")
            print("Set them before running this sample.")
            exit()

        # Create an Image Analysis client
        vision_client = sdk.VisionServiceOptions(url, key)

        # Get image
        if len(sys.argv) > 1:
            if len(sys.argv) > 2:
                image_file = os.path.join('static', 'input', sys.argv[2] + '.jpg') 
            else:
                image_file = 'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png'
            
            # Analyze image
            if sys.argv[1] == 'read':
                read_image(image_file)

        else:
            image_file = 'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png'
            read_image(image_file)

    def read_image(image_file):

        if is_url(image_file):
            outputfile = os.path.join('static', 'input', image_file.split('/')[-1].split('.')[0] + '.jpg')
            with open(outputfile, 'wb') as file:
                file.write(requests.get(image_file).content)
            image_file = outputfile
        
        # Specify features to be retrieved
        img = sdk.VisionSource(image_file)
        analysis_options = sdk.ImageAnalysisOptions()
        features = analysis_options.features = (
            sdk.ImageAnalysisFeature.TEXT
        )

        # Get image analysis
        image_analyzer = sdk.ImageAnalyzer(vision_client, img, analysis_options)
        result = image_analyzer.analyze()

        print("Image analysis results:")
        # Print caption results to the console
        print("\nCaption:")
        if result.caption is not None:
            print(f"\t'{result.caption.text}', Confidence {result.caption.confidence:.3f}")

        # Prepare image for drawing
        image = Image.open(image_file)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for line in result.text.lines:
            drawLinePolygon = True
            r = line.bounding_polygon
            bounding_polygon = ((r[0], r[1]),(r[2], r[3]),(r[4], r[5]),(r[6], r[7]))

            for word in (y for y in line.words if y.confidence > 0.5):
                r = word.bounding_polygon
                bounding_polygon = ((r[0], r[1]),(r[2], r[3]),(r[4], r[5]),(r[6], r[7]))
                print("  Word: '{}', Bounding Polygon: {}, Confidence: {}".format(word.content, bounding_polygon,word.confidence))

                # Draw word bounding polygon
                drawLinePolygon = False
                draw.polygon(bounding_polygon, outline=color, width=1)
            
            if drawLinePolygon:
                draw.polygon(bounding_polygon, outline=color, width=2)
        
        if is_url(img):
            outputfile = os.path.join('static', 'ocr', 'results_' + image_file.split('/')[-1].split('.')[0] + '.jpg')
        else:
            outputfile = os.path.join('static', 'ocr', 'results_' + image_file.split(os.sep)[-1].split('.')[0] + '.jpg')

        # Save image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        fig.savefig(outputfile)
        if os.path.isfile(image_file):
            print('\n  Results saved in', outputfile)

        # Print text (OCR) analysis results to the console
        outputfile = os.path.join('static', 'ocr', 'results_' + image_file.split(os.sep)[-1].split('.')[0] + '.txt')
        print("\nRead:")
        if result.text is not None:
            with open(outputfile, 'a') as file:
                for line in result.text.lines:
                    print(f"\tLine: '{line}', Bounding box {line.bounding_polygon}")

                    file.write(f'\n' + line.content)

                    for word in (y for y in line.words if y.confidence > 0.5):
                        print(f"\t\tWord: '{word.content}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.2f}")