# Day 1 Lab — Idempotent interface configuration

Run everything from Linux-native disk (e.g. `~/netlab`), **not** `/mnt/c` — drvfs can't set Linux permissions and SR Linux's config commit fails there.

## Steps

1. **Copy the lab to your run dir and deploy:**
   ```bash
   mkdir -p ~/netlab/day1 && cp -r . ~/netlab/day1 && cd ~/netlab/day1
   sudo containerlab deploy -t topology.clab.yml
   ```
2. **Install the collection and set creds:**
   ```bash
   ansible-galaxy collection install nokia.srlinux
   export SRL_PASSWORD='NokiaSrl1!'
   ```
3. **Smoke-test connectivity** (should read back the device version):
   ```bash
   ansible-playbook -i inventory.yml verify-connectivity.yml
   ```
4. **Write the config task** in `configure-interface.yml` — declare an IPv4 address on `ethernet-1/1`. Try before peeking at `solution/`.
5. **Run it twice** and watch the change flip to no-change:
   ```bash
   ansible-playbook -i inventory.yml configure-interface.yml   # run 1 -> changed
   ansible-playbook -i inventory.yml configure-interface.yml   # run 2 -> no change
   ```
6. **Verify on the device** (the truth, not the recap):
   ```bash
   docker exec -it clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1"
   ```
7. **Induce drift** by hand (change the IP on the device), re-run the playbook, and confirm only the drift is corrected.
8. **Tear down:**
   ```bash
   sudo containerlab destroy -t topology.clab.yml
   ```

## Done when
The second run reports no change, the device shows `10.0.0.1/30` on `ethernet-1/1`, and you can explain *why* re-running changed nothing.
