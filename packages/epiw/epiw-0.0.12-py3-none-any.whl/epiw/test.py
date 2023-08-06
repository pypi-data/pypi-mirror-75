import epiw

from epiw.grid import grid
'''
desc = epiw.hourly_weather_desc()

print(desc)

desc = epiw.daily_weather_desc()

print(desc)

values = epiw.hourly_weather('20200101', '20200101')

print(values)

values = epiw.read('weather', 'daily', '19810101', '20200101', lonlat='127,37')

print(values)

values = epiw.read_as_gpd('weather', 'daily', '19810101', '20200101', lonlat='127,37')
print(values)
'''

kma_data = epiw.read_as_gpd('weather', 'daily', '20200101', '20200101')
kma_data = kma_data.set_crs(4326).to_crs(5179)
kma_data.drop(['tm'], axis=1).to_file('output.json', driver='GeoJSON')
grid('output.json', 'output.tiff', 'tn', resolution=10000)
