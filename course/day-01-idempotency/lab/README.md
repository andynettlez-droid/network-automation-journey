# Day 1 Lab — Idempotent interface configuration

## The tools you'll use (plain English)
- **ContainerLab** — boots the virtual routers from the `topology.clab.yml` file.
- **SR Linux** — the router software running inside them; you talk to it with `sr_cli`.
- **Ansible** — runs your automation. You give it two files:
  - a **playbook** (`configure-interface.yml`) — *what* should be true, and
  - an **inventory** (`inventory.yml`) — *which* device to act on.
- **collection** (`nokia.srlinux`) — a plug-in that teaches Ansible how to talk to SR Linux.
- The `-i inventory.yml` flag just means "use this inventory file."

> **Where to run this:** if you're on Windows with WSL, work inside the Linux home folder (`~/netlab`), **not** the Windows `C:` drive (which shows up as `/mnt/c`). The two handle file permissions differently, and the device's config save fails on `/mnt/c`. `~` means your Linux home folder.

## Steps

1. **Boot the lab** (from Linux-native disk):
   ```bash
   mkdir -p ~/netlab/day1 && cp -r . ~/netlab/day1 && cd ~/netlab/day1
   sudo containerlab deploy -t topology.clab.yml
   ```
2. **Install the plug-in and set the device password** (`export` makes it available for this terminal session):
   ```bash
   ansible-galaxy collection install nokia.srlinux
   export SRL_PASSWORD='NokiaSrl1!'
   ```
3. **Smoke-test** that Ansible can reach the device (reads back its version):
   ```bash
   ansible-playbook -i inventory.yml verify-connectivity.yml
   ```
4. **Write the config task** in `configure-interface.yml` — declare an IP address on `ethernet-1/1`. Try before peeking at `solution/`.
5. **Run it twice** and watch change flip to no-change:
   ```bash
   ansible-playbook -i inventory.yml configure-interface.yml   # run 1 -> changed
   ansible-playbook -i inventory.yml configure-interface.yml   # run 2 -> no change
   ```
6. **Verify on the device** (the truth, not the recap):
   ```bash
   docker exec -it clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1"
   ```
7. **Cause drift on purpose, then watch automation fix it.** By hand, turn the port off on the device:
   ```bash
   docker exec -it clab-day1-idempotency-srl1 sr_cli
   # at the SR Linux prompt, type these three lines:
   enter candidate
   set /interface ethernet-1/1 admin-state disable
   commit now
   quit
   ```
   Now re-run the playbook. Your file says the port should be **enabled**, so Ansible turns it back on and reports **changed**. Run it once more → **no change**. You just watched automation heal a change someone made by hand.
8. **Tear down:**
   ```bash
   sudo containerlab destroy -t topology.clab.yml
   ```

## Done when
The second run reports no change, the device shows `10.0.0.1/30` on `ethernet-1/1`, you've seen drift get auto-corrected, and you can explain *why* re-running changed nothing.
