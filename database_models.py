"""
Modèles de base de données - BRAINBLUE URBAIN
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, UUID, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid_lib

db = None

def init_db(app):
    """Initialiser SQLAlchemy avec l'app Flask"""
    global db
    db = SQLAlchemy(app)

class User(db.Model):
    """Modèle utilisateur avec authentification sécurisée"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # admin, manager, analyst, user
    city = db.Column(db.String(50))  # Dakar, Abidjan, etc.
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hasher et définir le mot de passe"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'city': self.city,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }

class WaterNetwork(db.Model):
    """Modèle pour le réseau d'eau (tuyauterie, stations, etc.)"""
    __tablename__ = 'water_networks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(50), nullable=False, index=True)
    network_type = db.Column(db.String(30), nullable=False)  # potable, sewage, drainage
    
    # Géolocalisation (PostGIS)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    geom = db.Column(db.String(500))  # WKT format
    
    # Propriétés
    capacity = db.Column(db.Float)  # liters/hour
    current_flow = db.Column(db.Float, default=0)  # liters/hour
    pressure = db.Column(db.Float)  # bar
    status = db.Column(db.String(20), default='operational')  # operational, warning, critical, maintenance
    age_years = db.Column(db.Integer)
    last_maintenance = db.Column(db.DateTime)
    
    # Métadonnées
    metadata = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    real_time_data = db.relationship('RealTimeData', backref='network', cascade='all, delete-orphan')
    
    @hybrid_property
    def leak_risk(self):
        """Calculer risque de fuite basé sur l'âge et le type"""
        if self.age_years is None:
            return 0
        if self.age_years > 40:
            return 'high'
        elif self.age_years > 25:
            return 'medium'
        else:
            return 'low'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'type': self.network_type,
            'location': {'lat': self.latitude, 'lon': self.longitude},
            'capacity': self.capacity,
            'current_flow': self.current_flow,
            'pressure': self.pressure,
            'status': self.status,
            'leak_risk': self.leak_risk,
            'updated_at': self.updated_at.isoformat()
        }

class RiskZone(db.Model):
    """Modèle pour les zones à risques (inondation, sécheresse, etc.)"""
    __tablename__ = 'risk_zones'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(50), nullable=False, index=True)
    risk_type = db.Column(db.String(30), nullable=False)  # flood, drought, contamination, burst
    
    # Géométrie
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius_km = db.Column(db.Float)  # Rayon de la zone
    geom = db.Column(db.String(500))  # WKT format pour polygone
    
    # Analyse de risque
    risk_level = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    probability_percent = db.Column(db.Float, default=50)
    affected_population = db.Column(db.Integer)
    infrastructure_at_risk = db.Column(db.Integer)
    
    # Temporalité
    detected_date = db.Column(db.DateTime, default=datetime.utcnow)
    predicted_date = db.Column(db.DateTime)  # Date prédite pour événement
    resolved_date = db.Column(db.DateTime)
    
    # Métadonnées
    metadata = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'risk_type': self.risk_type,
            'location': {'lat': self.latitude, 'lon': self.longitude},
            'risk_level': self.risk_level,
            'probability_percent': self.probability_percent,
            'affected_population': self.affected_population,
            'detected_date': self.detected_date.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RealTimeData(db.Model):
    """Modèle pour les données en temps réel des capteurs IoT"""
    __tablename__ = 'real_time_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    network_id = db.Column(db.String(36), db.ForeignKey('water_networks.id'), nullable=False, index=True)
    
    # Mesures
    flow_rate = db.Column(db.Float)  # liters/hour
    pressure = db.Column(db.Float)  # bar
    water_level = db.Column(db.Float)  # meters
    temperature = db.Column(db.Float)  # celsius
    turbidity = db.Column(db.Float)  # NTU
    ph = db.Column(db.Float)
    chlorine = db.Column(db.Float)  # mg/L
    
    # Anomalies détectées
    anomaly_detected = db.Column(db.Boolean, default=False)
    anomaly_type = db.Column(db.String(30))  # leak, pressure_drop, contamination, etc.
    anomaly_confidence = db.Column(db.Float)  # 0-1
    
    # Timestamp
    measurement_timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'network_id': self.network_id,
            'measurements': {
                'flow_rate': self.flow_rate,
                'pressure': self.pressure,
                'water_level': self.water_level,
                'temperature': self.temperature,
                'turbidity': self.turbidity,
                'ph': self.ph,
                'chlorine': self.chlorine
            },
            'anomaly': {
                'detected': self.anomaly_detected,
                'type': self.anomaly_type,
                'confidence': self.anomaly_confidence
            },
            'timestamp': self.measurement_timestamp.isoformat()
        }

class Prediction(db.Model):
    """Modèle pour les prédictions ML"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    city = db.Column(db.String(50), nullable=False, index=True)
    prediction_type = db.Column(db.String(30), nullable=False)  # flood, water_level, demand, etc.
    
    # Données de prédiction
    target_location = db.Column(JSON)  # {'lat': float, 'lon': float}
    prediction_date = db.Column(db.DateTime, nullable=False)
    
    # Résultats
    predicted_value = db.Column(db.Float)
    predicted_probability = db.Column(db.Float)  # 0-1
    confidence_interval = db.Column(JSON)  # {'lower': float, 'upper': float}
    
    # Modèle utilisé
    model_name = db.Column(db.String(50))
    model_version = db.Column(db.String(20))
    
    # Validation
    actual_value = db.Column(db.Float)
    is_accurate = db.Column(db.Boolean)
    
    # Métadonnées
    metadata = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'prediction_type': self.prediction_type,
            'city': self.city,
            'location': self.target_location,
            'prediction_date': self.prediction_date.isoformat(),
            'predicted_value': self.predicted_value,
            'predicted_probability': self.predicted_probability,
            'confidence_interval': self.confidence_interval,
            'model': {
                'name': self.model_name,
                'version': self.model_version
            },
            'created_at': self.created_at.isoformat()
        }

class Report(db.Model):
    """Modèle pour les rapports générés"""
    __tablename__ = 'reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid_lib.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    report_type = db.Column(db.String(50))  # daily, weekly, monthly, sdg6
    city = db.Column(db.String(50), index=True)
    
    # Contenu
    summary = db.Column(db.Text)
    metrics = db.Column(JSON)
    visualizations = db.Column(JSON)
    recommendations = db.Column(JSON)
    
    # Timestamps
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.report_type,
            'city': self.city,
            'metrics': self.metrics,
            'generated_at': self.generated_at.isoformat()
        }
