

class SingeTargetDijkstraVistor(gt.DijkstraVisitor):

    def __init__(self, target):

        self.target = target

    def edge_relaxed(self, e: gt.Edge):

        if e.target() == self.target:
            raise gt.StopSearch()
        
class SingeTargetAStarVisitor(gt.AStarVisitor):

    def __init__(self, target):

        self.target = target

    def edge_relaxed(self, e: gt.Edge):

        if e.target() == self.target:
            raise gt.StopSearch()
        
def shortest_route_from_pred_tree(graph: gt.Graph, pred_tree: gt.VertexPropertyMap, source: gt.Vertex, target: gt.Vertex):

    node_deq = deque()

    curr_node = target
    while curr_node != source:

        p = graph.vertex(pred_tree[curr_node])

        for edge in curr_node.out_edges():

            if edge.target() == p:

                node_deq.appendleft(pred_tree[curr_node])

        curr_node = p


    return node_deq


def compute_shortest_route(graph: gt.Graph, weights: gt.EdgePropertyMap, source_idx: int , target_idx: int, methods) -> dict:

    routes = {}
    exec_times = {}

    source = graph.vertex(source_idx)
    target = graph.vertex(target_idx)

    if 'dijkstra' in methods:

        start_time = time.time()
        _, pred_tree = gt.dijkstra_search(g = graph, weight = weights, source = source,\
                                         visitor = SingeTargetDijkstraVistor(source))
        
        routes['dijkstra'] = shortest_route_from_pred_tree(graph = graph, pred_tree=pred_tree, source = source, target= target)
        print(routes['dijkstra'])
        exec_times['dijkstra'] = time.time() - start_time

    if 'a_star' in methods:

        start_time = time.time()
        routes['a_star'] = nx.astar_path(graph, source, target, heuristic= a_star_heuristic)
        exec_times['a_star'] = time.time() - start_time

    return routes, exec_times


def create_graph(terrain: Landscape, cost_function: Callable, args: dict, file: str):

    #shifts = [(-1,0),(1,0),(0,-1),(0,1)]
    print('Could not find pickled graph file with specified parameters, creating one instead...')

    pixel_size = args['ENVIRONMENT']['PIXEL_SIZE']
    connection_degree_to_distance = {1: pixel_size+1e-5,
                                     2: np.sqrt(2)*pixel_size+1e-5, 
                                     3: np.sqrt(5)*pixel_size+1e-5}

    # First populate graph.
    graph, vertices = gt.geometric_graph(np.stack([terrain.x_coords.flatten(),terrain.y_coords.flatten()], axis=1),\
         radius = connection_degree_to_distance[args['GRAPH_CONSTRUCTION']['CONNECTION_DEGREE']])
    
    weights = graph.new_edge_property("double")

    filename = f"{file}_{cost_function.__name__}_{args['GRAPH_CONSTRUCTION']}"
    pickle.dump((graph,vertices,weights), open(os.getcwd()+f'/graphs/gaussian/{filename}.pickle','wb'))

    weights.a = np.ones(shape=(graph.edge_index_range))

    print('finished creating graph.')

    return graph, vertices, weights