"""
Routes pour statistiques - BRAINBLUE URBAIN
"""

from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required
import logging
from datetime import datetime, timedelta
import random

statistics_bp = Blueprint('statistics', __name__)
logger = logging.getLogger(__name__)

@statistics_bp.route('/dashboard/<city>', methods=['GET'])
@jwt_required()
def get_dashboard_stats(city):
    """Obtenir les statistiques du dashboard principal"""
    try:
        city = city.lower()
        
        if city == 'dakar':
            stats = {
                'city': 'Dakar',
                'overview': {
                    'population_total': 1060000,
                    'population_served': 833000,
                    'water_access_percent': 78.5,
                    'sanitation_coverage_percent': 71.2,
                    'water_quality_score': 82
                },
                'water_infrastructure': {
                    'total_networks': 23,
                    'operational': 21,
                    'maintenance': 2,
                    'total_pipes_km': 892,
                    'pipe_age_avg_years': 18.5,
                    'water_loss_percent': 18.5
                },
                'daily_operations': {
                    'total_production': 680000,
                    'production_capacity': 900000,
                    'capacity_utilization_percent': 75.6,
                    'peak_hour_demand': 920000,
                    'supply_disruptions_active': 2,
                    'average_pressure_bar': 5.3
                },
                'quality_metrics': {
                    'turbidity_ntu_avg': 0.8,
                    'ph_avg': 7.2,
                    'chlorine_mg_l': 0.6,
                    'bacteria_detected_today': 0,
                    'quality_compliance_percent': 96.5
                },
                'financial': {
                    'revenue_usd_daily': 42000,
                    'operational_cost_daily': 28000,
                    'maintenance_budget_monthly': 150000,
                    'pending_invoices': 850000,
                    'collections_percent': 71.3
                }
            }
        else:  # Abidjan
            stats = {
                'city': 'Abidjan',
                'overview': {
                    'population_total': 4200000,
                    'population_served': 3444000,
                    'water_access_percent': 82.3,
                    'sanitation_coverage_percent': 75.8,
                    'water_quality_score': 85
                },
                'water_infrastructure': {
                    'total_networks': 42,
                    'operational': 40,
                    'maintenance': 2,
                    'total_pipes_km': 2145,
                    'pipe_age_avg_years': 16.2,
                    'water_loss_percent': 15.2
                },
                'daily_operations': {
                    'total_production': 1850000,
                    'production_capacity': 2200000,
                    'capacity_utilization_percent': 84.1,
                    'peak_hour_demand': 2450000,
                    'supply_disruptions_active': 1,
                    'average_pressure_bar': 5.7
                },
                'quality_metrics': {
                    'turbidity_ntu_avg': 0.6,
                    'ph_avg': 7.3,
                    'chlorine_mg_l': 0.65,
                    'bacteria_detected_today': 0,
                    'quality_compliance_percent': 97.8
                },
                'financial': {
                    'revenue_usd_daily': 185000,
                    'operational_cost_daily': 98000,
                    'maintenance_budget_monthly': 450000,
                    'pending_invoices': 2450000,
                    'collections_percent': 76.5
                }
            }
        
        return jsonify(stats), 200
    
    except Exception as e:
        logger.error(f'Dashboard stats error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve dashboard statistics'}), 500

