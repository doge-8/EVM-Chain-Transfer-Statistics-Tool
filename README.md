# EVM Transfer Analyzer / EVM 链上交互额统计程序

Export token transfer records for a specified wallet address on EVM chains (Polygon).

导出指定钱包地址在 EVM 链 (Polygon) 上的代币交易记录。

## Features / 功能特点

- Bypass the browser's 5000 record limit with automatic pagination / 突破浏览器 5000 条限制，自动分页获取所有数据
- Support USDT and aPolUSDT tokens / 支持 USDT 和 aPolUSDT 两种代币
- Group records by transaction hash, clearly showing fund flow / 按交易哈希整合记录，清晰展示资金流向
- Automatic calculation of total inflow/outflow / 自动统计总流入/流出金额
- Export to CSV format for Excel analysis / 导出为 CSV 格式，方便用 Excel 分析
- Save raw API data to JSON for further analysis / 保存原始 API 数据到 JSON 文件便于进一步分析

## Prerequisites / 使用前准备

### 1. Get API Key / 获取 API Key

Visit https://etherscan.io/apidashboard to register and get a free API Key

访问 https://etherscan.io/apidashboard 注册并获取免费 API Key

### 2. Install Environment / 安装环境

```bash
chmod +x install.sh start.sh
./install.sh
```

## Usage / 使用方法

### 1. Edit Configuration File / 修改配置文件

Edit `config.py` / 编辑 `config.py`：

```python
# Enter your API Key / 填入你的 API Key
API_KEY = "YOUR_API_KEY"

# Enter wallet address to query / 填入要查询的钱包地址
WALLET_ADDRESS = "0x..."

# Set date range / 设置查询日期范围
START_DATE = "2026-01-01"
END_DATE = "2026-01-31"
```

### 2. Run Program / 运行程序

```bash
./start.sh
```

### 3. View Results / 查看结果

The program generates two files / 程序会生成两个文件：

#### CSV File (Processed Data / 整合后数据)

File name / 文件名: `evm_transfers_{wallet}_{date}.csv`

| Field / 字段 | Description / 说明 |
|------|------|
| Transaction Hash | Transaction hash / 交易哈希 |
| Blockno | Block number / 区块号 |
| UnixTimestamp | Unix timestamp / Unix 时间戳 |
| DateTime (UTC) | UTC time / UTC 时间 |
| Direction | Direction: IN / OUT / SWAP / 方向: 流入/流出/交换 |
| In_TokenValue | Tokens received / 收到的代币数量 |
| In_TokenSymbol | Token symbol received / 收到的代币符号 |
| Out_TokenValue | Tokens sent / 发出的代币数量 |
| Out_TokenSymbol | Token symbol sent / 发出的代币符号 |
| Counterparty | Counterparty address / 交易对手地址 |

The CSV ends with a summary / CSV 末尾会显示统计汇总：
- Total IN: Total inflow by token / 各代币总流入
- Total OUT: Total outflow by token / 各代币总流出

#### JSON File (Raw API Data / 原始 API 数据)

File name / 文件名: `evm_raw_data_{wallet}_{date}.json`

Contains the raw data returned by Etherscan API / 包含 Etherscan API 返回的原始数据：

| Field / 字段 | Description / 说明 |
|------|------|
| blockNumber | Block number / 区块号 |
| timeStamp | Unix timestamp / Unix 时间戳 |
| hash | Transaction hash / 交易哈希 |
| nonce | Transaction nonce / 交易序号 |
| blockHash | Block hash / 区块哈希 |
| from | Sender address / 发送方地址 |
| to | Receiver address / 接收方地址 |
| contractAddress | Token contract address / 代币合约地址 |
| value | Raw token amount (divide by 10^decimals) / 原始代币数量 (需除以 10^decimals) |
| tokenName | Token full name / 代币全称 |
| tokenSymbol | Token symbol / 代币符号 |
| tokenDecimal | Token decimals / 代币精度 |
| transactionIndex | Transaction index in block / 交易在区块中的索引 |
| gas | Gas limit / Gas 限制 |
| gasPrice | Gas price in wei / Gas 价格 (wei) |
| gasUsed | Actual gas used / 实际使用的 Gas |
| cumulativeGasUsed | Cumulative gas used / 累计 Gas 使用量 |
| methodId | Method selector / 方法选择器 |
| functionName | Called function name / 调用的函数名 |
| confirmations | Number of confirmations / 确认数 |

**Note / 注意**: The raw data only contains successful transactions. Failed transactions do not trigger ERC-20 Transfer events.

原始数据只包含成功的交易，失败的交易不会触发 ERC-20 Transfer 事件，因此不会出现在结果中。

## Custom Tokens / 自定义代币

To query other tokens, modify `CONTRACTS` in `config.py`:

如需查询其他代币，在 `config.py` 中修改 `CONTRACTS`：

```python
CONTRACTS = {
    "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
    "aPolUSDT": "0x6ab707aca953edaefbc4fd23ba73294241490620",
    "USDC": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"  # Add new token / 添加新代币
}
```

## Supported Chains / 支持的链

Change `CHAIN_ID` in `config.py` to query other EVM chains:

修改 `config.py` 中的 `CHAIN_ID` 可查询其他 EVM 链：

| Chain / 链 | Chain ID |
|------|----------|
| Ethereum | 1 |
| Polygon | 137 |
| BSC | 56 |
| Arbitrum | 42161 |
| Optimism | 10 |
| Base | 8453 |

## Notes / 注意事项

- Date cannot exceed today / 日期不能超过当前日期
- Free API has rate limits (5 calls/sec), the program handles this automatically / 免费 API 有速率限制，程序会自动处理
- Large data exports may take a while, please be patient / 大量数据导出可能需要较长时间，请耐心等待
- Only successful transactions are included / 只包含成功的交易

## File Structure / 文件说明

```
├── config.py                 # Configuration file / 配置文件
├── evm_transfer_analyzer.py  # Main program / 主程序
├── requirements.txt          # Python dependencies / Python 依赖
├── install.sh                # Environment setup script / 环境配置脚本
├── start.sh                  # Startup script / 启动脚本
└── README.md                 # Documentation / 说明文档
```

## Output Files / 输出文件

```
├── evm_transfers_*.csv       # Processed transfer data / 整合后的转账数据
└── evm_raw_data_*.json       # Raw API response data / 原始 API 响应数据
```
