from yo_api import YO_API
from xml.dom.minidom import parseString
yoapi = YO_API("90005702859","MsUl-Ei4O-BmJo-apHP-npHY-wsYT-c8nc-skny")

#yoapi_response = yoapi.getMSISDNInfo("256703632468")
yoapi_response = yoapi.sendAirtime("256703632468","500")
print(yoapi_response)