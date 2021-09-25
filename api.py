import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFrends:
    """API библиотека методов для тестирования приложения PetFrends"""

# Метод 1.
    def __init__(self):
        """Метод (1) присваивает переменной URL сайта PetFrends"""
        self.base_url = "https://petfriends1.herokuapp.com/"

# Метод 2.
    def get_api_key(self, email: str, password: str):
        """Метод (2) делает запрос к API сервера и возвращает статус запроса от сервера и результат в формате json
        с уникальным ключом пользователя, найденного по указанным email и password """
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# Метод 3.
    def get_list_of_pets(self, auth_key: str, filter: str):
        """Метод (3) делает запрос к API сервера, возвращает статус запроса от сервера и результат в формате json
        со списком питомцев, которые удовлетворяют условию фильтра. Фильтр может иметь пустое значение, т.е.
        получить список всех питомцев, или значение my_pets - получить список собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# Метод 4.
    def post_new_pets(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод (4) отправляет на сервер данные о новом питомце, делает запрос к API сервера и возвращает статус запроса
         от сервера и результат в формате json с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# Метод 5.
    def delete_my_pets(self, auth_key: json, pet_id: json):
        """Метод (5) отправляет на сервер запрос на удаление данных о питомце по указанному ID, делает запрос к API сервера
        и возвращает статус запроса и результат в формате json с измененным списком питомцев"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'/api/pets/'+pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


# Метод 6.
    def put_info_pets(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str):
        """Метод (6) отправляет на сервер запрос на изменение данных о питомце по указанному ID, делает запрос к API
        сервера и возвращает статус запроса от сервера и результат в формате json с измененными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
        }

        res = requests.put(self.base_url + 'api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


# Метод 7.
    def post_new_pets_no_foto(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод (7) отправляет на сервер данные о новом питомце без фотографии, делает запрос к API сервера и
        возвращает статус запроса от сервера и результат в формате json с данными добавленного питомца"""

        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# Метод 8.
    def post_set_foto_my_pets(self, auth_key: json, pet_id: str, pet_photo: str):
        """Метод (8) отправляет на сервер данные - фотографию питомца , делает запрос к API сервера и возвращает статус
         запроса от сервера и результат в формате json с дополненными данными питомца"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image_1/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets/set_photo/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


# Метод 9.
    def post_new_pets_no_data(self, auth_key: json, pet_photo: str):
        """Метод (9) отправляет на сервер данные о новом питомце, в париаметрах которого присутствует только фотография,
         остальные параметры отсутствуют, делает запрос к API сервера и возвращает статус запроса
         от сервера и результат в формате json с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



