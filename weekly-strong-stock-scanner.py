import pandas as pd
import numpy as np
import os
from datetime import datetime

# === RSI ===
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_rsi_signal(df):
    df['RSI'] = calculate_rsi(df['CLOSING_TL'])
    if len(df) < 2:
        return None
    rsi_now = df['RSI'].iloc[-1]
    rsi_prev = df['RSI'].iloc[-2]
    if rsi_prev < 65 and rsi_now > 65 and rsi_now > 40:
        return 'AL'
    return None

# === MACD ===
def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def get_macd_signal(df):
    macd, signal = calculate_macd(df['CLOSING_TL'])
    if len(macd) < 2:
        return None
    if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
        return 'AL'
    return None

# === MDTM ===
def calculate_t3_ema(series, period):
    ema1 = series.ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    ema3 = ema2.ewm(span=period, adjust=False).mean()
    return 3 * ema1 - 3 * ema2 + ema3

def get_mdtm_signal(df, short_period=24, long_period=26, signal_period=24):
    ma1 = calculate_t3_ema(df['CLOSING_TL'], short_period)
    ma2 = calculate_t3_ema(df['CLOSING_TL'], long_period)
    mdtm = ma1 - ma2
    trigger = calculate_t3_ema(mdtm, signal_period)
    if len(mdtm) < 2:
        return None
    if mdtm.iloc[-2] < trigger.iloc[-2] and mdtm.iloc[-1] > trigger.iloc[-1]:
        return 'AL'
    return None

# === Ana Tarama ===
def run_multi_signal_scan(data_folder, output_path):
    files = [f for f in os.listdir(data_folder) if f.endswith('.xlsx')]
    results = []

    for file in files:
        try:
            df = pd.read_excel(os.path.join(data_folder, file))
            df = df.sort_values('DATE').reset_index(drop=True)
            if len(df) < 35:
                continue

            sinyal_rsi = get_rsi_signal(df)
            sinyal_macd = get_macd_signal(df)
            sinyal_mdtm = get_mdtm_signal(df)

            sinyal_listesi = [sinyal_rsi, sinyal_macd, sinyal_mdtm]
            al_sayisi = sum(1 for s in sinyal_listesi if s == 'AL')

            if al_sayisi >= 2:
                results.append({
                    'Hisse': file.replace('.xlsx', ''),
                    'RSI': sinyal_rsi or '-',
                    'MACD': sinyal_macd or '-',
                    'MDTM': sinyal_mdtm or '-',
                    'Tarih': df['DATE'].iloc[-1].date()
                })

        except Exception as e:
            print(f"{file} hata verdi: {e}")
            continue

    result_df = pd.DataFrame(results)
    if not result_df.empty:
        result_df.to_excel(output_path, index=False)
        print(f"🚀 {len(result_df)} hisse güçlü sinyal verdi. Dosya: {output_path}")
    else:
        print("Hiçbir hisse için 2/3 AL sinyali oluşmadı.")

# === Çalıştır ===
if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    data_folder = '/Users/yusufemreozden/Desktop/HAFTALIK_TARAMA'
    output_file = f'/Users/yusufemreozden/Desktop/GUCLU_SINYALLER_{today}.xlsx'
    run_multi_signal_scan(data_folder, output_file)

