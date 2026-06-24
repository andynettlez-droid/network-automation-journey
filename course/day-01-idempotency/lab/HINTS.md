# Day 1 — Hints (open one at a time, only after you've tried)

Each hint reveals a little more. The full answer lives in `solution/`.

## Hint 1 — which module?
You want a module that *declares state*, not one that runs commands. On SR Linux that's `nokia.srlinux.config` with an `update:` list. Each item has a `path` (where in the config) and a `value` (what it should be).

## Hint 2 — the path and shape
The port lives at `/interface[name=ethernet-1/1]`. Under it you need: the port enabled, a `subinterface` at index `0`, and under that an `ipv4` block with an `address` of `10.0.0.1/30`. SR Linux wants `admin-state: enable` at the interface, the subinterface, *and* the ipv4 level.

## Hint 3 — the skeleton (you finish it)
```yaml
- name: "configure ethernet-1/1"
  nokia.srlinux.config:
    update:
      - path: /interface[name=ethernet-1/1]
        value:
          admin-state: enable
          subinterface:
            - index: 0
              # you finish: admin-state, then an ipv4 block with admin-state + address
```

## Still stuck?
The complete, working task is in `solution/configure-interface.yml`. Read it, understand *why* each line is there, then type it yourself — don't copy-paste. The typing is part of the learning.

## Check yourself
When your second run reports no change, run `bash check.sh` — it grades idempotency *and* checks the device really has the address.
