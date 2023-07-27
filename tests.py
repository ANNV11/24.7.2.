def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_app_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_pets_with_valid_data(name='Fedor', animal_type='cat', age='3', pet_photo='images/Fedor.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Murzik', 'cat', '5', 'images/Fedor.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='из', animal_type='измененный', age='5'):
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

def test_add_pets_with_valid_data_without_photo(name='МурзикБезФото', animal_type='кот', age='6'):
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_at_pet(pet_photo='images/German.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

def test_add_pet_negative_age_number(name='Fedor', animal_type='cat', age='-3', pet_photo='images/Fedor.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'

def test_add_pet_with_four_digit_age_number(name='Fedor', animal_type='cat', age='1234', pet_photo='images/Fedor.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст'

def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='2', pet_photo='images/Fedor.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'
