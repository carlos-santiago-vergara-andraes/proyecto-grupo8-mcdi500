"""Tres gráficos descriptivos de F4; unidades, categorías y cobertura explícitas."""
from __future__ import annotations

from pathlib import Path
from textwrap import fill

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

from src.f4_analisis import TIPOS_ES

AZUL, ROJO, GRIS = '#1F3A5F', '#AA182C', '#718399'


def numero(valor: float, decimales: int = 0) -> str:
    return f'{valor:,.{decimales}f}'.replace(',', '@').replace('.', ',').replace('@', '.')


def _ejes(titulo: str, subtitulo: str, altura: float = 4.4):
    fig, ax = plt.subplots(figsize=(6.5, altura))
    fig.subplots_adjust(left=.34, right=.97, bottom=.33, top=.75)
    fig.suptitle(fill(titulo, 66), fontsize=11, fontweight='bold', x=.02, ha='left', y=.98)
    fig.text(.02, .805, fill(subtitulo, 94), fontsize=8.5, color='#444444')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='x', color='#E1E5E9', linewidth=.6)
    ax.set_axisbelow(True)
    return fig, ax


def grafico_tipos(principal: pd.DataFrame, tipos: pd.DataFrame):
    """Cajas horizontales, todos los anuncios, escala logarítmica sin recorte."""
    orden = tipos.sort_values('mediana_ARS')['tipo_alojamiento'].tolist()
    entrada = principal['entrada'].iloc[0].strftime('%d/%m/%Y')
    salida = principal['salida'].iloc[0].strftime('%d/%m/%Y')
    por_tipo = tipos.set_index('tipo_alojamiento')
    razon = por_tipo.loc['Entire home/apt','mediana_ARS']/por_tipo.loc['Private room','mediana_ARS']
    fig, ax = _ejes(f'Los completos tienen una mediana {numero(razon,2)} veces la de privadas',
                   f'Entrada {entrada} · salida {salida} · {int(principal["noches"].iloc[0])} noche · {numero(len(principal))} anuncios')
    listas = [principal.loc[principal['tipo_alojamiento'].eq(t), 'precio_ars_noche'].to_numpy() for t in orden]
    ax.boxplot(listas, orientation='horizontal', tick_labels=[
        f"{TIPOS_ES[t]}{' *' if len(v) < 30 else ''}\n(n={numero(len(v))})" for t, v in zip(orden, listas)],
        patch_artist=True, boxprops={'facecolor': '#DCE6EE', 'edgecolor': AZUL},
        medianprops={'color': ROJO, 'linewidth': 2}, whiskerprops={'color': AZUL},
        capprops={'color': AZUL}, flierprops={'marker': 'o', 'markersize': 2.5,
        'markerfacecolor': GRIS, 'markeredgecolor': GRIS, 'alpha': .5})
    ax.set_xscale('log')
    ax.set_xticks([10000,1000000,100000000])
    ax.set_xlim(left=min(float(v.min()) for v in listas)*.7,
                right=max(float(v.max()) for v in listas)*3)
    ax.tick_params(axis='x',labelsize=9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: numero(x)))
    ax.set_xlabel('Precio por noche (ARS, escala logarítmica)',fontsize=9)
    ax.set_ylabel('Tipo de alojamiento')
    fig.legend(handles=[Patch(facecolor='#DCE6EE', edgecolor=AZUL, label='Caja: Q1–Q3'),
        Line2D([0], [0], color=ROJO, label='Mediana'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor=GRIS, label='Valores fuera de los bigotes')],
        frameon=False, loc='lower center', bbox_to_anchor=(.51, .105), ncol=2, fontsize=8)
    fig.text(.02, .025, 'Bigotes: hasta 1,5 × rango intercuartílico; * n < 30. Sin recorte de valores.\n'
             'Fuente: Inside Airbnb, Buenos Aires (2026); elaboración propia.', fontsize=8)
    return fig


