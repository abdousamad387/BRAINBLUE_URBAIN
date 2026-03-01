"""
Routes pour les données d'eau - BRAINBLUE URBAIN
"""

from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required
import logging
from datetime import datetime, timedelta

water_bp = Blueprint('water', __name__)
logger = logging.getLogger(__name__)

# Données simulées pour démonstration
SIMULATED_NETWORKS = {
    'dakar': [
        {
            'id': 'net-dakar-001',
            'name': 'Réseau eau potable Dakar Centre',
            'type': 'potable',
            'city': 'Dakar',
            'location': {'lat': 14.7167, 'lon': -17.4674},
            'capacity': 500000,
            'current_flow': 420000,
            'pressure': 5.2,
            'status': 'operational',
            'age_years': 15
        },
        {
            'id': 'net-dakar-002',
            'name': 'Réseau assainissement Dakar Plateau',
            'type': 'sewage',
            'city': 'Dakar',
            'location': {'lat': 14.7200, 'lon': -17.4500},
            'capacity': 300000,
            'current_flow': 280000,
            'pressure': 2.8,
            'status': 'warning',
            'age_years': 22
        },
        {
            'id': 'net-dakar-003',
            'name': 'Système drainage Medina',
            'type': 'drainage',
            'city': 'Dakar',
            'location': {'lat': 14.6900, 'lon': -17.4800},
            'capacity': 200000,
            'current_flow': 85000,
            'pressure': 1.5,
            'status': 'operational',
            'age_years': 8
        }
    ],
    'abidjan': [
        {
            'id': 'net-abidjan-001',
            'name': 'Réseau eau potable Abidjan Plateau',
            'type': 'potable',
            'city': 'Abidjan',
            'location': {'lat': 5.3364, 'lon': -4.0283},
            'capacity': 800000,
            'current_flow': 720000,
            'pressure': 5.8,
            'status': 'operational',
            'age_years': 12
        },
        {
            'id': 'net-abidjan-002',
            'name': 'Réseau assainissement Cocody',
            'type': 'sewage',
            'city': 'Abidjan',
            'location': {'lat': 5.3600, 'lon': -4.0100},
            'capacity': 600000,
            'current_flow': 550000,
            'pressure': 4.2,
            'status': 'operational',
            'age_years': 18
        }
    ]
}

@water_bp.route('/networks', methods=['GET'])
@jwt_required()
def get_networks():
    """Obtenir tous les réseaux d'eau"""
    try:
        city = request.args.get('city', 'dakar').lower()
        network_type = request.args.get('type')
        
        networks = SIMULATED_NETWORKS.get(city, [])
        
        if network_type:
            networks = [n for n in networks if n['type'] == network_type]
        
        return jsonify({
            'count': len(networks),
            'city': city,
            'data': networks
        }), 200
    
    except Exception as e:
        logger.error(f'Get networks error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve networks'}), 500

@water_bp.route('/networks/<network_id>', methods=['GET'])
@jwt_required()
def get_network_detail(network_id):
    """Obtenir détails d'un réseau spécifique"""
    try:
        for city_networks in SIMULATED_NETWORKS.values():
            for network in city_networks:
                if network['id'] == network_id:
                    # Enrichir avec données en temps réel
                    network['real_time_data'] = {
                        'flow_rate': 420000,
                        'pressure': 5.2,
                        'water_level': 3.5,
                        'temperature': 26.3,
                        'turbidity': 0.8,
                        'ph': 7.2,
                        'chlorine': 0.6,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    network['statistics'] = {
                        'avg_daily_flow': 415000,
                        'peak_flow': 480000,
                        'min_flow': 350000,
                        'leakage_percent': 8.5
                    }
                    
                    return jsonify(network), 200
        
        return jsonify({'error': 'Network not found'}), 404
    
    except Exception as e:
        logger.error(f'Get network detail error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve network details'}), 500

