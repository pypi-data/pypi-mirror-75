import requests

URL = 'https://fsdk.uz/api/v2'

class UserApi():
    """
    Класс API юзера
    """
    def __init__(self):
        pass
    def get_stats(self, page=None):
        """
        Получить статистику игроков
        page=2 для получения второй страницы и т.д
        """
        data = requests.get(url=f'{URL}/stats', params={'page': page}).json()
        return data['data']
    def get_bans(self, page=None):
        """
        Получить забаненных игроков
        page=2 для получения второй страницы и т.д
        """
        data = requests.get(url=f'{URL}/bans', params={'page': page}).json()
        return data['data']
    def search_bans(self, query):
        """
        Поиск забаненного игрока
        query: может принимать Имя, IP, Steam ID игрока
        """
        data = requests.get(url=f'{URL}/bans', params={'search': query}).json()
        return data['data']
    def search_stats(self, query):
        """
        Поиск и получение статистики игрока
        query: может принимать Steam ID игрока
        """
        data = requests.get(url=f'{URL}/stats/steamid/{query}').json()
        return data['data']


class AdminApi():
    """
    Класс админ API
    token: принимает API токен
    """
    def __init__(self, token):
        """
        Класс админ API
        token: принимает API токен
        """
        self.token = token
    def get_info(self):
        """
        Получание информации о сервере
        """
        data = requests.get(url=f'{URL}/server-info', headers={'Authorization': self.token}).json()
        return data['data']
    def get_console_info(self):
        """
        Получение информации из консоли сервера
        """
        data = requests.get(url=f'{URL}/console', headers={'Authorization': self.token}).json()
        return data['data']
    def get_players(self):
        """
        Получение списка игроков на сервере
        """
        data = requests.get(url=f'{URL}/online', headers={'Authorization': self.token}).json()
        return data['data']
    def vote_map(self, name):
        """
        Голосование на карту
        name: принимает название карты
        """
        content = {"map": name, "type": "vote"}
        data = requests.post(url=f'{URL}/server/change-map', json=content, headers={'Authorization': self.token})
        return data.status_code
    def change_map(self, name):
        """
        Смена карты без голосования
        name: принимает название карты
        """
        content = {"map": name, "type": "direct"}
        data = requests.post(url=f'{URL}/server/change-map', json=content, headers={'Authorization': self.token})
        return data.status_code
    def get_admins(self):
        """
        Список админов, випов
        """
        data = requests.get(url=f'{URL}/admins', headers={'Authorization': self.token}).json()
        return data['data']
    def kick_player(self, user_id):
        """
        Кикнуть игрока с сервера
        user_id: принимает уникальный ид игрока
        """
        data = requests.post(f'{URL}/kick/{user_id}', headers={'Authorization': self.token})
        return data.status_code
    def send_rcon(self, rcon):
        """
        Отправить rcon команду на сервер
        rcon: принимает команду
        """
        content = {'command': rcon}
        data = requests.post(url=f'{URL}/server/rcon', json=content, headers={'Authorization': self.token})
        return data.status_code
    def add_admin(self, auth=None, access=None, flags=None, expires=None, password=None, note=None):
        """
        Добавления превилегий на сервер

        auth: принимает Имя, IP, Steam ID игрока
        access: принимает тип выдачи
        flags: принимает флаги доступа
        expires: принимает дату окончания превилегии
        password: принимает пароль превилегии
        note: принимает вашу запись к превилегии
        """
        content = {
            'auth': auth,
            'access': access,
            'flags': flags,
            'password': password,
            'expires_at': expires,
            'details': note
            }
        data = requests.post(url=f'{URL}/admins/update', params={'isUpdate': 'false'}, json=content, headers={'Authorization': self.token})
        return data.status_code
