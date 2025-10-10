import time
import random
import json

def execute_trade(wallet, amount, delay, count, dry_run=False):
    try:
        with open('wallets.json') as f:
            wallets = json.load(f)
    except Exception as e:
        return f"Error loading wallets: {e}"

    if wallet not in wallets:
        return f"Wallet '{wallet}' not found."

    for i in range(count):
        jitter = random.uniform(-0.5, 0.5)
        actual_delay = max(0, delay + jitter)

        if dry_run:
            print(f"[DRY RUN] Trade #{i+1} from {wallet} with ${amount}")
        else:
            print(f"Executing trade #{i+1} from {wallet} with ${amount}")
            # هنا ممكن تضيف تنفيذ فعلي باستخدام Web3 أو Solana API

        time.sleep(actual_delay)

    return f"Executed {count} trades from wallet '{wallet}'{' (dry-run)' if dry_run else ''}."
