"""
LSTM Time-Series Predictor
Phase 4: Predictive maintenance and capacity forecasting
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Try to import TensorFlow, but make it optional for local testing
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    TF_AVAILABLE = True
except ImportError:
    logger.warning("TensorFlow not available. LSTM functionality will be limited.")
    TF_AVAILABLE = False

class NetworkLSTMPredictor:
    """
    LSTM-based time-series predictor for network metrics
    
    Use cases:
    - Bandwidth utilization forecasting
    - Resource capacity planning
    - Predictive maintenance (failure prediction)
    - Traffic pattern prediction
    """
    
    def __init__(
        self, 
        sequence_length: int = 24,
        forecast_horizon: int = 6,
        hidden_units: List[int] = [64, 32]
    ):
        """
        Initialize LSTM predictor
        
        Args:
            sequence_length: Number of time steps to look back
            forecast_horizon: Number of time steps to forecast
            hidden_units: List of hidden units for LSTM layers
        """
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon
        self.hidden_units = hidden_units
        self.model = None
        self.scaler_X = None
        self.scaler_y = None
        self.is_trained = False
        
        if not TF_AVAILABLE:
            logger.warning("TensorFlow not available. LSTM model will not function.")
            return
        
        logger.info(f"Initialized LSTM Predictor (sequence={sequence_length}, forecast={forecast_horizon})")
    
    def _build_model(self, n_features: int) -> None:
        """Build LSTM model architecture"""
        if not TF_AVAILABLE:
            raise RuntimeError("TensorFlow is required but not available")
        
        self.model = Sequential()
        
        # First LSTM layer
        self.model.add(LSTM(
            self.hidden_units[0],
            return_sequences=len(self.hidden_units) > 1,
            input_shape=(self.sequence_length, n_features)
        ))
        self.model.add(Dropout(0.2))
        
        # Additional LSTM layers
        for i, units in enumerate(self.hidden_units[1:], 1):
            return_seq = i < len(self.hidden_units) - 1
            self.model.add(LSTM(units, return_sequences=return_seq))
            self.model.add(Dropout(0.2))
        
        # Output layer
        self.model.add(Dense(self.forecast_horizon))
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae', 'mape']
        )
        
        logger.info("LSTM model architecture built")
    
    def prepare_sequences(
        self, 
        data: np.ndarray, 
        target_col: int = 0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare time-series data into sequences
        
        Args:
            data: Time-series data array
            target_col: Column index to use as target
            
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        
        for i in range(len(data) - self.sequence_length - self.forecast_horizon + 1):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length:i + self.sequence_length + self.forecast_horizon, target_col])
        
        return np.array(X), np.array(y)
    
    def train(
        self, 
        df: pd.DataFrame,
        target_column: str = 'utilization',
        feature_columns: Optional[List[str]] = None,
        validation_split: float = 0.2,
        epochs: int = 50,
        batch_size: int = 32
    ) -> Dict:
        """
        Train LSTM model
        
        Args:
            df: Training data DataFrame with time-series data
            target_column: Column to predict
            feature_columns: Additional feature columns
            validation_split: Fraction of data for validation
            epochs: Training epochs
            batch_size: Batch size
            
        Returns:
            Training history dictionary
        """
        if not TF_AVAILABLE:
            raise RuntimeError("TensorFlow is required but not available")
        
        logger.info(f"Training LSTM on {len(df)} time steps")
        
        # Select features
        if feature_columns is None:
            feature_columns = [target_column]
        
        data = df[feature_columns].values
        
        # Normalize data
        from sklearn.preprocessing import StandardScaler
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        
        data_scaled = self.scaler_X.fit_transform(data)
        
        # Prepare sequences
        X, y = self.prepare_sequences(data_scaled)
        
        # Scale targets separately
        y_scaled = self.scaler_y.fit_transform(y)
        
        # Build model if not exists
        if self.model is None:
            self._build_model(n_features=len(feature_columns))
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            )
        ]
        
        # Train model
        history = self.model.fit(
            X, y_scaled,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        self.is_trained = True
        
        # Calculate training metrics
        train_metrics = {
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'final_mae': float(history.history['mae'][-1]),
            'final_val_mae': float(history.history['val_mae'][-1]),
            'epochs_trained': len(history.history['loss'])
        }
        
        logger.info(f"Training complete. Final val_loss: {train_metrics['final_val_loss']:.4f}")
        
        return train_metrics
    
    def predict(
        self, 
        recent_data: np.ndarray
    ) -> np.ndarray:
        """
        Make predictions on recent data
        
        Args:
            recent_data: Recent time-series data (shape: [sequence_length, n_features])
            
        Returns:
            Forecasted values
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Scale input
        recent_scaled = self.scaler_X.transform(recent_data)
        
        # Reshape for LSTM input
        X = recent_scaled.reshape(1, self.sequence_length, -1)
        
        # Predict
        y_scaled = self.model.predict(X, verbose=0)
        
        # Inverse transform
        y_pred = self.scaler_y.inverse_transform(y_scaled)
        
        return y_pred.flatten()
    
    def forecast(
        self, 
        df: pd.DataFrame,
        feature_columns: List[str],
        steps_ahead: int = 6
    ) -> pd.DataFrame:
        """
        Generate multi-step forecast
        
        Args:
            df: Recent historical data
            feature_columns: Feature columns to use
            steps_ahead: Number of steps to forecast
            
        Returns:
            DataFrame with predictions
        """
        if len(df) < self.sequence_length:
            raise ValueError(f"Need at least {self.sequence_length} historical data points")
        
        # Get recent data
        recent_data = df[feature_columns].values[-self.sequence_length:]
        
        # Make prediction
        predictions = self.predict(recent_data)
        
        # Create results DataFrame
        last_timestamp = df.index[-1] if isinstance(df.index, pd.DatetimeIndex) else None
        
        results = pd.DataFrame({
            'step': range(1, len(predictions) + 1),
            'predicted_value': predictions,
            'confidence_lower': predictions * 0.95,  # Simplified confidence intervals
            'confidence_upper': predictions * 1.05
        })
        
        if last_timestamp:
            results['timestamp'] = pd.date_range(
                start=last_timestamp,
                periods=len(predictions) + 1,
                freq='H'
            )[1:]
        
        return results
    
    def save_model(self, path: str) -> None:
        """Save model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        self.model.save(f"{path}.h5")
        
        import joblib
        joblib.dump({
            'scaler_X': self.scaler_X,
            'scaler_y': self.scaler_y,
            'sequence_length': self.sequence_length,
            'forecast_horizon': self.forecast_horizon,
            'hidden_units': self.hidden_units
        }, f"{path}_config.joblib")
        
        logger.info(f"Model saved to {path}")
    
    @classmethod
    def load_model(cls, path: str) -> 'NetworkLSTMPredictor':
        """Load model from disk"""
        if not TF_AVAILABLE:
            raise RuntimeError("TensorFlow is required but not available")
        
        import joblib
        
        config = joblib.load(f"{path}_config.joblib")
        
        predictor = cls(
            sequence_length=config['sequence_length'],
            forecast_horizon=config['forecast_horizon'],
            hidden_units=config['hidden_units']
        )
        
        predictor.model = keras.models.load_model(f"{path}.h5")
        predictor.scaler_X = config['scaler_X']
        predictor.scaler_y = config['scaler_y']
        predictor.is_trained = True
        
        logger.info(f"Model loaded from {path}")
        return predictor
