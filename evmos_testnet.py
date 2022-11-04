import sys

from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

private_key1 = ''

if __name__ == '__main__':
    gwei_tevmos_factor = 0.000000000000000001
    rpc_url = 'https://eth.bd.evmos.dev:8545'
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    chain_id = web3.eth.chainId

    if web3.isConnected():
        print("Is connected to {} with ChainId {}".format(rpc_url, chain_id))
    else:
        sys.exit('Not connected to rpc')
#    print(web3.eth.get_block('latest'))

    account_1 = '0xa71fd3a84678bccb3b667A7780679Bf6dF1ccEC4'
    account_2 = '0xBaE9A7A2210F94511F5050348251d0d7113E2cE3'
    balance_from = web3.fromWei(web3.eth.get_balance(account_1), "ether")
    balance_to = web3.fromWei(web3.eth.get_balance(account_2), "ether")

    print("The balance of {} is: {} Tevmos".format(account_1, balance_from))
    print("The balance of {} is: {} Tevmos".format(account_2, balance_to))

    account_from = {
        "private_key": private_key1,
        "address": account_1,
    }
    address_to = account_2

    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
    gas = web3.eth.generate_gas_price()
    print("Attempting to send transaction from {} to {} with gas cost {} tEVMOS ({} ntevmos)".format(account_from["address"],                                                                                                     address_to,
                                                                                                     gas * gwei_tevmos_factor,
                                                                                                     gas))
    tx_create = web3.eth.account.sign_transaction(
        {
            "chainId": chain_id,
            "nonce": web3.eth.get_transaction_count(account_from["address"]),
            "gasPrice": gas,
            "gas": gas,
            "to": address_to,
            "value": web3.toWei("0.1", "ether"),
        },
        account_from["private_key"],
    )
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction hash {}".format(tx_hash.hex()))
    print("All data {}".format(tx_receipt))
    print("Transaction successful with hash: {}".format(tx_receipt.transactionHash.hex()))