import sys
print(f"Python version: {sys.version}")
print("\n" + "="*60)
print("CHECKING INSTALLED PACKAGES")
print("="*60 + "\n")

packages = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'pydantic': 'Pydantic',
    'sqlalchemy': 'SQLAlchemy',
    'psycopg2': 'PostgreSQL Driver',
    'redis': 'Redis',
    'requests': 'Requests',
    'httpx': 'HTTPX',
    'numpy': 'NumPy',
    'pandas': 'Pandas',
    'sklearn': 'Scikit-Learn',
    'joblib': 'Joblib',
    'pytest': 'Pytest',
    'flask': 'Flask'
}

all_ok = True

for module, name in packages.items():
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {name:20} - Version {version}")
    except ImportError as e:
        print(f"✗ {name:20} - NOT INSTALLED")
        all_ok = False

print("\n" + "="*60)
if all_ok:
    print("✓✓✓ ALL PACKAGES INSTALLED SUCCESSFULLY! ✓✓✓")
else:
    print("✗✗✗ SOME PACKAGES ARE MISSING ✗✗✗")
print("="*60)
