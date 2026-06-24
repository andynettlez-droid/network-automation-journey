#!/usr/bin/env bash
# Run this FIRST, before the lab. It confirms your tools are ready so you don't
# hit cryptic failures mid-lesson.   bash preflight.sh
echo "Day 1 preflight - checking your tools..."
bad=0
chk(){ if "$@" >/dev/null 2>&1; then echo "  [OK]   $LABEL"; else echo "  [FIX]  $LABEL"; bad=$((bad+1)); fi; }

LABEL="Docker installed";        chk command -v docker
LABEL="ContainerLab installed";  chk command -v containerlab
LABEL="Ansible installed";       chk command -v ansible-playbook

if ansible-galaxy collection list 2>/dev/null | grep -qi 'nokia.srlinux'; then
  echo "  [OK]   nokia.srlinux collection"
else
  echo "  [FIX]  nokia.srlinux collection  ->  ansible-galaxy collection install nokia.srlinux"; bad=$((bad+1))
fi

if docker ps >/dev/null 2>&1 || sudo docker ps >/dev/null 2>&1; then
  echo "  [OK]   Docker daemon running"
else
  echo "  [FIX]  Docker daemon not running  ->  sudo service docker start"; bad=$((bad+1))
fi

case "$PWD" in
  /mnt/*) echo "  [FIX]  You're on the Windows drive (/mnt/c). Copy the lab to ~/netlab and run it there."; bad=$((bad+1));;
  *)      echo "  [OK]   Running on Linux-native disk";;
esac

echo
if [ "$bad" -eq 0 ]; then echo "  All set - start the lab."; else echo "  Fix the $bad item(s) above first, then re-run: bash preflight.sh"; fi
