"""
Routes pour les cartes géographiques - BRAINBLUE URBAIN
"""

from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required
import logging
from datetime import datetime
import random

map_bp = Blueprint('maps', __name__)
logger = logging.getLogger(__name__)

# Données GeoJSON simulées pour les cartes interactives
DAKAR_GEOJSON = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'id': 'water-pipe-1',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[-17.4674, 14.7167], [-17.4500, 14.7200], [-17.4400, 14.7300]]
            },
            'properties': {
                'name': 'Conduites eau potable - Dakar Centre',
                'type': 'main',
                'status': 'operational',
                'pressure': 5.2,
                'age_years': 15
            }
        },
        {
            'type': 'Feature',
            'id': 'water-pipe-2',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[-17.4800, 14.6900], [-17.4700, 14.7000], [-17.4600, 14.7100]]
            },
            'properties': {
                'name': 'System drainage - Medina',
                'type': 'drainage',
                'status': 'operational',
                'capacity': 200000,
                'age_years': 8
            }
        },
        {
            'type': 'Feature',
            'id': 'flood-zone-1',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [-17.49, 14.69],
                    [-17.48, 14.69],
                    [-17.48, 14.70],
                    [-17.49, 14.70],
                    [-17.49, 14.69]
                ]]
            },
            'properties': {
                'name': 'Zone inondable - Médina',
                'risk_level': 'high',
                'probability': 35,
                'affected_population': 50000
            }
        },
        {
            'type': 'Feature',
            'id': 'pumping-station-1',
            'geometry': {
                'type': 'Point',
                'coordinates': [-17.4674, 14.7167]
            },
            'properties': {
                'name': 'Station de pompage Dakar Centre',
                'type': 'pumping_station',
                'status': 'operational',
                'capacity': 500000,
                'current_flow': 420000
            }
        },
        {
            'type': 'Feature',
            'id': 'treatment-plant-1',
            'geometry': {
                'type': 'Point',
                'coordinates': [-17.5200, 14.7400]
            },
            'properties': {
                'name': 'Usine de traitement eau potable',
                'type': 'treatment_plant',
                'status': 'operational',
                'capacity': 450000
            }
        },
        {
            'type': 'Feature',
            'id': 'water-source-1',
            'geometry': {
                'type': 'Point',
                'coordinates': [-17.3500, 14.8000]
            },
            'properties': {
                'name': 'Source eau - Lac Rose',
                'type': 'water_source',
                'quality': 'good',
                'current_level': 3.5
            }
        }
    ]
}

ABIDJAN_GEOJSON = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'id': 'water-pipe-abj-1',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[-4.0283, 5.3364], [-4.0200, 5.3400], [-4.0100, 5.3500]]
            },
            'properties': {
                'name': 'Conduites eau potable - Plateau',
                'type': 'main',
                'status': 'operational',
                'pressure': 5.8,
                'age_years': 12
            }
        },
        {
            'type': 'Feature',
            'id': 'flood-zone-abj-1',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [-4.02, 5.33],
                    [-4.01, 5.33],
                    [-4.01, 5.34],
                    [-4.02, 5.34],
                    [-4.02, 5.33]
                ]]
            },
            'properties': {
                'name': 'Zone inondable - Lagune Ébrié',
                'risk_level': 'very_high',
                'probability': 42,
                'affected_population': 120000
            }
        },
        {
            'type': 'Feature',
            'id': 'pumping-station-abj-1',
            'geometry': {
                'type': 'Point',
                'coordinates': [-4.0283, 5.3364]
            },
            'properties': {
                'name': 'Station de pompage Plateau Cocody',
                'type': 'pumping_station',
                'status': 'operational',
                'capacity': 800000,
                'current_flow': 720000
            }
        }
    ]
}

