# -*- coding: utf-8 -*-
import pandas as pd
import os

def main():
    df = pd.read_csv('ventas_erroneas_completo.csv', header=None, dtype=str)
    cols = ['id_pedido','producto','cantidad','precio_unitario','cliente','fecha_hora','ciudad']
    df.columns = cols
    print('Forma:', df.shape)
    print('Duplicados iniciales:', df.duplicated().sum())
    # limpiar sucios
    m = {'nan': None,'NaN': None,'null': None,'NULL': None,'error': None,'cincuenta':'50'}
    for k,v in m.items():
        df = df.replace(k,v,regex=False)
    df['cantidad']=df['cantidad'].astype(str).str.strip()
    df['precio_unitario']=df['precio_unitario'].astype(str).str.strip()
    # fechas
    s=df['fecha_hora'].astype(str)
    mask=s.str.contains('/',na=False)
    df['fh']=df['fecha_hora']
    df.loc[mask,'fh']=pd.to_datetime(df.loc[mask,'fecha_hora'],dayfirst=True,errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['fh']=pd.to_datetime(df['fh'],errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['fecha_hora']=df['fh']
    df.drop(columns=['fh'],inplace=True)
    # duplicados
    dup=df[df.duplicated(keep='first')]
    print('Duplicados detectados:', len(dup))
    dfl=df.drop_duplicates(keep='first').copy()
    print('Original:', len(df), 'Limpio:', len(dfl), 'Eliminados:', len(df)-len(dfl))
    # guardar
    dfl.to_csv('ventas_limpias.csv', index=False, encoding='utf-8-sig')
    dfl.to_excel('ventas_limpias.xlsx', index=False)
    # verif
    print('Duplicados restantes:', dfl.duplicated().sum())
    chk=dfl['fecha_hora'].astype(str)
    mal=(chk.str.match(r'^\d{4}-\d{2}-\d{2} 00:00:00$', na=False)==False)
    print('Fechas no estándar:', mal.sum())
    print('Listo. Archivos: ventas_limpias.csv, ventas_limpias.xlsx, solucion.ipynb, solucion.py')

if __name__=='__main__':
    main()
