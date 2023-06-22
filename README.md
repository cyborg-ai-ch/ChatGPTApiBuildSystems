# DeepLearning.AI
## Building Systems with the ChatGPT API
 https://learn.deeplearning.ai/chatgpt-building-system/
 
Greate Course by:Isa Fulford, Andrew Ng, and Laurence Moroney 

Course structure:
L2: classification (to categories and subcategories)
L3: moderation api (stop prompt injection, test for validate non violated input)
{
  "flagged": false,
  "categories": {
    "sexual": false,
    "hate": false,
    "violence": false,
    "self-harm": false,
    "sexual/minors": false,
    "hate/threatening": false,
    "violence/graphic": false
  },
  "category_scores": {
    "sexual": 2.1934844e-05,
    "hate": 2.9083385e-06,
    "violence": 0.098616496,
    "self-harm": 2.9152812e-07,
    "sexual/minors": 2.4384206e-05,
    "hate/threatening": 2.8870053e-07,
    "violence/graphic": 5.059437e-05
  }
}

L4: Process Inputs: Chain of Thought Reasoning
It is given a product list. The assistant is advised to evaluate the
question step by step to find the answer after 4 steps of reasoning.

L5 Process Inputs: Chaining Prompts
In the first step get the main categories an products user is asking for
In the second step retrieve the category / product from the product list
In the third step give the assistance the list so the assistance can create a
user answer from.

L6: Check outputs
This is a important task! 
Use question, valid categories and assistance answer to the user to
validate the answer of the user question

Build an End-to-End System¶
This puts together the chain of prompts that you saw throughout the course