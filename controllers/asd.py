from guesslang import Guess


def get_text(text):

#     text = """public class AsciiValue {
#
#     public static void main(String[] args) {
#
#         System.out.println("The ASCII value of " + ch + " is: " + castAscii);
#     }
# } """
#
#     text = """
#     class Hello
#     {
#         static void Main()
#         {
#             Console.ReadKey();
#         }
#     }
# }"""
#
#     text = """Text messaging, or texting, is the act of composing and sending electronic messages, typically consisting of alphabetic and numeric characters, between two or ..."""

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

    c_file = "..\KeyWords\C.txt"
    java_file = "..\KeyWords\java.txt"
    cplusplus_file = "..\KeyWords\Cplusplus.txt"
    csharp_file = "..\KeyWords\Csharp.txt"
    javaScript_file = "..\KeyWords\JavaScript.txt"

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

    # name = Guess().language_name(text)
    # print(Guess.scores(text))
    # dict = Guess().language_name(text)
    # print(dict)

    # print(name)

    if value > 5:
        print("contains code. language is " + key)
    else:
        print("not contains code")