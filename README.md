# DeepLearning.AI

## Building Systems with the ChatGPT API

https://learn.deeplearning.ai/chatgpt-building-system/

Greate Course by:Isa Fulford, Andrew Ng, and Laurence Moroney

Course structure:
L2: classification (to categories and subcategories)
L3: moderation api (stop prompt injection, test for validate non violated input)

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

L7: Evaluation
Build an End-to-End System¶
This puts together the chain of prompts that you saw throughout the course

L8: Evaluation 1:
Evaluation part I¶
Evaluate LLM responses when there is a single "right answer"

L9: Evaluation Part II
Evaluate LLM responses where there isn't a single "right answer.

Greate link:
OpenAI evals:
https://github.com/openai/evals/blob/main/evals/registry/modelgraded/fact.yaml
