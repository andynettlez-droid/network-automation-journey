# Day 1 Cheat-Sheet

**The one idea:** declare the state you want; re-running changes nothing once the device already matches. `changed=1` on the first run, `changed=0` after = idempotent.

**The commands, in order:**
```bash
bash preflight.sh                                       # 0. are my tools ready?
sudo containerlab deploy -t topology.clab.yml          # 1. boot the lab
export SRL_PASSWORD='NokiaSrl1!'                        # 2. device password (per terminal!)
ansible-playbook -i inventory.yml verify-connectivity.yml   # 3. can Ansible reach it?
# 4. write your task in configure-interface.yml, then:
ansible-playbook -i inventory.yml configure-interface.yml   # 5. apply (run twice)
docker exec -it clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1"  # 6. verify on device
bash check.sh                                          # 7. grade yourself
sudo containerlab destroy -t topology.clab.yml         # 8. tear down
```

**Two things beginners trip on:**
- `export` only lasts for the **current terminal** — re-run it in any new terminal.
- `sr_cli` only exists **inside** the container — always prefix with `docker exec -it clab-day1-idempotency-srl1 ...`.
