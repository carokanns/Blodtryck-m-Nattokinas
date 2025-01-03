import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.dates import date2num
import matplotlib.dates as mdates

print("\nLäser från denna map\n\n")

file_path = 'Nattokinase_effekt.csv'  # Se till att filen finns i rätt katalog
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

    # Ta bort rader med saknade eller ogiltiga värden
    df_clean_filtered = df_clean.dropna(subset=['Datum', systolic_col, diastolic_col])

    dates = df_clean_filtered['Datum']
    systolic = df_clean_filtered[systolic_col]
    diastolic = df_clean_filtered[diastolic_col]
    
    # Konvertera datum till numeriska värden för trendlinjeberäkning
    dates_num = date2num(dates)
    
    # Plotta systoliskt och diastoliskt blodtryck med specifika färger
    plt.figure(figsize=(10, 6))
    plt.plot(dates, systolic, label=f'{label} Systolic', color='blue', marker='o')
    plt.plot(dates, diastolic, label=f'{label} Diastolic', color='red', marker='o')
    
    # Trendlinje för systoliskt blodtryck (blå)
    if len(dates_num) > 1 and len(systolic) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(dates_num, systolic)
        line = slope * dates_num + intercept
        plt.plot(dates, line, 'b--', label=f'{label} Systolic Trend')
        print(f"Systolic trend: slope={slope}, intercept={intercept}")
    else:
        print(f"Not enough data points for {label} systolic trend")
    
    # Trendlinje för diastoliskt blodtryck (röd)
    if len(dates_num) > 1 and len(diastolic) > 1:
        slope_dia, intercept_dia, r_value_dia, p_value_dia, std_err_dia = stats.linregress(dates_num, diastolic)
        line_dia = slope_dia * dates_num + intercept_dia
        plt.plot(dates, line_dia, 'r--', label=f'{label} Diastolic Trend')
        print(f"Diastolic trend: slope={slope_dia}, intercept={intercept_dia}")
    else:
        print(f"Not enough data points for {label} diastolic trend")
    
    # Sätt titlar och etiketter
    plt.title(f'{label} Blood Pressure Over Time')
    plt.xlabel('Date')
    plt.ylabel('Blood Pressure (mmHg)')
    plt.legend()
    plt.grid(True)
    
    # Formatera x-axeln för bättre datumvisning
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    plt.tight_layout()
    plt.show()

    # Skriv ut data för felsökning
    # print(f"\nData för {label}:")
    # print(f"Antal datapunkter: {len(dates)}")
    # print("Första fem datapunkter:")
    # for i in range(min(5, len(dates))):
    #     print(f"Datum: {dates.iloc[i]}, Systolic: {systolic.iloc[i]}, Diastolic: {diastolic.iloc[i]}")

# Testa funktionen för JP och Pat med specifika färger
plot_person_blood_pressure_with_colors('JP')
plot_person_blood_pressure_with_colors('Pat')