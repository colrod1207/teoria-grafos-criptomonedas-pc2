from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import os

cg = CoinGeckoAPI()

# Mostrar categorías disponibles desde CoinGecko (uso temporal)
categorias = cg.get_coins_categories_list()
for cat in categorias:
    print(f"{cat['category_id']:35} → {cat['name']}")

print("\n==============================\n")

categorias_objetivo = {
  'artificial-intelligence': 'Inteligencia Artificial',
  'gaming': 'Videojuegos',
  'meme-token': 'Memecoins',
  'real-world-assets-rwa': 'Activos del Mundo Real',
}

criptos_lista = []
# Iterar por cada categoría
for slug, nombre_categoria in categorias_objetivo.items():
    print(f"Recolectando: {nombre_categoria}")
    
    for page in range(1, 6):  # Máximo 5 páginas por categoría
        try:
            data = cg.get_coins_markets(
                vs_currency='usd',
                category=slug,
                order='market_cap_desc',
                per_page=100,
                page=page,
                sparkline=False
            )

            if not data:
                break

            for cripto in data:
                criptos_lista.append({
                  'id': cripto.get('id'),
                  'symbol': cripto.get('symbol'),
                  'name': cripto.get('name'),
                  'category': nombre_categoria,
                  'current_price': cripto.get('current_price'),
                  'market_cap': cripto.get('market_cap'),
                  'total_volume': cripto.get('total_volume'),
                  'circulating_supply': cripto.get('circulating_supply'),
                  'max_supply': cripto.get('max_supply'),
                  'rank': cripto.get('market_cap_rank'),
                  'price_change_percentage_24h': cripto.get('price_change_percentage_24h'),
                  'ath': cripto.get('ath'),  
                  'atl': cripto.get('atl'),  
                  'high_24h': cripto.get('high_24h'),
                  'low_24h': cripto.get('low_24h'),
                  'market_cap_change_percentage_24h': cripto.get('market_cap_change_percentage_24h'),
                  'last_updated': cripto.get('last_updated')
              })


            time.sleep(1)  # Evita sobrecargar la API
        except Exception as e:
            print(f"Error en {nombre_categoria} página {page}: {e}")
            break
        

# Crear DataFrame
df = pd.DataFrame(criptos_lista)

# Eliminar duplicados
df = df.drop_duplicates(subset='id')

# Guardar CSV en la carpeta /data
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "criptos_por_categoria.csv")
df.to_csv(output_path, index=False)

print(f"\nGuardado exitosamente en: {output_path}")
print(f"Total de criptos recolectadas: {len(df)}")