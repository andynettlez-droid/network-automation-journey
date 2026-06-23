# Day 0 — Networking & Tools, From Scratch

**Time:** ~30–45 min · **Prerequisite:** none. This is the start.

No automation yet. Today is about vocabulary and getting comfortable looking at a device. By the end, the words in Day 1 will make sense.

## Learning objectives
By the end you can explain, in your own words:
- What a **network**, a **device/router**, and an **interface (port)** are.
- What an **IP address** is, and what the **`/30`** part means.
- What a **device's configuration** is (and what "running config" means).
- What an **emulator** is, and why we practice on virtual devices.
- What the three tools do: **ContainerLab**, **SR Linux**, **Ansible**.

## 1. Lecture — listen first
Play [`lecture/lecture.mp3`](lecture/lecture.mp3) (or read [`lecture/lecture.txt`](lecture/lecture.txt)). Plain-English ideas, no typing. The picture [`lecture/concepts.svg`](lecture/concepts.svg) shows the words as a diagram.

## Plain-English glossary (keep this handy)
- **Network** — computers and devices connected so they can talk to each other.
- **Router** — a device whose job is to direct traffic between networks (like a postal sorting office).
- **Interface / port** — a socket on a device where a cable connects. Each one has a name like `ethernet-1/1`.
- **IP address** — a device's address on the network, e.g. `10.0.0.1`. Like a house number so messages know where to go.
- **`/30`** — shorthand for "this address lives on a tiny street with room for just 2 devices." (Bigger networks use `/24`, etc. The number is how big the street is — higher means smaller.)
- **Configuration ("config")** — the settings on a device: which ports are on, what addresses they have, etc.
- **Running config** — the settings the device is *actually using right now*. When you change a device, you change its running config.
- **Emulator** — software that pretends to be a real router so you can practice safely. **ContainerLab** is our emulator launcher; **SR Linux** is the router software (the "operating system") it runs.
- **Ansible** — the tool that makes configuration changes for you, automatically, from a file you write.

## 2. Demonstration + 3. Lab — look around a real (virtual) device
This gentle hands-on just *boots two virtual routers and looks at them*. No changes. Open [`lab/README.md`](lab/README.md).

## Recap
- Devices have **ports (interfaces)**; ports get **IP addresses**; the collection of settings is the **config**.
- We practice on **emulated** devices (ContainerLab + SR Linux) so mistakes are free.
- **Ansible** will do the configuring for us, starting Day 1.

## Next
**Day 1 — Idempotency:** you'll give a port an IP address with Ansible, and learn why running it twice should change nothing.
