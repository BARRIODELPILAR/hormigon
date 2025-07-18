import streamlit as st
import pandas as pd
import io
import csv
import math
import plotly.express as px

# --- Tablas de Datos ---

TABLE_7_22_WATER_DEMAND = {
    "dry": {
        "rounded": {20: 165, 40: 155, 80: 145},
        "crushed": {20: 180, 40: 170, 80: 160}
    },
    "plastic": {
        "rounded": {20: 180, 40: 170, 80: 160},
        "crushed": {20: 195, 40: 185, 80: 175}
    },
    "soft": {
        "rounded": {20: 195, 40: 185, 80: 175},
        "crushed": {20: 210, 40: 200, 80: 190}
    },
    "flowable": {
        "rounded": {20: 210, 40: 200, 80: 190},
        "crushed": {20: 225, 40: 215, 80: 205}
    }
}

TABLE_7_21_K_PARAMETER = {
    "rounded": 0.045,
    "crushed": 0.04
}

CEMENT_DENSITY = 3.1

# Los datos por defecto ahora son cadenas de texto para st.text_area
DEFAULT_SIEVE_DATA_2_FRACTIONS_STR = """80,0,0
40,30,0
20,40,0
10,65,50
5,100,60
2.5,100,70
1.25,100,80
0.63,100,88
0.32,100,90
0.16,100,95"""

DEFAULT_SIEVE_DATA_3_FRACTIONS_STR = """80,0,0,0
40,30,0,0
20,40,0,0
10,65,50,0
5,100,60,50
2.5,100,70,60
1.25,100,80,70
0.63,100,88,80
0.32,100,90,85
0.16,100,95,90"""

