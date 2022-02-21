// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase,Ownable {
    
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 internal keyHash;
    event RequestedRandomness(bytes32 requestId);

    constructor(address _priceFeedAddress, address _vrfCoordinator, address _link, uint256 _fee, bytes32 _keyhash) 
        public 
        VRFConsumerBase(_vrfCoordinator,_link) 
    {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyhash;
    }   

    function enter() public payable {
        // $50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "NOT ENOUGH FEE!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (,int price, , , ) = ethUsdPriceFeed.latestRoundData();

        uint256 adjustedPrice = uint256(price)*10**10; // 18 decimal
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED,
        'Cant start what is started'
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner{
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "YOU ARE NOT THERE YET");
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        // Reset all param
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}