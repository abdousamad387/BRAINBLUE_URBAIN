// BRAINBLUE URBAIN - Application React principale
// Configuration complète avec navigation, dashboards, cartes interactives

const { useState, useEffect, useRef, useCallback } = React;

// Configuration de l'API
const API_BASE_URL = 'http://localhost:5000/api';
const API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

// Client API
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_TOKEN}`
    }
});

// ============ COMPOSANTS RÉUTILISABLES ============

// Loader
function Loader() {
    return (
        <div className="d-flex justify-content-center align-items-center" style={{height: '200px'}}>
            <div className="loader"></div>
        </div>
    );
}

// Stat Box
function StatBox({ icon, label, value, change, color = 'primary' }) {
    return (
        <div className={`stat-box ${color}`}>
            <div className="stat-icon">
                <i className={`bi ${icon}`}></i>
            </div>
            <div className="stat-value">{value}</div>
            <div className="stat-label">{label}</div>
            {change && (
                <small className={change > 0 ? 'text-success' : 'text-danger'}>
                    <i className={`bi bi-arrow-${change > 0 ? 'up' : 'down'}`}></i>
                    {Math.abs(change)}%
                </small>
            )}
        </div>
    );
}

// Cartes Interactives
function MapComponent({ city, mapId }) {
    const mapRef = useRef(null);
    const mapInstance = useRef(null);
    
    useEffect(() => {
        if (!mapRef.current) return;
        
        // Coordonnées des villes
        const cities = {
            dakar: { lat: 14.7167, lon: -17.4674, zoom: 13 },
            abidjan: { lat: 5.3364, lon: -4.0283, zoom: 12 }
        };
        
        const cityData = cities[city] || cities.dakar;
        
        // Initialiser Leaflet
        if (!mapInstance.current) {
            mapInstance.current = L.map(mapId).setView(
                [cityData.lat, cityData.lon],
                cityData.zoom
            );
            
            // Ajouter tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(mapInstance.current);
            
            // Ajouter marqueurs d'infrastructures
            const infrastructure = [
                { name: 'Station de pompage', lat: cityData.lat, lon: cityData.lon, icon: 'water' },
                { name: 'Usine de traitement', lat: cityData.lat + 0.05, lon: cityData.lon + 0.05, icon: 'gear' },
                { name: 'Réservoir', lat: cityData.lat - 0.03, lon: cityData.lon + 0.03, icon: 'droplet' }
            ];
            
            infrastructure.forEach(item => {
                const marker = L.circleMarker(
                    [item.lat, item.lon],
                    {
                        radius: 8,
                        fillColor: '#0066cc',
                        color: '#fff',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    }
                ).addTo(mapInstance.current);
                
                marker.bindPopup(`<b>${item.name}</b><br/>Status: Operational`);
            });
            
            // Zones à risque
            const riskZones = city === 'dakar'
                ? [
                    { lat: 14.6900, lon: -17.4800, name: 'Médina - Zone inondable' },
                    { lat: 14.7500, lon: -17.4200, name: 'Thiaroye - Zone à risque' }
                  ]
                : [
                    { lat: 5.3364, lon: -4.0283, name: 'Lagune Ébrié - Très haut risque' }
                  ];
            
            riskZones.forEach(zone => {
                L.circleMarker(
                    [zone.lat, zone.lon],
                    {
                        radius: 12,
                        fillColor: '#d62828',
                        color: '#fff',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.6,
                        dashArray: '5, 5'
                    }
                ).addTo(mapInstance.current)
                .bindPopup(`<b>${zone.name}</b><br/><i class="bi bi-exclamation-triangle"></i> Risque d'inondation`);
            });
        }
        
        return () => {
            // Cleanup
        };
    }, [city, mapId]);
    
    return <div id={mapId} className="map-container"></div>;
}

