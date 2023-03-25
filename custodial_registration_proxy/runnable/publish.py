"""Deploys custodial registration proxy

.. adapted from cicnet like libraries https://holbrook.no/src/
.. changelog: use custodial proxy contract

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import logging

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt
from chainlib.eth.cli.arg import (
        Arg,
        ArgFlag,
        process_args,
        )
from chainlib.eth.cli.config import (
        Config,
        process_config,
        )
from chainlib.eth.cli.log import process_log
from chainlib.eth.settings import process_settings
from chainlib.settings import ChainSettings

# local imports
from custodial_registration_proxy import (
    CustodialRegistrationProxy,
    CustodialRegistrationProxySettings,
)

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

def process_config_local(config, arg, args, flags):
    config.add(args.proxy_eth_faucet_address, 'PROXY_ETH_FAUCET_ADDRESS')
    config.add(args.proxy_custodial_account_index_address, 'PROXY_CUSTODIAL_ACCOUNT_INDEX_ADDRESS')
    config.add(args.proxy_training_voucher_address, 'PROXY_TRAINING_VOUCHER_ADDRESS')
    config.add(args.proxy_system_account_address, 'PROXY_SYSTEM_ACCOUNT_ADDRESS')
    return config

arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_WRITE 

argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
argparser.add_argument('--eth-faucet-address', dest='proxy_eth_faucet_address', type=str, help='Faucet address')
argparser.add_argument('--account-index-address', dest='proxy_custodial_account_index_address', type=str, help='Account index address')
argparser.add_argument('--training-voucher-address', dest='proxy_training_voucher_address', type=str, help='Training voucher address')
argparser.add_argument('--system-account-address', dest='proxy_system_account_address', type=str, help='System account address')
args = argparser.parse_args()

logg = process_log(args, logg)

config = Config()
config = process_config(config, arg, args, flags)
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))

settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))


def main():
    conn = settings.get('CONN')

    c = CustodialRegistrationProxy(
            settings.get('CHAIN_SPEC'),
            signer=settings.get('SIGNER'),
            gas_oracle=settings.get('FEE_ORACLE'),
            nonce_oracle=settings.get('NONCE_ORACLE'),
            )

    c_args = CustodialRegistrationProxySettings()
    c_args.eth_faucet_address = config.get('PROXY_ETH_FAUCET_ADDRESS')
    c_args.custodial_account_index_address = config.get('PROXY_CUSTODIAL_ACCOUNT_INDEX_ADDRESS')
    c_args.training_voucher_address = config.get('PROXY_TRAINING_VOUCHER_ADDRESS')
    c_args.system_account_address = config.get('PROXY_SYSTEM_ACCOUNT_ADDRESS')

    (tx_hash_hex, o) = c.constructor(
            settings.get('SENDER_ADDRESS'),
            c_args,
            )

    if settings.get('RPC_SEND'):
        conn.do(o)
        if config.true('_WAIT'):
            r = conn.wait(tx_hash_hex)
            if r['status'] == 0:
                sys.stderr.write('EVM revert while deploying contract. Wish I had more to tell you')
                sys.exit(1)
            # TODO: pass through translator for keys (evm tester uses underscore instead of camelcase)
            address = r['contractAddress']

            print(address)
        else:
            print(tx_hash_hex)
    else:
        print(o)


if __name__ == '__main__':
    main()
