import requests
import json

accuweatherAPIKey = 'XCzlTx8FytDGRdpmnYiIGAdLzaBV8qHU'

def pegarCoordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200):
        print('Não foi possível obter a localização')
    else:
        localizacao = json.loads(r.text)
        coordenadas = {}
        coordenadas['lat'] = localizacao['geoplugin_latitude']
        coordenadas['long'] = localizacao['geoplugin_longitude']
        return coordenadas

def pegarCodigoLocal(lat, long):
    locationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition' \
                     + '/search?apikey=' + accuweatherAPIKey \
                     + '&q=' + lat + '%2C' + long + '&language=pt-br'

    r = requests.get(locationAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter o código do local')
    else:
        locationResponse = json.loads(r.text)
        infoLocal = {}
        infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + ', '\
                    + locationResponse['AdministrativeArea']['LocalizedName'] + '. '\
                    + locationResponse['Country']['LocalizedName']
        infoLocal['codigoLocal'] = locationResponse['Key']
        return infoLocal

def pegarTempoAgora(codigoLocal, nomeLocal):
    currentConditionsAPIUrl = 'http://dataservice.accuweather.com/currentconditions/v1/' \
                              + codigoLocal + '?apikey=' + accuweatherAPIKey + '&language=pt-br'

    r = requests.get(currentConditionsAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter o clima do local')
    else:
        currentConditionsAPIUrl = json.loads(r.text)
        infoClima = {}
        infoClima['textoClima'] = currentConditionsAPIUrl[0]['WeatherText']
        infoClima['temperatura'] = currentConditionsAPIUrl[0]['Temperature']['Metric']['Value']
        infoClima['nomeLocal'] = nomeLocal
    return infoClima

## Inicio do programa

coordenadas = pegarCoordenadas()

local = pegarCodigoLocal(coordenadas['lat'], coordenadas['long'])

climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])

print('Clima atual em: ' + climaAtual['nomeLocal'])
print(climaAtual['textoClima'])
print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')
