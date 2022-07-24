import re


def validate_base64_image(string):
    return re.match(r'data:image\/([a-zA-Z]*);base64,([^\"]*)', string)
