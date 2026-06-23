# Day 0 Lab — Look around a (virtual) router

No changes today. The goal is just to *boot two virtual routers and look at them*, so the words from the lecture become real. If you're on Windows + WSL, run this inside your Linux home (`~/netlab`), not the Windows `C:` drive (`/mnt/c`).

## Steps

1. **Boot two virtual routers:**
   ```bash
   mkdir -p ~/netlab/day0 && cp -r . ~/netlab/day0 && cd ~/netlab/day0
   sudo containerlab deploy -t topology.clab.yml
   ```
   You'll see a table listing `srl1` and `srl2` as `running`. Those are two virtual routers, connected by a virtual cable. You made a network.

2. **Step inside a router and look around:**
   ```bash
   docker exec -it clab-day0-primer-srl1 sr_cli
   ```
   You're now "inside" srl1, at its command line (`sr_cli`). Try these (type each, press Enter):
   ```
   show version                       # what software it's running
   show interface ethernet-1/1        # one of its ports (notice it has no address yet)
   quit                               # leave
   ```
   Notice `ethernet-1/1` exists but has **no IP address** yet. Tomorrow, on Day 1, you'll give it one — with automation.

3. **Throw it away** (this is the "safe to experiment" part):
   ```bash
   sudo containerlab destroy -t topology.clab.yml
   ```

## Done when
You've booted the routers, looked at a port with `show interface`, seen it has no address yet, and torn the lab down. That's the whole loop you'll repeat all course: **boot → look → change → verify → tear down.**