# --- Datos de CSV Integrados ---
LIMITS_DATA_DICT = {
    "X0": {"mass_min_cement": "150", "mass_max_cement": "", "mass_max_a_c": "0.7", "reinforced_min_cement": "180", "reinforced_max_cement": "", "reinforced_max_a_c": "0.65", "prestressed_min_cement": "200", "prestressed_max_cement": "", "prestressed_max_a_c": "0.6"},
    "XC1": {"mass_min_cement": "200", "mass_max_cement": "", "mass_max_a_c": "0.6", "reinforced_min_cement": "220", "reinforced_max_cement": "", "reinforced_max_a_c": "0.55", "prestressed_min_cement": "240", "prestressed_max_cement": "", "prestressed_max_a_c": "0.5"},
    "XC2": {"mass_min_cement": "220", "mass_max_cement": "", "mass_max_a_c": "0.55", "reinforced_min_cement": "240", "reinforced_max_cement": "", "reinforced_max_a_c": "0.5", "prestressed_min_cement": "260", "prestressed_max_cement": "", "prestressed_max_a_c": "0.45"},
    "XC3": {"mass_min_cement": "240", "mass_max_cement": "", "mass_max_a_c": "0.5", "reinforced_min_cement": "260", "reinforced_max_cement": "", "reinforced_max_a_c": "0.45", "prestressed_min_cement": "280", "reinforced_max_cement": "", "reinforced_max_a_c": "0.4"},
    "XC4": {"mass_min_cement": "260", "mass_max_cement": "", "mass_max_a_c": "0.45", "reinforced_min_cement": "280", "reinforced_max_cement": "", "reinforced_max_a_c": "0.4", "prestressed_min_cement": "300", "reinforced_max_cement": "", "prestressed_max_a_c": "0.35"},
    "XD1": {"mass_min_cement": "280", "mass_max_cement": "", "mass_max_a_c": "0.4", "reinforced_min_cement": "300", "reinforced_max_cement": "", "reinforced_max_a_c": "0.35", "prestressed_min_cement": "320", "reinforced_max_cement": "", "prestressed_max_a_c": "0.3"},
    "XD2": {"mass_min_cement": "300", "mass_max_cement": "", "mass_max_a_c": "0.35", "reinforced_min_cement": "320", "reinforced_max_cement": "", "reinforced_max_a_c": "0.3", "prestressed_min_cement": "340", "reinforced_max_cement": "", "prestressed_max_a_c": "0.28"},
    "XS1": {"mass_min_cement": "320", "mass_max_cement": "", "mass_max_a_c": "0.3", "reinforced_min_cement": "340", "reinforced_max_cement": "", "reinforced_max_a_c": "0.28", "prestressed_min_cement": "360", "reinforced_max_cement": "", "prestressed_max_a_c": "0.27"},
    "XS2": {"mass_min_cement": "340", "mass_max_cement": "", "mass_max_a_c": "0.28", "reinforced_min_cement": "360", "reinforced_max_cement": "", "reinforced_max_a_c": "0.27", "prestressed_min_cement": "380", "reinforced_max_cement": "", "prestressed_max_a_c": "0.26"},
    "XS3": {"mass_min_cement": "360", "mass_max_cement": "", "mass_max_a_c": "0.27", "reinforced_min_cement": "380", "reinforced_max_cement": "", "reinforced_max_a_c": "0.26", "prestressed_min_cement": "400", "reinforced_max_cement": "", "prestressed_max_a_c": "0.25"},
    "XF1": {"mass_min_cement": "260", "mass_max_cement": "", "mass_max_a_c": "0.45", "reinforced_min_cement": "280", "reinforced_max_cement": "", "reinforced_max_a_c": "0.4", "prestressed_min_cement": "300", "reinforced_max_cement": "", "prestressed_max_a_c": "0.35"},
    "XF2": {"mass_min_cement": "280", "mass_max_cement": "", "mass_max_a_c": "0.3", "reinforced_min_cement": "300", "reinforced_max_cement": "", "reinforced_max_a_c": "0.35", "prestressed_min_cement": "320", "reinforced_max_cement": "", "prestressed_max_a_c": "0.3"},
    "XF3": {"mass_min_cement": "300", "mass_max_cement": "", "mass_max_a_c": "0.35", "reinforced_min_cement": "320", "reinforced_max_cement": "", "reinforced_max_a_c": "0.28", "prestressed_min_cement": "340", "reinforced_max_cement": "", "prestressed_max_a_c": "0.28"},
    "XF4": {"mass_min_cement": "320", "mass_max_cement": "", "mass_max_a_c": "0.3", "reinforced_min_cement": "340", "reinforced_max_cement": "", "reinforced_max_a_c": "0.28", "prestressed_min_cement": "360", "reinforced_max_cement": "", "prestressed_max_a_c": "0.27"},
    "XA1": {"mass_min_cement": "280", "mass_max_cement": "", "mass_max_a_c": "0.4", "reinforced_min_cement": "300", "reinforced_max_cement": "", "reinforced_max_a_c": "0.35", "prestressed_min_cement": "320", "reinforced_max_cement": "", "prestressed_max_a_c": "0.3"},
    "XA2": {"mass_min_cement": "300", "mass_max_cement": "", "mass_max_a_c": "0.35", "reinforced_min_cement": "320", "reinforced_max_cement": "", "reinforced_max_a_c": "0.3", "prestressed_min_cement": "340", "reinforced_max_cement": "", "prestressed_max_a_c": "0.28"},
    "XA3": {"mass_min_cement": "320", "mass_max_cement": "", "mass_max_a_c": "0.3", "reinforced_min_cement": "340", "reinforced_max_cement": "", "reinforced_max_a_c": "0.28", "prestressed_min_cement": "360", "reinforced_max_cement": "", "prestressed_max_a_c": "0.27"},
    "XM1": {"mass_min_cement": "300", "mass_max_cement": "", "mass_max_a_c": "0.35", "reinforced_min_cement": "320", "mass_max_cement": "", "reinforced_max_a_c": "0.3", "prestressed_min_cement": "340", "mass_max_cement": "", "prestressed_max_a_c": "0.28"},
    "XM2": {"mass_min_cement": "320", "mass_max_cement": "", "mass_max_a_c": "0.3", "reinforced_min_cement": "340", "mass_max_cement": "", "reinforced_max_a_c": "0.28", "prestressed_min_cement": "360", "mass_max_cement": "", "prestressed_max_a_c": "0.27"},
    "XM3": {"mass_min_cement": "340", "mass_max_cement": "", "mass_max_a_c": "0.28", "reinforced_min_cement": "360", "mass_max_cement": "", "reinforced_max_a_c": "0.27", "prestressed_min_cement": "380", "mass_max_cement": "", "prestressed_max_a_c": "0.26"},
}

