import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Tuple, Any, Optional

class ChartGenerator:
    """Classe central para gestão de gráficos da aplicação."""
    
    def __init__(self):
        sns.set_theme(style="whitegrid")
        self.cores_padrao = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']

    @staticmethod
    def _limpar_memoria():
        """Garante que o backend do Matplotlib não acumule figuras."""
        plt.clf()
        plt.close('all')

    @staticmethod
    def _adicionar_rotulos(ax, formato: str):
        """Itera sobre as barras para adicionar os valores numéricos."""
        for p in ax.patches:
            altura = p.get_height()
            if altura > 0:
                ax.annotate(
                    formato.format(altura),
                    (p.get_x() + p.get_width() / 2., altura),
                    ha='center', va='bottom', fontsize=9
                )

    async def plot_barplot(
        self, 
        df: pd.DataFrame, 
        params: dict, 
        path_save: str, 
        formato_rotulo: str = "{:.1f}%"
    ):
        """
        Função Mestra de Barras. 
        Substitui a lógica repetitiva de todas as funções de barra do utils.py.
        """
        self._limpar_memoria()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.barplot(
            data=df, 
            x=params.get('x'), 
            y=params.get('y'), 
            hue=params.get('hue'), 
            order=params.get('order'),
            palette=params.get('palette', self.cores_padrao),
            ax=ax
        )
        
        self._adicionar_rotulos(ax, formato_rotulo)
        
        ax.set_title(params.get('titulo', ''), fontsize=14)
        ax.set_xlabel(params.get('label_x', ''))
        ax.set_ylabel(params.get('label_y', ''))
        plt.ylim(0, params.get('ylim', 100) + 10)
        plt.xticks(rotation=45)
       
        fig.tight_layout()
        fig.savefig(path_save)
        self._limpar_memoria()

# --- Instância global para uso nos serviços ---
chart_tool = ChartGenerator()