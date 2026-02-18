import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

scripts = [
    "automation-showcase/01_deploy_ise_policy.py",
    "automation-showcase/02_detect_config_drift.py",
    "automation-showcase/03_automated_health_check.py",
    "automation-showcase/04_incident_auto_response.py",
    "automation-showcase/05_policy_lifecycle.py",
    "automation-showcase/06_bulk_endpoint_management.py",
]

PATH_FIX = "import sys, os\nsys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"

for script in scripts:
    filepath = os.path.join(ROOT_DIR, script)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    path_inserted = False
    for line in lines:
        if ("sys.path.append" in line or "sys.path.insert" in line) and not path_inserted:
            new_lines.append(PATH_FIX)
            path_inserted = True
            continue
        if "import sys" in line and not path_inserted:
            continue
        new_lines.append(line)

    if not path_inserted:
        new_lines.insert(0, PATH_FIX)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Fixed: {script}")

print("\nAll scripts fixed! Now run:")
print("  python automation-showcase\\01_deploy_ise_policy.py")