# --- Funciones de Ayuda ---

def load_limits(exposure_class, placing_type):
    """
    Carga los límites de cemento y relación agua/cemento según la clase de exposición y el tipo de colocación.
    """
    if exposure_class.upper() not in LIMITS_DATA_DICT:
        raise ValueError(f"Clase de exposición '{exposure_class}' no encontrada en los datos.")

    row = LIMITS_DATA_DICT[exposure_class.upper()]
    prefix = f"{placing_type.lower()}_"

    min_cement_str = row.get(f"{prefix}min_cement")
    max_cement_str = row.get(f"{prefix}max_cement")
    max_a_c_str = row.get(f"{prefix}max_a_c")

    if not min_cement_str or not max_a_c_str:
        raise ValueError(f"Los límites para '{placing_type}' en la clase de exposición '{exposure_class}' están incompletos.")

    min_cement = float(min_cement_str)
    max_cement = float(max_cement_str) if max_cement_str and max_cement_str.strip() else None
    max_a_c = float(max_a_c_str)

    return min_cement, max_cement, max_a_c

def calc_water(consistency, aggregate_type, D):
    """
    Calcula la demanda de agua base (A) en l/m³ según la consistencia, tipo de árido y tamaño máximo.
    """
    try:
        water_demand = TABLE_7_22_WATER_DEMAND[consistency][aggregate_type][D]
        return float(water_demand)
    except KeyError as e:
        raise ValueError(f"No se pudo encontrar la demanda de agua para: consistencia='{consistency}', tipo_árido='{aggregate_type}', D={D}. Error: {e}")

def calc_Z_and_wc(fcm, aggregate_type):
    """
    Calcula el factor Z y la relación agua/cemento (w/c) inicial.
    """
    try:
        K = TABLE_7_21_K_PARAMETER[aggregate_type]
    except KeyError as e:
        raise ValueError(f"No se pudo encontrar el parámetro K para el tipo de árido: '{aggregate_type}'. Error: {e}")

    Z = K * fcm + 0.5
    if Z <= 0:
        raise ValueError("El factor Z calculado no es positivo, lo que lleva a una relación w/c inválida. Verifique los valores de fcm y K.")
    wc = 1 / Z
    return Z, wc

def adjust_cement(water_A, initial_cement_kg, initial_wc, min_cement_norm, max_wc_norm, max_cement_norm):
    """
    Ajusta el contenido de cemento según las normativas y límites.
    """
    adjusted_cement_kg = initial_cement_kg
    adjustment_message = ""

    # Ajuste por relación w/c máxima
    if initial_wc > max_wc_norm:
        required_cement_for_wc = water_A / max_wc_norm
        if required_cement_for_wc > adjusted_cement_kg:
            adjusted_cement_kg = required_cement_for_wc
            adjustment_message += f"Cemento aumentado a {adjusted_cement_kg:.2f} kg/m³ para cumplir el límite máximo de w/c de {max_wc_norm:.2f}. "

    # Ajuste por contenido mínimo de cemento
    if adjusted_cement_kg < min_cement_norm:
        original_adjusted_cement = adjusted_cement_kg
        adjusted_cement_kg = min_cement_norm
        if original_adjusted_cement != adjusted_cement_kg:
            adjustment_message += f"Cemento aumentado a {adjusted_cement_kg:.2f} kg/m³ para cumplir el contenido mínimo de cemento de {min_cement_norm:.2f} kg/m³. "

    # Ajuste por contenido máximo de cemento (si aplica)
    if max_cement_norm is not None and adjusted_cement_kg > max_cement_norm:
        original_adjusted_cement = adjusted_cement_kg
        adjusted_cement_kg = max_cement_norm
        adjustment_message += f"Cemento limitado a {max_cement_norm:.2f} kg/m³ para cumplir el contenido máximo de cemento permitido. Esto podría afectar la resistencia objetivo. "

    return adjusted_cement_kg, adjustment_message.strip()

