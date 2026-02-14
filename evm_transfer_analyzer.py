#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polygon 链上数据导出工具
导出指定钱包地址的 USDT 和 aPolUSDT 代币交易记录
配置请修改 config.py 文件
"""

import requests
import csv
import time
import json
from datetime import datetime

# 从配置文件导入
from config import (
    API_KEY, WALLET_ADDRESS, START_DATE, END_DATE,
    CONTRACTS, API_BASE_URL, CHAIN_ID, API_RATE_LIMIT
)

def parse_date(date_str):
    """解析多种格式的日期字符串"""
    # 尝试处理不带前导零的日期，如 2026-2-15
    parts = date_str.replace('/', '-').split('-')
    if len(parts) == 3:
        if len(parts[0]) == 4:
            try:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                return datetime(year, month, day)
            except ValueError:
                pass

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"无法解析日期: {date_str}")

def get_block_by_timestamp(timestamp, closest="before", api_key=""):
    """根据时间戳获取区块号"""
    params = {
        "chainid": CHAIN_ID,
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": closest,
        "apikey": api_key
    }

    response = requests.get(API_BASE_URL, params=params)
    data = response.json()

    if data["status"] == "1":
        return int(data["result"])
    else:
        error_msg = data.get('message', 'Unknown error')
        result = data.get('result', '')
        raise Exception(f"获取区块号失败: {error_msg} - {result}")

def get_token_transfers(address, contract_address, start_block, end_block, api_key=""):
    """获取代币转账记录"""
    all_transfers = []
    page = 1
    offset = 10000

    while True:
        params = {
            "chainid": CHAIN_ID,
            "module": "account",
            "action": "tokentx",
            "contractaddress": contract_address,
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": "asc",
            "apikey": api_key
        }

        time.sleep(API_RATE_LIMIT)
        response = requests.get(API_BASE_URL, params=params)
        data = response.json()

        if data["status"] == "1" and data["result"]:
            transfers = data["result"]
            all_transfers.extend(transfers)
            print(f"  已获取 {len(all_transfers)} 条记录...")

            if len(transfers) < offset:
                break
            page += 1
        elif data["status"] == "0" and data["message"] == "No transactions found":
            break
        else:
            if "Max rate limit reached" in str(data.get("result", "")):
                print("  达到 API 速率限制，等待后重试...")
                time.sleep(5)
                continue
            break

    return all_transfers

def format_token_value(value, decimals):
    """格式化代币数量"""
    try:
        decimals = int(decimals)
        value = int(value)
        return round(value / (10 ** decimals), 6)
    except:
        return value

def group_transfers_by_hash(transfers, wallet_address):
    """按交易哈希分组并整合转账记录"""
    grouped = {}

    for tx in transfers:
        tx_hash = tx.get("hash", "")
        if tx_hash not in grouped:
            grouped[tx_hash] = {
                "hash": tx_hash,
                "blockNumber": tx.get("blockNumber", ""),
                "timeStamp": tx.get("timeStamp", ""),
                "in_transfers": [],   # 流入
                "out_transfers": [],  # 流出
            }

        from_addr = tx.get("from", "").lower()
        to_addr = tx.get("to", "").lower()
        token_value = format_token_value(tx.get("value", "0"), tx.get("tokenDecimal", "6"))
        token_symbol = tx.get("tokenSymbol", "")

        transfer_info = {
            "value": token_value,
            "symbol": token_symbol,
            "from": from_addr,
            "to": to_addr
        }

        if to_addr == wallet_address:
            # 流入
            grouped[tx_hash]["in_transfers"].append(transfer_info)
        elif from_addr == wallet_address:
            # 流出
            grouped[tx_hash]["out_transfers"].append(transfer_info)

    return grouped

def export_to_csv(transfers, wallet_address, start_date, end_date):
    """导出数据到 CSV 文件"""
    if not transfers:
        print("\n没有找到符合条件的交易记录")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evm_transfers_{wallet_address[:10]}_{start_date}_{end_date}_{timestamp}.csv"

    # 按哈希分组整合
    grouped = group_transfers_by_hash(transfers, wallet_address)

    # 按时间戳排序
    sorted_txs = sorted(grouped.values(), key=lambda x: int(x.get("timeStamp", "0")))

    headers = [
        "Transaction Hash",
        "Blockno",
        "UnixTimestamp",
        "DateTime (UTC)",
        "Direction",
        "In_TokenValue",
        "In_TokenSymbol",
        "Out_TokenValue",
        "Out_TokenSymbol",
        "Counterparty"
    ]

    # 统计各代币的总流入和总流出
    total_in = {}   # {symbol: total_value}
    total_out = {}  # {symbol: total_value}

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for tx in sorted_txs:
            unix_ts = tx.get("timeStamp", "")
            try:
                dt_utc = datetime.utcfromtimestamp(int(unix_ts)).strftime("%Y-%m-%d %H:%M:%S")
            except:
                dt_utc = ""

            in_transfers = tx["in_transfers"]
            out_transfers = tx["out_transfers"]

            # 判断方向
            if in_transfers and out_transfers:
                direction = "SWAP"
            elif in_transfers:
                direction = "IN"
            else:
                direction = "OUT"

            # 合并流入金额和代币，并累计统计
            in_values = []
            in_symbols = []
            for t in in_transfers:
                in_values.append(str(t["value"]))
                symbol = t["symbol"]
                if symbol not in in_symbols:
                    in_symbols.append(symbol)
                # 累计统计
                total_in[symbol] = total_in.get(symbol, 0) + t["value"]

            # 合并流出金额和代币，并累计统计
            out_values = []
            out_symbols = []
            for t in out_transfers:
                out_values.append(str(t["value"]))
                symbol = t["symbol"]
                if symbol not in out_symbols:
                    out_symbols.append(symbol)
                # 累计统计
                total_out[symbol] = total_out.get(symbol, 0) + t["value"]

            # 找出交易对手（排除自己的地址）
            counterparties = set()
            for t in in_transfers:
                if t["from"] != wallet_address:
                    counterparties.add(t["from"])
            for t in out_transfers:
                if t["to"] != wallet_address:
                    counterparties.add(t["to"])

            row = [
                tx["hash"],
                tx["blockNumber"],
                unix_ts,
                dt_utc,
                direction,
                " + ".join(in_values) if in_values else "",
                " / ".join(in_symbols) if in_symbols else "",
                " + ".join(out_values) if out_values else "",
                " / ".join(out_symbols) if out_symbols else "",
                " | ".join(counterparties) if counterparties else ""
            ]
            writer.writerow(row)

        # 写入空行和统计汇总
        writer.writerow([])
        writer.writerow(["=== SUMMARY ==="])
        writer.writerow([])

        # 总流入统计
        writer.writerow(["Total IN:"])
        for symbol, value in total_in.items():
            writer.writerow(["", "", "", "", "", round(value, 6), symbol, "", "", ""])

        writer.writerow([])

        # 总流出统计
        writer.writerow(["Total OUT:"])
        for symbol, value in total_out.items():
            writer.writerow(["", "", "", "", "", "", "", round(value, 6), symbol, ""])

    return filename, len(sorted_txs)

def main():
    print("=" * 60)
    print("Polygon 链上数据导出工具")
    print("支持导出 USDT 和 aPolUSDT 代币交易记录")
    print("=" * 60)

    # 从配置文件读取
    api_key = API_KEY
    wallet_address = WALLET_ADDRESS.lower()
    start_date_str = START_DATE
    end_date_str = END_DATE

    # 验证钱包地址
    if not wallet_address.startswith("0x") or len(wallet_address) != 42:
        print("错误: config.py 中的钱包地址格式无效")
        return

    # 解析日期
    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        end_date = end_date.replace(hour=23, minute=59, second=59)
    except ValueError as e:
        print(f"错误: {e}")
        return

    # 标准化日期字符串
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # 显示配置信息
    print("\n当前配置 (可在 config.py 中修改):")
    print(f"  钱包地址: {wallet_address}")
    print(f"  开始日期: {start_date_str}")
    print(f"  结束日期: {end_date_str}")
    print(f"  目标代币: {', '.join(CONTRACTS.keys())}")
    print("=" * 60)

    confirm = input("\n确认开始查询? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消查询")
        return

    # 转换日期为时间戳
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # 获取区块范围
    print("\n正在获取区块范围...")
    try:
        start_block = get_block_by_timestamp(start_timestamp, "after", api_key)
        time.sleep(API_RATE_LIMIT)
        end_block = get_block_by_timestamp(end_timestamp, "before", api_key)
        print(f"  区块范围: {start_block} - {end_block}")
    except Exception as e:
        print(f"错误: {e}")
        return

    # 获取所有代币转账记录
    all_transfers = []

    for token_name, contract_address in CONTRACTS.items():
        print(f"\n正在获取 {token_name} 交易记录...")
        transfers = get_token_transfers(
            wallet_address,
            contract_address,
            start_block,
            end_block,
            api_key
        )
        print(f"  {token_name}: 获取到 {len(transfers)} 条记录")
        all_transfers.extend(transfers)

    # 按时间戳排序
    all_transfers.sort(key=lambda x: int(x.get("timeStamp", "0")))

    print(f"\n总共获取到 {len(all_transfers)} 条交易记录")

    # 保存原始数据到 JSON 文件
    raw_filename = f"evm_raw_data_{wallet_address[:10]}_{start_date_str}_{end_date_str}.json"
    with open(raw_filename, 'w', encoding='utf-8') as f:
        json.dump(all_transfers, f, indent=2, ensure_ascii=False)
    print(f"原始数据已保存到: {raw_filename}")

    # 导出 CSV
    print("\n正在导出数据到 CSV...")
    result = export_to_csv(all_transfers, wallet_address, start_date_str, end_date_str)

    if result:
        filename, tx_count = result
        print(f"\n导出成功!")
        print(f"文件名: {filename}")
        print(f"原始记录: {len(all_transfers)} 条")
        print(f"整合后交易: {tx_count} 笔")

if __name__ == "__main__":
    main()
