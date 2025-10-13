import time
import random
import json
from datetime import datetime

# Simulated price feed
def get_current_price():
    return random.uniform(0.5, 2.0)

# Simulated volume feed
def get_current_volume():
    return random.randint(0, 100)

# Simulated entry price tracking
wallet_entry_prices = {
    "wallet1": 0.8,
    "wallet2": 1.2
}

rotation_index = 0
SOL_LOW_THRESHOLD = 5.0
TOKEN_EXPOSURE_LIMIT = 1000

def log_audit(wallet, action, amount, price):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "wallet": wallet,
        "action": action,
        "amount": amount,
        "price": price
    }
    try:
        with open("audit_log.json", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[LOG ERROR] {e}")

def execute_trade(wallet, amount, delay, count, dry_run=False, action="buy",
                  continuous=False, preview=False, spacing=0,
                  limit_price=0, min_price=0, max_price=999999,
                  profit_target=1.5, volume_threshold=20,
                  rotate_wallets=False):
    try:
        with open('wallets.json') as f:
            wallets_data = json.load(f)
    except Exception as e:
        return f"Error loading wallets: {e}"

    groups = wallets_data.get("groups", {})
    all_wallets = []
    for group in groups.values():
        all_wallets.extend(group["wallets"].keys())

    global rotation_index
    executions = 0

    while True:
        if not continuous and executions >= count:
            break

        if rotate_wallets:
            wallet = all_wallets[rotation_index % len(all_wallets)]
            rotation_index += 1

        # Get wallet info
        wallet_info = None
        for group in groups.values():
            if wallet in group["wallets"]:
                wallet_info = group["wallets"][wallet]
                break

        if not wallet_info:
            return f"Wallet '{wallet}' not found in groups."

        sol_balance = wallet_info.get("sol_balance", 0)
        token_balance = wallet_info.get("token_balance", 0)

        # Exposure Tracking
        if sol_balance < SOL_LOW_THRESHOLD:
            print(f"[WARNING] Low SOL balance for {wallet}: {sol_balance} SOL")
        if token_balance > TOKEN_EXPOSURE_LIMIT:
            print(f"[WARNING] Token overexposure for {wallet}: {token_balance} tokens")

        current_price = get_current_price()
        current_volume = get_current_volume()

        # Profit Taking
        entry_price = wallet_entry_prices.get(wallet, 1.0)
        if action == "sell" and current_price < entry_price * profit_target:
            print(f"[SKIPPED] Profit target not reached for {wallet} (entry: ${entry_price:.2f}, current: ${current_price:.2f})")
            time.sleep(delay)
            continue

        # Volume Stabilization
        if action == "buy" and current_volume < volume_threshold:
            print(f"[VOLUME STABILIZATION] Micro-buy triggered for {wallet} at volume {current_volume}")
        elif action == "buy" and current_volume > volume_threshold * 2:
            print(f"[THROTTLED] Skipping buy due to high volume {current_volume}")
            time.sleep(delay)
            continue

        if not (min_price <= current_price <= max_price):
            print(f"[SKIPPED] {action.upper()} due to price ${current_price:.2f} outside range [{min_price}–{max_price}]")
            time.sleep(delay)
            continue

        jitter = random.uniform(-0.5, 0.5)
        actual_delay = max(0, delay + jitter)

        if dry_run:
            print(f"[DRY RUN] {action.upper()} #{executions+1} from {wallet} with ${amount} at price ${limit_price or current_price:.2f}")
        else:
            print(f"{action.upper()} #{executions+1} from {wallet} with ${amount} at price ${limit_price or current_price:.2f}")
            log_audit(wallet, action, amount, limit_price or current_price)
            # TODO: Add actual execution logic via Web3 or Solana API

        executions += 1
        time.sleep(actual_delay + spacing)

    return f"Executed {executions} {action} operations from wallet '{wallet}'{' (dry-run)' if dry_run else ''}."

def rebalance_wallets():
    try:
        with open('wallets.json') as f:
            wallets_data = json.load(f)
    except Exception as e:
        return f"Error loading wallets: {e}"

    groups = wallets_data.get("groups", {})
    for group_name, group in groups.items():
        wallets = group["wallets"]
        total_sol = sum(w["sol_balance"] for w in wallets.values())
        target_per_wallet = total_sol / len(wallets)

        print(f"[REBALANCE] Group '{group_name}' total SOL: {total_sol:.2f}")
        for wallet_name, wallet_info in wallets.items():
            current = wallet_info["sol_balance"]
            delta = target_per_wallet - current
            print(f"  Wallet '{wallet_name}': current {current:.2f}, target {target_per_wallet:.2f}, delta {delta:+.2f}")
            # TODO: Add actual transfer logic here

    return "Rebalance simulation completed."
