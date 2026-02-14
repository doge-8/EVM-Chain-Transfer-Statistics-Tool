# Polygon 链上数据导出工具

导出指定钱包地址在 Polygon 链上的 USDT 和 aPolUSDT 代币交易记录。

## 功能特点

- 突破浏览器 5000 条限制，自动分页获取所有数据
- 支持 USDT 和 aPolUSDT 两种代币
- 按交易哈希整合记录，清晰展示资金流向
- 自动统计总流入/流出金额
- 导出为 CSV 格式，方便用 Excel 分析

## 使用前准备

### 1. 获取 API Key

访问 https://etherscan.io/apidashboard 注册并获取免费 API Key

### 2. 安装环境

```bash
chmod +x install.sh start.sh
./install.sh
```

## 使用方法

### 1. 修改配置文件

编辑 `config.py`：

```python
# 填入你的 API Key
API_KEY = "你的API_KEY"

# 填入要查询的钱包地址
WALLET_ADDRESS = "0x..."

# 设置查询日期范围
START_DATE = "2026-01-01"
END_DATE = "2026-01-31"
```

### 2. 运行程序

```bash
./start.sh
```

### 3. 查看结果

程序会生成 CSV 文件，包含以下信息：

| 字段 | 说明 |
|------|------|
| Transaction Hash | 交易哈希 |
| Blockno | 区块号 |
| DateTime (UTC) | UTC 时间 |
| Direction | 方向: IN(流入) / OUT(流出) / SWAP(交换) |
| In_TokenValue | 收到的代币数量 |
| In_TokenSymbol | 收到的代币符号 |
| Out_TokenValue | 发出的代币数量 |
| Out_TokenSymbol | 发出的代币符号 |
| Counterparty | 交易对手地址 |

CSV 末尾会显示统计汇总：
- Total IN: 各代币总流入
- Total OUT: 各代币总流出

## 自定义代币

如需查询其他代币，在 `config.py` 中修改 `CONTRACTS`：

```python
CONTRACTS = {
    "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
    "aPolUSDT": "0x6ab707aca953edaefbc4fd23ba73294241490620",
    "USDC": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"  # 添加新代币
}
```

## 注意事项

- 日期不能超过当前日期
- 免费 API 有速率限制 (5 calls/sec)，程序会自动处理
- 大量数据导出可能需要较长时间，请耐心等待

## 文件说明

```
├── config.py           # 配置文件
├── polygon_exporter.py # 主程序
├── requirements.txt    # Python 依赖
├── install.sh          # 环境配置脚本
├── start.sh            # 启动脚本
└── README.md           # 说明文档
```
