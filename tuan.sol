pragma solidity ^0.5.1;
import './child.sol';

contract Parent {

  address payable owner;
  address public address_child;
  address[] public children;
  mapping(uint => Child) childList;
  uint public count; 
  uint public money;
  event LogCreatedChild(address child);
  constructor() public payable{
    owner  = msg.sender;
  }

  modifier onlyOnwer{
        require(msg.sender == owner);
        _;
    }
// get balance of contract parent
function getBalance() view public returns(uint256) {
    return owner.balance;  
}

// get address of contract parent
function getAdrress() view public returns(address) {
    return owner;
}

function getChildAddress() view public returns (address){
  return address_child;
}

function getCount() view public returns (uint){
  return count;
}

// create sub addresss
function createChild() public returns(address) {
    count++;
    Child child = new Child(owner);
    children.push(address(child));
    emit LogCreatedChild(address(child));
    address_child = address(child); 
    childList[count] = child;   // you can use the getter to fetch child addresses
    
    return address_child;

  }