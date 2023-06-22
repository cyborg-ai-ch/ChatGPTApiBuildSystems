import os
import openai
import sys

sys.path.append('../..')
from utils.functions import find_category_and_product_only, get_products_and_category, read_string_to_list
import panel as pn  # GUI

pn.extension()

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']

# Build an End-to-End System¶
# This puts together the chain of prompts that you saw throughout the course


user_message_1 = f"""
 tell me about the smartx pro phone and \
 the fotosnap camera, the dslr one. \
 Also tell me about your tvs """


# System of chained prompts for processing the user query
def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"

    # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    response = openai.Moderation.create(input=user_input)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request."

    if debug: print("Step 1: Input passed moderation check.")

    category_and_product_response = find_category_and_product_only(get_products_and_category(user_input))
    # Step 2: Extract the list of products
    # category_and_product_list = read_string_to_list(category_and_product_response)
    print(category_and_product_response)

    if debug: print("Step 2: Extracted list of products.")