def compute_fineness_modules_from_sieve(sieve_data_str, num_fractions):
    """
    Calcula los módulos de finura (m0, m1) a partir de los datos del tamiz.
    """
    sieve_data = []
    if not sieve_data_str.strip():
        default_data = DEFAULT_SIEVE_DATA_2_FRACTIONS_STR if num_fractions == 2 else DEFAULT_SIEVE_DATA_3_FRACTIONS_STR
        sio = io.StringIO(default_data)
        df = pd.read_csv(sio, header=None)
        sieve_data = df.values.tolist()
    else:
        try:
            sio = io.StringIO(sieve_data_str)
            df = pd.read_csv(sio, header=None)
            sieve_data = df.values.tolist()
        except Exception as e:
            raise ValueError(f"Error al procesar los datos de tamices. Verifique el formato CSV. Error: {e}")

    expected_cols = 3 if num_fractions == 2 else 4
    if not sieve_data or len(sieve_data[0]) != expected_cols:
        raise ValueError(f"Número incorrecto de columnas en los datos de tamices. Se esperaban {expected_cols} para {num_fractions} fracciones. Asegúrese de que los datos de tamices están bien formateados.")

    sum_retained_A2 = 0.0
    sum_retained_A3 = 0.0
    has_A3_column_in_data = (len(sieve_data[0]) == 4) if sieve_data else False

    for row in sieve_data:
        try:
            sum_retained_A2 += float(row[2])
            if has_A3_column_in_data:
                sum_retained_A3 += float(row[3])
        except ValueError:
            raise ValueError("Los datos de porcentaje retenido en la tabla de tamices deben ser números válidos.")
    
    m0, m1 = None, None
    if num_fractions == 2:
        m0 = sum_retained_A2 / 100.0
    elif num_fractions == 3:
        if has_A3_column_in_data:
            m0 = sum_retained_A3 / 100.0
            m1 = sum_retained_A2 / 100.0
        else:
            raise ValueError("Para 3 fracciones, se esperaba la columna '% que retiene A3' para calcular m0 y m1. Asegúrese de que los datos de tamices tienen 4 columnas.")
            
    return m0, m1

def apply_corrections(t_fractions, aggregate_type, vibrated, placing_type, air_pct):
    """
    Aplica correcciones a los porcentajes de las fracciones de árido.
    """
    corrected_t = list(t_fractions)
    if len(corrected_t) < 2: return corrected_t 

    # Corrección por tipo de árido (triturado)
    if aggregate_type == "crushed":
        bonus = 4.0
        corrected_t[0] += bonus 
        if len(corrected_t) > 1:
            remaining_sum = sum(corrected_t[1:])
            if remaining_sum > 0:
                for i in range(1, len(corrected_t)):
                    corrected_t[i] -= (bonus * (corrected_t[i] / remaining_sum))
    
    # Corrección por vibrado
    if vibrated:
        bonus = 4.0
        corrected_t[-1] += bonus 
        if len(corrected_t) > 1:
            remaining_sum = sum(corrected_t[:-1])
            if remaining_sum > 0:
                for i in range(len(corrected_t) - 1):
                    corrected_t[i] -= (bonus * (corrected_t[i] / remaining_sum))

    # Corrección por tipo de colocación (masa)
    if placing_type == "mass":
        bonus = 3.0
        corrected_t[-1] += bonus 
        if len(corrected_t) > 1:
            remaining_sum = sum(corrected_t[:-1])
            if remaining_sum > 0:
                for i in range(len(corrected_t) - 1):
                    corrected_t[i] -= (bonus * (corrected_t[i] / remaining_sum))

    # Corrección por aire ocluido
    if air_pct > 0:
        deduction = air_pct
        if len(corrected_t) > 0:
            corrected_t[0] -= deduction 

    # Asegurarse de que ningún porcentaje sea negativo
    return [max(0, val) for val in corrected_t]

def normalize_aggregate_percentages(t_fractions):
    """
    Normaliza los porcentajes de las fracciones de árido para que sumen 100%.
    """
    current_sum = sum(t_fractions)
    if current_sum <= 0:
        return [100.0 / len(t_fractions)] * len(t_fractions) if len(t_fractions) > 0 else []
    return [(val / current_sum) * 100.0 for val in t_fractions]

# --- Interfaz de Streamlit ---

st.set_page_config(layout="wide", page_title="Calculadora de Hormigones")

st.title("Bienvenido a la calculadora de hormigones")
st.header("--- Diseño de Mezclas de Hormigón Carlos de la Peña ---")

