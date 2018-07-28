from controllers.Utils import Service, encode_image


def detect_ide(photo_file):
    access_token = "AIzaSyCLCVwYnNNbOFUPByzQAJ143FNgLCxy8MY"
    service = Service('vision', 'v1', access_token=access_token)
    ide = "no"
    with open(photo_file, 'rb') as image:
        base64_image = encode_image(image)
        body = {
            'requests': [{
                'image': {
                    'content': base64_image,
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1,
                }]
            }]
        }

        response = service.execute(body=body)

        if response['responses'] and 'textAnnotations' in response['responses'][0]:
            text = response['responses'][0]['textAnnotations'][0]

            if "Eclipse" in text:
                ide = "Eclipse"
            elif "Intellij" in text:
                ide = "Intellij"
            elif "NetBeans" in text:
                ide = "NetBeans"
            elif "Android Studio" in text:
                ide = "Android Studio"
            elif "Studio Code" in text:
                ide = "Studio Code"
            else:
                ide = "no"

    return ide
