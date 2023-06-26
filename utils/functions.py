import json

import openai

from data.products_list import products, categeroy_string


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

    {categeroy_string}
    
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


def find_category_and_product_only(user_inout):
    return get_products_and_category(user_inout)


def answer_user_msg(user_msg, product_info):
    delimiter = "```"
    # Step 4: Answer the user question
    system_message = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_msg}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_info}"}
    ]

    return get_completion_from_messages(messages)
