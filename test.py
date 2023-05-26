from SeaRoute import SeaRoute

sr = SeaRoute()

routes,dist = sr.find((31.3,122.9),(21.9,114.3))

print(routes)
print(dist)