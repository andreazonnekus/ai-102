import asyncio, io, os, sys, time, uuid, requests
import azure.ai.vision as sdk
from dotenv import load_dotenv
from io import BytesIO
from urllib.parse import urlparse
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

load_dotenv()

class FacialDetection:
    def main(self):
        global vision_client

        try:
            # Base url for the Verify and Facelist/Large Facelist operations
            url = os.environ.get("VISION_URL")
            if not url:
                raise Exception("A key should be provided to invoke the endpoint as either the VISION_URL or as an argument to the cmd ")

            key = os.environ.get("VISION_KEY")
            if not key:
                raise Exception("A key should be provided to invoke the endpoint as either the VISION_KEY or as an argument to the cmd ")
            
            # Create an authenticated FaceClient
            vision_client = sdk.VisionServiceOptions(url, CognitiveServicesCredentials(key))

            # Get image
            if len(sys.argv) > 1:
            
                # Analyze faces
                if sys.argv[1] == 'detect':
                    print("\nThe following images are available:")
                    os.listdir(os.path.join('static', 'faces'))
                    img = input('Enter a image to process:')

                    while os.isfile( os.path.join('static', 'faces', img + '.jpg')) == False:
                        img = input('Enter a image to process:')

                    image_file = os.path.join('static', 'faces', img + '.jpg')
                    detect_faces(image_file)
                elif sys.argv[1] == 'group':
                    group_identify()
            else:
                image_file = os.path.join('static', 'faces', 'people.jpg')
                detect_faces(image_file)

        except Exception as ex:
            print(ex)

    def detect_faces(image_file):
        print('Detecting faces in', image_file)

        # Specify features to be retrieved (PEOPLE)
        analysis_options = sdk.ImageAnalysisOptions()
            
        features = analysis_options.features = (
            sdk.ImageAnalysisFeature.PEOPLE
        )

        # Get image analysis
        image = sdk.VisionSource(image_file)
            
        image_analyzer = sdk.ImageAnalyzer(vision_client, image, analysis_options)
            
        result = image_analyzer.analyze()
            
        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            # Get people in the image
            if result.people is not None:
                print("\nPeople in image:")
                
                # Prepare image for drawing
                image = Image.open(image_file)
                fig = plt.figure(figsize=(image.width/100, image.height/100))
                plt.axis('off')
                draw = ImageDraw.Draw(image)
                color = 'cyan'
                
                for detected_people in result.people:
                    # Draw object bounding box if confidence > 50%
                    if detected_people.confidence > 0.5:
                        # Draw object bounding box
                        r = detected_people.bounding_box
                        bounding_box = ((r.x, r.y), (r.x + r.w, r.y + r.h))
                        draw.rectangle(bounding_box, outline=color, width=3)
                    
                        # Return the confidence of the person detected
                        print(" {} (confidence: {:.2f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))
                            
                # Save annotated image
                plt.imshow(image)
                plt.tight_layout(pad=0)
                
                outputfile = os.path.join('static', 'output', 'detected_' + image_file.split(os.sep)[-1])
                fig.savefig(outputfile)
                print('\tResults saved in', outputfile)
            
        else:
            error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
            print("\nAnalysis failed.")
            print("\tError reason: {}".format(error_details.reason))
            print("\tError code: {}".format(error_details.error_code))
            print("\tError message: {}".format(error_details.message))    


    def group_identify():
        # Get faces
        IMAGE_BASE_URL = 'https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/'

        # Used in the Person Group Operations and Delete Person Group examples.
        # You can call list_person_groups to print a list of preexisting PersonGroups.
        # SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
        PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

        # Used for the Delete Person Group example.
        TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

        '''
        Create the PersonGroup
        '''
        # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
        print('Person group:', PERSON_GROUP_ID)
        vision_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID, recognition_model='recognition_04')

        # Define woman friend
        woman = vision_client.person_group_person.create(PERSON_GROUP_ID, name="Woman")
        # Define man friend
        man = vision_client.person_group_person.create(PERSON_GROUP_ID, name="Man")
        # Define child friend
        child = vision_client.person_group_person.create(PERSON_GROUP_ID, name="Child")

        '''
        Detect faces and register them to each person
        '''
        # Find all jpeg images of friends in working directory (TBD pull from web instead)
        woman_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom2.jpg"]
        man_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Dad1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Dad2.jpg"]
        child_images = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Son1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Son2.jpg"]

        # Add to woman person
        for image in woman_images:
            # Check if the image is of sufficent quality for recognition.
            sufficientQuality = True
            detected_faces = vision_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
            for face in detected_faces:
                if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
                    sufficientQuality = False
                    break
                vision_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, woman.person_id, image)
                print("face {} added to person {}".format(face.face_id, woman.person_id))

            if not sufficientQuality: continue

        # Add to man person
        for image in man_images:
            # Check if the image is of sufficent quality for recognition.
            sufficientQuality = True
            detected_faces = vision_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
            for face in detected_faces:
                if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
                    sufficientQuality = False
                    break
                vision_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, man.person_id, image)
                print("face {} added to person {}".format(face.face_id, man.person_id))

            if not sufficientQuality: continue

        # Add to child person
        for image in child_images:
            # Check if the image is of sufficent quality for recognition.
            sufficientQuality = True
            detected_faces = vision_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
            for face in detected_faces:
                if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
                    sufficientQuality = False
                    print("{} has insufficient quality".format(face))
                    break
                vision_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, child.person_id, image)
                print("face {} added to person {}".format(face.face_id, child.person_id))
            if not sufficientQuality: continue


        '''
        Train PersonGroup
        '''
        # Train the person group
        print("pg resource is {}".format(PERSON_GROUP_ID))
        rawresponse = vision_client.person_group.train(PERSON_GROUP_ID, raw= True)
        print(rawresponse)

        while (True):
            training_status = vision_client.person_group.get_training_status(PERSON_GROUP_ID)
            print("Training status: {}.".format(training_status.status))
            print()
            if (training_status.status is TrainingStatusType.succeeded):
                break
            elif (training_status.status is TrainingStatusType.failed):
                vision_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
                sys.exit('Training the person group has failed.')
            time.sleep(5)

        '''
        Identify a face against a defined PersonGroup
        '''
        # Group image for testing against
        test_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/identification1.jpg"

        print('Pausing for 10 seconds to avoid triggering rate limit on free account...')
        time.sleep (10)

        # Detect faces
        face_ids = []
        # We use detection model 3 to get better performance, recognition model 4 to support quality for recognition attribute.
        faces = vision_client.face.detect_with_url(test_image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
        for face in faces:
            # Only take the face if it is of sufficient quality.
            if face.face_attributes.quality_for_recognition == QualityForRecognition.high or face.face_attributes.quality_for_recognition == QualityForRecognition.medium:
                face_ids.append(face.face_id)

        # Identify faces
        results = vision_client.face.identify(face_ids, PERSON_GROUP_ID)
        print('Identifying faces in image')
        if not results:
            print('No person identified in the person group')
        for identifiedFace in results:
            if len(identifiedFace.candidates) > 0:
                print('Person is identified for face ID {} in image, with a confidence of {}.'.format(identifiedFace.face_id, identifiedFace.candidates[0].confidence)) # Get topmost confidence score

                # Verify faces
                verify_result = vision_client.face.verify_face_to_person(identifiedFace.face_id, identifiedFace.candidates[0].person_id, PERSON_GROUP_ID)
                print('verification result: {}. confidence: {}'.format(verify_result.is_identical, verify_result.confidence))
            else:
                print('No person identified for face ID {} in image.'.format(identifiedFace.face_id))

