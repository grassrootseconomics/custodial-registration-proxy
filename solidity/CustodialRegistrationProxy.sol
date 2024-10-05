// SPDX-License-Identifier:	AGPL-3.0-or-later
pragma solidity >=0.8.19;

interface IEthFaucet {
    function giveTo(address _recipient) external returns (uint256);
}

interface ICustodialAccountIndex {
    function add(address _account) external returns (bool);
}

contract CustodialRegistrationProxy {
    address public owner;
    address public systemAccount;

    IEthFaucet public EthFaucet;
    ICustodialAccountIndex public CustodialAccountIndex;

    event NewRegistration(address indexed subject);

    modifier ownerOnly() {
        require(msg.sender == owner);
        _;
    }

    modifier systemAccountOnly() {
        require(msg.sender == owner || msg.sender == systemAccount);
        _;
    }

    constructor(
        address _ethFaucetAddress,
        address _custodialAccountIndexAddress,
        address _systemAccount
    ) {
        owner = msg.sender;
        systemAccount = _systemAccount;

        EthFaucet = IEthFaucet(_ethFaucetAddress);
        CustodialAccountIndex = ICustodialAccountIndex(
            _custodialAccountIndexAddress
        );
    }

    function setNewOwner(address _newOwner) public ownerOnly {
        owner = _newOwner;
    }

    function setNewSystemAccount(address _newSystemAccount) public ownerOnly {
        systemAccount = _newSystemAccount;
    }

    function register(address _subject) public systemAccountOnly {
        CustodialAccountIndex.add(_subject);
        EthFaucet.giveTo(_subject);
        emit NewRegistration(_subject);
    }
}
