from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time, json, os, sys

def main():
    from dotenv import load_dotenv
    global training_client
    global custom_vision_project

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
        if len(sys.argv) > 1:
        
            # Train
            if sys.argv[1] == 'train':
                folder = os.path.join('static', sys.argv[2]) if sys.argv[2] else os.path.join('static', 'train')
                
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

def train(vision_project, folder):
    print("Uploading images...")

    # Get the tags defined in the project
    tags = training_client.get_tags(vision_project.id)

    # Create a list of images with tagged regions
    tagged_images_with_regions = []

    # Get the images and tagged regions from the JSON file
    with open('tagged-images.json', 'r') as json_file:
        tagged_images = json.load(json_file)
        for image in tagged_images['files']:
            # Get the filename
            file = image['filename']
            # Get the tagged regions
            regions = []
            for tag in image['tags']:
                tag_name = tag['tag']
                # Look up the tag ID for this tag name
                tag_id = next(t for t in tags if t.name == tag_name).id
                # Add a region for this tag using the coordinates and dimensions in the JSON
                regions.append(Region(tag_id=tag_id, left=tag['left'],top=tag['top'],width=tag['width'],height=tag['height']))
            # Add the image and its regions to the list
            with open(os.path.join(folder,file), mode="rb") as image_data:
                tagged_images_with_regions.append(ImageFileCreateEntry(name=file, contents=image_data.read(), regions=regions))

    # Upload the list of images as a batch
    upload_result = training_client.create_images_from_files(vision_project.id, ImageFileCreateBatch(images=tagged_images_with_regions))
    # Check for failure
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
    else:
        print("Images uploaded.")

def test(model, project, img):
    try:

        # Load image and get height, width and channels
        cv2.imshow('Detecting objects in', image_file)
        cv2.waitKey(0)

        image = Image.open(image_file)
        h, w, ch = np.array(image).shape

        # Detect objects in the test image
        with open(image_file, mode="rb") as image_data:
            results = prediction_client.detect_image(project.id, model, image_data)

        # Create a figure for the results
        fig = plt.figure(figsize=(8, 8))
        plt.axis('off')

        # Display the image with boxes around each detected object
        draw = ImageDraw.Draw(image)
        lineWidth = int(w/100)
        color = 'magenta'
        for prediction in results.predictions:
            # Only show objects with a > 50% probability
            if (prediction.probability*100) > 50:
                # Box coordinates and dimensions are proportional - convert to absolutes
                left = prediction.bounding_box.left * w 
                top = prediction.bounding_box.top * h 
                height = prediction.bounding_box.height * h
                width =  prediction.bounding_box.width * w
                # Draw the box
                points = ((left,top), (left+width,top), (left+width,top+height), (left,top+height),(left,top))
                draw.line(points, fill=color, width=lineWidth)
                # Add the tag name and probability
                plt.annotate(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100),(left,top), backgroundcolor=color)
        plt.imshow(image)
        
        outputfile = os.path.join('static', 'output', 'catogorised_' + image_file.split(os.sep)[-1])
        fig.savefig(outputfile)
        print('Results saved in ', outputfile)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()