pragma solidity ^0.5.0;
// đây là smart chơi lô đề dùng cho môn an toàn giao dịch điện tử
library StringUtils {
    /// @dev Does a byte-by-byte lexicographical comparison of two strings.
    /// @return a negative number if _a is smaller, zero if they are equal
    /// and a positive numbe if _b is smaller.
    function compare(string memory _a, string memory _b) public returns (int) {
        bytes memory a = bytes(_a);
        bytes memory b = bytes(_b);
        uint minLength = a.length;
        if (b.length < minLength) minLength = b.length;
        //@todo unroll the loop into increments of 32 and do full 32 byte comparisons
        for (uint i = 0; i < minLength; i ++)
            if (a[i] < b[i])
                return -1;
            else if (a[i] > b[i])
                return 1;
        if (a.length < b.length)
            return -1;
        else if (a.length > b.length)
            return 1;
        else
            return 0;
    }
    /// @dev Compares two strings and returns true iff they are equal.
    function equal(string memory _a, string memory _b) public returns (bool) {
        return compare(_a, _b) == 0;
    }
    /// @dev Finds the index of the first occurrence of _needle in _haystack
    function indexOf(string memory _haystack, string memory _needle) public returns (int)
    {
    	bytes memory h = bytes(_haystack);
    	bytes memory n = bytes(_needle);
    	if(h.length < 1 || n.length < 1 || (n.length > h.length)) 
    		return -1;
    	else if(h.length > (2**128 -1)) // since we have to be able to return -1 (if the char isn't found or input error), this function must return an "int" type with a max length of (2^128 - 1)
    		return -1;									
    	else
    	{
    		uint subindex = 0;
    		for (uint i = 0; i < h.length; i ++)
    		{
    			if (h[i] == n[0]) // found the first char of b
    			{
    				subindex = 1;
    				while(subindex < n.length && (i + subindex) < h.length && h[i + subindex] == n[subindex]) // search until the chars don't match or until we reach the end of a or b
    				{
    					subindex++;
    				}	
    				if(subindex == n.length)
    					return int(i);
    			}
    		}
    		return -1;
    	}	
    }
}

contract IT4320{
    event history_game(uint number,string time);
    uint public number_win;
    address payable owner;
    
    struct tx_hash{
        string  transaction; 
    }
    
    mapping (uint => tx_hash) public tx_hashs;
    
    uint tx_hash_count = 0;
    
    modifier checkWin(uint _number) {
        require(number_win == _number);
        _;
    }
    
    modifier onlyAdmin() {
        require(msg.sender == owner);
        _;
    }
    constructor() public payable{
        owner = msg.sender;
    }
    function() payable external {
        
    }   
    function push_tx_hash(string memory _tx) public {
        tx_hash_count++;
        tx_hashs[tx_hash_count].transaction = _tx;
    }
    
    function check_tx_hash(string memory _tx) public returns(uint){
        for(uint i=0; i <= tx_hash_count ; i++){
            if(StringUtils.equal(tx_hashs[i].transaction,_tx)){
                return 1;
            }
        }
        return 2;
    }
    
    
    
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
    
    function set_number_win(uint _number) public onlyAdmin() {
        number_win = _number;
    }
    
    function withDraw(address payable _to, uint _amount)  public  onlyAdmin()   {
       address(_to).transfer(_amount);
    }
    
    function submit(uint _number,address payable _to, uint _amount, string memory _tx)  public  checkWin(_number)   {
       require(check_tx_hash(_tx) == 2);
       address(_to).transfer(_amount);
       push_tx_hash(_tx);
    }
}
    