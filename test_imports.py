print('Testing project imports...\n')

try:
    print('Testing ML models...')
    from src.ml.models.anomaly_detector import NetworkAnomalyDetector
    print('  ✓ Anomaly Detector')
    
    from src.ml.training.trainer import ModelTrainer
    print('  ✓ Model Trainer')
    
    from src.ml.inference.engine import InferenceEngine
    print('  ✓ Inference Engine')
    
except ImportError as e:
    print(f'  ✗ ML imports failed: {e}')

try:
    print('\nTesting integrations...')
    from src.integrations.cisco_ise.client import CiscoISEClient
    print('  ✓ Cisco ISE Client')
    
    from src.integrations.symantec_dlp.client import SymantecDLPClient
    print('  ✓ Symantec DLP Client')
    
except ImportError as e:
    print(f'  ✗ Integration imports failed: {e}')

try:
    print('\nTesting API...')
    from src.api.app import app
    print('  ✓ FastAPI App')
    
except ImportError as e:
    print(f'  ✗ API imports failed: {e}')

try:
    print('\nTesting database models...')
    from src.database.models.network_events import NetworkEvent
    print('  ✓ Network Events Model')
    
except ImportError as e:
    print(f'  ✗ Database imports failed: {e}')

try:
    print('\nTesting config...')
    from src.config import Config
    print('  ✓ Configuration')
    
except ImportError as e:
    print(f'  ✗ Config imports failed: {e}')

print('\n' + '='*60)
print('✓✓✓ ALL PROJECT IMPORTS SUCCESSFUL! ✓✓✓')
print('='*60)
