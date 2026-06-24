#!/usr/bin/env bash
# Day 1 — live demonstration. Runs in a visible terminal so the learner watches in
# real time. Paced with pauses: read the ">>> why" line, then press Enter for each step.
REPO="/mnt/c/Users/andyn/Claude/Projects/ccna automation"
export TERM=${TERM:-xterm-256color}
mkdir -p ~/netlab/day1-demo && cd ~/netlab/day1-demo || exit 1
cp -r "$REPO/course/day-01-idempotency/lab/." . 2>/dev/null || true
export SRL_PASSWORD='NokiaSrl1!'

printf '\n\n'
echo "############################################################"
echo "#  DAY 1 DEMONSTRATION  -  Idempotency                      #"
echo "#  Watch each step. Read the 'why', then press Enter.       #"
echo "############################################################"
read -p $'\n[Press Enter when the lecture has finished, to BEGIN] '

echo; echo ">>> STEP 1 - Boot two virtual routers from a file"
echo "    why: the whole network is defined as code; one command brings it to life."
sudo containerlab deploy -t topology.clab.yml
read -p $'\n[Enter] apply the address with Ansible (first run)... '

echo; echo ">>> STEP 2 - Declare the address (FIRST run)"
echo "    why: we state the desired state. Expect changed=1 (it made the change)."
ansible-playbook -i inventory.yml solution/configure-interface.yml
read -p $'\n[Enter] now run the EXACT SAME thing again... '

echo; echo ">>> STEP 3 - Run the SAME automation AGAIN"
echo "    why: nothing should change. Expect changed=0. THAT is idempotency."
ansible-playbook -i inventory.yml solution/configure-interface.yml
read -p $'\n[Enter] verify on the device itself... '

echo; echo ">>> STEP 4 - Ask the DEVICE (ground truth)"
echo "    why: the playbook's report is a claim. The device is the proof."
sudo docker exec clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1"
read -p $'\n[Enter] tear the lab down... '

echo; echo ">>> STEP 5 - Clear the lab (experiments are free)"
sudo containerlab destroy -t topology.clab.yml
echo; echo ">>> Demonstration complete. Now it's your turn - the lab."
read -p $'\n[Press Enter to close this window] '
