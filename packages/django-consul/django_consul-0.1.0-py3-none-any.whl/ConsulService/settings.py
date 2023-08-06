from django.conf import settings
import consulate


def get(key, default):
    return getattr(settings, key, default)


AGENT_ADDRESS = get('CONSUL_AGENT_ADDRESS', consulate.DEFAULT_HOST)
AGENT_PORT = get('CONSUL_AGENT_PORT', consulate.DEFAULT_PORT)
CHECK_URL = get('CONSUL_CHECK_URL', 'http://127.0.0.1:8000/healthy')
CHECK_INTERVAL = get('CONSUL_CHECK_INTERVAL', '10s')

SERVICE_NAME = get('CONSUL_SERVICE_NAME', 'unknown-service')
SERVICE_ADDRESS = get('CONSUL_SERVICE_ADDRESS', '127.0.0.1')
SERVICE_PORT = get('CONSUL_SERVICE_PORT', 8000)



