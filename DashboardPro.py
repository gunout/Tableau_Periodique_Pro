import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import constants
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Tableau Périodique Complet par Date de Découverte",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #8B4513, #D2691E, #CD853F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        color: #8B4513;
        border-bottom: 2px solid #D2691E;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    .epoch-antiquite { 
        background-color: #F5DEB3; 
        border-left: 5px solid #8B4513; 
        color: #333;
    }
    .epoch-moyenage { 
        background-color: #DEB887; 
        border-left: 5px solid #A0522D; 
        color: #333;
    }
    .epoch-renaissance { 
        background-color: #F4A460; 
        border-left: 5px solid #D2691E; 
        color: #333;
    }
    .epoch-revolution { 
        background-color: #CD853F; 
        border-left: 5px solid #8B4513; 
        color: white;
    }
    .epoch-spectroscopique { 
        background-color: #D2691E; 
        border-left: 5px solid #A52A2A; 
        color: white;
    }
    .epoch-moderne { 
        background-color: #A0522D; 
        border-left: 5px solid #8B0000; 
        color: white;
    }
    .discovery-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #ddd;
        color: #333333;
    }
    .rgb-spectrum {
        height: 20px;
        border-radius: 10px;
        margin: 5px 0;
        border: 1px solid #ccc;
    }
    .periodic-cell {
        padding: 5px;
        border-radius: 5px;
        text-align: center;
        margin: 2px;
        font-size: 0.8em;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .periodic-cell:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .category-alkali { background-color: #FF6B6B; color: white; }
    .category-alkaline { background-color: #4ECDC4; color: white; }
    .category-transition { background-color: #45B7D1; color: white; }
    .category-post-transition { background-color: #96CEB4; color: #333; }
    .category-metalloid { background-color: #FFEAA7; color: #333; }
    .category-nonmetal { background-color: #DDA0DD; color: white; }
    .category-halogen { background-color: #98D8C8; color: #333; }
    .category-noble { background-color: #F7DC6F; color: #333; }
    .category-lanthanide { background-color: #BB8FCE; color: white; }
    .category-actinide { background-color: #85C1E9; color: white; }
</style>
""", unsafe_allow_html=True)

class CompletePeriodicTableDashboard:
    def __init__(self):
        self.elements_data = self.define_complete_elements_data()
        self.epochs_data = self.define_historical_epochs()
        self.spectral_data = self.define_complete_spectral_rgb_data()
        
    def define_historical_epochs(self):
        """Définit les périodes historiques de découverte"""
        return [
            {
                'nom': 'Antiquité', 'periode': 'Avant 500', 'couleur': '#F5DEB3',
                'description': 'Éléments connus depuis l\'antiquité',
                'elements': ['H', 'C', 'N', 'O', 'S', 'Cu', 'Ag', 'Sn', 'Sb', 'Au', 'Hg', 'Pb', 'Bi']
            },
            {
                'nom': 'Moyen-Âge', 'periode': '500-1500', 'couleur': '#DEB887',
                'description': 'Éléments découverts au Moyen-Âge',
                'elements': ['As', 'Zn', 'P']
            },
            {
                'nom': 'Renaissance', 'periode': '1500-1700', 'couleur': '#F4A460',
                'description': 'Découvertes de la Renaissance et Âge des Lumières',
                'elements': ['Co', 'Ni', 'Pt']
            },
            {
                'nom': 'Révolution Chimique', 'periode': '1700-1800', 'couleur': '#CD853F',
                'description': 'Période de la révolution chimique',
                'elements': ['Cl', 'Mn', 'Mo', 'Te', 'Cr', 'W', 'U', 'Ti', 'Be', 'Zr', 'Y', 'Ce']
            },
            {
                'nom': 'Ère Spectroscopique', 'periode': '1800-1900', 'couleur': '#D2691E',
                'description': 'Découvertes par spectroscopie et électrolyse',
                'elements': ['Li', 'Na', 'K', 'Rb', 'Cs', 'Ca', 'Sr', 'Ba', 'B', 'Al', 'Si', 'Se', 'Br', 'I', 
                           'He', 'Ne', 'Ar', 'Kr', 'Xe', 'Mg', 'Sc', 'V', 'Ga', 'Ge', 'Cd', 'In', 'F']
            },
            {
                'nom': 'Période Moderne', 'periode': '1900-Aujourd\'hui', 'couleur': '#A0522D',
                'description': 'Éléments découverts au 20ème siècle',
                'elements': ['Ra', 'Rn', 'Fr', 'Tc', 'Pm', 'Po', 'At', 'Ac', 'Pa', 'Np', 'Pu', 'Am', 'Cm', 
                           'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 
                           'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
            }
        ]
    
    def define_complete_elements_data(self):
        """Définit les données complètes pour tous les éléments du tableau périodique"""
        return [
            # Période 1
            {'symbole': 'H', 'nom': 'Hydrogène', 'numero_atomique': 1, 'masse_atomique': 1.008,
             'config_electronique': '1s¹', 'periode': 1, 'groupe': 1, 'categorie': 'Non-metal',
             'date_decouverte': 1766, 'decouvreur': 'Henry Cavendish', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'He', 'nom': 'Hélium', 'numero_atomique': 2, 'masse_atomique': 4.0026,
             'config_electronique': '1s²', 'periode': 1, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1868, 'decouvreur': 'Pierre Janssen', 'periode_epoch': 'Ère Spectroscopique'},
            
            # Période 2
            {'symbole': 'Li', 'nom': 'Lithium', 'numero_atomique': 3, 'masse_atomique': 6.94,
             'config_electronique': '[He] 2s¹', 'periode': 2, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1817, 'decouvreur': 'Johan Arfwedson', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Be', 'nom': 'Béryllium', 'numero_atomique': 4, 'masse_atomique': 9.0122,
             'config_electronique': '[He] 2s²', 'periode': 2, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1798, 'decouvreur': 'Louis Vauquelin', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'B', 'nom': 'Bore', 'numero_atomique': 5, 'masse_atomique': 10.81,
             'config_electronique': '[He] 2s² 2p¹', 'periode': 2, 'groupe': 13, 'categorie': 'Métalloïde',
             'date_decouverte': 1808, 'decouvreur': 'Joseph Gay-Lussac', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'C', 'nom': 'Carbone', 'numero_atomique': 6, 'masse_atomique': 12.011,
             'config_electronique': '[He] 2s² 2p²', 'periode': 2, 'groupe': 14, 'categorie': 'Non-metal',
             'date_decouverte': -25000, 'decouvreur': 'Préhistoire', 'periode_epoch': 'Antiquité'},
            {'symbole': 'N', 'nom': 'Azote', 'numero_atomique': 7, 'masse_atomique': 14.007,
             'config_electronique': '[He] 2s² 2p³', 'periode': 2, 'groupe': 15, 'categorie': 'Non-metal',
             'date_decouverte': 1772, 'decouvreur': 'Daniel Rutherford', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'O', 'nom': 'Oxygène', 'numero_atomique': 8, 'masse_atomique': 15.999,
             'config_electronique': '[He] 2s² 2p⁴', 'periode': 2, 'groupe': 16, 'categorie': 'Non-metal',
             'date_decouverte': 1774, 'decouvreur': 'Joseph Priestley', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'F', 'nom': 'Fluor', 'numero_atomique': 9, 'masse_atomique': 18.998,
             'config_electronique': '[He] 2s² 2p⁵', 'periode': 2, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 1886, 'decouvreur': 'Henri Moissan', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ne', 'nom': 'Néon', 'numero_atomique': 10, 'masse_atomique': 20.18,
             'config_electronique': '[He] 2s² 2p⁶', 'periode': 2, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1898, 'decouvreur': 'William Ramsay', 'periode_epoch': 'Ère Spectroscopique'},
            
            # Période 3
            {'symbole': 'Na', 'nom': 'Sodium', 'numero_atomique': 11, 'masse_atomique': 22.99,
             'config_electronique': '[Ne] 3s¹', 'periode': 3, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1807, 'decouvreur': 'Humphry Davy', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Mg', 'nom': 'Magnésium', 'numero_atomique': 12, 'masse_atomique': 24.305,
             'config_electronique': '[Ne] 3s²', 'periode': 3, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1808, 'decouvreur': 'Humphry Davy', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Al', 'nom': 'Aluminium', 'numero_atomique': 13, 'masse_atomique': 26.982,
             'config_electronique': '[Ne] 3s² 3p¹', 'periode': 3, 'groupe': 13, 'categorie': 'Métal pauvre',
             'date_decouverte': 1825, 'decouvreur': 'Hans Christian Ørsted', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Si', 'nom': 'Silicium', 'numero_atomique': 14, 'masse_atomique': 28.085,
             'config_electronique': '[Ne] 3s² 3p²', 'periode': 3, 'groupe': 14, 'categorie': 'Métalloïde',
             'date_decouverte': 1824, 'decouvreur': 'Jöns Berzelius', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'P', 'nom': 'Phosphore', 'numero_atomique': 15, 'masse_atomique': 30.974,
             'config_electronique': '[Ne] 3s² 3p³', 'periode': 3, 'groupe': 15, 'categorie': 'Non-metal',
             'date_decouverte': 1669, 'decouvreur': 'Hennig Brand', 'periode_epoch': 'Renaissance'},
            {'symbole': 'S', 'nom': 'Soufre', 'numero_atomique': 16, 'masse_atomique': 32.06,
             'config_electronique': '[Ne] 3s² 3p⁴', 'periode': 3, 'groupe': 16, 'categorie': 'Non-metal',
             'date_decouverte': -2000, 'decouvreur': 'Chinois anciens', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Cl', 'nom': 'Chlore', 'numero_atomique': 17, 'masse_atomique': 35.45,
             'config_electronique': '[Ne] 3s² 3p⁵', 'periode': 3, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 1774, 'decouvreur': 'Carl Scheele', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Ar', 'nom': 'Argon', 'numero_atomique': 18, 'masse_atomique': 39.948,
             'config_electronique': '[Ne] 3s² 3p⁶', 'periode': 3, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1894, 'decouvreur': 'Lord Rayleigh', 'periode_epoch': 'Ère Spectroscopique'},
            
            # Période 4
            {'symbole': 'K', 'nom': 'Potassium', 'numero_atomique': 19, 'masse_atomique': 39.098,
             'config_electronique': '[Ar] 4s¹', 'periode': 4, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1807, 'decouvreur': 'Humphry Davy', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ca', 'nom': 'Calcium', 'numero_atomique': 20, 'masse_atomique': 40.078,
             'config_electronique': '[Ar] 4s²', 'periode': 4, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1808, 'decouvreur': 'Humphry Davy', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Sc', 'nom': 'Scandium', 'numero_atomique': 21, 'masse_atomique': 44.956,
             'config_electronique': '[Ar] 3d¹ 4s²', 'periode': 4, 'groupe': 3, 'categorie': 'Métal de transition',
             'date_decouverte': 1879, 'decouvreur': 'Lars Nilson', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ti', 'nom': 'Titane', 'numero_atomique': 22, 'masse_atomique': 47.867,
             'config_electronique': '[Ar] 3d² 4s²', 'periode': 4, 'groupe': 4, 'categorie': 'Métal de transition',
             'date_decouverte': 1791, 'decouvreur': 'William Gregor', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'V', 'nom': 'Vanadium', 'numero_atomique': 23, 'masse_atomique': 50.942,
             'config_electronique': '[Ar] 3d³ 4s²', 'periode': 4, 'groupe': 5, 'categorie': 'Métal de transition',
             'date_decouverte': 1801, 'decouvreur': 'Andrés Manuel', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Cr', 'nom': 'Chrome', 'numero_atomique': 24, 'masse_atomique': 51.996,
             'config_electronique': '[Ar] 3d⁵ 4s¹', 'periode': 4, 'groupe': 6, 'categorie': 'Métal de transition',
             'date_decouverte': 1797, 'decouvreur': 'Louis Vauquelin', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Mn', 'nom': 'Manganèse', 'numero_atomique': 25, 'masse_atomique': 54.938,
             'config_electronique': '[Ar] 3d⁵ 4s²', 'periode': 4, 'groupe': 7, 'categorie': 'Métal de transition',
             'date_decouverte': 1774, 'decouvreur': 'Johan Gahn', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Fe', 'nom': 'Fer', 'numero_atomique': 26, 'masse_atomique': 55.845,
             'config_electronique': '[Ar] 3d⁶ 4s²', 'periode': 4, 'groupe': 8, 'categorie': 'Métal de transition',
             'date_decouverte': -1500, 'decouvreur': 'Hittites', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Co', 'nom': 'Cobalt', 'numero_atomique': 27, 'masse_atomique': 58.933,
             'config_electronique': '[Ar] 3d⁷ 4s²', 'periode': 4, 'groupe': 9, 'categorie': 'Métal de transition',
             'date_decouverte': 1735, 'decouvreur': 'Georg Brandt', 'periode_epoch': 'Renaissance'},
            {'symbole': 'Ni', 'nom': 'Nickel', 'numero_atomique': 28, 'masse_atomique': 58.693,
             'config_electronique': '[Ar] 3d⁸ 4s²', 'periode': 4, 'groupe': 10, 'categorie': 'Métal de transition',
             'date_decouverte': 1751, 'decouvreur': 'Axel Cronstedt', 'periode_epoch': 'Renaissance'},
            {'symbole': 'Cu', 'nom': 'Cuivre', 'numero_atomique': 29, 'masse_atomique': 63.546,
             'config_electronique': '[Ar] 3d¹⁰ 4s¹', 'periode': 4, 'groupe': 11, 'categorie': 'Métal de transition',
             'date_decouverte': -9000, 'decouvreur': 'Moyen-Orient', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Zn', 'nom': 'Zinc', 'numero_atomique': 30, 'masse_atomique': 65.38,
             'config_electronique': '[Ar] 3d¹⁰ 4s²', 'periode': 4, 'groupe': 12, 'categorie': 'Métal de transition',
             'date_decouverte': 1000, 'decouvreur': 'Indiens', 'periode_epoch': 'Moyen-Âge'},
            {'symbole': 'Ga', 'nom': 'Gallium', 'numero_atomique': 31, 'masse_atomique': 69.723,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p¹', 'periode': 4, 'groupe': 13, 'categorie': 'Métal pauvre',
             'date_decouverte': 1875, 'decouvreur': 'Paul Lecoq', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ge', 'nom': 'Germanium', 'numero_atomique': 32, 'masse_atomique': 72.63,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p²', 'periode': 4, 'groupe': 14, 'categorie': 'Métalloïde',
             'date_decouverte': 1886, 'decouvreur': 'Clemens Winkler', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'As', 'nom': 'Arsenic', 'numero_atomique': 33, 'masse_atomique': 74.922,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p³', 'periode': 4, 'groupe': 15, 'categorie': 'Métalloïde',
             'date_decouverte': 1250, 'decouvreur': 'Albert le Grand', 'periode_epoch': 'Moyen-Âge'},
            {'symbole': 'Se', 'nom': 'Sélénium', 'numero_atomique': 34, 'masse_atomique': 78.971,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p⁴', 'periode': 4, 'groupe': 16, 'categorie': 'Non-metal',
             'date_decouverte': 1817, 'decouvreur': 'Jöns Berzelius', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Br', 'nom': 'Brome', 'numero_atomique': 35, 'masse_atomique': 79.904,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p⁵', 'periode': 4, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 1826, 'decouvreur': 'Antoine Balard', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Kr', 'nom': 'Krypton', 'numero_atomique': 36, 'masse_atomique': 83.798,
             'config_electronique': '[Ar] 3d¹⁰ 4s² 4p⁶', 'periode': 4, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1898, 'decouvreur': 'William Ramsay', 'periode_epoch': 'Ère Spectroscopique'},
            
            # Période 5
            {'symbole': 'Rb', 'nom': 'Rubidium', 'numero_atomique': 37, 'masse_atomique': 85.468,
             'config_electronique': '[Kr] 5s¹', 'periode': 5, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1861, 'decouvreur': 'Robert Bunsen', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Sr', 'nom': 'Strontium', 'numero_atomique': 38, 'masse_atomique': 87.62,
             'config_electronique': '[Kr] 5s²', 'periode': 5, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1790, 'decouvreur': 'Adair Crawford', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Y', 'nom': 'Yttrium', 'numero_atomique': 39, 'masse_atomique': 88.906,
             'config_electronique': '[Kr] 4d¹ 5s²', 'periode': 5, 'groupe': 3, 'categorie': 'Métal de transition',
             'date_decouverte': 1794, 'decouvreur': 'Johan Gadolin', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Zr', 'nom': 'Zirconium', 'numero_atomique': 40, 'masse_atomique': 91.224,
             'config_electronique': '[Kr] 4d² 5s²', 'periode': 5, 'groupe': 4, 'categorie': 'Métal de transition',
             'date_decouverte': 1789, 'decouvreur': 'Martin Klaproth', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Nb', 'nom': 'Niobium', 'numero_atomique': 41, 'masse_atomique': 92.906,
             'config_electronique': '[Kr] 4d⁴ 5s¹', 'periode': 5, 'groupe': 5, 'categorie': 'Métal de transition',
             'date_decouverte': 1801, 'decouvreur': 'Charles Hatchett', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Mo', 'nom': 'Molybdène', 'numero_atomique': 42, 'masse_atomique': 95.95,
             'config_electronique': '[Kr] 4d⁵ 5s¹', 'periode': 5, 'groupe': 6, 'categorie': 'Métal de transition',
             'date_decouverte': 1778, 'decouvreur': 'Carl Scheele', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Tc', 'nom': 'Technétium', 'numero_atomique': 43, 'masse_atomique': 98.0,
             'config_electronique': '[Kr] 4d⁵ 5s²', 'periode': 5, 'groupe': 7, 'categorie': 'Métal de transition',
             'date_decouverte': 1937, 'decouvreur': 'Carlo Perrier', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ru', 'nom': 'Ruthénium', 'numero_atomique': 44, 'masse_atomique': 101.07,
             'config_electronique': '[Kr] 4d⁷ 5s¹', 'periode': 5, 'groupe': 8, 'categorie': 'Métal de transition',
             'date_decouverte': 1844, 'decouvreur': 'Karl Claus', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Rh', 'nom': 'Rhodium', 'numero_atomique': 45, 'masse_atomique': 102.91,
             'config_electronique': '[Kr] 4d⁸ 5s¹', 'periode': 5, 'groupe': 9, 'categorie': 'Métal de transition',
             'date_decouverte': 1803, 'decouvreur': 'William Wollaston', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Pd', 'nom': 'Palladium', 'numero_atomique': 46, 'masse_atomique': 106.42,
             'config_electronique': '[Kr] 4d¹⁰', 'periode': 5, 'groupe': 10, 'categorie': 'Métal de transition',
             'date_decouverte': 1803, 'decouvreur': 'William Wollaston', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ag', 'nom': 'Argent', 'numero_atomique': 47, 'masse_atomique': 107.87,
             'config_electronique': '[Kr] 4d¹⁰ 5s¹', 'periode': 5, 'groupe': 11, 'categorie': 'Métal de transition',
             'date_decouverte': -3000, 'decouvreur': 'Mésopotamiens', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Cd', 'nom': 'Cadmium', 'numero_atomique': 48, 'masse_atomique': 112.41,
             'config_electronique': '[Kr] 4d¹⁰ 5s²', 'periode': 5, 'groupe': 12, 'categorie': 'Métal de transition',
             'date_decouverte': 1817, 'decouvreur': 'Friedrich Stromeyer', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'In', 'nom': 'Indium', 'numero_atomique': 49, 'masse_atomique': 114.82,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p¹', 'periode': 5, 'groupe': 13, 'categorie': 'Métal pauvre',
             'date_decouverte': 1863, 'decouvreur': 'Ferdinand Reich', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Sn', 'nom': 'Étain', 'numero_atomique': 50, 'masse_atomique': 118.71,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p²', 'periode': 5, 'groupe': 14, 'categorie': 'Métal pauvre',
             'date_decouverte': -2000, 'decouvreur': 'Civilisations anciennes', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Sb', 'nom': 'Antimoine', 'numero_atomique': 51, 'masse_atomique': 121.76,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p³', 'periode': 5, 'groupe': 15, 'categorie': 'Métalloïde',
             'date_decouverte': 800, 'decouvreur': 'Jâbir ibn Hayyân', 'periode_epoch': 'Moyen-Âge'},
            {'symbole': 'Te', 'nom': 'Tellure', 'numero_atomique': 52, 'masse_atomique': 127.6,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p⁴', 'periode': 5, 'groupe': 16, 'categorie': 'Métalloïde',
             'date_decouverte': 1782, 'decouvreur': 'Franz Müller', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'I', 'nom': 'Iode', 'numero_atomique': 53, 'masse_atomique': 126.9,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p⁵', 'periode': 5, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 1811, 'decouvreur': 'Bernard Courtois', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Xe', 'nom': 'Xénon', 'numero_atomique': 54, 'masse_atomique': 131.29,
             'config_electronique': '[Kr] 4d¹⁰ 5s² 5p⁶', 'periode': 5, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1898, 'decouvreur': 'William Ramsay', 'periode_epoch': 'Ère Spectroscopique'},
            
            # Période 6
            {'symbole': 'Cs', 'nom': 'Césium', 'numero_atomique': 55, 'masse_atomique': 132.91,
             'config_electronique': '[Xe] 6s¹', 'periode': 6, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1860, 'decouvreur': 'Robert Bunsen', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ba', 'nom': 'Baryum', 'numero_atomique': 56, 'masse_atomique': 137.33,
             'config_electronique': '[Xe] 6s²', 'periode': 6, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1808, 'decouvreur': 'Humphry Davy', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'La', 'nom': 'Lanthane', 'numero_atomique': 57, 'masse_atomique': 138.91,
             'config_electronique': '[Xe] 5d¹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1839, 'decouvreur': 'Carl Mosander', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ce', 'nom': 'Cérium', 'numero_atomique': 58, 'masse_atomique': 140.12,
             'config_electronique': '[Xe] 4f¹ 5d¹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1803, 'decouvreur': 'Jöns Berzelius', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Pr', 'nom': 'Praséodyme', 'numero_atomique': 59, 'masse_atomique': 140.91,
             'config_electronique': '[Xe] 4f³ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1885, 'decouvreur': 'Carl von Welsbach', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Nd', 'nom': 'Néodyme', 'numero_atomique': 60, 'masse_atomique': 144.24,
             'config_electronique': '[Xe] 4f⁴ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1885, 'decouvreur': 'Carl von Welsbach', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Pm', 'nom': 'Prométhium', 'numero_atomique': 61, 'masse_atomique': 145.0,
             'config_electronique': '[Xe] 4f⁵ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1945, 'decouvreur': 'Jacob Marinsky', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Sm', 'nom': 'Samarium', 'numero_atomique': 62, 'masse_atomique': 150.36,
             'config_electronique': '[Xe] 4f⁶ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1879, 'decouvreur': 'Paul Lecoq', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Eu', 'nom': 'Europium', 'numero_atomique': 63, 'masse_atomique': 151.96,
             'config_electronique': '[Xe] 4f⁷ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1901, 'decouvreur': 'Eugène Demarçay', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Gd', 'nom': 'Gadolinium', 'numero_atomique': 64, 'masse_atomique': 157.25,
             'config_electronique': '[Xe] 4f⁷ 5d¹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1880, 'decouvreur': 'Jean de Marignac', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Tb', 'nom': 'Terbium', 'numero_atomique': 65, 'masse_atomique': 158.93,
             'config_electronique': '[Xe] 4f⁹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1843, 'decouvreur': 'Carl Mosander', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Dy', 'nom': 'Dysprosium', 'numero_atomique': 66, 'masse_atomique': 162.5,
             'config_electronique': '[Xe] 4f¹⁰ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1886, 'decouvreur': 'Paul Lecoq', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ho', 'nom': 'Holmium', 'numero_atomique': 67, 'masse_atomique': 164.93,
             'config_electronique': '[Xe] 4f¹¹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1878, 'decouvreur': 'Marc Delafontaine', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Er', 'nom': 'Erbium', 'numero_atomique': 68, 'masse_atomique': 167.26,
             'config_electronique': '[Xe] 4f¹² 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1843, 'decouvreur': 'Carl Mosander', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Tm', 'nom': 'Thulium', 'numero_atomique': 69, 'masse_atomique': 168.93,
             'config_electronique': '[Xe] 4f¹³ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1879, 'decouvreur': 'Per Teodor Cleve', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Yb', 'nom': 'Ytterbium', 'numero_atomique': 70, 'masse_atomique': 173.05,
             'config_electronique': '[Xe] 4f¹⁴ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1878, 'decouvreur': 'Jean de Marignac', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Lu', 'nom': 'Lutécium', 'numero_atomique': 71, 'masse_atomique': 174.97,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹ 6s²', 'periode': 6, 'groupe': 3, 'categorie': 'Lanthanide',
             'date_decouverte': 1907, 'decouvreur': 'Georges Urbain', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Hf', 'nom': 'Hafnium', 'numero_atomique': 72, 'masse_atomique': 178.49,
             'config_electronique': '[Xe] 4f¹⁴ 5d² 6s²', 'periode': 6, 'groupe': 4, 'categorie': 'Métal de transition',
             'date_decouverte': 1923, 'decouvreur': 'Dirk Coster', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ta', 'nom': 'Tantale', 'numero_atomique': 73, 'masse_atomique': 180.95,
             'config_electronique': '[Xe] 4f¹⁴ 5d³ 6s²', 'periode': 6, 'groupe': 5, 'categorie': 'Métal de transition',
             'date_decouverte': 1802, 'decouvreur': 'Anders Ekeberg', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'W', 'nom': 'Tungstène', 'numero_atomique': 74, 'masse_atomique': 183.84,
             'config_electronique': '[Xe] 4f¹⁴ 5d⁴ 6s²', 'periode': 6, 'groupe': 6, 'categorie': 'Métal de transition',
             'date_decouverte': 1783, 'decouvreur': 'Juan Elhuyar', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Re', 'nom': 'Rhénium', 'numero_atomique': 75, 'masse_atomique': 186.21,
             'config_electronique': '[Xe] 4f¹⁴ 5d⁵ 6s²', 'periode': 6, 'groupe': 7, 'categorie': 'Métal de transition',
             'date_decouverte': 1925, 'decouvreur': 'Walter Noddack', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Os', 'nom': 'Osmium', 'numero_atomique': 76, 'masse_atomique': 190.23,
             'config_electronique': '[Xe] 4f¹⁴ 5d⁶ 6s²', 'periode': 6, 'groupe': 8, 'categorie': 'Métal de transition',
             'date_decouverte': 1803, 'decouvreur': 'Smithson Tennant', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Ir', 'nom': 'Iridium', 'numero_atomique': 77, 'masse_atomique': 192.22,
             'config_electronique': '[Xe] 4f¹⁴ 5d⁷ 6s²', 'periode': 6, 'groupe': 9, 'categorie': 'Métal de transition',
             'date_decouverte': 1803, 'decouvreur': 'Smithson Tennant', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Pt', 'nom': 'Platine', 'numero_atomique': 78, 'masse_atomique': 195.08,
             'config_electronique': '[Xe] 4f¹⁴ 5d⁹ 6s¹', 'periode': 6, 'groupe': 10, 'categorie': 'Métal de transition',
             'date_decouverte': 1557, 'decouvreur': 'Julius Scaliger', 'periode_epoch': 'Renaissance'},
            {'symbole': 'Au', 'nom': 'Or', 'numero_atomique': 79, 'masse_atomique': 196.97,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s¹', 'periode': 6, 'groupe': 11, 'categorie': 'Métal de transition',
             'date_decouverte': -6000, 'decouvreur': 'Égyptiens', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Hg', 'nom': 'Mercure', 'numero_atomique': 80, 'masse_atomique': 200.59,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s²', 'periode': 6, 'groupe': 12, 'categorie': 'Métal de transition',
             'date_decouverte': -1500, 'decouvreur': 'Chinois/Égyptiens', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Tl', 'nom': 'Thallium', 'numero_atomique': 81, 'masse_atomique': 204.38,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹', 'periode': 6, 'groupe': 13, 'categorie': 'Métal pauvre',
             'date_decouverte': 1861, 'decouvreur': 'William Crookes', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Pb', 'nom': 'Plomb', 'numero_atomique': 82, 'masse_atomique': 207.2,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²', 'periode': 6, 'groupe': 14, 'categorie': 'Métal pauvre',
             'date_decouverte': -3000, 'decouvreur': 'Mésopotamiens', 'periode_epoch': 'Antiquité'},
            {'symbole': 'Bi', 'nom': 'Bismuth', 'numero_atomique': 83, 'masse_atomique': 208.98,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³', 'periode': 6, 'groupe': 15, 'categorie': 'Métal pauvre',
             'date_decouverte': 1400, 'decouvreur': 'Inconnu', 'periode_epoch': 'Moyen-Âge'},
            {'symbole': 'Po', 'nom': 'Polonium', 'numero_atomique': 84, 'masse_atomique': 209.0,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴', 'periode': 6, 'groupe': 16, 'categorie': 'Métalloïde',
             'date_decouverte': 1898, 'decouvreur': 'Pierre Curie', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'At', 'nom': 'Astate', 'numero_atomique': 85, 'masse_atomique': 210.0,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁵', 'periode': 6, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 1940, 'decouvreur': 'Dale Corson', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Rn', 'nom': 'Radon', 'numero_atomique': 86, 'masse_atomique': 222.0,
             'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶', 'periode': 6, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 1900, 'decouvreur': 'Friedrich Dorn', 'periode_epoch': 'Période Moderne'},
            
            # Période 7
            {'symbole': 'Fr', 'nom': 'Francium', 'numero_atomique': 87, 'masse_atomique': 223.0,
             'config_electronique': '[Rn] 7s¹', 'periode': 7, 'groupe': 1, 'categorie': 'Métal alcalin',
             'date_decouverte': 1939, 'decouvreur': 'Marguerite Perey', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ra', 'nom': 'Radium', 'numero_atomique': 88, 'masse_atomique': 226.0,
             'config_electronique': '[Rn] 7s²', 'periode': 7, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
             'date_decouverte': 1898, 'decouvreur': 'Pierre Curie', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ac', 'nom': 'Actinium', 'numero_atomique': 89, 'masse_atomique': 227.0,
             'config_electronique': '[Rn] 6d¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1899, 'decouvreur': 'André Debierne', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Th', 'nom': 'Thorium', 'numero_atomique': 90, 'masse_atomique': 232.04,
             'config_electronique': '[Rn] 6d² 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1828, 'decouvreur': 'Jöns Berzelius', 'periode_epoch': 'Ère Spectroscopique'},
            {'symbole': 'Pa', 'nom': 'Protactinium', 'numero_atomique': 91, 'masse_atomique': 231.04,
             'config_electronique': '[Rn] 5f² 6d¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1913, 'decouvreur': 'Kasimir Fajans', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'U', 'nom': 'Uranium', 'numero_atomique': 92, 'masse_atomique': 238.03,
             'config_electronique': '[Rn] 5f³ 6d¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1789, 'decouvreur': 'Martin Klaproth', 'periode_epoch': 'Révolution Chimique'},
            {'symbole': 'Np', 'nom': 'Neptunium', 'numero_atomique': 93, 'masse_atomique': 237.0,
             'config_electronique': '[Rn] 5f⁴ 6d¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1940, 'decouvreur': 'Edwin McMillan', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Pu', 'nom': 'Plutonium', 'numero_atomique': 94, 'masse_atomique': 244.0,
             'config_electronique': '[Rn] 5f⁶ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1940, 'decouvreur': 'Glenn Seaborg', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Am', 'nom': 'Américium', 'numero_atomique': 95, 'masse_atomique': 243.0,
             'config_electronique': '[Rn] 5f⁷ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1944, 'decouvreur': 'Glenn Seaborg', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Cm', 'nom': 'Curium', 'numero_atomique': 96, 'masse_atomique': 247.0,
             'config_electronique': '[Rn] 5f⁷ 6d¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1944, 'decouvreur': 'Glenn Seaborg', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Bk', 'nom': 'Berkélium', 'numero_atomique': 97, 'masse_atomique': 247.0,
             'config_electronique': '[Rn] 5f⁹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1949, 'decouvreur': 'Glenn Seaborg', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Cf', 'nom': 'Californium', 'numero_atomique': 98, 'masse_atomique': 251.0,
             'config_electronique': '[Rn] 5f¹⁰ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1950, 'decouvreur': 'Glenn Seaborg', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Es', 'nom': 'Einsteinium', 'numero_atomique': 99, 'masse_atomique': 252.0,
             'config_electronique': '[Rn] 5f¹¹ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1952, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Fm', 'nom': 'Fermium', 'numero_atomique': 100, 'masse_atomique': 257.0,
             'config_electronique': '[Rn] 5f¹² 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1952, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Md', 'nom': 'Mendélévium', 'numero_atomique': 101, 'masse_atomique': 258.0,
             'config_electronique': '[Rn] 5f¹³ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1955, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'No', 'nom': 'Nobélium', 'numero_atomique': 102, 'masse_atomique': 259.0,
             'config_electronique': '[Rn] 5f¹⁴ 7s²', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1958, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Lr', 'nom': 'Lawrencium', 'numero_atomique': 103, 'masse_atomique': 262.0,
             'config_electronique': '[Rn] 5f¹⁴ 7s² 7p¹', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
             'date_decouverte': 1961, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Rf', 'nom': 'Rutherfordium', 'numero_atomique': 104, 'masse_atomique': 267.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d² 7s²', 'periode': 7, 'groupe': 4, 'categorie': 'Métal de transition',
             'date_decouverte': 1964, 'decouvreur': 'Georgy Flerov', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Db', 'nom': 'Dubnium', 'numero_atomique': 105, 'masse_atomique': 268.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d³ 7s²', 'periode': 7, 'groupe': 5, 'categorie': 'Métal de transition',
             'date_decouverte': 1967, 'decouvreur': 'Georgy Flerov', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Sg', 'nom': 'Seaborgium', 'numero_atomique': 106, 'masse_atomique': 269.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d⁴ 7s²', 'periode': 7, 'groupe': 6, 'categorie': 'Métal de transition',
             'date_decouverte': 1974, 'decouvreur': 'Albert Ghiorso', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Bh', 'nom': 'Bohrium', 'numero_atomique': 107, 'masse_atomique': 270.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d⁵ 7s²', 'periode': 7, 'groupe': 7, 'categorie': 'Métal de transition',
             'date_decouverte': 1981, 'decouvreur': 'Peter Armbruster', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Hs', 'nom': 'Hassium', 'numero_atomique': 108, 'masse_atomique': 270.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d⁶ 7s²', 'periode': 7, 'groupe': 8, 'categorie': 'Métal de transition',
             'date_decouverte': 1984, 'decouvreur': 'Peter Armbruster', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Mt', 'nom': 'Meitnérium', 'numero_atomique': 109, 'masse_atomique': 278.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d⁷ 7s²', 'periode': 7, 'groupe': 9, 'categorie': 'Métal de transition',
             'date_decouverte': 1982, 'decouvreur': 'Peter Armbruster', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ds', 'nom': 'Darmstadtium', 'numero_atomique': 110, 'masse_atomique': 281.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d⁹ 7s¹', 'periode': 7, 'groupe': 10, 'categorie': 'Métal de transition',
             'date_decouverte': 1994, 'decouvreur': 'Sigurd Hofmann', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Rg', 'nom': 'Roentgenium', 'numero_atomique': 111, 'masse_atomique': 282.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s¹', 'periode': 7, 'groupe': 11, 'categorie': 'Métal de transition',
             'date_decouverte': 1994, 'decouvreur': 'Sigurd Hofmann', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Cn', 'nom': 'Copernicium', 'numero_atomique': 112, 'masse_atomique': 285.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s²', 'periode': 7, 'groupe': 12, 'categorie': 'Métal de transition',
             'date_decouverte': 1996, 'decouvreur': 'Sigurd Hofmann', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Nh', 'nom': 'Nihonium', 'numero_atomique': 113, 'masse_atomique': 286.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p¹', 'periode': 7, 'groupe': 13, 'categorie': 'Métal pauvre',
             'date_decouverte': 2004, 'decouvreur': 'RIKEN', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Fl', 'nom': 'Flérovium', 'numero_atomique': 114, 'masse_atomique': 289.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p²', 'periode': 7, 'groupe': 14, 'categorie': 'Métal pauvre',
             'date_decouverte': 1999, 'decouvreur': 'JINR', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Mc', 'nom': 'Moscovium', 'numero_atomique': 115, 'masse_atomique': 290.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p³', 'periode': 7, 'groupe': 15, 'categorie': 'Métal pauvre',
             'date_decouverte': 2004, 'decouvreur': 'JINR', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Lv', 'nom': 'Livermorium', 'numero_atomique': 116, 'masse_atomique': 293.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁴', 'periode': 7, 'groupe': 16, 'categorie': 'Métal pauvre',
             'date_decouverte': 2000, 'decouvreur': 'JINR', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Ts', 'nom': 'Tennessine', 'numero_atomique': 117, 'masse_atomique': 294.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁵', 'periode': 7, 'groupe': 17, 'categorie': 'Halogène',
             'date_decouverte': 2010, 'decouvreur': 'JINR', 'periode_epoch': 'Période Moderne'},
            {'symbole': 'Og', 'nom': 'Oganesson', 'numero_atomique': 118, 'masse_atomique': 294.0,
             'config_electronique': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁶', 'periode': 7, 'groupe': 18, 'categorie': 'Gaz noble',
             'date_decouverte': 2006, 'decouvreur': 'JINR', 'periode_epoch': 'Période Moderne'}
        ]
    
    def define_complete_spectral_rgb_data(self):
        """Définit les données spectrales RGB complètes pour tous les éléments"""
        return {
            # Spectres rouges caractéristiques
            'H': {'rgb': (255, 100, 100), 'longueur_onde_principale': 656.3, 'raies': ['656.3 nm (Hα)']},
            'Li': {'rgb': (255, 0, 0), 'longueur_onde_principale': 670.8, 'raies': ['670.8 nm']},
            'Rb': {'rgb': (200, 50, 50), 'longueur_onde_principale': 780.0, 'raies': ['780.0 nm', '794.8 nm']},
            'Sr': {'rgb': (255, 100, 100), 'longueur_onde_principale': 460.7, 'raies': ['460.7 nm']},
            'Ca': {'rgb': (255, 150, 150), 'longueur_onde_principale': 422.7, 'raies': ['422.7 nm']},
            
            # Spectres verts caractéristiques
            'Tl': {'rgb': (0, 255, 0), 'longueur_onde_principale': 535.0, 'raies': ['535.0 nm']},
            'Ba': {'rgb': (100, 255, 100), 'longueur_onde_principale': 553.5, 'raies': ['553.5 nm']},
            'Cu': {'rgb': (0, 200, 0), 'longueur_onde_principale': 521.8, 'raies': ['521.8 nm']},
            'B': {'rgb': (50, 255, 50), 'longueur_onde_principale': 518.0, 'raies': ['518.0 nm']},
            
            # Spectres bleus caractéristiques
            'Cs': {'rgb': (0, 0, 255), 'longueur_onde_principale': 455.5, 'raies': ['455.5 nm']},
            'Hg': {'rgb': (100, 100, 255), 'longueur_onde_principale': 435.8, 'raies': ['435.8 nm']},
            'As': {'rgb': (50, 50, 200), 'longueur_onde_principale': 450.0, 'raies': ['450.0 nm']},
            'Pb': {'rgb': (150, 150, 255), 'longueur_onde_principale': 405.8, 'raies': ['405.8 nm']},
            
            # Spectres jaunes/oranges
            'Na': {'rgb': (255, 255, 0), 'longueur_onde_principale': 589.0, 'raies': ['589.0 nm', '589.6 nm']},
            'K': {'rgb': (255, 200, 0), 'longueur_onde_principale': 766.5, 'raies': ['766.5 nm', '769.9 nm']},
            'Fe': {'rgb': (255, 165, 0), 'longueur_onde_principale': 438.4, 'raies': ['438.4 nm']},
            
            # Spectres violets/magentas
            'He': {'rgb': (200, 150, 255), 'longueur_onde_principale': 587.6, 'raies': ['587.6 nm']},
            'Ne': {'rgb': (255, 100, 255), 'longueur_onde_principale': 640.2, 'raies': ['640.2 nm']},
            'Ar': {'rgb': (180, 100, 220), 'longueur_onde_principale': 750.4, 'raies': ['750.4 nm']},
            
            # Métaux de transition - couleurs variées
            'Cr': {'rgb': (200, 200, 100), 'longueur_onde_principale': 520.8, 'raies': ['520.8 nm']},
            'Mn': {'rgb': (200, 150, 100), 'longueur_onde_principale': 403.3, 'raies': ['403.3 nm']},
            'Co': {'rgb': (150, 150, 200), 'longueur_onde_principale': 345.4, 'raies': ['345.4 nm']},
            'Ni': {'rgb': (100, 150, 150), 'longueur_onde_principale': 341.5, 'raies': ['341.5 nm']},
            'Ag': {'rgb': (200, 200, 200), 'longueur_onde_principale': 328.1, 'raies': ['328.1 nm']},
            'Au': {'rgb': (255, 215, 0), 'longueur_onde_principale': 267.6, 'raies': ['267.6 nm']},
            
            # Lanthanides - couleurs fluorescentes
            'Ce': {'rgb': (255, 200, 150), 'longueur_onde_principale': 456.2, 'raies': ['456.2 nm']},
            'Eu': {'rgb': (200, 255, 200), 'longueur_onde_principale': 612.0, 'raies': ['612.0 nm']},
            'Gd': {'rgb': (150, 200, 255), 'longueur_onde_principale': 376.8, 'raies': ['376.8 nm']},
            'Tb': {'rgb': (100, 255, 200), 'longueur_onde_principale': 541.0, 'raies': ['541.0 nm']},
            
            # Actinides
            'U': {'rgb': (100, 200, 100), 'longueur_onde_principale': 591.5, 'raies': ['591.5 nm']},
            'Pu': {'rgb': (150, 100, 150), 'longueur_onde_principale': 476.0, 'raies': ['476.0 nm']}
        }
    
    def get_element_rgb(self, element_symb):
        """Retourne la couleur RGB d'un élément"""
        if element_symb in self.spectral_data:
            return self.spectral_data[element_symb]['rgb']
        else:
            # Couleur par défaut basée sur la catégorie
            category_colors = {
                'Métal alcalin': (255, 100, 100),  # Rouge
                'Métal alcalino-terreux': (100, 255, 100),  # Vert
                'Métal de transition': (100, 100, 255),  # Bleu
                'Métal pauvre': (200, 200, 100),  # Jaune-vert
                'Métalloïde': (200, 100, 200),  # Violet
                'Non-metal': (100, 200, 200),  # Cyan
                'Halogène': (255, 200, 100),  # Orange
                'Gaz noble': (200, 150, 255),  # Lavande
                'Lanthanide': (255, 150, 150),  # Rose
                'Actinide': (150, 255, 150)  # Vert clair
            }
            element = next((e for e in self.elements_data if e['symbole'] == element_symb), None)
            if element and element['categorie'] in category_colors:
                return category_colors[element['categorie']]
            return (200, 200, 200)  # Gris par défaut
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🌌 Tableau Périodique Complet - Classification Historique et Spectrale</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; color: #666; margin-bottom: 2rem;'>
        <strong>Classification complète des 118 éléments par date de découverte avec leurs spectres RGB caractéristiques</strong><br>
        Explorez l'histoire complète de la découverte des éléments et leurs signatures spectrales uniques
        </div>
        """, unsafe_allow_html=True)
    
    def create_complete_periodic_table(self):
        """Crée une vue complète du tableau périodique"""
        st.markdown('<h3 class="section-header">🧪 TABLEAU PÉRIODIQUE COMPLET CLASSÉ PAR DATE DE DÉCOUVERTE</h3>', 
                   unsafe_allow_html=True)
        
        # Configuration du tableau périodique
        periodic_layout = [
            [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   2   ],
            [3,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   5,   6,   7,   8,   9,   10  ],
            [11,  12,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   13,  14,  15,  16,  17,  18  ],
            [19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36  ],
            [37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54  ],
            [55,  56,  57,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86  ],
            [87,  88,  89,  104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118 ],
            [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0   ],
            [0,   0,   'Lanthanides', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0,   0,   58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  0,   0   ],
            [0,   0,   'Actinides', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0,   0,   90,  91,  92,  93,  94,  95,  96,  97,  98,  99,  100, 101, 102, 103, 0,   0   ]
        ]
        
        # Créer le tableau périodique
        for row in periodic_layout:
            cols = st.columns(18)
            for i, atomic_number in enumerate(row):
                with cols[i]:
                    if atomic_number == 0:
                        st.write("")  # Case vide
                    elif isinstance(atomic_number, str):
                        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{atomic_number}</div>", 
                                   unsafe_allow_html=True)
                    else:
                        element = next((e for e in self.elements_data if e['numero_atomique'] == atomic_number), None)
                        if element:
                            rgb = self.get_element_rgb(element['symbole'])
                            rgb_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
                            text_color = 'white' if sum(rgb) < 450 else 'black'
                            
                            category_class = f"category-{element['categorie'].lower().replace(' ', '-').replace('é', 'e')}"
                            
                            st.markdown(f"""
                            <div class="periodic-cell {category_class}" 
                                 style="background-color: {rgb_hex}; color: {text_color};"
                                 title="{element['nom']} - Découvert en {element['date_decouverte'] if element['date_decouverte'] > 0 else 'Antiquité'}">
                                <strong>{element['symbole']}</strong><br>
                                <small>{element['numero_atomique']}</small>
                            </div>
                            """, unsafe_allow_html=True)
    
    def create_epoch_timeline(self):
        """Crée une frise chronologique interactive"""
        st.markdown('<h3 class="section-header">📅 FRISE CHRONOLOGIQUE COMPLÈTE DES DÉCOUVERTES</h3>', 
                   unsafe_allow_html=True)
        
        # Préparer les données pour la timeline
        timeline_data = []
        for element in self.elements_data:
            if element['date_decouverte'] > -10000:
                rgb = self.get_element_rgb(element['symbole'])
                timeline_data.append({
                    'Element': element['symbole'],
                    'Nom': element['nom'],
                    'Année': max(0, element['date_decouverte']),
                    'Découvreur': element['decouvreur'],
                    'Période': element['periode_epoch'],
                    'Couleur': f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})',
                    'Numéro': element['numero_atomique']
                })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        # Timeline interactive
        fig = px.scatter(df_timeline, 
                        x='Année', 
                        y='Numéro',
                        color='Période',
                        hover_data=['Nom', 'Découvreur', 'Element'],
                        title="Chronologie Complète des Découvertes des Éléments",
                        color_discrete_sequence=['#F5DEB3', '#DEB887', '#F4A460', '#CD853F', '#D2691E', '#A0522D'])
        
        fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')),
                         selector=dict(mode='markers'))
        fig.update_layout(height=500, xaxis_title="Année de Découverte", yaxis_title="Numéro Atomique")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_epoch_overview(self):
        """Affiche une vue détaillée par époque historique"""
        st.markdown('<h3 class="section-header">🏛️ VUE DÉTAILLÉE PAR ÉPOQUE HISTORIQUE</h3>', 
                   unsafe_allow_html=True)
        
        for epoch in self.epochs_data:
            elements_epoch = [e for e in self.elements_data if e['periode_epoch'] == epoch['nom']]
            
            st.markdown(f"""
            <div class="epoch-{epoch['nom'].lower().replace(' ', '').replace('é', 'e')}">
                <h3>{epoch['nom']} ({epoch['periode']})</h3>
                <p>{epoch['description']} - {len(elements_epoch)} éléments</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Afficher les éléments de cette époque
            elements_per_row = 6
            for i in range(0, len(elements_epoch), elements_per_row):
                cols = st.columns(elements_per_row)
                for j in range(elements_per_row):
                    if i + j < len(elements_epoch):
                        element = elements_epoch[i + j]
                        with cols[j]:
                            rgb = self.get_element_rgb(element['symbole'])
                            rgb_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
                            
                            st.markdown(f"""
                            <div class="discovery-card">
                                <div style="text-align: center;">
                                    <h4>{element['symbole']}</h4>
                                    <div class="rgb-spectrum" style="background: linear-gradient(90deg, {rgb_hex}80, {rgb_hex});"></div>
                                    <strong>{element['nom']}</strong><br>
                                    <small>N° {element['numero_atomique']}</small><br>
                                    <small>Découvert en {element['date_decouverte'] if element['date_decouverte'] > 0 else 'Antiquité'}</small><br>
                                    <small><em>{element['decouvreur'][:25]}{'...' if len(element['decouvreur']) > 25 else ''}</em></small>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    def create_spectral_analysis(self):
        """Analyse spectrale complète"""
        st.markdown('<h3 class="section-header">🌈 ANALYSE SPECTRALE COMPLÈTE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Par Catégorie", "Par Époque", "Comparaison"])
        
        with tab1:
            # Analyse par catégorie
            categories = list(set([e['categorie'] for e in self.elements_data]))
            
            for category in categories:
                elements_cat = [e for e in self.elements_data if e['categorie'] == category]
                st.subheader(f"{category} ({len(elements_cat)} éléments)")
                
                cols = st.columns(6)
                for i, element in enumerate(elements_cat[:6]):
                    with cols[i]:
                        rgb = self.get_element_rgb(element['symbole'])
                        rgb_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; background-color: {rgb_hex}30; border-radius: 5px;">
                            <strong>{element['symbole']}</strong><br>
                            <div style="width: 100%; height: 20px; background: linear-gradient(90deg, {rgb_hex}80, {rgb_hex}); border-radius: 3px; margin: 5px 0;"></div>
                            <small>{element['nom']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                if len(elements_cat) > 6:
                    with st.expander(f"Voir tous les {len(elements_cat)} éléments {category}"):
                        additional_cols = st.columns(6)
                        for i, element in enumerate(elements_cat[6:]):
                            with additional_cols[i % 6]:
                                rgb = self.get_element_rgb(element['symbole'])
                                rgb_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
                                
                                st.markdown(f"""
                                <div style="text-align: center; padding: 5px; background-color: {rgb_hex}30; border-radius: 3px; margin: 2px;">
                                    <strong>{element['symbole']}</strong><br>
                                    <small>{element['nom']}</small>
                                </div>
                                """, unsafe_allow_html=True)
        
        with tab2:
            # Analyse par époque
            for epoch in self.epochs_data:
                elements_epoch = [e for e in self.elements_data if e['periode_epoch'] == epoch['nom']]
                
                # Calculer la couleur moyenne de l'époque
                rgb_values = [self.get_element_rgb(e['symbole']) for e in elements_epoch]
                if rgb_values:
                    avg_rgb = tuple(int(np.mean([rgb[i] for rgb in rgb_values])) for i in range(3))
                    avg_hex = f'#{avg_rgb[0]:02x}{avg_rgb[1]:02x}{avg_rgb[2]:02x}'
                    
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin: 10px 0; padding: 15px; background: linear-gradient(135deg, {avg_hex}20, {avg_hex}50); border-radius: 10px;">
                        <div style="width: 60px; height: 60px; background-color: {avg_hex}; border-radius: 5px; margin-right: 15px; border: 2px solid white;"></div>
                        <div>
                            <h4>{epoch['nom']} ({epoch['periode']})</h4>
                            <p>{epoch['description']} - {len(elements_epoch)} éléments</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            # Comparaison des spectres
            st.subheader("Comparaison des Palettes Spectrales")
            
            selected_elements = st.multiselect(
                "Sélectionnez des éléments à comparer:",
                [f"{e['symbole']} - {e['nom']}" for e in self.elements_data],
                default=['H - Hydrogène', 'Na - Sodium', 'Hg - Mercure', 'Ne - Néon']
            )
            
            if selected_elements:
                fig = go.Figure()
                
                for element_str in selected_elements:
                    element_symb = element_str.split(' - ')[0]
                    element = next(e for e in self.elements_data if e['symbole'] == element_symb)
                    rgb = self.get_element_rgb(element_symb)
                    rgb_hex = f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})'
                    
                    # Spectre simulé
                    lambda_range = np.linspace(380, 780, 500)
                    spectre = np.zeros_like(lambda_range)
                    
                    if element_symb in self.spectral_data:
                        raie_principale = self.spectral_data[element_symb]['longueur_onde_principale']
                        if 380 <= raie_principale <= 780:
                            spectre += 0.8 * np.exp(-0.5 * ((lambda_range - raie_principale) / 15)**2)
                    
                    # Ajouter des raies secondaires simulées
                    for i in range(3):
                        raie_pos = 400 + i * 100
                        if 380 <= raie_pos <= 780:
                            spectre += 0.3 * np.exp(-0.5 * ((lambda_range - raie_pos) / 10)**2)
                    
                    fig.add_trace(go.Scatter(
                        x=lambda_range, y=spectre,
                        mode='lines',
                        name=f"{element_symb} - {element['nom']}",
                        line=dict(color=rgb_hex, width=3)
                    ))
                
                fig.update_layout(
                    title="Comparaison des Spectres Simulés",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def create_element_explorer(self):
        """Explorateur détaillé des éléments"""
        st.markdown('<h3 class="section-header">🔍 EXPLORATEUR DÉTAILLÉ DES ÉLÉMENTS</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            element_choice = st.selectbox("Choisir un élément:", 
                                        [f"{e['symbole']} - {e['nom']}" for e in self.elements_data])
            element_symb = element_choice.split(' - ')[0]
            element_data = next(e for e in self.elements_data if e['symbole'] == element_symb)
        
        with col2:
            rgb = self.get_element_rgb(element_symb)
            rgb_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {rgb_hex}20, {rgb_hex}50); border-radius: 10px; border: 2px solid {rgb_hex};">
                <h2>{element_data['symbole']} - {element_data['nom']}</h2>
                <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
                    <div style="width: 120px; height: 120px; background-color: {rgb_hex}; border-radius: 50%; border: 4px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.3);"></div>
                </div>
                <p><strong>Spectre RGB caractéristique</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Détails complets de l'élément
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="discovery-card">
                <h4>📜 Données Historiques</h4>
                <strong>Numéro atomique:</strong> {element_data['numero_atomique']}<br>
                <strong>Date de découverte:</strong> {element_data['date_decouverte'] if element_data['date_decouverte'] > 0 else 'Antiquité'}<br>
                <strong>Découvreur:</strong> {element_data['decouvreur']}<br>
                <strong>Période historique:</strong> {element_data['periode_epoch']}<br>
                <strong>Période:</strong> {element_data['periode']}<br>
                <strong>Groupe:</strong> {element_data['groupe']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="discovery-card">
                <h4>⚛️ Propriétés Atomiques</h4>
                <strong>Masse atomique:</strong> {element_data['masse_atomique']} u<br>
                <strong>Configuration électronique:</strong> {element_data['config_electronique']}<br>
                <strong>Catégorie:</strong> {element_data['categorie']}
            </div>
            """, unsafe_allow_html=True)
            
            if element_symb in self.spectral_data:
                spectral_info = self.spectral_data[element_symb]
                st.markdown(f"""
                <div class="discovery-card">
                    <h4>🌈 Données Spectrales</h4>
                    <strong>Couleur RGB:</strong> {rgb}<br>
                    <strong>Longueur d'onde principale:</strong> {spectral_info['longueur_onde_principale']} nm<br>
                    <strong>Raies caractéristiques:</strong><br>
                    {', '.join(spectral_info['raies'])}
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            # Spectre simulé détaillé
            st.markdown(f"""
            <div class="discovery-card">
                <h4>📊 Spectre Simulé</h4>
            </div>
            """, unsafe_allow_html=True)
            
            lambda_range = np.linspace(380, 780, 500)
            spectre = np.zeros_like(lambda_range)
            
            if element_symb in self.spectral_data:
                raie_principale = self.spectral_data[element_symb]['longueur_onde_principale']
                if 380 <= raie_principale <= 780:
                    spectre += 0.8 * np.exp(-0.5 * ((lambda_range - raie_principale) / 10)**2)
                
                # Ajouter des raies secondaires
                for i in range(2):
                    raie_pos = raie_principale + (i+1)*40 * (-1)**i
                    if 380 <= raie_pos <= 780:
                        spectre += 0.4 * np.exp(-0.5 * ((lambda_range - raie_pos) / 8)**2)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=lambda_range, y=spectre,
                mode='lines',
                line=dict(color=rgb_hex, width=3),
                name=f"Spectre {element_symb}",
                fill='tozeroy',
                fillcolor=rgb_hex + '40'
            ))
            
            fig.update_layout(
                title=f"Spectre simulé de {element_symb}",
                xaxis=dict(title="Longueur d'onde (nm)"),
                yaxis=dict(title="Intensité relative"),
                height=250,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ NAVIGATION COMPLÈTE")
        
        # Navigation principale
        st.sidebar.markdown("### 🧭 Vues Principales")
        section = st.sidebar.radio("Choisir la vue:", 
                                 ["Tableau Périodique", "Frise Chronologique", "Vue par Époque", 
                                  "Analyse Spectrale", "Explorateur d'Éléments"])
        
        # Filtres
        st.sidebar.markdown("### 🔍 Filtres Avancés")
        epoch_filter = st.sidebar.multiselect(
            "Filtrer par époque:",
            [epoch['nom'] for epoch in self.epochs_data],
            default=[epoch['nom'] for epoch in self.epochs_data]
        )
        
        category_filter = st.sidebar.multiselect(
            "Filtrer par catégorie:",
            list(set([e['categorie'] for e in self.elements_data])),
            default=list(set([e['categorie'] for e in self.elements_data]))
        )
        
        # Options d'affichage
        st.sidebar.markdown("### 🎨 Options d'Affichage")
        show_spectra = st.sidebar.checkbox("Afficher les spectres simulés", value=True)
        group_by_epoch = st.sidebar.checkbox("Grouper par époque historique", value=True)
        
        return {
            'section': section,
            'epoch_filter': epoch_filter,
            'category_filter': category_filter,
            'show_spectra': show_spectra,
            'group_by_epoch': group_by_epoch
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Navigation principale
        if controls['section'] == "Tableau Périodique":
            self.create_complete_periodic_table()
            self.create_epoch_overview()
        elif controls['section'] == "Frise Chronologique":
            self.create_epoch_timeline()
            self.create_spectral_analysis()
        elif controls['section'] == "Vue par Époque":
            self.create_epoch_overview()
            self.create_spectral_analysis()
        elif controls['section'] == "Analyse Spectrale":
            self.create_spectral_analysis()
            self.create_element_explorer()
        elif controls['section'] == "Explorateur d'Éléments":
            self.create_element_explorer()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        <strong>Tableau Périodique Complet - Classification Historique et Spectrale</strong><br>
        Base de données complète des 118 éléments avec dates de découverte et spectres RGB caractéristiques<br>
        Données historiques et spectrales compilées pour l'étude de l'évolution de la chimie et de la spectroscopie
        </div>
        """, unsafe_allow_html=True)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = CompletePeriodicTableDashboard()
    dashboard.run_dashboard()