# searoute-python

### geojson route finder

* example with searoute-js

* use geojson and dijkstra

* geojson dataset use LineString

* you can make your geojson.json with geojson tools website, example geojson.tools

* Example Code:
```
from SeaRoute import SeaRoute
sr = SeaRoute('geojson.json')
routes,dist = sr.find((31.3,122.9),(21.7,114.1))

print(routes)
print('%s km' % dist)
```
