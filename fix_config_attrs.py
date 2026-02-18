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

fixes = [
    ("base_url=config.ise.url",      "base_url=config.ise.base_url"),
    ("base_url=config.dlp.url",      "base_url=config.dlp.base_url"),
    ("config.ise.url",               "config.ise.base_url"),
    ("config.dlp.url",               "config.dlp.base_url"),
]

for script in scripts:
    filepath = os.path.join(ROOT_DIR, script)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    for old, new in fixes:
        content = content.replace(old, new)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed: {script}")

print("\nAll attribute names fixed!")
