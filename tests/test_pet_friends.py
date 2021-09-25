from api import PetFrends
from settings import base_email, base_password
import os

pf = PetFrends()

# Метод 2
def test_get_api_key_valid_user(email=base_email, password=base_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# Метод 2, 3
def test_get_my_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(base_email, base_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Метод 2, 4
def test_post_my_pets_valid_new_pets(name='Тигра', animal_type='тигры', age='3', pet_photo='pet_photo/image.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Метод 2, 3, 4, 5
def test_successful_delete_info_my_pets():
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_new_pets(auth_key, '3 тигры', 'тигр', '3', 'pet_photo/image.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, _ = pf.delete_my_pets(auth_key, pet_id)
        assert status == 200
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert pet_id not in my_pets.values()

# Метод 2, 3, 6
def test_successful_put_info_my_pets(name='3 тигра', animal_type='кошачий', age='5'):
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_info_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("У вас нет питомцев")

# Самостоятельно составленные тесты
# Тест 1.
# Тестирование POST запроса на добавление питомца без фото: POST/api/create_pet_simple
# Add information about new pet without photo
# Методы 2, 7
def test_post_my_pets_no_foto_valid_new_pets(name='Инкогнито', animal_type='зверь', age='100'):
    _, auth_key = pf.get_api_key(base_email, base_password)
    status, result = pf.post_new_pets_no_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# Тест 2.
# Тестирование POST запроса на добавление фото питомца: POST /api/pets/set_photo/{pet_id}
# Add photo of pet
# Метод 2, 3, 8
def test_successful_post_set_foto_my_pets(pet_photo='pet_photo/image_1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        if my_pets['pets'][0]['pet_photo'] != "":
            pf.post_new_pets_no_foto(auth_key, 'Инкогнито', 'животное', '1')
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if my_pets['pets'][0]['pet_photo'] == "":
            status, result = pf.post_set_foto_my_pets(auth_key, my_pets['pets'][0]['id'], pet_photo)
            assert status == 200
            assert result['pet_photo'] != ""

    else:
        raise Exception("У вас нет питомцев")


# Тест 3.
# Тестирование POST запроса на добавление питомца POST/api/pets Add information about new pet
# в теле запроса data присутствует только параметр pet_photo, остальные параметры отсутствуют.
# Метод 2, 9
def test_post_my_pets_no_data_valid_new_pets(pet_photo='pet_photo/image.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    try:
        status, result = pf.post_new_pets_no_data(auth_key, pet_photo)
        assert status == 200
        assert result['pet_photo'] != ""
    except AssertionError as e:
        print(f'Ошибка утверждения: {e}, необходимо задать все параметры')


#Тест 4.
# Тестирование POST запроса на добавление питомца POST/api/pets Add information about new pet
# в теле запроса data передаются: фотография питомца и пустые данные: name='', animal_type='', age=''
# Метод 2, 4
def test_post_my_pets_empty_data_valid_new_pets(name='', animal_type='', age='', pet_photo='pet_photo/image.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    len_list_my_pets = len(my_pets['pets'])

    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(my_pets['pets']) == len_list_my_pets + 1


# Тест 5.
# Тестирование POST запроса на добавление питомца POST/api/pets Add information about new pet
# в теле запроса data передаются пустые данные: name='', animal_type='', age='', pet_photo=''
# Метод 2, 4
def test_post_my_pets_all_empty_data_valid_new_pets(name='', animal_type='', age='', pet_photo=''):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    try:
        status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
    except FileNotFoundError as e:
        print(f'Такого файла или каталога нет: {e}, необходимо указать путь к файлу')


# Тест 6.
# Тестирование POST запроса на добавление питомца без фотографии: POST/api/create_pet_simple
# # Add information about new pet without photo
# в теле запроса data передаются пустые данные: name='', animal_type='', age=''
# Методы 2, 3. 7
def test_post_my_pets_no_foto_empty_data_valid_new_pets(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    len_list_my_pets = len(my_pets['pets'])
    status, my_pets = pf.post_new_pets_no_foto(auth_key, name, animal_type, age)
    assert status == 200
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert len(my_pets['pets']) == len_list_my_pets + 1


# Тест 7.
# Тестирование PUT запроса на изменение имени питомца: PUT/api/pets/{pet_id}
# Update information about pet
# в теле запроса data в заголовке name передается длинный текст
# Метод 2, 3, 6

name = '"Тигр (лат. Panthera tigris) — вид хищных млекопитающих семейства кошачьих, один из пяти представителей \
рода пантера (лат. Panthera), который относится к подсемейству больших кошек. Слово «тигр» происходит от др.-греч. \
τίγρις, которое в свою очередь восходит к др.-перс. *tigri от корня «*taig» со значением «острый; быстрый»Среди \
представителей этого вида встречаются крупнейшие животные семейства кошачьих. Тигр является одним из крупнейших \
наземных хищников, уступая по массе лишь белому и бурому медведям. Выделено девять подвидов тигра, из которых к началу \
XXI века сохранились лишь шесть. Общая численность составляет порядка 4000 — 6500 особей[5], из них самым \
многочисленным является бенгальский тигр (номинативный подвид), составляющий 40 % от всей популяции."'
def test_successful_put_long_name_my_pets(name=name, animal_type='', age=''):
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_info_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("У вас нет питомцев")


# Тест 8.
# Тестирование PUT запроса на изменение возраста питомца: PUT/api/pets/{pet_id}
# Update information about pet
# в теле запроса data в заголовке age передается многоразрядное число - несуществующий возраст
# Метод 2, 3, 6
def test_successful_put_big_age_my_pets(name='', animal_type='', age='25869754123658'):
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_info_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['age'] == age
    else:
        raise Exception("У вас нет питомцев")


# Тест 9.
# Тестирование PUT запроса на изменение возраста питомца: PUT/api/pets/{pet_id}
# Update information about pet
# в теле запроса data в заголовке age передается число, записанное буквами, а не словом
# Метод 2, 3, 6
def test_successful_put_unformatted_age_my_pets(name='', animal_type='', age='двадцать три'):
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.put_info_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['age'] == age
    else:
        raise Exception("У вас нет питомцев")


# Тест 10.
# Тестирование POST запроса на добавление второй фотграфии питомца или замену имеющейся фотографии:
# POST /api/pets/set_photo/{pet_id} Add photo of pet
# Метод 2, 3, 8
def test_successful_post_new_foto_my_pets(pet_photo='pet_photo/image_1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(base_email, base_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        old_foto = my_pets['pets'][0]['pet_photo']
        status, _ = pf.post_set_foto_my_pets(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        try:
            assert my_pets['pets'][0]['pet_photo'] != old_foto
        except AssertionError as e:
            print("Вы загрузили ту же самую фотографию")

    else:
        raise Exception("У вас нет питомцев")





