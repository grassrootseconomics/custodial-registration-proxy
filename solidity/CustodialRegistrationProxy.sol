// SPDX-License-Identifier:	AGPL-3.0-or-later
pragma solidity >= 0.8.19;

interface IEthFaucet {
    function giveTo(address _recipient) external returns(uint256);
}

interface ICustodialAccountIndex {
    function add(address _account) external returns (bool);
}

interface IDemurrageTokenSingleNocap {
    function mintTo(address _beneficiary, uint256 _amount) external returns (bool);
}

contract CustodialRegistrationProxy {
    address public owner;
    address public systemAccount;
    uint256 public constant trainingVoucerGiftAmount = 5000000;

    IEthFaucet public EthFaucet;
    ICustodialAccountIndex public CustodialAccountIndex;
    IDemurrageTokenSingleNocap public TrainingVoucher;

    event NewRegistration(address indexed subject);

    modifier ownerOnly() {
        require(msg.sender == owner);
        _;
    }

    modifier systemAccountOnly() {
        require(msg.sender == owner || msg.sender == systemAccount);
        _;
    }

    constructor(address _ethFaucetAddress, address _custodialAccountIndexAddress, address _trainingVoucherAddress, address _systemAccount) {
        owner = msg.sender;
        systemAccount = _systemAccount;

        EthFaucet = IEthFaucet(_ethFaucetAddress);
        CustodialAccountIndex = ICustodialAccountIndex(_custodialAccountIndexAddress);
        TrainingVoucher = IDemurrageTokenSingleNocap(_trainingVoucherAddress);
    }

    function setNewOwner(address _newOwner)
        public
        ownerOnly 
    {
        owner = _newOwner;
    }

    function setNewSystemAccount(address _newSystemAccount)
        public
        ownerOnly 
    {
        systemAccount = _newSystemAccount;
    }

    function register(address _subject)
        public
        systemAccountOnly
    {
        CustodialAccountIndex.add(_subject);
        EthFaucet.giveTo(_subject);
        TrainingVoucher.mintTo(_subject, trainingVoucerGiftAmount);
        emit NewRegistration(_subject);
    }
}