#!/usr/bin/env bash
# Day 1 self-check. Run it after you've written your task and deployed the lab:
#   bash check.sh
# It grades YOUR configure-interface.yml: is it idempotent, and did it really
# set the address on the device? Green = pass, red = fix and re-run.
cd "$(dirname "$0")" || exit 1
export SRL_PASSWORD="${SRL_PASSWORD:-NokiaSrl1!}"
pass=0; fail=0
ok(){ echo "  [PASS] $1"; pass=$((pass+1)); }
no(){ echo "  [FAIL] $1"; fail=$((fail+1)); }

echo "Checking your Day 1 lab (this runs your playbook twice)..."

r1=$(ansible-playbook -i inventory.yml configure-interface.yml 2>/dev/null | grep -oE 'changed=[0-9]+' | head -1)
r2=$(ansible-playbook -i inventory.yml configure-interface.yml 2>/dev/null | grep -oE 'changed=[0-9]+' | head -1)
echo "  (run 1: ${r1:-none}   run 2: ${r2:-none})"
if [ "$r2" = "changed=0" ]; then ok "Idempotent: the second run made no change"; else no "Not idempotent yet (second run expected changed=0, got ${r2:-none})"; fi

ip=$(sudo docker exec clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1" 2>/dev/null | grep -oE '10\.0\.0\.1/30')
if [ -n "$ip" ]; then ok "Device really shows 10.0.0.1/30 on ethernet-1/1 (verified on the device)"; else no "Device does not show 10.0.0.1/30 - check your task"; fi

echo
if [ "$fail" -eq 0 ]; then
  echo "  *** All $pass checks passed. Day 1 complete - well done. ***"
else
  echo "  $pass passed, $fail to fix. Tweak your task and run: bash check.sh"
fi
