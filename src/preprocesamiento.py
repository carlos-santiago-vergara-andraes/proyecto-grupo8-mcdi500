"""F2: diagnóstico, selección y transformación trazables de cotizaciones.

La fuente se recibe como DataFrame y nunca se modifica. Las salidas por anuncio
se conservan localmente; los informes publicados contienen agregados.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

SHA256_ESPERADO = 'c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a'
REQUERIDAS = [
    'id', 'host_id', 'last_scraped', 'neighbourhood_cleansed', 'room_type',
    'accommodates', 'price', 'price_quote_price_per_night', 'price_quote_total_price',
    'price_quote_checkin_date', 'price_quote_checkout_date', 'price_quote_raw',
    'bedrooms', 'beds', 'review_scores_rating',
]
TIPOS_ALOJAMIENTO = ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']


def _numerica(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(serie, errors='coerce').astype(float)


def _finita(serie: pd.Series) -> pd.Series:
    return pd.Series(np.isfinite(serie.to_numpy(dtype=float)), index=serie.index)


def _coinciden(a: pd.Series, b: pd.Series, tolerancia: float = 0.01) -> pd.Series:
    return pd.Series(np.isclose(a, b, rtol=0, atol=tolerancia, equal_nan=False), index=a.index)


def interpretar_price(serie: pd.Series) -> pd.Series:
    """Admitir importes positivos con $ opcional, coma de miles y punto decimal.

    El formato se valida antes de convertir; no se intercambian separadores
    arbitrariamente. La moneda se verifica por separado en el JSON.
    """
    texto = serie.astype('string').str.strip()
    patron = r'\$?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?'
    valido = texto.str.fullmatch(patron, na=False)
    limpio = texto.where(valido).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    return _numerica(limpio)


def extraer_cotizacion(valor: object) -> dict:
    """Extraer campos necesarios, sin propagar nombres, enlaces ni texto libre."""
    vacio = {'estado_json': 'ausente', 'moneda': None, 'precio_json': np.nan,
             'total_json': np.nan, 'entrada_json': None, 'salida_json': None}
    if valor is None or valor is pd.NA or (isinstance(valor, float) and math.isnan(valor)):
        return vacio
    try:
        objeto = json.loads(valor)
    except (TypeError, ValueError):
        return {**vacio, 'estado_json': 'invalido'}
    q = objeto.get('quote') if isinstance(objeto, dict) else None
    if not isinstance(q, dict):
        return {**vacio, 'estado_json': 'estructura_inesperada'}
    moneda = q.get('currency')
    return {
        'estado_json': 'objeto_quote',
        'moneda': moneda.strip().upper() if isinstance(moneda, str) else None,
        'precio_json': q.get('price_per_night'), 'total_json': q.get('total_price'),
        'entrada_json': q.get('requested_checkin_date'),
        'salida_json': q.get('requested_checkout_date'),
    }


def perfil_seleccion(datos: pd.DataFrame) -> pd.DataFrame:
    """Contar faltantes originales en las variables efectivamente inspeccionadas."""
    faltan = sorted(set(REQUERIDAS) - set(datos.columns))
    if faltan:
        raise ValueError(f'Faltan columnas requeridas: {faltan}')
    if datos.empty:
        raise ValueError('El dataset no contiene filas.')
    if not datos.columns.is_unique:
        raise ValueError('Hay nombres de columna duplicados.')
    return pd.DataFrame([
        {'variable': c, 'tipo_original': str(datos[c].dtype),
         'n_faltantes': int(datos[c].isna().sum()),
         'porcentaje_faltantes': 100 * float(datos[c].isna().mean()),
         'n_distintos': int(datos[c].nunique(dropna=True))}
        for c in REQUERIDAS
    ])


def preparar_vista(datos: pd.DataFrame) -> pd.DataFrame:
    """Construir una vista de diagnóstico con motivos de exclusión explícitos.

    Los identificadores repetidos se rechazan: no se elige una fila de forma
    arbitraria. Los nulos de variables complementarias no excluyen anuncios.
    """
    perfil_seleccion(datos)
    if datos['id'].dropna().duplicated().any():
        raise ValueError('Existen id repetidos; se requiere resolver su procedencia antes de continuar.')
    d = datos.reset_index(drop=True)
    q = pd.DataFrame([extraer_cotizacion(x) for x in d['price_quote_raw']])
    v = pd.DataFrame(index=d.index)
    # String conserva identificadores como etiquetas y evita tratarlos como medidas.
    v['id'] = d['id'].astype('string')
    v['host_id'] = d['host_id'].astype('string')
    v['barrio'] = d['neighbourhood_cleansed'].astype('string').str.strip().replace('', pd.NA)
    v['tipo_alojamiento'] = d['room_type'].astype('string').str.strip().replace('', pd.NA)
    v['capacidad'] = _numerica(d['accommodates'])
    v['price_interpretado'] = interpretar_price(d['price'])
    v['precio_ars_noche'] = _numerica(d['price_quote_price_per_night'])
    v['total_cotizado_ars'] = _numerica(d['price_quote_total_price'])
    v['moneda'] = q['moneda'].astype('string')
    v['estado_json'] = q['estado_json']
    v['precio_json'] = _numerica(q['precio_json'])
    v['total_json'] = _numerica(q['total_json'])
    for destino, original in [('fecha_extraccion', 'last_scraped'),
                               ('entrada', 'price_quote_checkin_date'),
                               ('salida', 'price_quote_checkout_date')]:
        v[destino] = pd.to_datetime(d[original], format='%Y-%m-%d', errors='coerce')
    for c in ['entrada_json', 'salida_json']:
        v[c] = pd.to_datetime(q[c], format='%Y-%m-%d', errors='coerce')
    v['noches'] = (v['salida'] - v['entrada']).dt.days
    for destino, original in [('dormitorios', 'bedrooms'), ('camas', 'beds'),
                               ('valoracion', 'review_scores_rating')]:
        v[destino] = _numerica(d[original])
    reglas = {
        'id_ausente': v['id'].isna() | v['id'].eq('').fillna(False),
        'moneda_no_ARS': ~v['moneda'].eq('ARS').fillna(False),
        'precio_no_positivo_o_no_finito': ~(_finita(v['precio_ars_noche']) & v['precio_ars_noche'].gt(0)),
        'precio_no_coincide_JSON': ~_coinciden(v['precio_ars_noche'], v['precio_json']),
        'fechas_no_validas': v['entrada'].isna() | v['salida'].isna() | v['noches'].le(0),
        'fechas_no_coinciden_JSON': ~(v['entrada'].eq(v['entrada_json']) & v['salida'].eq(v['salida_json'])),
        'capacidad_no_entera_positiva': ~(_finita(v['capacidad']) & v['capacidad'].gt(0) & v['capacidad'].mod(1).eq(0)),
        'barrio_ausente': v['barrio'].isna(),
        'tipo_no_reconocido': ~v['tipo_alojamiento'].isin(TIPOS_ALOJAMIENTO),
    }
    for nombre, mascara in reglas.items():
        v['excluir_' + nombre] = mascara.astype(bool)
    v['elegible'] = ~v.filter(like='excluir_').any(axis=1)
    return v


def comparar_precios(datos: pd.DataFrame, vista: pd.DataFrame) -> pd.DataFrame:
    """Cobertura, solapamiento y concordancia; tolerancia 0,01 ARS, rtol=0."""
    a, b = vista['price_interpretado'], vista['precio_ars_noche']
    presentes_a = datos['price'].notna().to_numpy()
    presentes_b = datos['price_quote_price_per_night'].notna().to_numpy()
    ambos = _finita(a) & _finita(b)
    diferencia = (a[ambos] - b[ambos]).abs()
    n = int(ambos.sum())
    valores = {
        'anuncios_totales': len(vista),
        'price_presente_original': int(presentes_a.sum()),
        'price_numerico_finito': int(_finita(a).sum()),
        'price_presente_no_interpretable': int((presentes_a & ~_finita(a)).sum()),
        'precio_quote_presente_original': int(presentes_b.sum()),
        'precio_quote_numerico_finito': int(_finita(b).sum()),
        'ambos_numericos_finitos': n,
        'solo_price_finito': int((_finita(a) & ~_finita(b)).sum()),
        'solo_precio_quote_finito': int((~_finita(a) & _finita(b)).sum()),
        'coinciden_tolerancia_0_01_ARS': int(_coinciden(a[ambos], b[ambos]).sum()),
        'difieren_mas_0_01_ARS': int((~_coinciden(a[ambos], b[ambos])).sum()),
        'porcentaje_coincidencia_entre_ambos': 100 * float(_coinciden(a[ambos], b[ambos]).mean()) if n else None,
        'diferencia_absoluta_maxima_ARS': float(diferencia.max()) if n else None,
        'cotizacion_precio_coincide_JSON': int(_coinciden(b, vista['precio_json']).sum()),
        'cotizacion_total_coincide_JSON': int(_coinciden(vista['total_cotizado_ars'], vista['total_json']).sum()),
    }
    return pd.DataFrame([{'indicador': k, 'valor': val} for k, val in valores.items()])


def contar_exclusiones(vista: pd.DataFrame) -> pd.DataFrame:
    """Separar motivos superpuestos y pérdidas secuenciales, sin sumarlos dos veces."""
    restante = pd.Series(True, index=vista.index)
    filas = []
    for c in vista.filter(like='excluir_').columns:
        excluidas = restante & vista[c]
        restante &= ~vista[c]
        filas.append({'regla': c.removeprefix('excluir_'),
                      'n_con_motivo_en_fuente': int(vista[c].sum()),
                      'n_excluidos_en_este_paso': int(excluidas.sum()),
                      'n_restantes': int(restante.sum())})
    return pd.DataFrame(filas)


def alternativas_faltantes(vista: pd.DataFrame) -> pd.DataFrame:
    """Comparar casos completos, media, mediana y mediana por tipo, sin imputar la base.

    La desviación se calcula como población (ddof=0), respecto de los valores
    observados válidos. El agrupamiento se limita a tipo de alojamiento.
    """
    filas = []
    d = vista.loc[vista['elegible']]
    for nombre in ['dormitorios', 'camas']:
        s = d[nombre].copy()
        valido = _finita(s) & s.ge(0) & s.mod(1).eq(0)
        s = s.where(valido)
        hay_observados = s.notna().any()
        mediana = s.median() if hay_observados else np.nan
        media = s.mean() if hay_observados else np.nan
        por_tipo = s.groupby(d['tipo_alojamiento']).transform('median') if hay_observados else s.copy()
        propuestas = {
            'casos_completos': s.dropna(),
            'media_global': s.fillna(media),
            'mediana_global': s.fillna(mediana),
            'mediana_por_tipo_con_respaldo_global': s.fillna(por_tipo).fillna(mediana),
        }
        base_std = float(s.std(ddof=0)) if hay_observados else np.nan
        for metodo, resultado in propuestas.items():
            contiene_observados = resultado.notna().any()
            std = float(resultado.std(ddof=0)) if contiene_observados else np.nan
            filas.append({'variable': nombre, 'alternativa': metodo, 'n_original': len(s),
                          'n_ausentes_o_invalidos': int(s.isna().sum()),
                          'n_resultante': int(resultado.notna().sum()),
                          'n_rellenos': int(s.isna().sum() - (len(s) - resultado.notna().sum())) if metodo != 'casos_completos' else 0,
                          'media_resultante': float(resultado.mean()) if contiene_observados else np.nan,
                          'mediana_resultante': float(resultado.median()) if contiene_observados else np.nan,
                          'desviacion_poblacional': std,
                          'cambio_porcentual_desviacion': 100 * (std / base_std - 1) if base_std > 0 else None,
                          'n_valores_fraccionarios': int((resultado.dropna().mod(1).abs() > 1e-10).sum())})
    return pd.DataFrame(filas)


def preparar_base(vista: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Conservar cotizaciones verificadas; no rellenar precios ni valores accesorios.

    Los atípicos por IQR se marcan por tipo, sin descartarlos por su magnitud.
    Se conserva precio en ARS; log1p facilita inspeccionar su asimetría.
    """
    columnas = ['id', 'host_id', 'fecha_extraccion', 'barrio', 'tipo_alojamiento',
                'capacidad', 'precio_ars_noche', 'total_cotizado_ars', 'moneda',
                'entrada', 'salida', 'noches', 'dormitorios', 'camas', 'valoracion']
    b = vista.loc[vista['elegible'], columnas].copy()
    if b.empty:
        raise ValueError('No quedan cotizaciones elegibles; revisar diagnóstico y reglas.')
    cambios = []
    for nombre in ['dormitorios', 'camas', 'valoracion']:
        s = b[nombre]
        valido = _finita(s)
        if nombre == 'valoracion':
            valido &= s.between(1, 5)
        else:
            valido &= s.ge(0) & s.mod(1).eq(0)
        cambios.append({'variable': nombre, 'faltantes_antes': int(s.isna().sum()),
                        'invalidos_convertidos_a_faltante': int((s.notna() & ~valido).sum())})
        b[nombre] = s.where(valido)
        b[nombre + '_faltante'] = b[nombre].isna()
    for nombre in ['capacidad', 'noches']:
        b[nombre] = b[nombre].astype('int64')
    b['precio_log1p'] = np.log1p(b['precio_ars_noche'].to_numpy())
    b['precio_ars_por_plaza'] = b['precio_ars_noche'] / b['capacidad']
    # Esta razón describe precio/capacidad anunciada: no es un cobro por persona.
    grupos = b.groupby('tipo_alojamiento')['precio_ars_noche']
    q1 = grupos.transform(lambda x: x.quantile(0.25))
    q3 = grupos.transform(lambda x: x.quantile(0.75))
    iqr = q3 - q1
    b['precio_atipico_iqr_tipo'] = (b['precio_ars_noche'] < q1 - 1.5 * iqr) | (b['precio_ars_noche'] > q3 + 1.5 * iqr)
    return b.reset_index(drop=True), pd.DataFrame(cambios)


