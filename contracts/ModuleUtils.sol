// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "interfaces/chainlink/IAggregatorV3.sol";

import {ModuleConstants} from "./ModuleConstants.sol";

contract ModuleUtils is ModuleConstants {
    /* ========== ERRORS ========== */

    error StalePriceFeed(
        uint256 currentTime,
        uint256 updateTime,
        uint256 maxPeriod
    );

    function getCvxAmountInEth(uint256 _cvxAmount)
        internal
        view
        returns (uint256 ethAmount_)
    {
        uint256 cvxInEth = fetchPriceFromClFeed(
            CVX_ETH_FEED,
            CL_FEED_DAY_HEARTBEAT
        );
        // Divisor is 10^18 and uint256 max ~ 10^77 so this shouldn't overflow for normal amounts
        ethAmount_ = (_cvxAmount * cvxInEth) / FEED_DIVISOR_ETH;
    }

    function getWethAmountInUsdc(uint256 _wethAmount)
        internal
        view
        returns (uint256 usdcAmount_)
    {
        uint256 usdcInWeth = fetchPriceFromClFeed(
            USDC_ETH_FEED,
            CL_FEED_DAY_HEARTBEAT
        );
        // Divide by the rate from oracle since it is dai expressed in eth
        // FEED_USDC_MULTIPLIER has 1e6 precision
        usdcAmount_ = (_wethAmount * FEED_USDC_MULTIPLIER) / usdcInWeth;
    }

    function fetchPriceFromClFeed(IAggregatorV3 _feed, uint256 _maxStalePeriod)
        internal
        view
        returns (uint256 answerUint256_)
    {
        (, int256 answer, , uint256 updateTime, ) = _feed.latestRoundData();

        if (block.timestamp - updateTime > _maxStalePeriod) {
            revert StalePriceFeed(block.timestamp, updateTime, _maxStalePeriod);
        }

        answerUint256_ = uint256(answer);
    }
}