// Dashboard Dakar
function DakarDashboard() {
    const [stats, setStats] = useState(null);
    const [predictions, setPredictions] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedMetric, setSelectedMetric] = useState('water-level');
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [statsRes, predRes] = await Promise.all([
                    apiClient.get('/statistics/dashboard/dakar'),
                    apiClient.get('/predictions/water-level/dakar')
                ]);
                setStats(statsRes.data);
                setPredictions(predRes.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
        const interval = setInterval(fetchData, 300000); // Mettre à jour toutes les 5 minutes
        
        return () => clearInterval(interval);
    }, []);
    
    if (loading) return <Loader />;
    
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-geo-alt-fill"></i> Tableau de Bord Dakar
            </h1>
            
            {/* Stats principales */}
            <div className="row mb-4">
                <div className="col-md-3"><StatBox icon="bi-droplet" label="Accès à l'eau" value="78.5%" /></div>
                <div className="col-md-3"><StatBox icon="bi-pipe" label="Réseaux opérationnels" value="21/23" color="success" /></div>
                <div className="col-md-3"><StatBox icon="bi-percent" label="Utilisation capacité" value="75.6%" color="warning" /></div>
                <div className="col-md-3"><StatBox icon="bi-exclamation-triangle" label="Fuites détectées" value="18.5%" color="danger" /></div>
            </div>
            
            {/* Cartes et graphiques */}
            <div className="row">
                <div className="col-lg-6">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-map"></i> Carte - Réseaux d'eau</h6>
                        </div>
                        <div className="card-body p-0">
                            <MapComponent city="dakar" mapId="dakar-map" />
                        </div>
                    </div>
                </div>
                
                <div className="col-lg-6">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-graph-up"></i> Prédictions 7 jours</h6>
                        </div>
                        <div className="card-body">
                            <div className="chart-container">
                                <canvas id="dakar-prediction-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Alertes */}
            <div className="mt-4">
                <h5 className="mb-3"><i className="bi bi-exclamation-circle"></i> Alertes Actives</h5>
                <div className="alert-custom alert-warning">
                    <b><i className="bi bi-exclamation-triangle"></i> Chute de pression anormale</b> - Secteur Plateau détecté il y a 2 heures
                </div>
                <div className="alert-custom alert-danger">
                    <b><i className="bi bi-exclamation-circle"></i> Turbidité élevée</b> - Secteur Médina détecté il y a 1 heure
                </div>
            </div>
            
            {/* SDG 6 Indicators */}
            <div className="card-modern mt-4">
                <div className="card-header">
                    <h6><i className="bi bi-bullseye"></i> Indicateurs SDG 6</h6>
                </div>
                <div className="card-body">
                    <div className="row text-center">
                        <div className="col-md-4">
                            <h5>78.5%</h5>
                            <p>Eau potable sûre</p>
                            <div className="progress">
                                <div className="progress-bar bg-success" style={{width: '78.5%'}}></div>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <h5>71.2%</h5>
                            <p>Assainissement adéquat</p>
                            <div className="progress">
                                <div className="progress-bar bg-info" style={{width: '71.2%'}}></div>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <h5>82%</h5>
                            <p>Qualité de l'eau</p>
                            <div className="progress">
                                <div className="progress-bar bg-warning" style={{width: '82%'}}></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Dashboard Abidjan
