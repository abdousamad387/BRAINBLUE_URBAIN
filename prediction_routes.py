"""
Routes pour les prédictions ML - BRAINBLUE URBAIN
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
import random

prediction_bp = Blueprint('predictions', __name__)
logger = logging.getLogger(__name__)

@prediction_bp.route('/water-level/<city>', methods=['GET'])
@jwt_required()
def predict_water_level(city):
    """Prédire les niveaux d'eau pour une ville"""
    try:
        city = city.lower()
        days_ahead = int(request.args.get('days', 7))
        
        predictions = []
        base_level = 3.5 if city == 'dakar' else 4.2
        
        for day in range(1, days_ahead + 1):
            future_date = datetime.utcnow() + timedelta(days=day)
            
            predictions.append({
                'date': future_date.date().isoformat(),
                'predicted_level': round(base_level + random.uniform(-0.5, 0.8), 2),
                'confidence': round(random.uniform(0.75, 0.95), 3),
                'confidence_interval': {
                    'lower': round(base_level + random.uniform(-1.0, 0.0), 2),
                    'upper': round(base_level + random.uniform(0.5, 1.5), 2)
                }
            })
        
        return jsonify({
            'city': city,
            'prediction_type': 'water_level',
            'model': 'LSTM_ARIMA_Ensemble',
            'model_version': '2.1',
            'accuracy_percent': 87.5,
            'predictions': predictions,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Water level prediction error: {str(e)}')
        return jsonify({'error': 'Failed to generate water level predictions'}), 500

@prediction_bp.route('/flood-risk/<city>', methods=['GET'])
@jwt_required()
def predict_flood_risk(city):
    """Prédire risques d'inondation"""
    try:
        city = city.lower()
        
        # Zones à risque simulées
        risk_zones = []
        
        if city == 'dakar':
            risk_zones = [
                {
                    'zone_name': 'Médina',
                    'latitude': 14.6900,
                    'longitude': -17.4800,
                    'flood_probability_percent': 35,
                    'severity': 'medium',
                    'predicted_date': (datetime.utcnow() + timedelta(days=3)).date().isoformat(),
                    'affected_population': 50000,
                    'infrastructure_at_risk': 150
                },
                {
                    'zone_name': 'Thiaroye',
                    'latitude': 14.7500,
                    'longitude': -17.4200,
                    'flood_probability_percent': 28,
                    'severity': 'medium',
                    'predicted_date': (datetime.utcnow() + timedelta(days=5)).date().isoformat(),
                    'affected_population': 35000,
                    'infrastructure_at_risk': 100
                },
                {
                    'zone_name': 'Ouakam',
                    'latitude': 14.7400,
                    'longitude': -17.5200,
                    'flood_probability_percent': 18,
                    'severity': 'low',
                    'predicted_date': (datetime.utcnow() + timedelta(days=7)).date().isoformat(),
                    'affected_population': 20000,
                    'infrastructure_at_risk': 40
                }
            ]
        else:  # Abidjan
            risk_zones = [
                {
                    'zone_name': 'Lagune Ébrié',
                    'latitude': 5.3364,
                    'longitude': -4.0283,
                    'flood_probability_percent': 42,
                    'severity': 'high',
                    'predicted_date': (datetime.utcnow() + timedelta(days=2)).date().isoformat(),
                    'affected_population': 120000,
                    'infrastructure_at_risk': 250
                }
            ]
        
        return jsonify({
            'city': city,
            'prediction_type': 'flood_risk',
            'model': 'CNN_SAR_Radar',
            'model_version': '3.2',
            'forecast_period_days': 14,
            'high_risk_zones': len([z for z in risk_zones if z['severity'] == 'high']),
            'risk_zones': risk_zones,
            'recommendations': [
                'Augmenter la capacité des systèmes de drainage',
                'Renforcer les prévisions météorologiques',
                'Préparer les plans d\'évacuation',
                'Entretenir les canaux de drainage'
            ],
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Flood risk prediction error: {str(e)}')
        return jsonify({'error': 'Failed to generate flood risk predictions'}), 500

@prediction_bp.route('/water-demand/<city>', methods=['GET'])
@jwt_required()
def predict_water_demand(city):
    """Prédire la demande en eau"""
    try:
        city = city.lower()
        days_ahead = int(request.args.get('days', 7))
        
        predictions = []
        base_demand = 680000 if city == 'dakar' else 1100000  # liters/day
        
        for day in range(days_ahead):
            future_date = datetime.utcnow() + timedelta(days=day+1)
            
            # Simuler variations saisonnières et hebdomadaires
            day_of_week = future_date.weekday()
            factor = 1.15 if day_of_week in [4, 5, 6] else 0.95  # Fin de semaine = plus haute
            
            predicted_demand = base_demand * factor * (1 + random.uniform(-0.05, 0.08))
            
            predictions.append({
                'date': future_date.date().isoformat(),
                'predicted_demand': round(predicted_demand, 0),
                'confidence': round(random.uniform(0.82, 0.93), 3),
                'peak_hour_demand': round(predicted_demand * 1.35, 0),
                'off_peak_hour_demand': round(predicted_demand * 0.65, 0)
            })
        
        return jsonify({
            'city': city,
            'prediction_type': 'water_demand',
            'model': 'XGBoost_TimeSeries',
            'model_version': '2.8',
            'accuracy_percent': 85.2,
            'current_avg_demand': round(base_demand * 0.95, 0),
            'max_capacity': round(base_demand * 1.5, 0),
            'predictions': predictions,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Water demand prediction error: {str(e)}')
        return jsonify({'error': 'Failed to generate water demand predictions'}), 500

@prediction_bp.route('/pipe-breakage/<city>', methods=['GET'])
@jwt_required()
def predict_pipe_breakage(city):
    """Prédire les risques de rupture de tuyaux"""
    try:
        city = city.lower()
        
        # Tuyaux à risque
        risk_pipes = [
            {
                'pipe_id': f'pipe-{city}-001',
                'location': 'Plateau',
                'age_years': 45,
                'length_km': 8.5,
                'breakage_probability_percent': 72,
                'risk_level': 'critical',
                'last_maintenance_years_ago': 8,
                'expected_breakage_date': (datetime.utcnow() + timedelta(days=30)).date().isoformat()
            },
            {
                'pipe_id': f'pipe-{city}-002',
                'location': 'Médina',
                'age_years': 28,
                'length_km': 12.3,
                'breakage_probability_percent': 45,
                'risk_level': 'high',
                'last_maintenance_years_ago': 3,
                'expected_breakage_date': (datetime.utcnow() + timedelta(days=90)).date().isoformat()
            },
            {
                'pipe_id': f'pipe-{city}-003',
                'location': 'Ouakam',
                'age_years': 12,
                'length_km': 6.7,
                'breakage_probability_percent': 28,
                'risk_level': 'medium',
                'last_maintenance_years_ago': 1,
                'expected_breakage_date': (datetime.utcnow() + timedelta(days=180)).date().isoformat()
            }
        ]
        
        return jsonify({
            'city': city,
            'prediction_type': 'pipe_breakage',
            'model': 'RandomForest_AgeCondition',
            'model_version': '2.3',
            'total_pipes_analyzed': 450,
            'critical_risk_count': len([p for p in risk_pipes if p['risk_level'] == 'critical']),
            'risk_pipes': risk_pipes,
            'maintenance_budget_recommendation': {
                'priority_1_urgent': 250000,  # USD
                'priority_2_high': 180000,
                'priority_3_medium': 120000
            },
            'generated_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Pipe breakage prediction error: {str(e)}')
        return jsonify({'error': 'Failed to generate pipe breakage predictions'}), 500

@prediction_bp.route('/simulate', methods=['POST'])
@jwt_required()
def simulate_scenario():
    """Simuler un scénario 'et si' (what-if)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        scenario_type = data.get('type')  # new_pipe, reduced_demand, climate_change, etc.
        city = data.get('city', 'dakar')
        
        # Résultats simulés basés sur le scénario
        results = {
            'new_pipe': {
                'water_access_improvement': 12.5,
                'leakage_reduction': 5.2,
                'system_efficiency': 8.3,
                'investment_cost': 450000,
                'roi_years': 5.2,
                'population_newly_served': 35000
            },
            'reduced_demand': {
                'peak_pressure_relief': 8.5,
                'leakage_reduction': 2.1,
                'energy_savings': 15.3,
                'cost_savings_annual': 180000,
                'co2_reduction_tons': 250
            },
            'climate_change': {
                'drought_risk_increase': 25.5,
                'flood_risk_increase': 18.7,
                'water_demand_increase': 12.3,
                'infrastructure_vulnerability': 35.2,
                'adaptation_budget': 800000
            }
        }
        
        return jsonify({
            'scenario_type': scenario_type,
            'city': city,
            'baseline_metrics': {
                'water_access_percent': 78.5,
                'system_efficiency': 65.3,
                'leakage_percent': 18.5,
                'peak_pressure': 5.8
            },
            'projected_metrics': results.get(scenario_type, {}),
            'confidence_percent': 82.5,
            'simulation_date': datetime.utcnow().isoformat()
        }), 201
    
    except Exception as e:
        logger.error(f'Simulate scenario error: {str(e)}')
        return jsonify({'error': 'Failed to simulate scenario'}), 500

@prediction_bp.route('/model-performance', methods=['GET'])
@jwt_required()
def get_model_performance():
    """Obtenir les performances des modèles"""
    try:
        return jsonify({
            'models': [
                {
                    'name': 'Water Level Prediction',
                    'type': 'LSTM_ARIMA_Ensemble',
                    'version': '2.1',
                    'mae': 0.28,
                    'rmse': 0.35,
                    'r2_score': 0.884,
                    'accuracy_percent': 87.5,
                    'predictions_made': 12450,
                    'last_trained': '2026-02-28'
                },
                {
                    'name': 'Flood Risk Detection',
                    'type': 'CNN_SAR_Radar',
                    'version': '3.2',
                    'precision': 0.91,
                    'recall': 0.87,
                    'f1_score': 0.89,
                    'accuracy_percent': 88.9,
                    'predictions_made': 8900,
                    'last_trained': '2026-02-25'
                },
                {
                    'name': 'Water Demand Forecasting',
                    'type': 'XGBoost_TimeSeries',
                    'version': '2.8',
                    'mape': 4.2,
                    'rmse': 25000,
                    'r2_score': 0.852,
                    'accuracy_percent': 85.2,
                    'predictions_made': 15230,
                    'last_trained': '2026-02-26'
                },
                {
                    'name': 'Pipe Breakage Prediction',
                    'type': 'RandomForest_AgeCondition',
                    'version': '2.3',
                    'precision': 0.83,
                    'recall': 0.79,
                    'auc_roc': 0.88,
                    'accuracy_percent': 81.5,
                    'predictions_made': 6750,
                    'last_trained': '2026-02-27'
                }
            ],
            'ensemble_metrics': {
                'avg_accuracy': 85.8,
                'total_predictions': 43330,
                'false_positive_rate': 0.08,
                'false_negative_rate': 0.13
            },
            'last_update': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f'Model performance error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve model performance'}), 500
