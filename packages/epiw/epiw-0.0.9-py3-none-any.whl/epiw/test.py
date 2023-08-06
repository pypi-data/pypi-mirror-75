import epiw

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