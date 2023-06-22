import openai
import json
#
from data import products


def get_completion(prompt, model="gpt-3.5-turbo") -> str:
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
        max_tokens=max_tokens,  # the maximum number of tokens the model can ouptut
    )
    return response.choices[0].message["content"]


def get_products_and_category(user_input) -> list:
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with \
    {delimiter} characters.
    Output a python list of objects, where each object has \
    the following format:
        'category': <one of Computers and Laptops, \
        Smartphones and Accessories, \
        Televisions and Home Theater Systems, \
        Gaming Consoles and Accessories, 
        Audio Equipment, Cameras and Camcorders>,
    OR
        'products': <a list of products that must \
        be found in the allowed products below>

    Where the categories and products must be found in \
    the customer service query.
    If a product is mentioned, it must be associated with \
    the correct category in the allowed products list below.
    If no products or categories are found, output an \
    empty list.

    Allowed products: 

    Computers and Laptops category:
    TechPro Ultrabook
    BlueWave Gaming Laptop
    PowerLite Convertible
    TechPro Desktop
    BlueWave Chromebook

    Smartphones and Accessories category:
    SmartX ProPhone
    MobiTech PowerCase
    SmartX MiniPhone
    MobiTech Wireless Charger
    SmartX EarBuds

    Televisions and Home Theater Systems category:
    CineView 4K TV
    SoundMax Home Theater
    CineView 8K TV
    SoundMax Soundbar
    CineView OLED TV

    Gaming Consoles and Accessories category:
    GameSphere X
    ProGamer Controller
    GameSphere Y
    ProGamer Racing Wheel
    GameSphere VR Headset

    Audio Equipment category:
    AudioPhonic Noise-Canceling Headphones
    WaveSound Bluetooth Speaker
    AudioPhonic True Wireless Earbuds
    WaveSound Soundbar
    AudioPhonic Turntable

    Cameras and Camcorders category:
    FotoSnap DSLR Camera
    ActionCam 4K
    FotoSnap Mirrorless Camera
    ZoomMaster Camcorder
    FotoSnap Instant Camera

    Only output the list of objects, with nothing else.
    """

    messages = [
        {'role': 'system',
         'content': system_message},
        {'role': 'user',
         'content': f"{delimiter}{user_input}{delimiter}"},
    ]

    return get_completion_from_messages(messages)


def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None


def get_product_by_name(name: str) -> str:
    return products.get(name, None)


def get_products_by_category(category: str) -> list:
    """
    This is a helper function to read the product for a given category.

    """
    return [product for product in products.values() if product["category"] == category]


def generate_output_string(data_list: json) -> str:
    """
    Input is the detail product list user is asking about in thr format json.
    Output is the string of the json input file

    """
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


def find_category_and_product_only(products_and_category):
    return generate_output_string(read_string_to_list(products_and_category))
