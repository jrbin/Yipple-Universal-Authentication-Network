import os
import json
import bcrypt
import uuid

class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))

def registerUser(username, password):
    if not username or not password:
        return 500
    komrade = KomradeConfig("user")
    users = komrade.read()
    user = next((u for uid, u in users.items() if u.get('username') == username), None)
    if user is None:
        uid = str(uuid.uuid4())
        hashedpasswd = bcrypt.hashpw(password.encode(errors='ignore'), bcrypt.gensalt()).decode()
        users[uid] = {
            'id': uid,
            'username': username,
            'password': hashedpasswd,
        }
        komrade.write(users)
        return None
    # username exists
    return 400

def validateUser(username, password):
    komrade = KomradeConfig("user")
    users = komrade.read()
    user = next((u for uid, u in users.items() if u.get('username') == username), None)
    if user is None or any([key not in user for key in ['id', 'username', 'password']]):
        return None, 403
    hashedpasswd = bcrypt.hashpw(password.encode(errors='ignore'), user['password'].encode(errors='ignore')).decode()
    if user['password'] != hashedpasswd:
        return None, 403
    return user, None