st.subheader("Por favor, proporcione los siguientes parámetros:")

# Inicializar estados de sesión
if 'show_final_results' not in st.session_state:
    st.session_state.show_final_results = False
if 't1_pct_input' not in st.session_state:
    st.session_state.t1_pct_input = 25.0

# Columna para inputs generales
col1, col2 = st.columns(2)
with col1:
    fcm = st.number_input("Resistencia a la compresión a los 28 días (fcm en N/mm²)", min_value=5.0, value=32.0, step=1.0)
    consistency = st.selectbox("Consistencia", ["dry", "plastic", "soft", "flowable"], index=0)
    S = st.number_input("Asentamiento en mm (cono de Abrams)", min_value=0.0, value=40.0, step=5.0)
    aggregate_type = st.selectbox("Tipo de árido", ["rounded", "crushed"], index=0)
    D = st.selectbox("Tamaño máximo del árido en mm", [20, 40, 80], index=2)

with col2:
    # Este selectbox controla directamente la visibilidad de t1
    st.session_state.num_fractions = st.selectbox("Número de fracciones de árido", [2, 3], index=0, help="3 fracciones requieren entrada de análisis granulométrico con 3 columnas de %retenido")
    
    placing_type = st.selectbox("Tipo de colocación", ["mass", "reinforced", "prestressed"], index=0)
    exposure_class = st.text_input("Clase de exposición (ej., X0, XC1... XM3)", "XC3").upper().strip()
    vibrated_input = st.radio("¿Está el hormigón vibrado?", ["yes", "no"], index=0)
    vibrated = (vibrated_input == "yes")
    air_pct = st.number_input("Porcentaje de aire ocluido (ej., 0 para sin aire)", min_value=0.0, value=1.0, step=0.1)
    st.session_state.air_pct = air_pct
    

st.subheader("--- Datos de Análisis Granulométrico ---")

sieve_help_text = "Formato: Tamiz_mm,% retenido A1,% retenido A2[,% retenido A3]"
sieve_data_str = st.text_area(
    "Tabla de análisis granulométrico (dejar en blanco para usar datos por defecto)", 
    height=250, 
    help=sieve_help_text
)

# --- Sección de inputs para t0 y t1 (SIEMPRE VISIBLE, t1 CONDICIONAL) ---
st.subheader("--- Proporciones de Árido ---")

st.image(
    "assets/t0_instructions.png",
    caption="🛈 El valor de t0 es el % de la fracción más fina sobre el volumen total de áridos.",
    use_container_width=True
)

t0_finest_agg_pct = st.number_input(
    "Porcentaje t0 para la fracción de árido más fina (del volumen total de áridos)",
    min_value=0.0, max_value=100.0, value=65.0, step=1.0,
    key="t0_input"
)

# Lógica para mostrar t1_pct_input SÓLO si num_fractions es 3
t1_pct = 0.0 # Inicializamos t1_pct con un valor por defecto
if st.session_state.num_fractions == 3: 
    st.image(
        "assets/t1_instructions.png", 
        caption="🛈 El valor de t1 es el % de la segunda fracción de árido (del volumen total de áridos).",
        use_container_width=True
    )
    t1_pct = st.number_input(
        "Porcentaje t1 para la segunda fracción de árido (del volumen total de áridos)",
        min_value=0.0, max_value=100.0, value=st.session_state.t1_pct_input, step=1.0, # Usa el valor guardado
        key="t1_input" 
    )
    st.session_state.t1_pct_input = t1_pct # Actualiza el valor en session_state
    
    if t0_finest_agg_pct + t1_pct > 100.0:
        st.warning(f"Advertencia: La suma de t0 ({t0_finest_agg_pct:.2f}%) y t1 ({t1_pct:.2f}%) excede el 100%. Por favor, ajuste t0 o t1.")
        st.stop() 
else: # Si num_fractions es 2, t1_pct se calcula
    t1_pct = 100.0 - t0_finest_agg_pct
    st.session_state.t1_pct_input = t1_pct # Guarda el calculado para consistencia

