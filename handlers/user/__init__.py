from .commands import router as router_commands
from .actions_with_weather import router as router_actions_with_weather
from .user_requests_history import router as router_user_requests_history

user_routers = [router_commands,
                router_actions_with_weather,
                router_user_requests_history]
