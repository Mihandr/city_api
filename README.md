# city_api

Простое api для городов с координатами

**GET**	*http://[hostname]/api/v1.0/city*	\Получить список всех городов<br><br>
**GET**	*http://[hostname]/api/v1.0/city/[city_id]*	\Получить город по id или названию<br><br>
**POST**	*http://[hostname]/api/v1.0/cities/nearest*	\Получить два города рядом с точкой<br><br>
```
{
    "latitude": 56.7522,
    "longitude": 38.6155
}
```
**POST**	*http://[hostname]/api/v1.0/city*	\Добавить город<br><br>
```
{
    "title":"Saratov"
}
```
**DELETE**	*http://[hostname]/api/v1.0/city/[city_id]*	\Удалить город по id или названию
