# Adapted from cicnet like libraries https://holbrook.no/src/
# Changes: Uses custodial registration proxy ABI and bytecode
# Original Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
# SPDX-License-Identifier:	AGPL-3.0-or-later
# File-version: 1
# Description: Python interface to abi and bin files for custodial proxy

# standard imports
import logging
import json
import os

# external imports
from chainlib.eth.tx import TxFactory
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.tx import (
    TxFactory,
    TxFormat,
    )
from chainlib.jsonrpc import JSONRPCRequest

logg = logging.getLogger().getChild(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')

class CustodialRegistrationProxySettings:
    def __init__(self):
        self.eth_faucet_address = None
        self.custodial_account_index_address = None
        self.training_voucher_address = None
        self.system_account_address = None

class CustodialRegistrationProxy(TxFactory):
    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if CustodialRegistrationProxy.__abi == None:
            f = open(os.path.join(datadir, 'CustodialRegistrationProxy.json'), 'r')
            CustodialRegistrationProxy.__abi = json.load(f)
            f.close()
        return CustodialRegistrationProxy.__abi


    @staticmethod
    def bytecode():
        if CustodialRegistrationProxy.__bytecode == None:
            f = open(os.path.join(datadir, 'CustodialRegistrationProxy.bin'))
            CustodialRegistrationProxy.__bytecode = f.read()
            f.close()
        return CustodialRegistrationProxy.__bytecode

    @staticmethod
    def gas(code=None):
        return 2000000

    def constructor(self, sender_address, settings):
        code = CustodialRegistrationProxy.bytecode()
        enc = ABIContractEncoder()
        enc.address(settings.eth_faucet_address)
        enc.address(settings.custodial_account_index_address)
        enc.address(settings.training_voucher_address)
        enc.address(settings.system_account_address)
        code += enc.get()
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.build(tx)
