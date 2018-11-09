from guesslang import Guess

from controllers.Utils import Service, encode_image


# extract texts from a image
def detect_codes(image_file):
    print("Identifying code visibility in " + image_file)

    access_token = ""
    service = Service('vision', 'v1', access_token=access_token)

    code = False

    with open(image_file, 'rb') as image:
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
            text = response['responses'][0]['textAnnotations'][0]  # texts in the image

            print("language " + text['locale'])
            print("detected programming language is :" + detect_language(str(text['description'])))

            try:
                if get_text(str(text['description'])):
                    code = True
                else:
                    code = False
            except Exception as e:
                print(e)

        return code


def get_text(text):
    text_to_array = text \
        .replace(".", " ") \
        .replace("(", " ( ") \
        .replace(")", " ) ") \
        .replace("{", " { ") \
        .replace("}", " } ") \
        .replace(";", " ; ") \
        .replace("//", " // ") \
        .replace(":", " : ") \
        .split()

    c_file = "KeyWords/C.txt"
    java_file = "KeyWords/java.txt"
    cplusplus_file = "KeyWords/Cplusplus.txt"
    csharp_file = "KeyWords/Csharp.txt"
    javaScript_file = "KeyWords/JavaScript.txt"

    c_keywords = []
    java_keywords = []
    cplusplus_keywords = []
    csharp_keywords = []
    javaScript_keywords = []

    count_list = {}

    with open(c_file, "r") as f:
        c_keywords = f.read().split(',')

    with open(java_file, "r") as f:
        java_keywords = f.read().split(',')

    with open(cplusplus_file, "r") as f:
        cplusplus_keywords = f.read().split(',')

    with open(csharp_file, "r") as f:
        csharp_keywords = f.read().split(',')

    with open(javaScript_file, "r") as f:
        javaScript_keywords = f.read().split(',')

    csharp_count = len(set(text_to_array) & set(csharp_keywords))
    c_count = len(set(text_to_array) & set(c_keywords))
    java_count = len(set(text_to_array) & set(java_keywords))
    cplusplus_count = len(set(text_to_array) & set(cplusplus_keywords))
    javaScript_count = len(set(text_to_array) & set(javaScript_keywords))

    count_list["csharp"] = csharp_count
    count_list["c"] = c_count
    count_list["java"] = java_count
    count_list["cplusplus"] = cplusplus_count
    count_list["javaScript"] = javaScript_count

    print("csharp " + str(csharp_count))
    print("c " + str(c_count))
    print("java " + str(java_count))
    print("cplusplus " + str(cplusplus_count))
    print("javaScript " + str(javaScript_count))

    key, value = max(count_list.items(), key=lambda x: x[1])

    if value > 5:
        print("contains code. language is " + key)
        return True
    else:
        print("not contains code")
        return False


def detect_language(text):
    name = Guess().language_name(text)
    return name
