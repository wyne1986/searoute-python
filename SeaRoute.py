import dijkstra
import json
from geopy.distance import geodesic
from geopy.point import Point

class SeaRoute(object):

    #初始化读取geojson文件并解析为节点和dijkstra集
    def __init__(self,route_file='geojson.json'):
        try:
            self.__f = open(route_file,encoding='utf-8')
            self.__content = self.__f.read()
            self.__f.close()
            self.__features = json.loads(self.__content)['features']
        except Exception as e:
            raise e
        self.__graph = dijkstra.Graph()
        self.__nodes = {}
        self.graph = dijkstra.Graph()
        for f in range(len(self.__features)):
            list(map(lambda x,y:self.__add_nodes(x,y),
                     list(self.__features[f]['geometry']['coordinates']),
                     list(self.__features[f]['geometry']['coordinates'])[1:]))


    #将geojson单个航线段解析为节点和dijkstra集
    def __add_nodes(self,p1,p2):
        if ('%s_%s' % (p1[1], p1[0])) not in self.__nodes or ('%s_%s' % (p2[1], p2[0])) not in self.__nodes:
            self.graph.add_edge('%s_%s' % (p1[1], p1[0]),'%s_%s' % (p2[1], p2[0]),self.__tran_to_int(geodesic(Point(latitude=p1[1], longitude=p1[0]),Point(latitude=p2[1],longitude=p2[0])).km))
            self.graph.add_edge('%s_%s' % (p2[1], p2[0]),'%s_%s' % (p1[1], p1[0]),self.__tran_to_int(geodesic(Point(latitude=p1[1], longitude=p1[0]),Point(latitude=p2[1],longitude=p2[0])).km))
        self.__nodes['%s_%s' % (p1[1], p1[0])] = [p1[1], p1[0]]


    #在节点集里查找距离传入值最近的节点
    def __nearest_node(self,point):
        return min(map(lambda x: x, self.__nodes), key = lambda k:geodesic(Point(latitude=self.__nodes[k][0], longitude=self.__nodes[k][1]), point).km)


    #寻路调用方法,传入start经纬度和end经纬度,返回航线路径经纬度list和总距离km
    def find(self,start,end):
        routes = list(map(lambda x:self.__nodes[x],dijkstra.DijkstraSPF(self.graph,self.__nearest_node(start)).get_path(self.__nearest_node(end))))
        distkm = sum(list(map(lambda x,y:geodesic(Point(latitude=x[0],longitude=x[1]),Point(latitude=y[0],longitude=y[1])).km,routes,routes.copy()[1:])))
        return routes,format(distkm,'.2f')


    #dijkstra集的距离值需要将带小数的千米距离转换为整数米来使用
    @staticmethod
    def __tran_to_int(numb):
        return int(numb*1000)


# power by wyne1986