# --- Botón para iniciar el cálculo principal ---
if st.button("Calcular Diseño Final de Mezcla"):
    st.session_state.show_final_results = False # Resetea los resultados anteriores
    
    try:
        # 1. Cargar límites ambientales
        min_cement_norm, max_cement_norm, max_a_c_norm = load_limits(exposure_class, placing_type)
        st.session_state.min_cement_norm = min_cement_norm
        st.session_state.max_cement_norm = max_cement_norm
        st.session_state.max_a_c_norm = max_a_c_norm

        # 2. Calcular la demanda de agua base (A) en l/m³)
        water_A = calc_water(consistency, aggregate_type, D)
        st.session_state.water_A = water_A

        # 3. Calcular Z y la relación w/c
        Z_factor, initial_wc = calc_Z_and_wc(fcm, aggregate_type)
        st.session_state.initial_wc = initial_wc

        # 4. Calcular el contenido inicial de cemento
        initial_cement_kg = water_A * Z_factor
        st.session_state.initial_cement_kg = initial_cement_kg

        # 5. Validación normativa y ajuste de cemento
        adjusted_cement_kg, adjustment_message = adjust_cement(water_A, initial_cement_kg, initial_wc, min_cement_norm, max_a_c_norm, max_cement_norm)
        st.session_state.adjusted_cement_kg = adjusted_cement_kg

        # Calcular el volumen de cemento para ajuste posterior
        cement_volume_initial = initial_cement_kg / CEMENT_DENSITY
        cement_volume_adjusted = adjusted_cement_kg / CEMENT_DENSITY
        cement_volume_difference = cement_volume_adjusted - cement_volume_initial
        st.session_state.cement_volume_difference = cement_volume_difference

        # 6. Cálculo de Módulos de Finura (usando num_fractions del session_state)
        m0_sieve, m1_sieve = compute_fineness_modules_from_sieve(sieve_data_str, st.session_state.num_fractions)
        st.session_state.m0_sieve = m0_sieve
        st.session_state.m1_sieve = m1_sieve

        # Aseguramos que current_t1_pct tome el valor correcto (input o calculado)
        if st.session_state.num_fractions == 3:
            current_t1_pct = st.session_state.t1_pct_input # Usamos el valor del input directo
        else: 
            current_t1_pct = 100.0 - t0_finest_agg_pct # Se calcula t1 para 2 fracciones
        
        # Cálculo de proporciones de árido
        if st.session_state.num_fractions == 3:
            t2_pct = 100.0 - (t0_finest_agg_pct + current_t1_pct) 
            if t2_pct < 0:
                 st.warning(f"Advertencia: La suma de t0 ({t0_finest_agg_pct:.2f}%) y t1 ({current_t1_pct:.2f}%) excede el 100%. La tercera fracción (t2) se ha ajustado a 0%.")
                 t2_pct = 0.0
            initial_t_fractions = [max(0.0, t0_finest_agg_pct), max(0.0, current_t1_pct), max(0.0, t2_pct)]
            st.write(f"**Porcentajes iniciales de árido (t0, t1, t2):** {', '.join([f'{t:.2f}%' for t in initial_t_fractions])}")
        else: 
            initial_t_fractions = [t0_finest_agg_pct, current_t1_pct] 
            st.write(f"**Porcentajes iniciales de árido (t0, t1 calculados):** {', '.join([f'{t:.2f}%' for t in initial_t_fractions])}")

        # Aplicar correcciones
        corrected_t_fractions = apply_corrections(initial_t_fractions, aggregate_type, vibrated, placing_type, air_pct)
        st.write(f"**Porcentajes de árido después de las correcciones:** {', '.join([f'{t:.2f}%' for t in corrected_t_fractions])}")

        # Normalizar porcentajes
        final_aggregate_percentages = normalize_aggregate_percentages(corrected_t_fractions)
        st.write(f"**Porcentajes finales de árido normalizados:** {', '.join([f'{t:.2f}%' for t in final_aggregate_percentages])}")

        # --- Volúmenes Finales de Diseño de Mezcla ---
        st.header("--- Volúmenes Finales de Diseño de Mezcla ---")
        Vc = adjusted_cement_kg / CEMENT_DENSITY
        V_aridos = 1025.0 - Vc - water_A
        st.write(f"**Volumen disponible para áridos (V_aridos):** {V_aridos:.2f} litros/m³")

        # Cálculo inicial de volúmenes de árido (antes del ajuste por cemento)
        aggregate_volumes = [(t_pct / 100.0) * V_aridos for t_pct in final_aggregate_percentages]
        
        # Ajuste final del volumen de árido fino por diferencia de volumen de cemento
        if cement_volume_difference > 0 and len(aggregate_volumes) > 0:
            aggregate_volumes[0] -= cement_volume_difference
            if aggregate_volumes[0] < 0:
                st.warning(f"Advertencia: El volumen de árido fino se volvió negativo ({aggregate_volumes[0]:.2f} L) tras el ajuste por cemento. Se ha limitado a 0.")
                aggregate_volumes[0] = 0.0

        actual_total_agg_vol = sum(aggregate_volumes) 
        
        st.subheader("Proporciones Finales de Mezcla (por m³)")
        st.write(f"**Agua:** {water_A:.2f} litros")
        st.write(f"**Cemento:** {adjusted_cement_kg:.2f} kg ({Vc:.2f} litros)")
        st.write(f"**Porcentaje Granulométrico de Árido más fino (t0):** {t0_finest_agg_pct:.2f}%")
        if st.session_state.num_fractions == 3: # Solo muestra t1 si hay 3 fracciones
            st.write(f"**Porcentaje Granulométrico de Árido intermedio (t1):** {current_t1_pct:.2f}%")
        st.markdown("---")

        for i, vol in enumerate(aggregate_volumes):
            st.write(f"**Fracción de Árido {i+1}:**")
            st.write(f"  - Porcentaje (relativo a la porción total de árido): {final_aggregate_percentages[i]:.2f}%")
            st.write(f"  - Volumen: {vol:.2f} litros")

        # Comprobación final del volumen
        total_calculated_volume = water_A + Vc + actual_total_agg_vol
        st.subheader("Comprobación de Volumen Total")
        st.write(f"**Volumen total calculado:** {total_calculated_volume:.2f} litros/m³ (debería ser aproximadamente 1025 L/m³)")
        if abs(total_calculated_volume - 1025) > 10:
            st.warning("Advertencia: El volumen total calculado se desvía significativamente de 1025 L/m³. Por favor, verifique las entradas y los cálculos.")

        # Guardar en session_state para las gráficas
        st.session_state.aggregate_volumes = aggregate_volumes
        st.session_state.final_aggregate_percentages = final_aggregate_percentages
        st.session_state.show_final_results = True

    except (ValueError, KeyError, IndexError) as e:
        st.error(f"Ocurrió un error en el cálculo: {e}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado durante el cálculo: {e}")

