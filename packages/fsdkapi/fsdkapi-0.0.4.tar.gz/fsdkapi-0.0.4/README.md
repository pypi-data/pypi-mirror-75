# <p align="center">FSDK API

## Getting started.
```
$ pip install fsdkapi
```

## User API example
```python
from fsdk import UserApi

api = UserApi()

api.get_stats() # Get server players stats
api.search_stats() # Search player stats

api.get_bans() # Get server players bans
api.search_bans() # Search banned player
```

## Info API example
```python
from fsdk import InfoApi

api = InfoApi()

api.get_all_info() # Get all server info
api.get_players() # Get server players
```

## Admin API example
```python
from fsdk import AdminApi

api = AdminApi(token='secret')

api.get_info() # Get server info
api.get_console_info() # Get server console info
api.get_players() # Get server players
api.get_admins() # Get admins and vips

api.vote_map(name='de_dust2') # Vode for change map
api.change_map(name='de_dust2') # Direct change map
api.kick_player(user_id='228') # Kick player
api.send_rcon(rcon='amx_reloadadmins') # Send rcon command

# Add admin and vip
api.add_admin(auth='Layer', access='a', flags='ce', expires='', password='88005553555', note='Layer test API')
```