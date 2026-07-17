# nostr-summary-miner

Backfills + tails the nostr-summary firehose (npub10l479...), classifies tool mentions,
builds a local discovery index. Runs as cron (already scheduled on 0xDevBot).

## Run
```
pip install nostr-relay-monitor  # or use websocket-client
python3 miner.py --sample 20
```
State in state.json; index in tool_index.json. Tags: Payments/Cashu, Relay, Identity/WoT,
Privacy/Messaging, Client, SDK, NoT/P2P, AI/DVM, Search, KeyMgmt, General.