# ——— Sección de gráficas ———
if st.session_state.get("show_final_results", False):
    st.subheader("📊 Composición de la mezcla")

    # Datos básicos (ya inicializados)
    water_l    = st.session_state.get("water_A", 0.0)
    cement_kg = st.session_state.get("adjusted_cement_kg", 0.0)
    cement_l  = cement_kg / CEMENT_DENSITY
    air_pct    = st.session_state.get("air_pct", 0.0)
    air_l      = (air_pct / 100.0) * 1025.0

    # Áridos
    agg_vols      = st.session_state.get("aggregate_volumes", [])
    agg_percents = st.session_state.get("final_aggregate_percentages", [])
    n_agg         = len(agg_vols)

    # Etiquetas con % granular
    componentes = ["Agua", "Cemento", "Aire ocluido"] \
                  + [f"Árido {i+1} ({agg_percents[i]:.1f}%)" for i in range(n_agg)]
    volumenes   = [water_l, cement_l, air_l] + agg_vols
    densidades  = [1.0, CEMENT_DENSITY, 0.0012] + [2.6] * n_agg 
    pesos       = [v * d for v, d in zip(volumenes, densidades)]

    df_comp = pd.DataFrame({
        "Componente":      componentes,
        "Volumen (L)":     volumenes,
        "Densidad (kg/L)": densidades,
        "Peso (kg)":       pesos
    }).set_index("Componente")

    st.dataframe(df_comp)

    fig = px.bar(
        df_comp.reset_index(),
        x="Componente",
        y=["Volumen (L)", "Peso (kg)"],
        barmode="group",
        title="Volumen y Peso de cada componente",
        text_auto=".1f"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Ejecuta primero el cálculo final para ver aquí la composición de la mezcla.")
