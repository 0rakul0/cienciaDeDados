# Plotagem de mapa com python

import webbrowser
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

longe = None
latt = None

# Pegando as cordenadas do monuciopio
loc = Nominatim(user_agent="GetLoc")
municipio = input(f"Digite o nome do municipio: ")
getLoc = loc.geocode(municipio)
# getLoc = loc.geocode("Jardim América")
endereco = getLoc[0]
endereco = endereco.split(',')

for x in endereco:
    print(f"\t{x}")

longe = getLoc[1][0]
latt = getLoc[1][1]

coordenadas = [longe,latt]
print("cordenadas = ", coordenadas)

#chamando o mapa
mapa = folium.Map(location=[longe, latt], zoom_start = 16
                  # ,tiles='Stamen Toner'
                  # ,tiles='Stamen Terrain'
                  )
# adicionando um marcador
folium.Marker(location=[longe, latt],
              popup=f'<i>{getLoc[0]}</i>',
              tooltip='Click aqui',
              icon=folium.Icon(color='red')
              ).add_to(mapa)
# adiciondo area circular
folium.CircleMarker(
    location=[longe, latt],
    radius=50,
    color='#2186cc',
    fill = True,
    fill_color = '2186cc'
              ).add_to(mapa)

# add evento de click para pegar uma nova localização
mapa.add_child(folium.LatLngPopup())

# mapa de calor claro que quanto mais dados melhor e tem que ir como lista
HeatMap([coordenadas]).add_to(mapa)

mapa.save(r'./data/mapa.html')
