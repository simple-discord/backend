import bcrypt
import uuid
# байт строка
password = b"0986s"
# солед пароль (доп уровень безопасности)
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password, salt)

print(hashed_password, salt)


get_uuid = uuid.uuid4().hex
print(get_uuid)
