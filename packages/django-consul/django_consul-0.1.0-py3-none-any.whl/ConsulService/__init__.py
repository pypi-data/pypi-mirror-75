from .settings import *

consul = consulate.Consul(host=AGENT_ADDRESS, port=AGENT_PORT)

consul.agent.service.register(
    SERVICE_NAME,
    address=SERVICE_ADDRESS,
    port=SERVICE_PORT,
    interval=CHECK_INTERVAL,
    httpcheck=CHECK_URL
)
