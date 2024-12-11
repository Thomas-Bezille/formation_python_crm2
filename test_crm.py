import pytest
from crm import User
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    u.save()
    return u


def test_first_name(user):
    assert user.first_name == "Patrick"


def test_last_name(user):
    assert user.last_name == "Martin"


def test_address(user):
    assert user.address == "1 rue du chemin, 75000 Paris"


def test_phone_number(user):
    assert user.phone_number == "0123456789"


def test_full_name(user):
    assert user.full_name == "Patrick Martin"


def test_find_user(user):
    assert isinstance(user.find_user, table.Document)
    assert user.find_user["first_name"] == "Patrick"
    assert user.find_user["last_name"] == "Martin"
    assert user.find_user["address"] == "1 rue du chemin, 75000 Paris"
    assert user.find_user["phone_number"] == "0123456789"


def test_not_find_user(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.find_user is None


def test_check_phone_number(setup_db):
    good_user = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015 Paris",
                     phone_number="0123456789")
    bad_user = User(first_name="Jean",
                    last_name="Smith",
                    address="1 rue du chemin, 75015 Paris",
                    phone_number="abcd")
    
    with pytest.raises(ValueError) as err:
        bad_user._check_phone_number()
    assert "invalide" in str(err.value)
    
    good_user.save(validate_data=True)
    assert good_user.exists() is True


def test_check_names_empty(setup_db):
    bad_user = User(first_name="",
                    last_name="",
                    address="1 rue du chemin, 75015 Paris",
                    phone_number="0123456789")
    
    with pytest.raises(ValueError) as err:
        bad_user._check_names()
    assert "Le prénom et le nom de famille ne peuvent pas être vides." in str(err.value)


def test_check_invalid_characters(setup_db):
    bad_user = User(first_name="Patrick%#/?/",
                    last_name="Martin%#/?/",
                    address="1 rue du chemin, 75015 Paris",
                    phone_number="0123456789")
    
    with pytest.raises(ValueError) as err:
        bad_user._check_names()
    assert "Nom invalide Patrick%#/?/ Martin%#/?/" in str(err.value)
    

def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.exists() is False


def test_delete(setup_db):
    user_test = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015 Paris",
                     phone_number="0123456789")
    
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()
    
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)


def test_save(setup_db):
    user_test = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015 Paris",
                     phone_number="0123456789")
    user_test_duplicate = User(first_name="Jean",
                               last_name="Smith",
                               address="1 rue du chemin, 75015 Paris",
                               phone_number="abcd")

    first = user_test.save()
    second = user_test_duplicate.save()
    
    assert isinstance(first, str)
    assert not isinstance(second, str)
    assert "✅ Élément ajouté ✅" in first
    assert second is None