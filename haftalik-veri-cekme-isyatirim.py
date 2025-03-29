import pandas as pd
from isyatirimhisse import StockData
import os

hisse_kodları = [
    "AHGAZ", "AGESA", "AGHOL", "AKBNK", "AKFGY", "AKGRT", "AKMGY", "AKSGY", "ALBRK", "ALCTL", "ANHYT", 
    "ANSGR", "ARDYZ",  "ASELS", "ASTOR", "ATATP", "ATLAS", "AVGYO", "AVHOL", "AYEN", "AYGAZ", "AZTEK", 
    "BANVT", "BASGZ", "BFREN", "BIGCH", "BIMAS", "BRISA", "BRLSM", "BURCE", "BURVA", "CCOLA", "CIMSA", 
    "CLEBI", "CRDFA", "CUSAN", "CVKMD", "DARDL", "DERIM", "DESA", "DESPC", "DGATE", "DNISI", "DOCO", "DOHOL", 
    "DYOBY", "DZGYO", "EBEBK", "EDIP", "EGEEN", "EGGUB", "EGPRO", "EKGYO", "ELITE", "EMKEL", "ENERY", 
    "ENJSA", "ENKAI", "EREGL", "ETILR", "EUPWR", "EUREN", "EYGYO", "FADE", "FMIZP", "FONET", "FORTE", "FRIGO", 
    "FROTO", "GARAN", "GARFA", "GENIL", "GEREL", "GESAN", "GLCVY", "GLYHO", "GMTAS", "GOKNR", "GRSEL", "GSDDE", 
    "GSDHO", "GUBRF", "GZNMI", "HALKB", "HTTBT", "HUNER", "IMASM", "INGRM", "IPEKE", "ISCTR", "ISDMR", "ISFIN", 
    "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISYAT", "KATMR", "KERVT", "KLKIM", "KLSYN", "KONTR", "KOPOL", "KOZAA", 
    "KRPLS", "KRSTL", "KUTPO", "KUYAS", "LIDFA", "LINK", "LKMNH", "LOGO", "MACKO", "MAKTK", "MARTI", "MAVI", 
    "MERIT", "MERKO", "MGROS", "MIATK", "MPARK", "MRGYO", "MTRKS", "NTGAZ", "NTHOL", "NUHCM", "OBASE", "ORGE", 
    "OYAKC", "OZKGY", "PAGYO", "PAPIL", "PASEU", "PCILT", "PENTA", "PETUN", "PGSUS", "PINSU", "PLTUR", "PRKME", 
    "RNPOL", "RYGYO", "RYSAS", "SAFKR", "SAHOL", "SANEL", "SEKFK", "SELEC", "SILVR", "SUNTK", "SUWEN", "TAVHL", 
    "TBORG", "TCELL", "TEZOL", "TGSAS", "THYAO", "TKFEN", "TNZTP", "TRGYO", "TRILC", "TSKB", "TTKOM", "TUKAS", 
    "TURSG", "ULKER", "ULUFA", "VAKBN", "VAKFN", "VERUS", "VKGYO", "YEOTK", "YKBNK", "ZRGYO"
]

stock_data = StockData()
save_directory = "/Users/yusufemreozden/Desktop/HAFTALIK_TARAMA"
os.makedirs(save_directory, exist_ok=True)

for hisse in hisse_kodları:
    try:
        df = stock_data.get_data(symbols=hisse, start_date='01-01-2019')

        df['DATE'] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)

        # Sadece CLOSING_TL ve VOLUME_TL yeterli
        df = df.resample('W').agg({
            'CLOSING_TL': 'last',
            'VOLUME_TL': 'sum'
        }).dropna().reset_index()

        file_name = f"{hisse}.xlsx"
        file_path = os.path.join(save_directory, file_name)
        df.to_excel(file_path, index=False)

        print(f"{hisse} haftalık kapanışlar kaydedildi: {file_path}")

    except Exception as e:
        print(f"{hisse} hata: {e}")