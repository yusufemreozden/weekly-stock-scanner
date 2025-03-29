import yfinance as yf
import pandas as pd
import os
import time

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

save_directory = "/Users/yusufemreozden/Desktop/HAFTALIK_TARAMA_YAHOO"
os.makedirs(save_directory, exist_ok=True)

for hisse in hisse_kodları:
    symbol = hisse + ".IS"
    try:
        df = yf.download(symbol, start="2019-01-01", interval="1wk", auto_adjust=False, group_by="ticker", progress=False)

        if df.empty:
            print(f"{symbol} için veri bulunamadı.")
            continue

        # MultiIndex düzleştir
        df.columns = df.columns.map(lambda x: x[1] if isinstance(x, tuple) else x)
        df.reset_index(inplace=True)

        # print(f"{symbol} kolonlar: {df.columns}") bu satırdan vazgeçtim çok gereksiz bir info oldu

        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        file_path = os.path.join(save_directory, f"{hisse}.xlsx")
        df.to_excel(file_path, index=False)

        print(f"{hisse} verisi başarıyla kaydedildi: {file_path}")

        time.sleep(0.25)  # Rate limit yedik bu riske karşı 1 saniye bekle

    except Exception as e:
        print(f"{hisse} için hata oluştu: {e}")