@water_bp.route('/networks/<network_id>/real-time', methods=['GET'])
@jwt_required()
def get_network_realtime(network_id):
    """Obtenir données en temps réel d'un réseau"""
    try:
        import random
        
        return jsonify({
            'network_id': network_id,
            'timestamp': datetime.utcnow().isoformat(),
            'measurements': {
                'flow_rate': round(random.uniform(350000, 480000), 0),
                'pressure': round(random.uniform(4.5, 6.0), 2),
                'water_level': round(random.uniform(2.5, 4.5), 2),
                'temperature': round(random.uniform(24, 28), 1),
                'turbidity': round(random.uniform(0.5, 1.5), 2),
                'ph': round(random.uniform(7.0, 7.5), 2),
                'chlorine': round(random.uniform(0.4, 0.8), 2)
            },
            'anomalies': {
                'detected': False,
                'types': [],
                'confidence': 0
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Get realtime data error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve real-time data'}), 500

@water_bp.route('/statistics/<city>', methods=['GET'])
@jwt_required()
def get_city_statistics(city):
    """Obtenir statistiques d'une ville"""
    try:
        city = city.lower()
        networks = SIMULATED_NETWORKS.get(city, [])
        
        total_capacity = sum(n['capacity'] for n in networks)
        total_flow = sum(n['current_flow'] for n in networks)
        
        return jsonify({
            'city': city,
            'total_networks': len(networks),
            'total_capacity': total_capacity,
            'total_flow': total_flow,
            'capacity_utilization_percent': round((total_flow / total_capacity * 100) if total_capacity > 0 else 0, 2),
            'operational_networks': len([n for n in networks if n['status'] == 'operational']),
            'warning_networks': len([n for n in networks if n['status'] == 'warning']),
            'critical_networks': len([n for n in networks if n['status'] == 'critical']),
            'avg_system_pressure': round(sum(n['pressure'] for n in networks) / len(networks), 2) if networks else 0,
            'total_population_served': 2500000 if city == 'dakar' else 4200000,
            'water_access_percent': 78.5 if city == 'dakar' else 82.3,
            'sanitation_coverage_percent': 71.2 if city == 'dakar' else 75.8
        }), 200
    
    except Exception as e:
        logger.error(f'Get statistics error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@water_bp.route('/alerts/<city>', methods=['GET'])
@jwt_required()
def get_city_alerts(city):
    """Obtenir alertes actives pour une ville"""
    try:
        city = city.lower()
        
        alerts = [
            {
                'id': 'alert-001',
                'type': 'pressure_drop',
                'severity': 'high',
                'location': 'Dakar Plateau',
                'message': 'Chute de pression anormale dans le secteur Plateau',
                'detected_at': (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                'status': 'active'
            },
            {
                'id': 'alert-002',
                'type': 'high_turbidity',
                'severity': 'medium',
                'location': 'Medina',
                'message': 'Turbidité élevée détectée',
                'detected_at': (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                'status': 'active'
            }
        ] if city == 'dakar' else []
        
        return jsonify({
            'city': city,
            'total_alerts': len(alerts),
            'active_alerts': alerts,
            'last_update': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Get alerts error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve alerts'}), 500

@water_bp.route('/networks', methods=['POST'])
@jwt_required()
def create_network():
    """Créer un nouveau réseau d'eau"""
    try:
        data = request.get_json()
        
        new_network = {
            'id': f"net-{data.get('city', 'unknown')}-{len(SIMULATED_NETWORKS.get(data.get('city', 'dakar').lower(), [])) + 1:03d}",
            'name': data.get('name'),
            'type': data.get('type'),
            'city': data.get('city'),
            'location': data.get('location'),
            'capacity': data.get('capacity'),
            'current_flow': 0,
            'pressure': 0,
            'status': 'new',
            'age_years': 0
        }
        
        return jsonify({
            'message': 'Network created successfully',
            'network': new_network
        }), 201
    
    except Exception as e:
        logger.error(f'Create network error: {str(e)}')
        return jsonify({'error': 'Failed to create network'}), 500

@water_bp.route('/networks/<network_id>', methods=['PUT'])
@jwt_required()
def update_network(network_id):
    """Mettre à jour un réseau d'eau"""
    try:
        data = request.get_json()
        
        return jsonify({
            'message': 'Network updated successfully',
            'network_id': network_id
        }), 200
    
    except Exception as e:
        logger.error(f'Update network error: {str(e)}')
        return jsonify({'error': 'Failed to update network'}), 500
