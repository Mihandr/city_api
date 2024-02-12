"""
Описание запросов:

GET	http://[hostname]/api/v1.0/city	Получить список всех городов
GET	http://[hostname]/api/v1.0/city/[city_id]	Получить город по id или названию
POST	http://[hostname]/api/v1.0/cities/nearest	Получить два города рядом с точкой
{
    "latitude": 56.7522,
    "longitude": 38.6155
}
POST	http://[hostname]/api/v1.0/city	Добавить город
{
    "title":"Saratov"
}
DELETE	http://[hostname]/api/v1.0/city/[city_id]	Удалить город по id или названию

т.к. расстояние в км нам не важно, а необходимо лишь показать ближайшие к точке города,
для простоты выбрана формула для расчета растояния на плоскости √((хА – хВ)2 + (уА – уВ)2)

"""

from flask import Flask, jsonify, abort, make_response, request
from geopy.geocoders import Nominatim
import random
import math

app = Flask(__name__)

cities = [
    {
        'id': 1,
        'title': u'Moscow',
        'latitude': 55.6256,
        'longitude': 37.6064,
    },
    {
        'id': 2,
        'title': u'Volgograd',
        'latitude': 48.6484,
        'longitude': 44.3849,
    },
    {
        'id': 3,
        'title': u'Saransk',
        'latitude': 54.1867,
        'longitude': 45.1838,
    }
]


def distance_between(latitude_A, longitude_A, latitude_B, longitude_B):
    answer = round(math.sqrt((latitude_A - latitude_B) ** 2 + (longitude_A - longitude_B) ** 2), 4)
    return answer


def nearest_cities(list, latitude_X, longitude_X):
    nearest_1 = {'dist': 999.9, 'title': u'Test'}
    nearest_2 = {'dist': 999.9, 'title': u'Test'}
    for i in list:
        x = distance_between(latitude_X, longitude_X, i["latitude"], i["longitude"])
        if x < nearest_1['dist']:
            nearest_2 = nearest_1.copy()
            nearest_1['dist'] = x
            nearest_1['title'] = i['title']
        elif x < nearest_2['dist']:
            nearest_2['dist'] = x
            nearest_2['title'] = i['title']
    return nearest_1['title'], nearest_2['title']


def get_loc(city_name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name)
    return round(getLoc.latitude, 4), round(getLoc.longitude, 4)


@app.route('/api/v1.0/cities', methods=['GET'])
def get_cities():
    return jsonify({'cities': cities})


@app.route('/api/v1.0/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    if city_id.isdigit():
        city = [list(filter(lambda t: t['id'] == int(city_id), cities))]
    else:
        city = [list(filter(lambda t: t['title'] == city_id, cities))]
    if len(city) == 0:
        abort(404)
    return jsonify({'city': city[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1.0/cities', methods=['POST'])
def create_city():
    if not request.json or not 'title' in request.json:
        abort(400)
    if cities == []:
        c_id = 1
    else:
        c_id = cities[-1]['id'] + 1
    title = request.json['title']
    latitude, longitude = get_loc(title)
    city = {
        'id': c_id,
        'title': title,
        'latitude': latitude,
        'longitude': longitude,
    }
    cities.append(city)
    return jsonify({'city': city}), 201


@app.route('/api/v1.0/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    if city_id.isdigit():
        city = [list(filter(lambda t: t['id'] == int(city_id), cities))]
    else:
        city = [list(filter(lambda t: t['title'] == city_id, cities))]
    if len(city) == 0:
        abort(404)
    cities.remove(city[0][0])
    return jsonify({'result': True})


@app.route('/api/v1.0/cities/nearest', methods=['POST'])
def two_cities():
    if not request.json or not 'latitude' in request.json or not 'longitude' in request.json or len(cities) == 0:
        abort(400)
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    answer = nearest_cities(cities, latitude, longitude)
    dict_return = {'title_1': answer[0], 'title_2': answer[1]}
    return jsonify(dict_return)


if __name__ == '__main__':
    app.run(debug=True)