@map_bp.route('/layers/<city>', methods=['GET'])
@jwt_required()
def get_map_layers(city):
    """Obtenir les couches cartographiques pour une ville"""
    try:
        city = city.lower()
        
        geojson = DAKAR_GEOJSON if city == 'dakar' else ABIDJAN_GEOJSON
        
        return jsonify({
            'city': city,
            'base_layers': [
                {'name': 'OpenStreetMap', 'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'},
                {'name': 'Satellite', 'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'}
            ],
            'overlay_layers': [
                {'id': 'water-network', 'name': 'Réseau d\'eau', 'type': 'LineString', 'visible': True},
                {'id': 'flood-zones', 'name': 'Zones inondables', 'type': 'Polygon', 'visible': True},
                {'id': 'infrastructure', 'name': 'Infrastructures', 'type': 'Point', 'visible': True},
                {'id': 'risk-zones', 'name': 'Zones à risque', 'type': 'Polygon', 'visible': True},
                {'id': 'water-quality', 'name': 'Qualité de l\'eau', 'type': 'Point', 'visible': False},
                {'id': 'drought-zones', 'name': 'Zones sécheresse', 'type': 'Polygon', 'visible': False}
            ],
            'geojson': geojson
        }), 200
    
    except Exception as e:
        logger.error(f'Map layers error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve map layers'}), 500

@map_bp.route('/water-paths/<city>', methods=['GET'])
@jwt_required()
def get_water_paths(city):
    """Obtenir les chemins d'eau (rivières, canaux, drainage)"""
    try:
        city = city.lower()
        
        if city == 'dakar':
            water_paths = [
                {
                    'id': 'river-1',
                    'name': 'Fleuve Sénégal',
                    'type': 'natural_river',
                    'coordinates': [[-17.5000, 14.8000], [-17.4000, 14.7500]],
                    'width_m': 500,
                    'flow_rate': 'seasonal',
                    'quality': 'degraded'
                },
                {
                    'id': 'canal-1',
                    'name': 'Canal de drainage Grand Yoff',
                    'type': 'constructed_canal',
                    'coordinates': [[-17.4800, 14.6900], [-17.4600, 14.7000]],
                    'width_m': 8,
                    'flow_rate': 'variable',
                    'quality': 'poor',
                    'maintenance_needed': True
                },
                {
                    'id': 'drainage-1',
                    'name': 'Système di drainage Médina',
                    'type': 'drainage_system',
                    'coordinates': [[-17.4700, 14.7000], [-17.4500, 14.7200]],
                    'width_m': 2,
                    'flow_rate': 'seasonal',
                    'quality': 'poor'
                }
            ]
        else:  # Abidjan
            water_paths = [
                {
                    'id': 'lagoon-ebrie',
                    'name': 'Lagune Ébrié',
                    'type': 'lagoon',
                    'coordinates': [[-4.0500, 5.3000], [-3.9000, 5.4000]],
                    'surface_km2': 570,
                    'average_depth_m': 3.5,
                    'quality': 'degraded',
                    'flood_risk': 'high'
                },
                {
                    'id': 'canal-ebrie',
                    'name': 'Canal de Vridi',
                    'type': 'constructed_canal',
                    'coordinates': [[-4.0300, 5.3200], [-4.0100, 5.3500]],
                    'width_m': 350,
                    'flow_rate': 'tidal',
                    'quality': 'poor'
                }
            ]
        
        return jsonify({
            'city': city,
            'water_paths': water_paths,
            'total_paths': len(water_paths),
            'last_updated': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Water paths error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve water paths'}), 500

@map_bp.route('/heatmap/<city>', methods=['GET'])
@jwt_required()
def get_heatmap_data(city):
    """Obtenir données pour heatmap (densité de population, demande eau, etc.)"""
    try:
        city = city.lower()
        heatmap_type = request.args.get('type', 'population_density')
        
        if city == 'dakar':
            center = {'lat': 14.7167, 'lon': -17.4674}
            points = [
                {'lat': 14.7167, 'lon': -17.4674, 'value': 85, 'label': 'Dakar Centre'},
                {'lat': 14.7200, 'lon': -17.4500, 'value': 72, 'label': 'Plateau'},
                {'lat': 14.6900, 'lon': -17.4800, 'value': 65, 'label': 'Médina'},
                {'lat': 14.7400, 'lon': -17.5200, 'value': 45, 'label': 'Ouakam'},
                {'lat': 14.7500, 'lon': -17.4200, 'value': 55, 'label': 'Thiaroye'}
            ]
        else:  # Abidjan
            center = {'lat': 5.3364, 'lon': -4.0283}
            points = [
                {'lat': 5.3364, 'lon': -4.0283, 'value': 88, 'label': 'Plateau'},
                {'lat': 5.3600, 'lon': -4.0100, 'value': 78, 'label': 'Cocody'},
                {'lat': 5.3200, 'lon': -4.0500, 'value': 82, 'label': 'Treichville'},
                {'lat': 5.3000, 'lon': -3.9500, 'value': 65, 'label': 'Yopougon'},
                {'lat': 5.2800, 'lon': -4.0100, 'value': 58, 'label': 'Marcory'}
            ]
        
        return jsonify({
            'city': city,
            'heatmap_type': heatmap_type,
            'center': center,
            'zoom': 12,
            'radius': 50,
            'blur': 15,
            'max_zoom': 1,
            'points': points
        }), 200
    
    except Exception as e:
        logger.error(f'Heatmap error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve heatmap data'}), 500

@map_bp.route('/infrastructure/<city>', methods=['GET'])
@jwt_required()
def get_infrastructure_locations(city):
    """Obtenir localisation de toutes les infrastructures"""
    try:
        city = city.lower()
        
        if city == 'dakar':
            infrastructure = [
                {'id': 'pump-1', 'name': 'Station de pompage Dakar Centre', 'type': 'pumping_station', 'lat': 14.7167, 'lon': -17.4674, 'status': 'operational', 'capacity': 500000},
                {'id': 'treatment-1', 'name': 'Usine de traitement eau potable', 'type': 'treatment_plant', 'lat': 14.7250, 'lon': -17.5200, 'status': 'operational', 'capacity': 450000},
                {'id': 'reservoir-1', 'name': 'Réservoir Dakar', 'type': 'reservoir', 'lat': 14.7400, 'lon': -17.4900, 'status': 'operational', 'capacity': 50000},
                {'id': 'wastewater-1', 'name': 'Station traitement eaux usées', 'type': 'wastewater_plant', 'lat': 14.6800, 'lon': -17.5000, 'status': 'operational', 'capacity': 280000}
            ]
        else:  # Abidjan
            infrastructure = [
                {'id': 'pump-abj-1', 'name': 'Station de pompage Plateau', 'type': 'pumping_station', 'lat': 5.3364, 'lon': -4.0283, 'status': 'operational', 'capacity': 800000},
                {'id': 'treatment-abj-1', 'name': 'Usine de traitement Abidjan', 'type': 'treatment_plant', 'lat': 5.3450, 'lon': -4.0200, 'status': 'operational', 'capacity': 750000},
                {'id': 'reservoir-abj-1', 'name': 'Réservoir Cocody', 'type': 'reservoir', 'lat': 5.3600, 'lon': -4.0100, 'status': 'operational', 'capacity': 100000},
                {'id': 'wastewater-abj-1', 'name': 'Station traitement eaux usées Abidjan', 'type': 'wastewater_plant', 'lat': 5.3200, 'lon': -4.0500, 'status': 'operational', 'capacity': 550000}
            ]
        
        return jsonify({
            'city': city,
            'total_infrastructure': len(infrastructure),
            'infrastructure': infrastructure
        }), 200
    
    except Exception as e:
        logger.error(f'Infrastructure locations error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve infrastructure locations'}), 500

