import networkx as nx


def create_hospital_graph():

    graph = nx.Graph()

    # ==========================================
    # GROUND FLOOR
    # ==========================================

    graph.add_edge(
        "Main Entrance",
        "Reception",
        weight=1
    )

    graph.add_edge(
        "Reception",
        "Pharmacy",
        weight=2
    )

    graph.add_edge(
        "Reception",
        "Emergency",
        weight=2
    )

    graph.add_edge(
        "Reception",
        "Lift",
        weight=2
    )

    # Dedicated emergency entrance
    graph.add_edge(
        "Emergency Entrance",
        "Emergency",
        weight=1
    )

    # ==========================================
    # FIRST FLOOR
    # ==========================================

    graph.add_edge(
        "Lift",
        "First Floor",
        weight=1
    )

    graph.add_edge(
        "First Floor",
        "Orthopedics",
        weight=2
    )

    graph.add_edge(
        "First Floor",
        "Laboratory",
        weight=2
    )

    # ==========================================
    # SECOND FLOOR
    # ==========================================

    graph.add_edge(
        "Lift",
        "Second Floor",
        weight=1
    )

    graph.add_edge(
        "Second Floor",
        "Cardiology",
        weight=2
    )

    graph.add_edge(
        "Second Floor",
        "Neurology",
        weight=2
    )

    return graph


def find_route(source, destination):

    graph = create_hospital_graph()

    path = nx.shortest_path(
        graph,
        source=source,
        target=destination,
        weight="weight"
    )

    return path