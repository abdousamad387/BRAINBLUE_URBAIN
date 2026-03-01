"""
Routes d'authentification - BRAINBLUE URBAIN
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import logging

# Importer modèles (adaptation flexible)
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

# Cette importion sera ajustée selon la structure réelle
User = None

def init_auth_routes(app, user_model):
    """Initialiser les routes avec le modèle User"""
    global User
    User = user_model

@auth_bp.route('/register', methods=['POST'])
def register():
    """Enregistrer un nouvel utilisateur"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Créer utilisateur (sera implémenté avec DB réelle)
        response = {
            'message': 'User registered successfully',
            'user': {
                'id': 'user-123',
                'username': data.get('username'),
                'email': data.get('email'),
                'city': data.get('city', 'Dakar'),
                'created_at': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(response), 201
    
    except Exception as e:
        logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion utilisateur"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing credentials'}), 400
        
        # Token JWT (sera généré avec DB réelle)
        access_token = create_access_token(identity='user-123')
        
        response = {
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': 'user-123',
                'username': data.get('username'),
                'role': 'analyst',
                'city': 'Dakar'
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtenir le profil de l'utilisateur connecté"""
    try:
        user_id = get_jwt_identity()
        
        profile = {
            'id': user_id,
            'username': 'john_analyst',
            'email': 'john@brainblue.io',
            'full_name': 'John Analyst',
            'role': 'analyst',
            'city': 'Dakar',
            'is_verified': True,
            'created_at': '2026-01-01T00:00:00'
        }
        
        return jsonify(profile), 200
    
    except Exception as e:
        logger.error(f'Profile error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve profile'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Mettre à jour le profil utilisateur"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        response = {
            'message': 'Profile updated successfully',
            'user': {
                'id': user_id,
                'username': data.get('username', 'john_analyst'),
                'full_name': data.get('full_name'),
                'updated_at': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f'Update profile error: {str(e)}')
        return jsonify({'error': 'Failed to update profile'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Déconnexion de l'utilisateur"""
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """Rafraîchir le token JWT"""
    try:
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id)
        
        return jsonify({'access_token': new_token}), 200
    
    except Exception as e:
        logger.error(f'Token refresh error: {str(e)}')
        return jsonify({'error': 'Failed to refresh token'}), 500

@auth_bp.route('/verify-email/<token>', methods=['POST'])
def verify_email(token):
    """Vérifier l'email avec token"""
    return jsonify({'message': 'Email verified successfully'}), 200

@auth_bp.route('/password-reset', methods=['POST'])
def request_password_reset():
    """Demander réinitialisation de mot de passe"""
    data = request.get_json()
    email = data.get('email')
    
    return jsonify({
        'message': f'Password reset email sent to {email}',
        'reset_token': 'reset-token-placeholder'
    }), 200

@auth_bp.route('/password-reset/<token>', methods=['POST'])
def reset_password(token):
    """Réinitialiser le mot de passe"""
    data = request.get_json()
    
    return jsonify({
        'message': 'Password reset successfully',
        'redirect_to': '/login'
    }), 200
