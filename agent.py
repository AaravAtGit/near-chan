from nearai.agents.environment import Environment
from functions import send_tokens, get_balance, get_test_tokens
import asyncio
import json

def send_tokens_doc(address, amount):
    """
    Send NEAR tokens to another account.

    Args:
        address (str): The account ID of the recipient.
        amount (int): The number of NEAR tokens to send.

    Returns:
        str: The hash of the transaction.
    """
    return asyncio.run(send_tokens(address, amount))

def get_bal(user=None):
    """
    Retrieve the balance of the specified user account.

    Args:
        user (str): The address of the user whose balance is to be retrieved. 
                    Defaults to the user's address.

    Returns:
        float: The balance of the user account in NEAR tokens.
    """
    return asyncio.run(get_balance(user))


def get_testnet_tokens(recipient, amount):
    """
    Request test tokens from the NEAR faucet for a specified recipient.

    Args:
        recipient (str): The address of the recipient to receive the test tokens.
                         Defaults to the user's address.
        amount (int): The number of NEAR tokens to request from the faucet. Defaults to 1.

    Returns:
        dict: The JSON response from the faucet, which contains the transaction hash.
    """
    print("Here is addreesss and amount: ", recipient, amount)
    return asyncio.run(get_test_tokens(recipient, amount))



VECTOR_STORE_ID = "vs_cb8d5537f64d4f4aa6cbc95f"


def run(env: Environment):

    # RAG IMPLIMENTATION
    user_query = env.list_messages()[-1]["content"]
    vector_results = env.query_vector_store(VECTOR_STORE_ID, user_query)     # Query the Vector Store
    docs = [{"file": res["chunk_text"]} for res in vector_results[:6]]


    # Tools implimentation
    tool_registry = env.get_tool_registry(new=True)
    tool_registry.register_tool(send_tokens_doc)
    tool_registry.register_tool(get_bal)
    tool_registry.register_tool(get_testnet_tokens)

    prompt = [
        {
            "role": "user query",
            "content": user_query,
        },
        {
            "role": "documentation",
            "content": json.dumps(docs),
        },
        {
            "role": "system",
            "content": "You are near-chan an AI assistant for NEAR blockchain. give short and concise answers to user queries like a human. be friendly and helpful."
        }
    ]

    response = env.completions_and_run_tools([prompt] + env.list_messages(), tools=tool_registry.get_all_tool_definitions())



run(env)

