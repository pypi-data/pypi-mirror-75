from spell.serving import server
from spell.serving import settings


app = server.make_app(server.make_api_from_env(), debug=settings.DEBUG)
