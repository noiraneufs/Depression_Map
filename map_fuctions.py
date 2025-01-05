import folium
import requests
import pandas as pd
from folium import GeoJson, GeoJsonTooltip
from branca.colormap import linear
from country_data import country_mapping  # Importando o dicionário

# Carregar o mapa de calor
def create_map():
    world_map = folium.Map(
        location=[0, 0], 
        zoom_start=2, 
        tiles='http://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png', 
        attr='© CARTO'
    )
    
    # Carregar dados GeoJSON
    url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
    response = requests.get(url)
    geojson_data = response.json()

    return world_map, geojson_data

# Função para adicionar o GeoJson com base no índice de depressão
def add_geojson(map_obj, geojson_data, df):
    # Mapeando os países pelos nomes (a coluna 'country' já deve conter o nome do país)
    df['country_name'] = df['country'].map(country_mapping)
    
    # Filtrando para manter apenas os países que estão presentes no GeoJSON (usando nome completo)
    geojson_countries = {feature['properties']['name'] for feature in geojson_data['features']}
    df = df[df['country_name'].isin(geojson_countries)]
    
    # Agrupar e calcular a média de depressão por país
    country_depression = df.groupby('country_name')['indice_depressao'].mean().reset_index()
    
    # Converter para dicionário com o país como chave
    depression_dict = country_depression.set_index('country_name')['indice_depressao'].to_dict()
    
    # Adicionar o índice de depressão ao objeto GeoJSON
    for feature in geojson_data['features']:
        country_name = feature['properties']['name']
        if country_name in depression_dict:
            feature['properties']['mean_depression_index'] = depression_dict[country_name]
        else:
            feature['properties']['mean_depression_index'] = None  # País sem participantes
    
    # Definir a faixa de valores para o colormap
    min_value = min(depression_dict.values(), default=0)
    max_value = max(depression_dict.values(), default=1)
    
    colormap = linear.YlOrRd_09.scale(min_value, max_value)
    
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': (
                colormap(feature['properties'].get('mean_depression_index', 0))
                if feature['properties'].get('mean_depression_index') is not None else '#b4b49c'
            ),
            'color': 'black',  
            'weight': 1,
            'fillOpacity': 0.7 if feature['properties'].get('mean_depression_index') is not None else 0.3,
        },
        tooltip=GeoJsonTooltip(
            fields=['name', 'mean_depression_index'],
            aliases=['Country:', 'Average Depression Index:'],
            localize=True,
            sticky=True,
            labels=True,
            html='<div style="font-size: 14px;"><strong>Country:</strong> {name}<br><strong>Average Depression Index:</strong> {mean_depression_index:.2f}</div>'
        )
    ).add_to(map_obj)
    
    return map_obj

# Carregar mapa e dados
world_map, geojson_data = create_map()

# Carregar dataset
dataset_url = 'dataset.csv'  # Substitua pelo caminho correto para o seu dataset
df = pd.read_csv(dataset_url)

# Adicionar o GeoJson e o tooltip
map_with_geojson = add_geojson(world_map, geojson_data, df)

# Colormap para os valores de depressão
colormap = linear.YlOrRd_09.scale(df['indice_depressao'].min(), df['indice_depressao'].max())

# Função para adicionar a legenda personalizada
def add_custom_legend(map_obj, colormap):
    legend_values = [colormap.vmin, colormap.vmin + (colormap.vmax - colormap.vmin) * 0.25,
                     colormap.vmin + (colormap.vmax - colormap.vmin) * 0.50,
                     colormap.vmin + (colormap.vmax - colormap.vmin) * 0.75, colormap.vmax]
    
    # Criar a faixa de cores para a legenda
    legend_colors = [colormap(val) for val in legend_values]
    
    # Criar uma legenda baseada no colormap
    legend_html = '''
    <div style="position: fixed; bottom: 20px; left: 20px; width: 220px; height: 100px; 
        background-color: rgba(0, 0, 0, 0.7); border:0px solid grey; 
        border-radius: 6px; z-index:9999; font-size:12px; color: white; padding: 8px;">
        <div style="text-align: center; font-weight: bold; margin-bottom: 5px;">Average Index Legend</div>
        <div style="margin-bottom: 5px;">
            <div style="width: 100%; height: 15px; background: linear-gradient(to right, {}); border-radius: 10px;"></div>
            <div style="display: flex; justify-content: space-between; width: 100%; margin-top: 5px;">
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
            </div>
        </div>
        <div style="margin-top: 10px;">
            <div style="width: 15px; height: 15px; background-color: #403438; display: inline-block; border: 1px solid black;"></div>
            <span style="margin-left: 5px;">Insufficient sample</span>
        </div>
    </div>
    '''.format(
        ', '.join(legend_colors),
        *legend_values
    )
    
    map_obj.get_root().html.add_child(folium.Element(legend_html))

# Adicionar a legenda personalizada
add_custom_legend(map_with_geojson, colormap)

# Salvar o mapa
map_with_geojson.save('mapa_de_calor_com_legenda.html')
