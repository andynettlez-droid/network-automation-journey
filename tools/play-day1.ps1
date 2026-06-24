# Day 1 lesson launcher — opens the lesson player, the narration, and VS Code on your lab.
# Run it any time to start Day 1.  (PowerShell)
$ErrorActionPreference = "SilentlyContinue"
$lecture = "C:\Users\andyn\Claude\Projects\ccna automation\course\day-01-idempotency\lecture"

# 1. Make sure your lab folder exists in WSL (won't overwrite work you've already started).
wsl -d Ubuntu -- bash -lc "test -d ~/netlab/day1-mine || (mkdir -p ~/netlab/day1-mine && cp -r '/mnt/c/Users/andyn/Claude/Projects/ccna automation/course/day-01-idempotency/lab/.' ~/netlab/day1-mine/)"

# 2. Start the lesson server (powers Explain-diagram, the AI tutor, and voice), then open the player + narration.
Start-Process wsl -WindowStyle Minimized -ArgumentList @('-d','Ubuntu','--','bash','/home/andyn/.lesson-server.sh')
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000/lesson.html"
Start-Sleep -Seconds 1
Start-Process "$lecture\lecture.mp3"

# 3. Open VS Code on your lab folder, landing on the guided playbook (not the Welcome tab).
wsl -d Ubuntu -- bash -lic "cd ~/netlab/day1-mine && setsid code . configure-interface.yml >/dev/null 2>&1 </dev/null &"

Write-Host "Day 1 launched: lesson player + narration + VS Code on your lab."
