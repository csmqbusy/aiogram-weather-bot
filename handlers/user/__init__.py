from .commands import router as router_commands
from .user_requests_history import router as router_user_requests_history

user_routers = [router_commands,
                router_user_requests_history]