@map_bp.route('/risk-overlay/<city>', methods=['GET'])
@jwt_required()
def get_risk_overlay(city):
    """Obtenir couche overlay de risques combinés"""
    try:
        city = city.lower()
        
        risk_data = {
            'city': city,
            'risk_types': ['flood', 'drought', 'contamination', 'infrastructure'],
            'zones': [
                {
                    'id': 'zone-1',
                    'name': 'High Risk Zone 1',
                    'lat': 14.7000 if city == 'dakar' else 5.3300,
                    'lon': -17.4800 if city == 'dakar' else -4.0300,
                    'risk_score': 85,
                    'flood_risk': 35,
                    'drought_risk': 15,
                    'contamination_risk': 25,
                    'infrastructure_risk': 35
                },
                {
                    'id': 'zone-2',
                    'name': 'Medium Risk Zone',
                    'lat': 14.7300 if city == 'dakar' else 5.3600,
                    'lon': -17.4500 if city == 'dakar' else -4.0100,
                    'risk_score': 55,
                    'flood_risk': 20,
                    'drought_risk': 10,
                    'contamination_risk': 15,
                    'infrastructure_risk': 20
                }
            ]
        }
        
        return jsonify(risk_data), 200
    
    except Exception as e:
        logger.error(f'Risk overlay error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve risk overlay'}), 500
