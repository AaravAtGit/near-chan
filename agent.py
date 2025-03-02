from nearai.agents.environment import Environment
from functions import send_tokens, get_balance, get_test_tokens
import asyncio


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





def run(env: Environment):
    tool_registry = env.get_tool_registry(new=True)
    # Define tools
    tool_registry.register_tool(send_tokens_doc)
    tool_registry.register_tool(get_bal)
    tool_registry.register_tool(get_testnet_tokens)

    

    prompt = {"role": "system", "content": "You are near-chan an AI assistant for NEAR blockchain. give short and concise answers to user queries like a human. be friendly and helpful."}
    response = env.completions_and_run_tools([prompt] + env.list_messages(), tools=tool_registry.get_all_tool_definitions())



run(env)

