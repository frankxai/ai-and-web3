// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "openzeppelin/token/ERC721/extensions/ERC721URIStorage.sol";

contract ERC721Simple is ERC721URIStorage {
    uint256 public nextTokenId;

    constructor() ERC721("AI+Web3 Demo", "AIW3") {}

    function safeMint(address to, string memory tokenURI) external {
        uint256 tokenId = nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }
}

