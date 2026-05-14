import pandas as pd

# --- 1. Creación del archivo Excel ---
def create_student_excel(filename):
    data = {
        'Student Name': ['Alice Johnson', 'Bob Smith', 'Charlie Davis', 'Diana Prince', 'Evan Wright'],
        'Student Age': [20, 21, 19, 22, 20],
        'No. of Lab completed': [10, 8, 12, 11, 9],
        'Average score': [92.5, 78.0, 88.4, 95.2, 81.6]
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Archivo '{filename}' creado exitosamente.\n")

# --- 2. Extracción con Programación Funcional ---

def load_data(filename):
    """Función pura para cargar datos."""
    return pd.read_excel(filename)

def format_row(row):
    """Función para dar formato a una fila individual (mapeo)."""
    return f"Estudiante: {row['Student Name']} | Edad: {row['Student Age']} | Labs: {row['No. of Lab completed']} | Promedio: {row['Average score']}"

def process_and_print(df):
    """Utiliza map para aplicar la lógica de formato a cada fila."""
    formatted_data = list(map(format_row, df.to_dict('records')))
    
    for line in formatted_data:
        print(line)


file_name = 'student_lab_records.xlsx'

# 1. Crear el archivo (Solo necesario la primera vez)
create_student_excel(file_name)

# 2. Pipeline funcional: Cargar -> Procesar -> Imprimir
data_df = load_data(file_name)
process_and_print(data_df)