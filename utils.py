import validators

is_url = lambda txt: validators.url(txt)

openai_image_sizes = ['256x256', '512x512', '1024x1024']