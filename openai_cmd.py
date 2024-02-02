import time, json, sys, cv2, os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    
    load_dotenv()
    # key = os.getenv('OPENAI_API_KEY')

    client = OpenAI()

    # Analyze image
    if len(sys.argv) > 0:
        prompt = None

        if len(sys.argv) > 2:
            prompt = sys.argv[2]
    
        # Chat
        if sys.argv[1] == 'chat':
            chat_completions(client)
        # Get embeddings
        elif sys.argv[1] == 'embed':
            chat_completions(client, prompt)
        # Generate image
        elif sys.argv[1] == 'image':
            chat_completions(client, prompt)


def chat_completions(client):
    system_prompt, user_prompt = None, None

    while system_prompt is None:
        test = input("\nEnter 'y' to use the test system guide:\n\tYou are a fanciful 15th century Italian poet\n")
        if test == 'y':
            system_prompt = 'You are a fanciful 15th century Italian poet'
        else:
            system_prompt = input('\nPlease supply some basic context for the system. Eg. What role to take on and how to act:\n')

    while user_prompt is None:
        test = input("\nEnter 'y' to use the test prompt:\n\tWrite a short poem about your love for a bread called lembas\n")
        if test == 'y':
            user_prompt = 'Write a short poem about your love for a bread called lembas'
        else:
            user_prompt = input('\nPlease supply some basic instructions for the system. Eg. What information to process:\n')
    
    filename = input('\nPlease supply a name for generated text:\n')

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])


    if filename:
        outputfile = os.path.join('static', 'output', 'generated_' + filename + '.txt')
        with open(outputfile, 'w') as file:
            file.write(completion.choices[0].message.content)
        if os.path.isfile(outputfile):
            print(f'File was saved at {outputfile}')
    else:
        print(completion.choices[0].message.content)


def embeddings(client, prompt = None):
    while prompt is None:
        prompt = input('\nPlease supply text to generate embeddings:')

    embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=prompt        
    )

    if filename:
        outputfile = os.path.join('static', 'output', 'embeddings_' + filename + '.txt')
        with open(outputfile, 'w') as file:
            file.write(embedding)
        if os.path.isfile(outputfile):
            print(f'File was saved at {outputfile}')
    else:
        print(embedding)



def images(client, prompt = None):
    while prompt is None:
        prompt = input('\nPlease supply a prompt to generate images:')
    
    filename = input(f'\nFor saving in  Please supply a file name for generated images:')

    response = client.images.generate(
        prompt=prompt,
        n=2,
        size="1024x1024"
    )

    if filename:
        outputfile = os.path.join('static', 'output', 'generated_' + filename + '.jpg')
        cv2.imwrite(outputfile, response)

        if os.path.isfile(outputfile):
            print(f'File was saved at {outputfile}')
    else:
        cv2.imshow(filename, response)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




if __name__ == "__main__":
    main()