"""
Utilitaires et fonctions helper - BRAINBLUE URBAIN
"""

import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataGenerator:
    """Générateur de données simulées réalistes"""
    
    @staticmethod
    def generate_simulated_water_data(network_id, num_records=100):
        """Générer données d'eau simulées"""
        import random
        
        data = []
        for i in range(num_records):
            hours_ago = num_records - i
            data.append({
                'timestamp': datetime.utcnow(),
                'flow_rate': round(random.uniform(350000, 480000), 0),
                'pressure': round(random.uniform(4.5, 6.0), 2),
                'water_level': round(random.uniform(2.5, 4.5), 2),
                'temperature': round(random.uniform(24, 28), 1),
                'turbidity': round(random.uniform(0.5, 1.5), 2),
                'ph': round(random.uniform(7.0, 7.5), 2),
                'chlorine': round(random.uniform(0.4, 0.8), 2)
            })
        
        return data
    
    @staticmethod
    def generate_risk_zones(city):
        """Générer zones à risque pour une ville"""
        if city == 'dakar':
            return [
                {
                    'name': 'Médina Flood Zone',
                    'risk_type': 'flood',
                    'risk_level': 'high',
                    'probability': 35,
                    'lat': 14.6900,
                    'lon': -17.4800
                },
                {
                    'name': 'Plateau Drought Area',
                    'risk_type': 'drought',
                    'risk_level': 'medium',
                    'probability': 18,
                    'lat': 14.7200,
                    'lon': -17.4500
                }
            ]
        else:
            return [
                {
                    'name': 'Lagune Ébrié Zone',
                    'risk_type': 'flood',
                    'risk_level': 'very_high',
                    'probability': 42,
                    'lat': 5.3364,
                    'lon': -4.0283
                }
            ]

def success_response(data, message='Success', status_code=200):
    """Formater réponse succès"""
    return {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }, status_code

def error_response(message, error_code=None, status_code=400):
    """Formater réponse erreur"""
    return {
        'success': False,
        'error': message,
        'error_code': error_code,
        'timestamp': datetime.utcnow().isoformat()
    }, status_code

def paginate_results(results, page=1, per_page=10):
    """Paginer les résultats"""
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'data': results[start:end],
        'pagination': {
            'current_page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }

def cache_key(prefix, *args):
    """Générer clé de cache"""
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"
