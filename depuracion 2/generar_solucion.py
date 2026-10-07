import nbformat as nbf
nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_code_cell('# Actividad 2.2 - Depuración de Registros de Pedidos\nimport pandas as pd\nimport numpy as np\nimport os\n\n# Cargar dataset\nruta = "ventas_erroneas_completo.csv"\ndf = pd.read_csv(ruta, header=None, dtype=str)\ncols = ["id_pedido","producto","cantidad","precio_unitario","cliente","fecha_hora","ciudad"]\ndf.columns = cols\ndf.head()'))

cells.append(nbf.v4.new_code_cell('# 1. Inspección inicial\ndf.shape, df.duplicated().sum(), df.isna().sum()'))

cells.append(nbf.v4.new_code_cell('# 2. Limpiar valores no numéricos/erróneos\n# Convertir valores sucios a NaN o corregir\nm = {"nan": None, "NaN": None, "null": None, "NULL": None, "error": None, "cincuenta": "50"}\nfor k,v in m.items():\n    df = df.replace(k, v, regex=False)\n\ndf[\"cantidad\"] = df[\"cantidad\"].astype(str).str.strip()\ndf[\"precio_unitario\"] = df[\"precio_unitario\"].astype(str).str.strip()\n\ndf.head()'))

cells.append(nbf.v4.new_code_cell('# 3. Normalizar fecha/hora al formato YYYY-MM-DD HH:MM:SS\ndf[\"fecha_hora_clean\"] = df[\"fecha_hora\"]\n# Formato DD/MM/YYYY\nmask = df[\"fecha_hora\"].astype(str).str.contains("/", na=False)\ndf.loc[mask, \"fecha_hora_clean\"] = pd.to_datetime(df.loc[mask, \"fecha_hora\"], dayfirst=True, errors=\"coerce\").dt.strftime(\"%Y-%m-%d %H:%M:%S\")\n# Formato YYYY-MM-DD HH:MM:SS existente\ndf[\"fecha_hora_clean\"] = pd.to_datetime(df[\"fecha_hora_clean\"], errors=\"coerce\").dt.strftime(\"%Y-%m-%d %H:%M:%S\")\ndf[\"fecha_hora\"] = df[\"fecha_hora_clean\"]\ndf.drop(columns=[\"fecha_hora_clean\"], inplace=True)\ndf.head()'))

cells.append(nbf.v4.new_code_cell('# 4. Detectar duplicados\nduplicados = df[df.duplicated(keep=\"first\")]\nprint(\"Registros duplicados detectados:\", len(duplicados))\nduplicados.head()'))

cells.append(nbf.v4.new_code_cell('# 5. Eliminar duplicados\ndf_limpio = df.drop_duplicates(keep=\"first\").copy()\nprint(\"Registros originales:\", len(df))\nprint(\"Registros después de limpieza:\", len(df_limpio))\nprint(\"Eliminados:\", len(df)-len(df_limpio))'))

cells.append(nbf.v4.new_code_cell('# 6. Guardar dataset mejorado\ndf_limpio.to_csv(\"ventas_limpias.csv\", index=False, encoding=\"utf-8-sig\")\ndf_limpio.to_excel(\"ventas_limpias.xlsx\", index=False)\ndf_limpio.head()'))

cells.append(nbf.v4.new_code_cell('# 7. Verificación\nprint(\"Duplicados restantes:\", df_limpio.duplicated().sum())\nmal = df_limpio[\"fecha_hora\"].astype(str)\nprint(\"Fechas no estándar (deben ser YYYY-MM-DD 00:00:00):\", (mal.str.match(r\"^\\d{4}-\\d{2}-\\d{2} 00:00:00$\", na=False)==False).sum())'))

cells.append(nbf.v4.new_code_cell('# Enlace a Colab (GitHub -> Colab)\n# https://colab.research.google.com/github/aresoff24/Actividad-2.2---Depuraci-n-de-Registros-de-Pedidos-.git'))

nb.cells = cells
nbf.write(nb, \"solucion.ipynb\")
print(\"ok\")
