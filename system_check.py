import sys
import os
from pathlib import Path

print('='*70)
print('WALMART NETWORK SECURITY AUTOMATION - INSTALLATION CHECK')
print('='*70)

checks = []

# 1. Python version
python_version = sys.version_info
checks.append(('Python 3.11+', python_version.major == 3 and python_version.minor >= 11))

# 2. Required directories exist
required_dirs = ['src', 'terraform', 'ansible', 'tests', 'data', 'dashboards']
for d in required_dirs:
    checks.append((f'Directory: {d}', Path(d).exists()))

# 3. Required files exist
required_files = [
    'setup_master.py',
    'docker-compose.yml',
    'Dockerfile',
    'requirements.txt',
    '.env.example',
    'README.md'
]
for f in required_files:
    checks.append((f'File: {f}', Path(f).exists()))

# 4. Python packages
packages_to_check = [
    'fastapi', 'uvicorn', 'sqlalchemy', 'numpy', 
    'pandas', 'sklearn', 'flask', 'pytest'
]
for pkg in packages_to_check:
    try:
        __import__(pkg)
        checks.append((f'Package: {pkg}', True))
    except ImportError:
        checks.append((f'Package: {pkg}', False))

# 5. Data directories
data_dirs = ['data/training', 'data/models', 'data/synthetic']
for d in data_dirs:
    checks.append((f'Data dir: {d}', Path(d).exists()))

# Print results
print('\nCHECK RESULTS:')
print('-'*70)
all_passed = True
for check_name, result in checks:
    status = '✓ PASS' if result else '✗ FAIL'
    print(f'{check_name:40} {status}')
    if not result:
        all_passed = False

print('-'*70)
if all_passed:
    print('\n✓✓✓ ALL CHECKS PASSED - SYSTEM READY! ✓✓✓')
    print('\nNext steps:')
    print('1. Copy .env.example to .env')
    print('2. Run: python scripts/data_generation/generate_synthetic_data.py')
    print('3. Run: docker compose up -d --build')
else:
    print('\n✗✗✗ SOME CHECKS FAILED - REVIEW ABOVE ✗✗✗')

print('='*70)
