import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from pyinfoblox import InfobloxWAPI

infoblox = InfobloxWAPI(
    username='jdesgarennes.admin',
    password='Man bear pig lives!!!',
    wapi='https://10.0.20.13/wapi/v1.1/'
)


network_function = infoblox.network.function(
    objref='network/ZG5zLm5ldHdvcmskMTAuMTAuMC4wLzE2LzA:10.10.0.0/16/default',
    _function='next_available_ip',
    num=1
)

print(network_function)
