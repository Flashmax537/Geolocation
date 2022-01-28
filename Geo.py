import folium
from shapely.geometry import Point, Polygon
from folium.plugins import MarkerCluster
from geopy import Nominatim, Photon

# Точки на карте
points = [53.31344, 50.31275],\
         [53.326337949999996, 50.30529586355098],\
         [53.310510, 50.310060],\
         [53.310330, 50.308564]

# Добавление карты с координатой начала просмотра
my_map = folium.Map(location=[53.31344, 50.31275], zoom_start=15)
marker_cluster = MarkerCluster().add_to(my_map)

# Координаты полигона
coords = [(53.080002, 49.813385), (53.359568, 50.182114), (53.351781, 50.502090), (53.034607, 50.386047)]
coords2 = [(53.175610, 50.068990),
           (53.224670, 50.149820),
           (53.206135, 50.190182),
           (53.197140, 50.139440),
           (53.172927, 50.068784)]

# Полигон для проверки вхождения точки в него
poly = Polygon(coords)
poly2 = Polygon(coords2)

# Отрисовка точек на карте
for point in points:
    # Создание точки для проверочного полигона
    p = Point(point)

    geo_locator = Photon()
    loc = geo_locator.reverse(str(point[0]) + ', ' + str(point[1]))
    full_address = loc.raw['properties']
    city = full_address.get('city', '')
    street = full_address.get('street', '')
    house_number = full_address.get('housenumber', '')
    address = city + ', ' + street + ', д. ' + house_number

    # Описание текста точки
    popup = str(point) + ' ' + address

    # Проверка вхождения точки в полигон
    if p.within(poly):
        popup += ' "Входит" '
    else:
        popup += ' "Не входит" '
    if p.within(poly2):
        popup += ' "Входит" '
    else:
        popup += ' "Не входит" '

    # Добавление точки на карте
    folium.Marker(location=point, tooltip=popup, icon=folium.Icon(color='blue'), draggable=True).add_to(marker_cluster)

# Отрисовка полигона на карте
folium.Polygon(coords, color='red').add_to(my_map)
folium.Polygon(coords2, color='green').add_to(my_map)

# Сохранение карты в html
my_map.save("map.html")
