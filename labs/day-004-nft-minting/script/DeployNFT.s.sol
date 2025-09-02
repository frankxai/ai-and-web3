// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import {ERC721Simple} from "src/ERC721Simple.sol";

contract DeployNFT is Script {
    function run() external {
        vm.startBroadcast();
        new ERC721Simple();
        vm.stopBroadcast();
    }
}

