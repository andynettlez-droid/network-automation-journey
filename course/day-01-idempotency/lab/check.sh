#!/usr/bin/env bash
# Day 1 self-check. Run after you've written your task and deployed the lab:
#   bash check.sh
# Grades YOUR configure-interface.yml: did you write a real task, is it idempotent,
# and is the address really on the device? Note: this is end-state grading - it runs
# your playbook itself, so it checks the result, not whether you personally ran it.
cd "$(dirname "$0")" || exit 1
export SRL_PASSWORD="${SRL_PASSWORD:-NokiaSrl1!}"
pass=0; fail=0
ok(){ echo "  [PASS] $1"; pass=$((pass+1)); }
no(){ echo "  [FAIL] $1"; fail=$((fail+1)); }
# docker exec without sudo, fall back to sudo (works whether or not you're in the docker group)
dx(){ docker exec "$@" 2>/dev/null || sudo docker exec "$@" 2>/dev/null; }

echo "Checking your Day 1 lab..."

# 0. Did you actually write the task? (the starter ships an ansible.builtin.debug stub)
if ! grep -q 'nokia.srlinux.config' configure-interface.yml; then
  no "You haven't written the task yet - replace the TODO debug stub with a nokia.srlinux.config task (see HINTS.md)"
  echo; echo "  $pass passed, $fail to fix."; exit 1
fi
ok "You wrote a real config task"

# 1. Idempotency: re-running must report no change.
r1=$(ansible-playbook -i inventory.yml configure-interface.yml 2>/dev/null | grep -oE 'changed=[0-9]+' | head -1)
r2=$(ansible-playbook -i inventory.yml configure-interface.yml 2>/dev/null | grep -oE 'changed=[0-9]+' | head -1)
echo "  (run 1: ${r1:-none}   run 2: ${r2:-none})"
if [ "$r2" = "changed=0" ]; then ok "Idempotent: the second run made no change"; else no "Not idempotent yet (second run expected changed=0, got ${r2:-none})"; fi

# 2. Device really has the address (ground truth).
ip=$(dx clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1" | grep -oE '10\.0\.0\.1/30')
if [ -n "$ip" ]; then ok "Device shows 10.0.0.1/30 on ethernet-1/1 (verified on the device)"; else no "Device does not show 10.0.0.1/30 - check your task"; fi

echo
if [ "$fail" -eq 0 ]; then
  echo "  +------------------------------------------+"
  echo "  |   DAY 1 COMPLETE - Idempotency Badge     |"
  echo "  |   All $pass checks passed. Well done!         |"
  echo "  +------------------------------------------+"
else
  echo "  $pass passed, $fail to fix. Tweak your task and run: bash check.sh"
fi
