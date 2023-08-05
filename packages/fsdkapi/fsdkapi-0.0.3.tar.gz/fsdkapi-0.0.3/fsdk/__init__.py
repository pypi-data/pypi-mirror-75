import requests
from bs4 import BeautifulSoup

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

class InfoApi():
    """
    Класс API информации
    """
    def __init__(self):
        pass
    def get_all_info(self):
        """
        Выдает информацию серверов
        """
        try:
            response = requests.get('http://u2.crazymusic.uz/botfor/')
            soup = BeautifulSoup(response.text, 'html.parser')

            public = soup.find('div', class_='public')
            public_two = soup.find('div', class_='public2')
            brush = soup.find('div', class_='brush')
            all_online = soup.find('div', class_='allOnline')

            public_data = {
                'name': public.find('p', class_='name').get_text(strip=True),
                'map': public.find('p', class_='map').get_text(strip=True),
                'online': public.find('p', class_='online').get_text(strip=True),
                'ip': public.find('p', class_='ip').get_text(strip=True)
            }

            public_two_data = {
                'name': public_two.find('p', class_='name').get_text(strip=True),
                'map': public_two.find('p', class_='map').get_text(strip=True),
                'online': public_two.find('p', class_='online').get_text(strip=True),
                'ip': public_two.find('p', class_='ip').get_text(strip=True)
            }

            brush_data = {
                'name': brush.find('p', class_='name').get_text(strip=True),
                'map': brush.find('p', class_='map').get_text(strip=True),
                'online': brush.find('p', class_='online').get_text(strip=True),
                'ip': brush.find('p', class_='ip').get_text(strip=True)
            }
            
            all_data = {
                'error': 0,
                'errorMessage': '',
                'data': {
                    'all_online': all_online.find('p').get_text(strip=True),
                    'public': public_data,
                    'public_two': public_two_data,
                    'brush': brush_data
                }
            }
            return all_data
        except Exception as e:
            return {
                'error': 1,
                'errorMessage': 'Check the code bro :)',
                'data': ''
            }

    def get_players(self, server):
        """
        Выдает игроков
        """
        def sorted_players(data, name):
            try:
                lens = '-------------------------------------'
                answer = f'<b>{name}</b>\n{lens}\n<b>[Счет]</b> [Ник] <b>[Время](Ч:М:С)</b>\n{lens}\n'
                for player in data:
                    answer += f"<b>[{player['score']}]</b> {player['name'].replace('<', '').replace('>', '')} <b>[{player['time']}]</b>\n"
                return answer
            except Exception:
                return f'<b>{name}</b>\n{lens}\n<b>[Счет]</b> [Ник] <b>[Время](Ч:М:С)</b>\n{lens}\nИгроков нет'
        public = []
        public_two = []
        bhop = []
        response = requests.get('http://u2.crazymusic.uz/botfor')
        soup = BeautifulSoup(response.content, 'html.parser')
        public_items = soup.find('div', class_='public_players').find_all('tr')
        public_two_items = soup.find('div', class_='public2_players').find_all('tr')
        bhop_items = soup.find('div', class_='brush_players').find_all('tr')
        if server == 'public':
            try:
                for item in public_items:
                    public.append({
                        'name': item.find('td', class_='Name').get_text(strip=True),
                        'score': item.find('td', class_='Frags').get_text(strip=True),
                        'time': item.find('td', class_='TimeF').get_text(strip=True)
                    })
                return sorted_players(public, '📌FSDK | Public [TAS-IX] [1000 fps]')
            except Exception:
                return sorted_players(public, '📌FSDK | Public [TAS-IX] [1000 fps]')
        
        elif server == 'public_two':
            try:
                for item in public_two_items:
                    public_two.append({
                        'name': item.find('td', class_='Name').get_text(strip=True),
                        'score': item.find('td', class_='Frags').get_text(strip=True),
                        'time': item.find('td', class_='TimeF').get_text(strip=True)
                    })
                return sorted_players(public_two, '📌FSDK | Public#2 [TAS-IX] [1000 fps]')
            except Exception:
                return sorted_players(public_two, '📌FSDK | Public#2 [TAS-IX] [1000 fps]')

        elif server == 'bhop':
            try:
                for item in bhop_items:
                    bhop.append({
                        'name': item.find('td', class_='Name').get_text(strip=True),
                        'score': item.find('td', class_='Frags').get_text(strip=True),
                        'time': item.find('td', class_='TimeF').get_text(strip=True)
                    })
                return sorted_players(bhop, '📌FSDK | Bhop [TAS-IX] [1000 fps]')
            except Exception:
                return sorted_players(bhop, '📌FSDK | Bhop [TAS-IX] [1000 fps]')




api = InfoApi()
print(api.get_players(server='public_two'))