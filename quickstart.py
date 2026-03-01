#!/usr/bin/env python
"""
BRAINBLUE URBAIN - Quick Start Script
Lance l'application en mode développement
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

def print_header():
    """Afficher bannère"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║          🌊 BRAINBLUE URBAIN - Quick Start 🌊                ║
    ║     Plateforme SIG pour Gestion Intégrée de l'Eau Urbaine    ║
    ║                    Lancement Automatique                      ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Vérifier Python"""
    print("✓ Python version:", platform.python_version())

def launch_frontend():
    """Lancer serveur frontend"""
    print("\n📱 Démarrage Frontend...")
    print("   URL: http://localhost:8000")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("   ❌ Dossier frontend non trouvé")
        return None
    
    # Lancer simple serveur HTTP
    try:
        if platform.system() == "Windows":
            subprocess.Popen(
                ["python", "-m", "http.server", "8000", "--directory", "frontend"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            subprocess.Popen(
                ["python3", "-m", "http.server", "8000", "--directory", "frontend"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        print("   ✅ Frontend démarré")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def launch_backend():
    """Lancer serveur backend"""
    print("\n🔧 Démarrage Backend...")
    print("   URL: http://localhost:5000")
    print("   Health: http://localhost:5000/api/health")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("   ❌ Dossier backend non trouvé")
        return None
    
    try:
        if platform.system() == "Windows":
            subprocess.Popen(
                ["python", "app.py"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            subprocess.Popen(
                ["python3", "app.py"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        print("   ✅ Backend démarré")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Main"""
    print_header()
    
    print("📋 Vérifications préalables...")
    check_python()
    
    print("\n🚀 Lancement des services...")
    
    backend_ok = launch_backend()
    time.sleep(2)
    frontend_ok = launch_frontend()
    
    if backend_ok and frontend_ok:
        print("\n" + "="*60)
        print("✨ BRAINBLUE URBAIN EST PRÊT!")
        print("="*60)
        print("\n📦 Services actifs:")
        print("   Frontend:  http://localhost:8000")
        print("   Backend:   http://localhost:5000/api")
        print("   Health:    http://localhost:5000/api/health")
        print("   Info:      http://localhost:5000/api/info")
        print("\n🔐 Test Login:")
        print("   Email: john@brainblue.io")
        print("   Password: password123")
        print("\n⚠️  Appuyez Ctrl+C pour arrêter\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Application arrêtée")
    else:
        print("\n❌ Erreur au démarrage")
        sys.exit(1)

if __name__ == '__main__':
    main()
