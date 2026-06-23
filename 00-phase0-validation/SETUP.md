# Phase 0 — Toolchain setup & validation

Goal: prove the lab environment works before building anything on it. Deploy a throwaway 2-node topology, confirm the nodes are up and reachable, then tear it down.

## Detected state (2026-06-23)

| Component | Status |
| --- | --- |
| WSL2 | ✅ installed (v2.7.8) |
| Distro: **Ubuntu 26.04 LTS** (default) | ✅ — **this is the lab home** |
| Distro: `ccna-ubuntu` | ⛔ belongs to the separate study project — **do not use** |
| `python3`, `git` (in Ubuntu) | ✅ present |
| **Docker** (in Ubuntu) | ❌ missing — install |
| **ContainerLab** (in Ubuntu) | ❌ missing — install |
| **Ansible** (in Ubuntu) | ❌ missing — install |

The lab runs **inside the default `Ubuntu` distro**, not on the Windows host. The Windows-side `git`/`node` and the locale-broken host `ansible` are not used here.

> This repo is reachable from inside WSL at:
> `/mnt/c/Users/andyn/Claude/Projects/ccna automation`

## Steps (run inside Ubuntu)

Open the distro from PowerShell:

```powershell
wsl -d Ubuntu
```

### 1. Docker engine (native in WSL, no Docker Desktop needed)

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

WSL doesn't run Docker as a service automatically. Either enable systemd once:

```bash
# /etc/wsl.conf
# [boot]
# systemd=true
sudoedit /etc/wsl.conf      # add the two lines above
```
…then from PowerShell `wsl --shutdown` and reopen — or just start it each session with `sudo service docker start`. Verify: `docker run --rm hello-world`.

### 2. ContainerLab (official installer)

```bash
bash -c "$(curl -sL https://get.containerlab.dev)"
containerlab version
```

### 3. Ansible

```bash
sudo apt update && sudo apt install -y ansible
ansible --version
```

## Validate (the Phase 0 gate)

```bash
cd "/mnt/c/Users/andyn/Claude/Projects/ccna automation/00-phase0-validation"
sudo containerlab deploy -t topology.clab.yml
sudo containerlab inspect -t topology.clab.yml   # both nodes should show "running"
```

Confirm ground truth — drop into a node's CLI and look at the real device:

```bash
docker exec -it clab-phase0-validation-srl1 sr_cli
# in the SR Linux prompt:
show version
show interface ethernet-1/1
quit
```

Tear it down (blast-radius discipline — never leave a lab running):

```bash
sudo containerlab destroy -t topology.clab.yml
```

**Gate passed when:** the topology deploys, both nodes show `running`, you reach the SR Linux CLI, and `destroy` cleans up with no leftovers (`containerlab inspect --all` shows nothing).

## Notes

- ContainerLab needs `sudo`.
- If image pull is slow the first time, that's GHCR fetching SR Linux — it caches after.
- Authority for install steps is the official docs (`containerlab.dev`, `docs.docker.com`) — if a command drifts, defer to those.
- Optional stricter isolation: create a dedicated `netlab-ubuntu` distro instead of using the default `Ubuntu`. Not required; the default distro is fine as long as `ccna-ubuntu` stays untouched.
