SOLC = solc

all: 
	$(SOLC) CustodialRegistrationProxy.sol --abi --evm-version istanbul | awk 'NR>3' > CustodialRegistrationProxy.json
	$(SOLC) CustodialRegistrationProxy.sol --bin --evm-version istanbul | awk 'NR>3' > CustodialRegistrationProxy.bin
	$(SOLC) CustodialRegistrationProxy.sol --metadata --evm-version istanbul | awk 'NR>3' > CustodialRegistrationProxy.metadata.json
	truncate -s -1 CustodialRegistrationProxy.bin

install: all
	cp -v *.json ../custodial_registration_proxy/data/
	cp -v *.bin ../custodial_registration_proxy/data/
	
.PHONY: install