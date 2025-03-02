import os
import asyncio
from dotenv import load_dotenv
from py_near.account import Account
from py_near.dapps.core import NEAR
import requests

# Load environment variables from .env file
load_dotenv()

# Get the account_id and private_key from environment variables
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

acc = Account(ACCOUNT_ID, PRIVATE_KEY, rpc_addr="https://rpc.testnet.near.org")



async def send_tokens(address, amount):
    await acc.startup()
    tr = await acc.send_money(address, NEAR * amount)
    return tr.transaction.hash


async def get_balance(user=ACCOUNT_ID):

    return await acc.get_balance(user) / NEAR


async def get_test_tokens(recipient=ACCOUNT_ID, amount=1):
    print("Before sending the request")
    print("Here is addreesss and amount: ", recipient, amount)
    print("Here is addreesss and amount: ", type(recipient), type(amount))
    r = requests.post("https://near-faucet.io/api/faucet/tokens", json={
        "amount": str(int(amount) * NEAR),
        "contractId": "near_faucet",
        "receiverId": recipient
    })
    print("These is what got returned", r.json())
    return r.json()


async def main():
    await acc.startup()
    print(await get_balance())
    print(await get_balance("bob.testnet"))

    # print("sending money")
    # tr = await send_tokens("bob.testnet", 1)
    # print("transaction hash:", tr.transaction.hash)

    # print(await get_test_tokens("bob.testnet", 1))




if __name__ == "__main__":
    asyncio.run(main())

