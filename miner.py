#!/usr/bin/env python3
"""nostr-summary-miner: classify tool mentions from the nostr-summary firehose."""
import json, os, argparse, websocket, ssl

FEED = "npub10l479fv64qn03a3n0dqsryu74tyzl48xef0nc7u0z09q8tfx72ls7sv2ux"
RELAYS = ["wss://relay.damus.io","wss://nos.lol","wss://relay.primal.net"]
TAGS = ["Payments/Cashu","Relay","Identity/WoT","Privacy/Messaging","Client","SDK",
        "NoT/P2P","AI/DVM","Search","KeyMgmt","General"]

def classify(text):
    t = text.lower()
    for kw, tag in [("cashu","Payments/Cashu"),("nwc","Payments/Cashu"),("relay","Relay"),
                    ("wot","Identity/WoT"),("nip-05","Identity/WoT"),("simplex","Privacy/Messaging"),
                    ("amethyst","Client"),("ndk","SDK"),("hyperswarm","NoT/P2P"),("dvm","AI/DVM"),
                    ("search","Search"),("key","KeyMgmt")]:
        if kw in t: return tag
    return "General"

def mine(sample=20):
    ws = websocket.create_connection(RELAYS[0], sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.send(json.dumps(["REQ","miner",{"authors":[FEED],"limit":sample}]))
    tools = {}
    for _ in range(sample*2):
        try:
            msg = json.loads(ws.recv())
            if msg[0] == "EVENT":
                ev = msg[2]
                tag = classify(ev["content"])
                slug = ev["id"][:12]
                tools[slug] = {"tag": tag, "snippet": ev["content"][:120]}
        except Exception:
            break
    ws.close()
    with open("tool_index.json","w") as f: json.dump(tools, f, indent=2)
    print(f"[miner] classified {len(tools)} events")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--sample", type=int, default=20)
    a = ap.parse_args(); mine(a.sample)