function AbidjanDashboard() {
    const [stats, setStats] = useState(null);
    
    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await apiClient.get('/statistics/dashboard/abidjan');
                setStats(res.data);
            } catch (error) {
                console.error('Error:', error);
            }
        };
        
        fetchStats();
    }, []);
    
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-geo-alt-fill"></i> Tableau de Bord Abidjan
            </h1>
            
            <div className="row mb-4">
                <div className="col-md-3"><StatBox icon="bi-droplet" label="Accès à l'eau" value="82.3%" color="success" /></div>
                <div className="col-md-3"><StatBox icon="bi-pipe" label="Réseaux opérationnels" value="40/42" color="success" /></div>
                <div className="col-md-3"><StatBox icon="bi-percent" label="Utilisation capacité" value="84.1%" color="warning" /></div>
                <div className="col-md-3"><StatBox icon="bi-exclamation-triangle" label="Fuites détectées" value="15.2%" color="danger" /></div>
            </div>
            
            <div className="row">
                <div className="col-lg-6">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-map"></i> Carte - Réseaux d'eau</h6>
                        </div>
                        <div className="card-body p-0">
                            <MapComponent city="abidjan" mapId="abidjan-map" />
                        </div>
                    </div>
                </div>
                
                <div className="col-lg-6">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-graph-up"></i> État des Systèmes</h6>
                        </div>
                        <div className="card-body">
                            <ul className="list-unstyled">
                                <li className="mb-3">
                                    <span className="badge-custom badge-operational">Opérationnel</span>
                                    Station de pompage Plateau - 720,000 L/h
                                </li>
                                <li className="mb-3">
                                    <span className="badge-custom badge-operational">Opérationnel</span>
                                    Usine traitement Cocody - 750,000 L/h
                                </li>
                                <li className="mb-3">
                                    <span className="badge-custom badge-operational">Opérationnel</span>
                                    Réservoir Cocody - 100,000 L
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Page Prédictions IA
function PredictionsPage() {
    const [city, setCity] = useState('dakar');
    const [predictions, setPredictions] = useState(null);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        const fetchPredictions = async () => {
            try {
                setLoading(true);
                const res = await apiClient.get(`/predictions/water-level/${city}`);
                setPredictions(res.data);
            } catch (error) {
                console.error('Error:', error);
            } finally {
                setLoading(false);
            }
        };
        
        fetchPredictions();
    }, [city]);
    
    if (loading) return <Loader />;
    
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-robot"></i> Prédictions IA Avancées
            </h1>
            
            <div className="row mb-4">
                <div className="col-md-6 mb-3">
                    <label className="form-label">Sélectionner une ville</label>
                    <select className="form-control" value={city} onChange={(e) => setCity(e.target.value)}>
                        <option value="dakar">Dakar</option>
                        <option value="abidjan">Abidjan</option>
                    </select>
                </div>
                <div className="col-md-6 mb-3">
                    <label className="form-label">Type de prédiction</label>
                    <select className="form-control">
                        <option>Niveau d'eau</option>
                        <option>Demande en eau</option>
                        <option>Risques d'inondation</option>
                        <option>Ruptures de tuyaux</option>
                    </select>
                </div>
            </div>
            
            {/* Cartes de prédictions */}
            <div className="row">
                <div className="col-lg-8">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-graph-up"></i> Prédictions 7 jours - Niveau d'eau</h6>
                        </div>
                        <div className="card-body">
                            <div className="alert-custom alert-success">
                                <i className="bi bi-check-circle"></i>
                                <b>Modèle LSTM performant</b> - Précision: 87.5%, MAE: 0.28m
                            </div>
                            
                            {predictions && (
                                <div>
                                    <h6 className="mb-3">Prédictions détaillées:</h6>
                                    <table className="table table-custom">
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th>Niveau prédit (m)</th>
                                                <th>Confiance</th>
                                                <th>Intervalle</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {predictions.predictions && predictions.predictions.slice(0, 5).map((pred, idx) => (
                                                <tr key={idx}>
                                                    <td>{pred.date}</td>
                                                    <td><b>{pred.predicted_level}</b></td>
                                                    <td>{(pred.confidence * 100).toFixed(1)}%</td>
                                                    <td>[{pred.confidence_interval.lower}, {pred.confidence_interval.upper}]</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                
                <div className="col-lg-4">
                    <div className="card-modern mb-3">
                        <div className="card-header">
                            <h6><i className="bi bi-info-circle"></i> Modèles utilisés</h6>
                        </div>
                        <div className="card-body">
                            <ul className="list-unstyled">
                                <li className="mb-3">
                                    <b>LSTM Ensemble</b>
                                    <div className="progress mt-2">
                                        <div className="progress-bar" style={{width: '87.5%'}}></div>
                                    </div>
                                    <small>Accuracy: 87.5%</small>
                                </li>
                                <li className="mb-3">
                                    <b>XGBoost</b>
                                    <div className="progress mt-2">
                                        <div className="progress-bar bg-success" style={{width: '85.2%'}}></div>
                                    </div>
                                    <small>Accuracy: 85.2%</small>
                                </li>
                                <li className="mb-3">
                                    <b>CNN SAR</b>
                                    <div className="progress mt-2">
                                        <div className="progress-bar bg-info" style={{width: '88.9%'}}></div>
                                    </div>
                                    <small>Accuracy: 88.9%</small>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            {/* Simulation What-If */}
            <div className="card-modern mt-4">
                <div className="card-header">
                    <h6><i className="bi bi-gear"></i> Simulateur "Et Si ?" </h6>
                </div>
                <div className="card-body">
                    <div className="row">
                        <div className="col-md-6 mb-3">
                            <label className="form-label">Scénario à simuler</label>
                            <select className="form-control">
                                <option>Nouvelle canalisation</option>
                                <option>Réduction de demande</option>
                                <option>Changement climatique</option>
                                <option>Maintenance infrastructure</option>
                            </select>
                        </div>
                        <div className="col-md-6 mb-3">
                            <label className="form-label">Paramètre</label>
                            <input type="number" className="form-control" placeholder="Ex: 50 km de tuyaux" />
                        </div>
                    </div>
                    <button className="btn btn-primary-custom">
                        <i className="bi bi-play-circle"></i> Lancer simulation
                    </button>
                </div>
            </div>
        </div>
    );
}

// Page Statistiques SDG6
function StatisticsPage() {
    const [city, setCity] = useState('dakar');
    const [sdg6Data, setSDG6Data] = useState(null);
    
    useEffect(() => {
        const fetchSDG6 = async () => {
            try {
                const res = await apiClient.get(`/statistics/sdg6/${city}`);
                setSDG6Data(res.data);
            } catch (error) {
                console.error('Error:', error);
            }
        };
        
        fetchSDG6();
    }, [city]);
    
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-bar-chart"></i> Statistiques SDG 6
            </h1>
            
            <div className="mb-4">
                <label className="form-label">Ville</label>
                <select className="form-control" value={city} onChange={(e) => setCity(e.target.value)}>
                    <option value="dakar">Dakar</option>
                    <option value="abidjan">Abidjan</option>
                </select>
            </div>
            
            {sdg6Data && (
                <div className="row">
                    {Object.entries(sdg6Data.indicators).map(([key, indicator]) => (
                        <div key={key} className="col-lg-6 mb-4">
                            <div className="card-modern">
                                <div className="card-body">
                                    <h6 className="mb-3">{indicator.name}</h6>
                                    <div className="row align-items-center">
                                        <div className="col-8">
                                            <div className="progress" style={{height: '25px'}}>
                                                <div className="progress-bar" style={{width: `${indicator.value_percent}%`, lineHeight: '25px'}}>
                                                    {indicator.value_percent}%
                                                </div>
                                            </div>
                                            <small className="text-muted">
                                                Cible 2030: {indicator.target_2030}%
                                            </small>
                                        </div>
                                        <div className="col-4 text-center">
                                            <span className={`badge-custom badge-${indicator.status === 'on_track' ? 'success' : 'warning'}`}>
                                                {indicator.status}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

// Page Compareraison Villes
function ComparisonPage() {
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-diagram-3"></i> Comparaison Dakar vs Abidjan
            </h1>
            
            <table className="table table-custom">
                <thead>
                    <tr>
                        <th>Métrique</th>
                        <th>Dakar</th>
                        <th>Abidjan</th>
                        <th>Meilleur</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Population</td>
                        <td>1,060,000</td>
                        <td>4,200,000</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Accès à l'eau</td>
                        <td>78.5%</td>
                        <td>82.3%</td>
                        <td><span className="badge bg-success">Abidjan</span></td>
                    </tr>
                    <tr>
                        <td>Assainissement</td>
                        <td>71.2%</td>
                        <td>75.8%</td>
                        <td><span className="badge bg-success">Abidjan</span></td>
                    </tr>
                    <tr>
                        <td>Fuites d'eau</td>
                        <td>18.5%</td>
                        <td>15.2%</td>
                        <td><span className="badge bg-success">Abidjan</span></td>
                    </tr>
                    <tr>
                        <td>Qualité eau</td>
                        <td>82/100</td>
                        <td>85/100</td>
                        <td><span className="badge bg-success">Abidjan</span></td>
                    </tr>
                    <tr>
                        <td>Âge infrastructure</td>
                        <td>18.5 ans</td>
                        <td>16.2 ans</td>
                        <td><span className="badge bg-success">Abidjan</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}

// Page Paramètres
function SettingsPage() {
    const [userInfo, setUserInfo] = useState({
        username: 'john_analyst',
        email: 'john@brainblue.io',
        full_name: 'John Analyst',
        city: 'dakar'
    });
    
    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserInfo(prev => ({ ...prev, [name]: value }));
    };
    
    return (
        <div className="fade-in-up">
            <h1 className="mb-4">
                <i className="bi bi-gear"></i> Paramètres
            </h1>
            
            <div className="row">
                <div className="col-lg-8">
                    <div className="card-modern">
                        <div className="card-header">
                            <h6><i className="bi bi-person"></i> Profil Utilisateur</h6>
                        </div>
                        <div className="card-body">
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">Nom complet</label>
                                    <input type="text" className="form-control" name="full_name" value={userInfo.full_name} onChange={handleChange} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input type="email" className="form-control" name="email" value={userInfo.email} onChange={handleChange} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Ville preference</label>
                                    <select className="form-control" name="city" value={userInfo.city} onChange={handleChange}>
                                        <option value="dakar">Dakar</option>
                                        <option value="abidjan">Abidjan</option>
                                    </select>
                                </div>
                                <button type="button" className="btn btn-primary-custom">
                                    <i className="bi bi-check-circle"></i> Enregistrer les modifications
                                </button>
                            </form>
                        </div>
                    </div>
                    
                    <div className="card-modern mt-4">
                        <div className="card-header">
                            <h6><i className="bi bi-lock"></i> Sécurité</h6>
                        </div>
                        <div className="card-body">
                            <button className="btn btn-outline-custom w-100 mb-3">
                                <i className="bi bi-key"></i> Changer le mot de passe
                            </button>
                            <button className="btn btn-outline-custom w-100">
                                <i className="bi bi-shield-lock"></i> Authentification à deux facteurs
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Application principale
function BrainBlueApp() {
    const [currentPage, setCurrentPage] = useState('dashboard-dakar');
    const [isAuthenticated, setIsAuthenticated] = useState(true);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    
    const renderPage = () => {
        switch(currentPage) {
            case 'dashboard-dakar': return <DakarDashboard />;
            case 'dashboard-abidjan': return <AbidjanDashboard />;
            case 'predictions': return <PredictionsPage />;
            case 'statistics': return <StatisticsPage />;
            case 'comparison': return <ComparisonPage />;
            case 'settings': return <SettingsPage />;
            default: return <DakarDashboard />;
        }
    };
    
    return (
        <>
            {/* Navbar */}
            <nav className="navbar navbar-expand-lg navbar-brainblue">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('dashboard-dakar'); }}>
                        <i className="bi bi-water"></i> BRAINBLUE URBAIN
                    </a>
                    
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <a className="nav-link" href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('dashboard-dakar'); }}>
                                    <i className="bi bi-bell"></i> Alertes
                                </a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="#">
                                    <i className="bi bi-question-circle"></i> Aide
                                </a>
                            </li>
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                    <i className="bi bi-person-circle"></i> Mon compte
                                </a>
                                <ul className="dropdown-menu">
                                    <li><a className="dropdown-item" href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('settings'); }}>Profil</a></li>
                                    <li><hr className="dropdown-divider"></li>
                                    <li><a className="dropdown-item" href="#">Déconnexion</a></li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            
            {/* Sidebar */}
            <div className="sidebar">
                <div style={{padding: '1rem'}}>
                    <h6 style={{color: 'white', marginBottom: '1rem'}}>MENU PRINCIPAL</h6>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('dashboard-dakar')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-speedometer2"></i> Tableau Dakar
                    </div>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('dashboard-abidjan')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-speedometer2"></i> Tableau Abidjan
                    </div>
                    
                    <div className="sidebar-separator"></div>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('predictions')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-robot"></i> Prédictions IA
                    </div>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('statistics')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-bar-chart"></i> Statistiques
                    </div>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('comparison')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-diagram-3"></i> Comparaison
                    </div>
                    
                    <div className="sidebar-separator"></div>
                    
                    <div className="sidebar-item" onClick={() => setCurrentPage('settings')} style={{cursor: 'pointer'}}>
                        <i className="bi bi-gear"></i> Paramètres
                    </div>
                </div>
            </div>
            
            {/* Main Content */}
            <div className="main-content">
                {renderPage()}
            </div>
        </>
    );
}

// Render l'app
ReactDOM.render(<BrainBlueApp />, document.getElementById('root'));