def grafico_barrios(barrios: pd.DataFrame):
    """Puntos y cuartiles para igual tipo, capacidad y estancia; sin causalidad."""
    datos = barrios.loc[barrios['incluido_en_grafico']].sort_values('mediana_ARS')
    mayor = datos.iloc[-1]['barrio']
    fig, ax = _ejes(f'{mayor} presenta la mayor mediana entre los barrios comparados',
        'Alojamientos completos · capacidad 2 · 27–28/09/2026 · una noche · barrios con n ≥ 30', altura=3.5)
    y = np.arange(len(datos))
    ax.hlines(y, datos['q1_ARS'], datos['q3_ARS'], color=GRIS, linewidth=3)
    ax.scatter(datos['mediana_ARS'], y, s=50, color=AZUL, zorder=3)
    ax.scatter([datos.iloc[-1]['mediana_ARS']], [len(datos)-1], color=ROJO, s=50, zorder=4)
    ax.set_yticks(y, [f"{r.barrio} (n={numero(r.n)})" for r in datos.itertuples()])
    ax.set_xticks([0,50000,100000,150000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: numero(x)))
    ax.set_xlim(left=0)
    ax.set_xlabel('Precio cotizado por noche (ARS)',fontsize=9)
    ax.set_ylabel('Barrio')
    fig.legend(handles=[Line2D([0],[0],marker='o',color='none',markerfacecolor=AZUL,label='Mediana'),
        Line2D([0],[0],color=GRIS,linewidth=3,label='Q1–Q3; no es intervalo de confianza')],
        loc='lower center', bbox_to_anchor=(.51,.105), frameon=False, ncol=1, fontsize=8)
    fig.text(.02, .025, 'Se fijan tipo, capacidad y estancia; otras características pueden diferir.\n'
        'Fuente: Inside Airbnb, Buenos Aires (2026); elaboración propia.', fontsize=8)
    return fig


def grafico_capacidades(capacidades: pd.DataFrame, cambios: pd.DataFrame):
    """Barras desde cero con cuartiles; el grupo mensual incluye al principal."""
    maximo = cambios['cambio_mediana_porcentaje'].abs().max()
    fig, ax = _ejes(f'La ampliación mensual cambia las medianas hasta {numero(maximo, 2)} %',
        'Alojamientos completos · una noche · capacidades con n ≥ 30 en ambos grupos', altura=3.5)
    fig.subplots_adjust(left=.17,bottom=.39)
    datos = capacidades.loc[capacidades['incluido_en_grafico']]
    caps = sorted(datos['capacidad'].unique())
    x, ancho = np.arange(len(caps)), .34
    for grupo, desplazamiento, color, etiqueta in [
        ('principal', -ancho/2, AZUL, 'Principal: entrada 27/09/2026'),
        ('mensual', ancho/2, '#B9C6D3', 'Ampliación: entradas en septiembre de 2026')]:
        d = datos.loc[datos['grupo'].eq(grupo)].set_index('capacidad').loc[caps]
        ax.bar(x+desplazamiento, d['mediana_ARS'], ancho, color=color, label=etiqueta,
               yerr=np.vstack([d['mediana_ARS']-d['q1_ARS'], d['q3_ARS']-d['mediana_ARS']]),
               error_kw={'elinewidth':1, 'capsize':3, 'ecolor':'#444444'})
    ax.grid(axis='x', visible=False); ax.grid(axis='y', color='#E1E5E9', linewidth=.6)
    ax.set_ylim(bottom=0, top=datos['q3_ARS'].max()*1.2)
    ax.set_yticks([0,100000,200000,300000])
    soporte = datos.pivot(index='capacidad',columns='grupo',values='n')
    ax.set_xticks(x, [f"{numero(c)}\n{numero(soporte.loc[c,'principal'])} / {numero(soporte.loc[c,'mensual'])}" for c in caps],fontsize=8.5)
    ax.set_xlabel('Capacidad (personas) · n principal / ampliación',fontsize=9)
    ax.set_ylabel('Precio por noche (ARS)')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos: numero(y)))
    handles,labels=ax.get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center', bbox_to_anchor=(.51,.105), frameon=False, fontsize=8)
    fig.text(.02, .025, 'Barras: medianas; trazos: Q1–Q3. La ampliación incluye al principal.\n'
        'No ajusta inflación. Fuente: Inside Airbnb, Buenos Aires (2026); elaboración propia.', fontsize=8)
    return fig


def guardar_figuras(principal: pd.DataFrame, resumenes: dict[str, pd.DataFrame], carpeta: Path) -> list[Path]:
    """Exportar los mismos tres objetos mostrados por el notebook, a 300 dpi."""
    carpeta = Path(carpeta); carpeta.mkdir(parents=True, exist_ok=True)
    figuras = [grafico_tipos(principal, resumenes['tipos']),
               grafico_barrios(resumenes['barrios']),
               grafico_capacidades(resumenes['capacidades'], resumenes['sensibilidad_temporal'])]
    rutas = []
    for nombre, figura in zip(['01_tipos', '02_barrios', '03_capacidades'], figuras):
        ruta = carpeta / f'{nombre}.png'
        figura.savefig(ruta, dpi=300, facecolor='white')
        rutas.append(ruta)
        plt.close(figura)
    return rutas
