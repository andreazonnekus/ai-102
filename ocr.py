import os, sys, requests
from dotenv import load_dotenv
import azure.ai.vision as sdk
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image

from utils import *

load_dotenv()


def main():
    from dotenv import load_dotenv
    global cv_client

    # Set the values of your computer vision endpoint and computer vision key as environment variables:
    try:
        url = os.environ.get("VISION_URL")
        key = os.environ.get("VISION_KEY")
    except KeyError:
        print("Missing environment variable 'VISION_URL' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    # Create an Image Analysis client
    cv_client = ImageAnalysisClient(
        endpoint=url,
        credential=AzureKeyCredential(key)
    )

    # Get image
    if len(sys.argv) > 1:
        image_file = os.path.join('static', 'input', sys.argv[2] + '.jpg') if sys.argv[2] else 'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png'
    
        # Analyze image
        if sys.argv[1] == 'read':
            read_image(image_file, cv_client)

    else:
        image_file = 'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png'
        read_image(image_file, cv_client)

def read_image(image_file, client):

    if is_url(image_file):
        outputfile = os.path.join('static', 'input', image_file.split('/')[-1].split('.')[0] + '.jpg')
        with open(outputfile, 'wb') as file:
            file.write(requests.get(image_file).content)
        img = sdk.VisionSource(outputfile)
    else:
        img = sdk.VisionSource(image_file)

    analysis_options = sdk.ImageAnalysisOptions()
    analysis_options.features = sdk.ImageAnalysisFeature.TEXT

    image_analyzer = sdk.ImageAnalyzer(cv_client, image, analysis_options)

    result = image_analyzer.analyze()

    print("Image analysis results:")
    # Print caption results to the console
    print("\nCaption:")
    if result.caption is not None:
        print(f"\t'{result.caption.text}', Confidence {result.caption.confidence:.3f}")

    # Prepare image for drawing
    image = Image.open(img)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'


    drawLinePolygon = True
    r = line.bounding_polygon
    bounding_polygon = ((r[0], r[1]),(r[2], r[3]),(r[4], r[5]),(r[6], r[7]))

    for word in line.words:
        r = word.bounding_polygon
        bounding_polygon = ((r[0], r[1]),(r[2], r[3]),(r[4], r[5]),(r[6], r[7]))
        print("  Word: '{}', Bounding Polygon: {}, Confidence: {}".format(word.content, bounding_polygon,word.confidence))

        # Draw word bounding polygon
        drawLinePolygon = False
        draw.polygon(bounding_polygon, outline=color, width=3)
    
    if drawLinePolygon:
        draw.polygon(bounding_polygon, outline=color, width=3)
    
    if is_url(img):
        outputfile = os.path.join('static', 'ocr', 'results_' + img.split('/')[-1].split('.')[0] + '.jpg')
    else:
        outputfile = os.path.join('static', 'ocr', 'results_' + img.split(os.sep)[-1].split('.')[0] + '.jpg')

    # Save image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    fig.savefig(outputfile)
    print('\n  Results saved in', outputfile)

    # Print text (OCR) analysis results to the console
    outputfile = os.path.join('static', 'ocr', 'results_' + img.split(os.sep)[-1].split('.')[0] + '.txt')
    print("\nRead:")
    if result.read is not None:
        with open(outputfile, 'a') as file:
            for line in result.read.blocks[0].lines:
                print(f"\tLine: '{line.text}', Bounding box {line.bounding_polygon}")

                file.write(f'\n' + line)

                for word in line.words:
                    print(f"\t\tWord: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.3f}")
    

if __name__ == "__main__":
    main()