def seleccionar_cohortes(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Elegir fecha y duración con mayor cobertura, sin consultar los precios.

    Desempate: fecha más temprana y menor duración. La sensibilidad amplía a
    entradas del mismo mes con idéntica duración, nunca a todas las fechas.
    """
    if base.empty:
        raise ValueError('La selección de cohortes requiere una base no vacía.')
    cobertura = base.groupby(['entrada', 'noches'], as_index=False).size().rename(columns={'size': 'n_anuncios'})
    cobertura = cobertura.sort_values(['n_anuncios', 'entrada', 'noches'], ascending=[False, True, True]).reset_index(drop=True)
    eleccion = cobertura.iloc[0]
    fecha, noches = eleccion['entrada'], int(eleccion['noches'])
    principal = base.loc[base['entrada'].eq(fecha) & base['noches'].eq(noches)].copy()
    sensibilidad = base.loc[base['entrada'].dt.to_period('M').eq(fecha.to_period('M')) & base['noches'].eq(noches)].copy()
    decision = {
        'regla': 'Mayor cobertura por fecha exacta de entrada y duración; desempate por fecha y duración crecientes.',
        'fecha_entrada_principal': fecha.date().isoformat(), 'noches': noches,
        'n_base_elegible': len(base), 'n_principal': len(principal),
        'porcentaje_base_en_principal': 100 * len(principal) / len(base),
        'mes_entrada_sensibilidad': str(fecha.to_period('M')), 'n_sensibilidad': len(sensibilidad),
        'limitacion': 'La cohorte no es representativa de toda la oferta. El mismo mes no garantiza igualdad de precios reales ni elimina la inflación.',
    }
    return principal, sensibilidad, cobertura, decision


def resumir_grupos(datos: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Informar tamaño, mediana y cuartiles, preservando grupos pequeños visibles."""
    return datos.groupby(variable, observed=True)['precio_ars_noche'].agg(
        n='size', mediana_ARS='median', q1_ARS=lambda x: x.quantile(.25),
        q3_ARS=lambda x: x.quantile(.75),
    ).reset_index().assign(grupo_menor_30=lambda x: x['n'] < 30)


def medir_composicion(base: pd.DataFrame, principal: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for variable in ['barrio', 'tipo_alojamiento', 'capacidad']:
        a, b = base[variable].value_counts(), principal[variable].value_counts()
        for grupo, n in a.items():
            n2 = int(b.get(grupo, 0))
            filas.append({'variable': variable, 'grupo': str(grupo), 'n_base': int(n),
                          'n_principal': n2, 'porcentaje_base': 100 * int(n) / len(base),
                          'porcentaje_principal': 100 * n2 / len(principal),
                          'retencion_del_grupo_pct': 100 * n2 / int(n)})
    return pd.DataFrame(filas)


def codificar_tipos(base: pd.DataFrame) -> pd.DataFrame:
    """Indicadores nominales completos para verificar cobertura por tipo.

    Sin códigos ordinales. No se mezclan con la variable de precio ni se usan
    para atribuir causalidad. El barrio conserva su etiqueta original.
    """
    etiquetas = pd.Categorical(base['tipo_alojamiento'], categories=TIPOS_ALOJAMIENTO)
    matriz = pd.get_dummies(etiquetas, prefix='tipo', dtype='int8')
    matriz.insert(0, 'id', base['id'].to_numpy())
    if not matriz.drop(columns='id').sum(axis=1).eq(1).all():
        raise ValueError('Cada anuncio debe pertenecer a exactamente un tipo reconocido.')
    return matriz


def validar_base(base: pd.DataFrame) -> pd.DataFrame:
    """Comprobar integridad, dominios, fechas, transformaciones y privacidad del esquema."""
    controles = {
        'base_no_vacia': not base.empty,
        'id_unico_y_presente': base['id'].notna().all() and base['id'].is_unique,
        'precio_finito_positivo': (_finita(base['precio_ars_noche']) & base['precio_ars_noche'].gt(0)).all(),
        'moneda_ARS': base['moneda'].eq('ARS').all(),
        'fechas_y_duracion_coherentes': (base['salida'].gt(base['entrada']) & (base['salida'] - base['entrada']).dt.days.eq(base['noches'])).all(),
        'capacidad_entera_positiva': (base['capacidad'].gt(0) & base['capacidad'].mod(1).eq(0)).all(),
        'grupos_principales_presentes': base[['barrio', 'tipo_alojamiento']].notna().all().all(),
        'tipos_reconocidos': base['tipo_alojamiento'].isin(TIPOS_ALOJAMIENTO).all(),
        'log_precio_reversible': np.isclose(np.expm1(base['precio_log1p']), base['precio_ars_noche'], rtol=1e-12, atol=1e-7).all(),
        'razon_por_plaza_coherente': _coinciden(base['precio_ars_por_plaza'] * base['capacidad'], base['precio_ars_noche'], 1e-6).all(),
        'sin_nombres_URL_texto_libre_coordenadas': not bool(set(base.columns) & {'host_name', 'host_url', 'name', 'listing_url', 'description', 'latitude', 'longitude', 'price_quote_raw'}),
    }
    resultado = pd.DataFrame([{'control': k, 'cumple': bool(v)} for k, v in controles.items()])
    if not resultado['cumple'].all():
        raise ValueError('Falló la validación: ' + ', '.join(resultado.loc[~resultado['cumple'], 'control']))
    return resultado


def exportar_y_verificar(base: pd.DataFrame, ruta: Path) -> pd.DataFrame:
    """Exportar un CSV local y releerlo con tipos, fechas y valores verificados."""
    validar_base(base)
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(ruta, index=False, encoding='utf-8', date_format='%Y-%m-%d')
    fechas = ['fecha_extraccion', 'entrada', 'salida']
    leido = pd.read_csv(ruta, dtype={'id': 'string', 'host_id': 'string'}, parse_dates=fechas)
    pd.testing.assert_frame_equal(base.reset_index(drop=True), leido, check_dtype=False,
                                  check_exact=False, rtol=1e-12, atol=1e-7)
    return pd.DataFrame([{'control': 'exportacion_y_relectura', 'cumple': True, 'filas': len(leido), 'columnas': len(leido.columns)}])


def tabla_markdown(tabla: pd.DataFrame) -> str:
    """Renderizar tablas pequeñas sin añadir tabulate a las dependencias."""
    def celda(valor):
        if pd.isna(valor):
            return '—'
        if isinstance(valor, (float, np.floating)):
            return f'{valor:.4f}'.rstrip('0').rstrip('.')
        return str(valor).replace('|', '\\|').replace('\n', ' ')
    filas = [list(tabla.columns)] + [[celda(x) for x in fila] for fila in tabla.itertuples(index=False, name=None)]
    lineas = ['| ' + ' | '.join(map(str, filas[0])) + ' |', '| ' + ' | '.join(['---'] * len(filas[0])) + ' |']
    return '\n'.join(lineas + ['| ' + ' | '.join(fila) + ' |' for fila in filas[1:]])


def guardar_informe(ruta: Path, tablas: dict[str, pd.DataFrame], decision: dict, contexto: dict) -> None:
    """Documentar resultados agregados de la ejecución real, sin identificar anfitriones."""
    texto = [
        '# F2 — Preprocesamiento y decisiones verificadas',
        '## Procedencia y ejecución',
        f"SHA-256 de la fuente: `{contexto['sha256']}`.",
        f"Python {contexto['python']}; pandas {contexto['pandas']}; NumPy {contexto['numpy']}.",
        f"Rama y commit consultados al iniciar: `{contexto.get('git', {})}`. La referencia identifica el estado consultado; los archivos guardados se incorporan en un commit posterior.",
        f"Ámbito de ejecución: {contexto.get('ambito', 'entorno que ejecutó el notebook')}.",
        '## Elección de precio',
        '`price_quote_price_per_night` es la variable principal: evita interpretar separadores monetarios y se coteja con `quote.price_per_night`. Se exige moneda ARS comprobada en el JSON. `price` se utiliza como contraste; su ausencia no se rellena ni se fusionan importes sin comprobación.',
        'La concordancia se evalúa con tolerancia absoluta de 0,01 ARS y tolerancia relativa cero, sobre pares finitos. Los precios no se imputan.',
        tabla_markdown(tablas['comparacion_precios']),
        '## Condiciones comparables',
        f"Se seleccionó entrada **{decision['fecha_entrada_principal']}**, estancia de **{decision['noches']} noche(s)**: **{decision['n_principal']} anuncios**, de {decision['n_base_elegible']} elegibles ({decision['porcentaje_base_en_principal']:.2f} %).",
        'La regla selecciona la combinación fecha exacta–duración con mayor cobertura, antes de comparar precios por barrio. El desempate utiliza fecha y duración crecientes. Se conserva la tabla completa de cobertura para reproducir la decisión.',
        f"La sensibilidad amplía las entradas al mes {decision['mes_entrada_sensibilidad']} y conserva la duración: {decision['n_sensibilidad']} anuncios. No representa una corrección por inflación. Las fechas de estancia solicitadas no son fechas de transacciones ni una serie histórica de precios.",
        'Se informa la composición de la cohorte y sus diferencias con la base elegible. Los grupos pequeños se identifican; no se presentan como referencias estables. La selección limita la generalización al mercado completo.',
        tabla_markdown(tablas['ventanas'].head(10)),
        '## Faltantes y reglas de limpieza',
        'La tabla siguiente describe las variables inspeccionadas antes de transformar. La ausencia de precio, moneda o condiciones verificables impide formar la base principal. Los motivos pueden superponerse; solo la columna secuencial se suma para explicar la pérdida total.',
        tabla_markdown(tablas['faltantes']), tabla_markdown(tablas['exclusiones']),
        '## Alternativas para variables complementarias',
        'Se compararon casos completos, media, mediana global y mediana por tipo con respaldo global en dormitorios y camas. Se midieron cobertura, valores fraccionarios y cambio de desviación poblacional. Ninguna de estas variables determina la cohorte principal; se conservan sus faltantes, con indicadores, para evitar alterar la cobertura o crear conteos artificiales. Los importes principales tampoco se rellenan.',
        tabla_markdown(tablas['alternativas_faltantes']), tabla_markdown(tablas['cambios_complementarias']),
        '## Transformaciones y atípicos',
        'Los identificadores se tratan como etiquetas; las fechas se interpretan como fechas y la capacidad y duración como enteros. Se conserva el precio en ARS. `precio_log1p` permite inspeccionar asimetría y su reversibilidad se valida. `precio_ars_por_plaza` normaliza por capacidad anunciada: no describe un cobro por persona ni sustituye el precio por anuncio.',
        'Los indicadores one-hot del tipo de alojamiento no imponen orden a la variable nominal. Se exportan separados, con cuatro categorías declaradas, y se verifica una pertenencia por fila. El barrio conserva su etiqueta para las comparaciones descriptivas.',
        'Los precios fuera de 1,5 IQR se marcan dentro de cada tipo; permanecen en la base. Se informa una comparación con y sin estas marcas como sensibilidad, sin identificar automáticamente precios altos con errores.',
        tabla_markdown(tablas['atipicos']), tabla_markdown(tablas['sensibilidad_atipicos']),
        '## Composición y sensibilidad temporal',
        tabla_markdown(tablas['sensibilidad_tipos']),
        'Las diferencias entre la cohorte exacta y la ampliada pueden reflejar cambios de composición y de condiciones de oferta; no se atribuyen causalmente a la fecha o la inflación.',
        '## Validación y exportación local', tabla_markdown(tablas['validacion']),
        'La fuente original permanece inmutable. Los CSV por anuncio se guardan localmente en `data/processed/`, excluido de Git. El repositorio conserva el código, los informes agregados y las evidencias de ejecución. La exportación se relee y se coteja con la tabla en memoria.',
        '## Correspondencia con objetivos',
        '| Objetivo | Sección de F2_Preprocesamiento.ipynb | Evidencia |\n| --- | --- | --- |\n| 1. Calidad y cobertura | 1. Obtención; 2. Exploración; 3. Limpieza. | Huella, faltantes, cotejo de precios y JSON, reglas de elegibilidad. |\n| 2. Base trazable | 3. Limpieza; 5. Transformación; 6. Validación y exportación. | Conteos secuenciales, alternativas de faltantes, variables derivadas y relectura verificada. |\n| 3. Descripción por grupos | 5. Transformación: Resúmenes iniciales y sensibilidad temporal. | n, mediana y cuartiles por barrio, tipo y capacidad. Los gráficos y su interpretación siguen pendientes en la fase analítica. |\n| 4. Estabilidad | 4. Condiciones comparables; 5. Transformación y revisión de atípicos. | Cohorte exacta, ampliación al mismo mes, composición y contraste con/sin marcas IQR. |',
        'Este registro técnico no sustituye el informe sumativo en la plantilla institucional ni las referencias APA 7 del entregable.',
    ]
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text('\n\n'.join(texto) + '\n', encoding='utf-8')


def ejecutar_preprocesamiento(datos: pd.DataFrame) -> dict:
    """Orquestar etapas sin escribir archivos ni modificar la fuente recibida."""
    perfil = perfil_seleccion(datos)
    vista = preparar_vista(datos)
    comparacion = comparar_precios(datos, vista)
    base, cambios = preparar_base(vista)
    principal, sensibilidad, ventanas, decision = seleccionar_cohortes(base)
    tablas = {'faltantes': perfil, 'comparacion_precios': comparacion,
              'exclusiones': contar_exclusiones(vista),
              'alternativas_faltantes': alternativas_faltantes(vista),
              'cambios_complementarias': cambios, 'ventanas': ventanas,
              'composicion': medir_composicion(base, principal), 'validacion': validar_base(base)}
    for nombre, variable in [('barrios', 'barrio'), ('tipos', 'tipo_alojamiento'), ('capacidades', 'capacidad')]:
        tablas[nombre] = resumir_grupos(principal, variable)
    tablas['sensibilidad_tipos'] = tablas['tipos'].merge(
        resumir_grupos(sensibilidad, 'tipo_alojamiento'), on='tipo_alojamiento', how='outer', suffixes=('_exacta', '_mismo_mes'))
    tablas['atipicos'] = base.groupby('tipo_alojamiento')['precio_atipico_iqr_tipo'].agg(n='size', n_marcados='sum').reset_index()
    filas = []
    for nombre, d in [('principal_completa', principal), ('principal_sin_marcas_IQR', principal.loc[~principal['precio_atipico_iqr_tipo']])]:
        filas.append({'alternativa': nombre, 'n': len(d), 'mediana_ARS': d['precio_ars_noche'].median(),
                      'q1_ARS': d['precio_ars_noche'].quantile(.25), 'q3_ARS': d['precio_ars_noche'].quantile(.75)})
    tablas['sensibilidad_atipicos'] = pd.DataFrame(filas)
    return {'base': base, 'principal': principal, 'sensibilidad': sensibilidad,
            'indicadores_tipo': codificar_tipos(base), 'tablas': tablas, 'decision': decision}
