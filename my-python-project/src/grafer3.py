df = pd.read_csv(file_path)

# Rensa och strukturera datan
df_clean = df.iloc[4:, [1, 7, 8, 9, 10]].copy()
df_clean.columns = ['Datum', 'JP_Systoliskt', 'JP_Diastoliskt', 'Pat_Systoliskt', 'Pat_Diastoliskt']
df_clean['Datum'] = pd.to_datetime(df_clean['Datum'], errors='coerce')

# Funktion för att plotta blodtrycksgraf med specifika färger
def plot_person_blood_pressure_with_colors(person):
    if person == 'Pat':
        systolic_col = 'Pat_Systoliskt'
        diastolic_col = 'Pat_Diastoliskt'
        label = 'Pat'
    elif person == 'JP':
        systolic_col = 'JP_Systoliskt'
        diastolic_col = 'JP_Diastoliskt'
        label = 'JP'
    else:
        raise ValueError("Invalid person. Choose either 'Pat' or 'JP'.")
    
    # Säkerställ att värdena är numeriska
    df_clean[systolic_col] = pd.to_numeric(df_clean[systolic_col], errors='coerce')
    df_clean[diastolic_col] = pd.to_numeric(df_clean[diastolic_col], errors='coerce')