@statistics_bp.route('/sdg6/<city>', methods=['GET'])
@jwt_required()
def get_sdg6_indicators(city):
    """Obtenir indicateurs SDG 6 (Eau propre et assainissement)"""
    try:
        city = city.lower()
        
        if city == 'dakar':
            sdg6 = {
                'indicator_6_1_1': {
                    'name': 'Safe drinking water',
                    'value_percent': 78.5,
                    'target_2030': 90,
                    'progress_percent': 87.2,
                    'status': 'on_track',
                    'trend': 'improving'
                },
                'indicator_6_2_1': {
                    'name': 'Adequate sanitation and hygiene',
                    'value_percent': 71.2,
                    'target_2030': 85,
                    'progress_percent': 83.8,
                    'status': 'on_track',
                    'trend': 'improving'
                },
                'indicator_6_3_1': {
                    'name': 'Water quality index',
                    'value_percent': 82,
                    'target_2030': 90,
                    'progress_percent': 91.1,
                    'status': 'on_track',
                    'trend': 'stable'
                },
                'indicator_6_4_1': {
                    'name': 'Water use efficiency',
                    'value_percent': 65.3,
                    'target_2030': 75,
                    'progress_percent': 87.1,
                    'status': 'on_track',
                    'trend': 'improving'
                },
                'indicator_6_5_1': {
                    'name': 'Transboundary water cooperation',
                    'value_percent': 60,
                    'target_2030': 80,
                    'progress_percent': 75,
                    'status': 'off_track',
                    'trend': 'stable'
                },
                'indicator_6_6_1': {
                    'name': 'Water-related ecosystems protection',
                    'value_percent': 55.3,
                    'target_2030': 75,
                    'progress_percent': 73.7,
                    'status': 'off_track',
                    'trend': 'improving'
                }
            }
        else:  # Abidjan
            sdg6 = {
                'indicator_6_1_1': {'name': 'Safe drinking water', 'value_percent': 82.3, 'target_2030': 90, 'progress_percent': 91.4, 'status': 'on_track', 'trend': 'improving'},
                'indicator_6_2_1': {'name': 'Adequate sanitation and hygiene', 'value_percent': 75.8, 'target_2030': 85, 'progress_percent': 89.2, 'status': 'on_track', 'trend': 'improving'},
                'indicator_6_3_1': {'name': 'Water quality index', 'value_percent': 85, 'target_2030': 90, 'progress_percent': 94.4, 'status': 'on_track', 'trend': 'improving'},
                'indicator_6_4_1': {'name': 'Water use efficiency', 'value_percent': 68.5, 'target_2030': 75, 'progress_percent': 91.3, 'status': 'on_track', 'trend': 'improving'},
                'indicator_6_5_1': {'name': 'Transboundary water cooperation', 'value_percent': 65, 'target_2030': 80, 'progress_percent': 81.3, 'status': 'on_track', 'trend': 'improving'},
                'indicator_6_6_1': {'name': 'Water-related ecosystems protection', 'value_percent': 62.5, 'target_2030': 75, 'progress_percent': 83.3, 'status': 'on_track', 'trend': 'improving'}
            }
        
        return jsonify({
            'city': city,
            'sdg': 'SDG 6 - Clean Water and Sanitation',
            'indicators': sdg6,
            'overall_achievement_percent': sum(v['value_percent'] for v in sdg6.values()) / len(sdg6),
            'on_track_indicators': len([v for v in sdg6.values() if v['status'] == 'on_track']),
            'off_track_indicators': len([v for v in sdg6.values() if v['status'] == 'off_track']),
            'last_updated': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'SDG6 indicators error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve SDG6 indicators'}), 500

@statistics_bp.route('/trends/<city>', methods=['GET'])
@jwt_required()
def get_trends(city):
    """Obtenir les tendances sur 30 jours"""
    try:
        city = city.lower()
        period_days = int(request.args.get('period', 30))
        
        # Générer données de tendances
        trend_data = []
        base_value = 680000 if city == 'dakar' else 1850000
        
        for day in range(period_days):
            date = datetime.utcnow() - timedelta(days=period_days - day - 1)
            trend_data.append({
                'date': date.date().isoformat(),
                'daily_production': round(base_value * (0.9 + random.uniform(-0.1, 0.2)), 0),
                'daily_demand': round(base_value * (0.85 + random.uniform(-0.08, 0.15)), 0),
                'avg_pressure': round(5.3 + random.uniform(-0.5, 0.5), 2),
                'water_quality_score': round(82 + random.uniform(-3, 5), 1),
                'system_uptime_percent': round(98 + random.uniform(-3, 1.5), 1)
            })
        
        return jsonify({
            'city': city,
            'period_days': period_days,
            'trend_data': trend_data,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Trends error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve trends'}), 500

@statistics_bp.route('/comparison', methods=['GET'])
@jwt_required()
def compare_cities():
    """Comparer les deux villes pilotes"""
    try:
        return jsonify({
            'comparison': {
                'dakar': {
                    'population': 1060000,
                    'water_access': 78.5,
                    'sanitation': 71.2,
                    'water_loss': 18.5,
                    'quality_score': 82,
                    'infrastructure_age': 18.5
                },
                'abidjan': {
                    'population': 4200000,
                    'water_access': 82.3,
                    'sanitation': 75.8,
                    'water_loss': 15.2,
                    'quality_score': 85,
                    'infrastructure_age': 16.2
                }
            },
            'better_performance': {
                'water_access': 'Abidjan',
                'sanitation': 'Abidjan',
                'water_loss': 'Abidjan',
                'quality': 'Abidjan',
                'infrastructure': 'Abidjan'
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Comparison error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve city comparison'}), 500

@statistics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Résumé global de la plateforme"""
    try:
        return jsonify({
            'platform': 'BRAINBLUE URBAIN',
            'total_cities': 2,
            'cities': ['Dakar', 'Abidjan'],
            'total_population_served': 2900000,
            'total_networks': 65,
            'total_infrastructure_km': 3037,
            'total_predictions_generated': 50000,
            'platform_uptime_percent': 99.7,
            'data_update_frequency': '5 minutes',
            'last_full_sync': (datetime.utcnow() - timedelta(minutes=2)).isoformat(),
            'active_users': 157,
            'total_registered_users': 892
        }), 200
    
    except Exception as e:
        logger.error(f'Summary error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve summary'}), 500
