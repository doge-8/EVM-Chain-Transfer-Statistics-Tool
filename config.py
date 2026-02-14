# -*- coding: utf-8 -*-
"""
EVM Transfer Analyzer - Configuration File
EVM 链上交互额统计程序 - 配置文件

Edit this file and run start.sh to start the program.
修改此文件中的配置后运行 start.sh 即可
"""

# =============================================================================
# API Configuration / API 配置
# =============================================================================
# Etherscan API Key (Required / 必填)
# Get your API key at / 获取地址: https://etherscan.io/apidashboard
API_KEY = "Your Etherscan Api-Key"

# =============================================================================
# Query Configuration / 查询配置
# =============================================================================
# Wallet address to query / 要查询的钱包地址
WALLET_ADDRESS = "0x3A9837Efab387d96349Bfc89dd3f7eCE9262774A"

# Date range (Format: YYYY-MM-DD or YYYY-M-D)
# 查询日期范围 (格式: YYYY-MM-DD 或 YYYY-M-D)
START_DATE = "2026-01-15"
END_DATE = "2026-01-25"

# =============================================================================
# Token Contract Configuration / 代币合约配置
# =============================================================================
# Token contract addresses to query (can add or remove)
# 要查询的代币合约地址 (可以添加或删除)
CONTRACTS = {
    "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
    "aPolUSDT": "0x6ab707aca953edaefbc4fd23ba73294241490620"
}

# =============================================================================
# Advanced Configuration (Usually no need to modify)
# 高级配置 (一般不需要修改)
# =============================================================================
# Etherscan API V2 Endpoint / Etherscan API V2 端点
API_BASE_URL = "https://api.etherscan.io/v2/api"

# Polygon Mainnet Chain ID / Polygon 主网链 ID
CHAIN_ID = 137

# API request interval in seconds (to avoid rate limiting)
# API 请求间隔 (秒)，避免触发限速
API_RATE_LIMIT = 0.25
