"""
SARVIIN A/L HARI
32885741
"""

# ==========
# Shortest Path Finding Algorithm with Dijkstra's Algorithm

class TreeMap:

    def __init__(self, roads, solulus):
        """
        This is an __init__ method where I will initialize a new list, self.vertices with the length of the vertex list
        followed by substituting the index of 0 to N-1 with a new instance of Vertex for each index. Next i will set the
        is_final_vertex variable of the final vertex in the list to True indicating it is the last vertex at which the
        exits will end. Next, I initalize variables, start_mode (indicating forward edges)

        The approach I am planning to use for this assignment is the negative edges approach, where I will run dijkstra
        twice to find the shortest time from the source tree to all the other trees. The first dijkstra runs from the
        start tree (forward roads as in input) and second dijkstra runs from all exits (reversed roads, where the "from"
        and "to" vertices are switched to "to" and "from" vertices respectively). Since dijkstra works by a
        single source, and given we can have multiple exits, I created a new vertex to connect all exits to one final
        tree with a weight of "0" (edges added in escape()), which is the reason why I have one additional final tree
        when initializing the Graph instance. In addition to that I have 2 lists to manage, the forward edges (for first
        dijkstra) and reverse_edges (for second dijkstra) in the Vertex class (denoting the Trees) to store the list of
        outgoing edges for each vertex "from" and "to" for both forward and reverse edges cases. I have done this to
        avoid creating 2 graphs which will increase the Auxiliary space complexity, thus, by creating one additional
        list for reverse_edges of O(|R|) complexity I can find the shortest time from start and from exit to all trees
        within the same graph instance.
        Written by Sarviin Hari (32885741)

        Precondition:
            - the roads and solulus are not empty
            - each tuple in the roads (u, v, w) will have a valid tree id for u and v within the range of |T| where the
            id's start from 0 to |T|-1, where T denotes the number of trees in the forest and the weight w where all of
            u, v, and w are a non-negative integer
            - each tuple in the solulus (x, y, z) will have a valid tree id for x and z, within the range of 0 to |T|-1
            where each Tree, T will only have 1 possible solulu and y is the time needed to break a tree before
            teleportation where all x, y, and z are a non-negative integer
            - the list of tuples for roads and solulus are not sorte din any order
        Postcondition:
            - the TreeMap will have a graph object, self.g, which has a length of |T| + 1, where T is the total number
            of trees in the forest and it also have an additional Tree (T+1) created as the final tree
            - each Vertex instantiated in the graph will have a list of edges (denoting the trees that the graph can
            travel to through the roads) and a list of reverse_edges (denoting the opposite direction of the roads that
            the trees can travel from)
            - the id's for each and every trees will be unique in the graph

        Input
            roads: A list of tuples (u, v, w), where u, v, and w are integers, where u denotes the start Tree id,
                v denotes the end Tree and w denotes the time taken for the travel from Tree u to Tree v along the road
            solulus: A list of tuples (x, y, z), where x, y, and z are integers, where x denotes the Solulu Tree id,
                z denotes the Tree teleported to by the x Solulu Tree when destroyed and y denotes the time taken to
                break the x Solulu Tree
        Return:
            None

        Time complexity:
            Best case analysis: The best case complexity is similar to the worse case complexity where it is set to be
                O(|T|+|R|), where T denotes the set of Trees in the forest and R denotes the set of roads in the forest
            Worst case analysis: To analyze the worst case complexity, let us look at each operation complexity.
                - First we have to loop through all the roads in the forest to get the number of trees in the graph.
                This has a complexity of O(|R|), where R is the set of roads in the forest
                - Second we have to instantiate the Graph. The Graph initialization has a worse case complexity of
                O(|T|), where T is the set of unique trees in the roads
                - Third we have to loop through all the roads in the forest to add forward edges and reverse edges for
                the "from" vertex in the roads of the forest. Since the add_edges and add_reverse_edges methods only
                involves appending an Edge instance to the edges list which takes constant time of O(1), this loop has a
                complexity of O(|R|), where R is the set of roads in the forest
                - Thus, the total complexity is O(|T|+|R|+|R|) = O(|T|+2|R|) = O(|T|+|R|), where T denotes the set of
                Trees in the forest and R denotes the set of roads in the forest

        Space complexity:
            Input space analysis: O(|T|+|R|), where T denotes the set of Trees in the forest and R denotes the set of
                roads in the forest
            Aux space analysis:
                - O(|T|), where T is the set of Trees in the forest is required as the additional memory for temporary
                elements required to instantiate a list, self.vertices in the graph to store new instance of Vertices
                - O(2|R|), where R is the set of Roads in the forest is required as the additional memory for temporary
                elements to store the edges and reverse edges instances in their respective lists in each Vertex (trees)
                - Thus, the total complexity is O(|T|+2|R|) = O(|T|+|R|), where T denotes the set of Trees in the forest
                and R denotes the set of roads in the forest
        """
        # instantiate roads and solulus into variables
        self.roads = roads
        self.solulus = solulus

        self.max_tree = 0

        # To get the num of trees, by finding the max between the current tree id, left edge's tree id and right edge's
        # tree id
        for road_tuple in roads:
            self.max_tree = max(self.max_tree, road_tuple[0], road_tuple[1])

        # Number of Trees from 0 to K + 1 (for all trees) + 1 (for last vertex)
        self.max_tree += 1
        self.max_tree += 1

        # Number of new vertices
        self.total_vertices = self.max_tree

        # create graph instance which contains teh vertex
        self.g = Graph(self.total_vertices)

        # In this loop we will add forward and reverse edges to each of the Trees in their respective lists in the
        # Vertex class
        for i in range(len(roads)):
            self.g.graph_add_edges(roads[i][0], roads[i][1], roads[i][2])
            self.g.graph_add_reverse_edges(roads[i][1], roads[i][0], roads[i][2])




    def escape(self, start, exits):
        """
        This is the escape method of the TreeMap where we will find the shortest time between the start tree and one of
        the exits.
        First I will call the complete_reset method from the graph class to reset the mode to start_mode and
        also resetting the vertices values to their default as well as resetting the reverse_edges list for the
        final_tree to an empty list.
        Next I will call the dijkstra method from the Graph class to run a dijkstra from the start tree to all of the
        trees in the forest (from the Graph instance) to find the shortest time taken from start tree to all the
        remaining trees. The complete working principle of dijkstra is included in the dijkstra function in the Graph
        class. As a summary, dijkstra works with a min heap which stores a tuple of time taken and vertex instance in a
        sorted order from smallest to largest. In the dijkstra we will loop through each of the tree instances and find
        the shortest time from the source to each tree and if the previous time from one vertex is higher than the
        other we will update the new smaller time.
        Next I will call another reset method to reset the time, visited, discovered and pointer as well as setting the
        start_Mode to false to reset the tree instances for a second round of dijkstra. Since the start mode is set to
        false, the second round of Dijkstra's algorithm will use the reverse_edges list instead of the edges list to
        perform the Dijkstra operation.
        In this round, the starting vertex will be the single final tree (final vertex which is the last vertex in the
        list of vertices), which was connected to the exit trees with an edge of weight zero. At the end of the two
        rounds of dijkstra, I will loop through all the Solulu trees where for each of the Solulu trees I will check if
        the start solulu is either a start tree or it has a past and also check if the end tree (the tree teleported to
        when a solulu tree is broken) is either an end tree or have a reverse past. This is to ensure that the there is
        a path from the start to the start Solulu and there is also a path from the tree teleported to to the exit.
        If yes then I will calculate the total time taken from start to exit through the Solulu tree by breaking it and
        compare it with the previous smallest time. If it is smaller I will reset the smallest_solulu and smallest_time
        with the new time taken value and the respective solulu tuple. Next, I will check if the smallest_path is None.
        If it is None, it means that there is no existing smallest time from the start tree to one of the exits, so I
        will return None.
        If the smallest_path is not None, it indicates that there is a smallest time from the start to one of the exits.
        So, I perform a backtracking from the start tree to the start Solulu by looping through all the previous trees
        from selected start Solulu to the start until there is no past trees, store the tree id's in a list, and reverse
        the list. In addition to that, I will perform another backtracking from the tree teleported to, to the exit.
        Similar to the previous backtracking step, I will find all the vertices from the tree teleported to, to the exit
        and store all the tree id's in the list.
        Written by Sarviin Hari (32885741)

        Precondition:
            - the TreeMap already have a graph object, self.g, which has a length of |T| + 1, where T is the total number
            of trees in the forest and it also have an additional Tree (T+1) created as the final tree
            - each Vertex instantiated in the graph will have a list of edges (denoting the trees that the graph can
            travel to through the roads) and a list of reverse_edges (denoting the opposite direction of the roads that the trees can travel from)
            - the id's for each and every trees will be unique in the graph
        Postcondition
            - the time instance in the vertex contains the time taken from end tree to all trees at the end of dijkstra,
            while start_time instance contains the time taken from start tree to all other trees
            - the number of trees and the number of roads remains the same after the operation

        Input
            start: An integer denoting the start Tree id
            exits: A list consisting of Integers that denotes the exit Tree id's

        Return:
            (smallest_time, time_v_list): A tuple consisting of the smallest time taken to from the start to one of the
                exits and a list of tree id's that denotes the path taken from the start tree to exit tree

        Time complexity:
            Best case analysis: The best case complexity is similar to the worse case complexity where it is
                O(|R| log |T|), where T denotes the set of Trees in the forest and R denotes the set of roads in the
                forest
            Worst case analysis: To analyze the worst case complexity, let us look at each operation complexity.
                - First we have the complete_reset method that loops through every trees in the graph and reset their
                values to default. This has a time complexity of O(|T|), where T denotes the set of Trees in the forest.
                - Next I will run the dijkstra method to find the shortest time from the start tree to all the other
                remaining trees which at its worst case has a time complexity of O(|R| log |T|), where T denotes the set
                of Trees in the forest and R denotes the set of roads in the forest.
                - Next I will again call the reset method that loops through each and every trees in the graph to reset
                its pointers, visited , discovered and time values to default False or 0. This has a time complexity of
                O(|T|), where T denotes the set of Trees in the forest.
                - Next I will run the dijkstra method again for the reversed_edges to find the shortest time from
                the end tree (connected to teh exits with an edge weight of 0) to all the other remaining trees which at
                its worst case has a time complexity of O(|R| log |T|), where T denotes the set of Trees in the forest
                and R denotes the set of roads in the forest.
                - Next I will loop through the list of all Solulu trees to find the set of path from start to end tree
                through each of the Solulu trees with the smallest time. This has a time complexity of O(|T|), where
                T denotes the set of Trees in the forest as the remaining operations are integer or None comparison and
                restoring values which has a constant time complexity.
                - Next I will do a backtracking for the start tree to the start Solulu and store it in a list as well as
                reversing the list since the order is in reverse. This has a time complexity of O(2|T|) = O(|T|), where
                T denotes the set of Trees in the forest.
                - Next I will also do a backtracking for the tree teleported "to" from the Start solulu to the exit and
                store it in a list. This has a time complexity of O(|T|), where T denotes the set of Trees in the forest
                -  Thus, the total complexity is O(|T|+|R| log |T|+|T|+|R| log |T|+|T|+|T|+|T|)
                = O(5|T|+2*(|R| log |T|)) = O(|T|+|R| log |T|) = O(|R| log |T|), where T denotes the set of Trees in the
                forest and R denotes the set of roads in the forest

        Space complexity:
            Input space analysis: O(|T|), where T is the set of Trees as we will be using the
                self.vertices in the graph to access the Tree Vertices and their respective methods / attributes
                (dijkstra)
            Aux space analysis: O(2|T|), where T is the set of Trees, as there is additional memory required to create
                2 lists to store the tree id's for backtracking and reversing the tree id's for the start to Start
                Solulu, and we will append the remaining trees obtained from backtracking from tree teleported "to"
                until the end tree. Thus the final complexity is O(2|T|) =  O(|T|), where T is the set of Trees
        """
        # resets the states of the graph completely including starts and exits
        self.g.complete_reset()

        # Call dijkstra from start to all vertex
        vertex_list = self.g.dijkstra(self.g.vertices[start])

        # loop through all vertices and reset state
        self.g.reset()

        # set the exits and add a new edge from the exit vertex to the end new final vertex
        for exit in exits:
            (self.g.setExit(exit))

        # Call dijkstra from end vertex to all vertex
        v_list2 = self.g.dijkstra(self.g.vertices[-1])

        smallest_solulu = None
        smallest_time = math.inf
        # For each of the solulu, we will check if the start solulu is either a start Tree or have a past and check
        # if the end solulu is either a end tree and have a reverse_past
        # if no, this means that there is no path from the start to Solulu or Teleport to exit
        for i in self.solulus:
            if (v_list2[i[0]].id == start or v_list2[i[0]].past != None) and (v_list2[i[2]].is_end_tree or v_list2[i[2]].reverse_past != None):
                if (v_list2[i[0]].start_time + v_list2[i[2]].time + i[1]) < smallest_time:
                    smallest_solulu = i
                    smallest_time = (v_list2[i[0]].start_time + v_list2[i[2]].time + i[1])


        # No smallest time
        if smallest_solulu is None:
            return None
        # backtracking
        else:
            past1 = v_list2[smallest_solulu[0]]
            past2 = v_list2[smallest_solulu[2]]

            # loop through each of the past of the start Solulu to find the previous trees till the start
            lst = []
            curr = past1
            while curr != None:
                lst.append(curr.id)
                curr = curr.past
            time_v_list = []
            for i in range(len(lst)-1, -1, -1):
                time_v_list.append(lst[i])

            # loop through each of the past of the end Solulu to find the previous trees till the end
            while not past2.is_final_vertex:
                if time_v_list[-1] != past2.id:
                    time_v_list.append(past2.id)
                past2 = past2.reverse_past

            return (smallest_time, time_v_list)

class Graph:
    def __init__(self, max_vertex: int):
        """
        This is an __init__ method where I will initialize a new list, self.vertices with the length of the vertex list
        followed by substituting the index of 0 to N-1 with a new instance of Vertex for each index. Next i will set the
        is_final_vertex variable of the final vertex in the list to True indicating it is the last vertex at which the
        exits will end. Next, I initalize 2 variables, start_mode (indicating forward edges)
        Written by Sarviin Hari (32885741)

        Precondition:
            - The max_vertex denotes the maximum number of vertices in the graph
            - The graph must be a simple graph
            - All Vertices will have at least one edge
        Postcondition:
            - A Graph instance is intitialized with the maximum number of vertices
            - The last vertex in the vertex list is the final vertex that will connect all the exits with a weight of 0
            - Initial mode of start is set to false

        Input
            max_vertex: An integer denoting the maximum number of vertex
        Return:
            None

        Time complexity:
            Best case analysis: O(V), where V is the maximum number of vertices
            Worst case analysis: O(V), where V is the maximum number of vertices

        Space complexity:
            Input space analysis: O(1), where the input consists of an integer denoting the maximum number of Vertex
            Aux space analysis: O(V), as the additional memory for temporary elements required is to instantiate a new
                list, self.vertices to store new instance of Vertices
        """

        # intialize a list of for the vertices with the length in parameter
        self.vertices = [None] * max_vertex

        # intialize a vertex instance for each index
        for i in range(max_vertex):
            self.vertices[i] = Vertex(i)

        # set the final vertex as the final vertex
        self.vertices[-1].is_final_vertex = True

        # set the modes to false
        self.start_Mode = False

    def reset(self):
        """
        This is a method to reset the state of the instances of time, visited, discovered, pointer in each and every
        vertex to their default values. This is done to ensure that there is no complications in computation when I run
        the second dijkstra operation on the reversed edges due to the previous state of these variables once the
        first dijkstra is done.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The start_mode is True indicating the edges will be used for dijkstra computation
            - the variables in vertices stores the instances and values of the first dijkstra for forward edges
        Postcondition:
            - The start_mode is set to False indicating the reverse edges will be used for dijkstra computation
            - the variables in vertices is reset to default values to prevent overlapping of outputs from first dijkstra
            iteration

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: O(V), where V is the maximum number of vertices (length of self.vertices)
            Worst case analysis: O(V), where V is the maximum number of vertices (length of self.vertices)

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be looping through
                each of these vertices to reset their state to their original values
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """
        # set the start mode to false and reset certain vertices instances
        self.start_Mode = False

        for i in self.vertices:
            i.time = 0
            i.visited = False
            i.discovered = False
            i.pointer = None

    def complete_reset(self):
        """
        This method is called for every start iteration of escape function to reset the states to default states so that
        the previous computations does not affect the current computation
        This is a method to reset the state of the instances of time, visited, discovered, pointer, past,
        reversed_past, is_end_tree in each and every vertex to their default values. This is done to ensure that there
        is no complications in computation when I repeatedly run the escape function from the TreeMap the previous
        output does not affect the current output as they will have different starts and exits and their past and
        reversed_past will vary based on their new start and new ends. I will also set the reversed_edges for the last
        vertex (a vertex connecting to all the exit trees) due to the new exits for a new iteration of escape
        Written by Sarviin Hari (32885741)

        Precondition:
            - The start_mode is False indicating the reverse edges will be used for dijkstra computation
            - The list of reversed_edges contains the list of edges from exit to final vertex from the previous
            iteration of escape function
            - the variables in vertices stores the previous instances of escape function
        Postcondition:
            - The start_mode is set to True indicating the forward edges will be used for dijkstra computation
            - The list of reversed_edges is set to an empty list as a new set of exits will be present for new iteration
            - the variables in vertices is reset to default values to prevent overlapping of outputs from one iteration
            of escape to the other

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: O(V), where V is the maximum number of vertices (length of self.vertices)
            Worst case analysis: O(V), where V is the maximum number of vertices (length of self.vertices)

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be looping through
                each of these vertices to reset their state to their original values
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """
        # set the start mode to false and reset certain vertices instances
        self.start_Mode = True

        for i in self.vertices:
            i.time = 0
            i.start_time = 0
            i.visited = False
            i.discovered = False
            i.pointer = None
            i.past = None
            i.reverse_past = None
            i.is_end_tree = False

        self.vertices[-1].reverse_edges = []

    def setExit(self, ind):
        """
        This is a method that is called for each and every exit of the escape function in TreeMap, where we will set
        the variable is_end_tree for the exit trees to be true, and we will also add the reversed edges to the last
        Vertex (which is the last Tree that connects multiple end trees to one common vertex (the final vertex)). This
        is done mainly for the reversed dijkstra where we will set the last Vertex connecting to multiple exits with
        a weight of 0, and we will run the dijkstra with the last vertex as the start. Since the last vertex is the
        start and there are edges from the last vertex to the exits, this ensures that the dijkstra covers all possible
        exits.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The end_tree for all vertices is false
            - The list of reversed_edges for the final vertex is empty
        Postcondition:
            - The end_tree for all exits is set to True
            - The list of reversed_edges will append the Edges instance from the final vertex to the exit with a weight
            of "0"

        Input
            ind: An integer that denotes the index of the Exit
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving the accessing of attributes and setting
                the boolean value to True and also appending an Edge instance to the reverse_edges attribute in the
                list which both takes constant time complexity
            Worst case analysis: O(1), where the computations are only involving the accessing of attributes and setting
                the boolean value to True and also appending an Edge instance to the reverse_edges attribute in the
                list which both takes constant time complexity

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be using the
                self.vertices to access the Vertices and their respective methods / attributes
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """
        # set end_tree (exit) to True and add an edge from final vertex to exits with weight 0
        self.vertices[ind].is_end_tree = True
        self.vertices[-1].add_reverse_edges(self.vertices[ind], 0)

    # def __str__(self):
    #     return_string = ""
    #     for vertex in self.vertices:
    #         return_string += "Vertex: " + str(vertex) + " " + "\n"
    #     return return_string

    def graph_add_edges(self, fro, to, weight):
        """
        This is a method that is called for the given fro vertex and to vertex, where we will add an edge with the given
        weight to these vertices. This is done by calling the add_edges function from the instance of the fro Vertex and
        add a new instance of edge with u = fro Vertex, v = to Vertex and w = weight into the list of edges of the fro
        Vertex.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The forward edge from the "from" vertex to "to" vertex is not in the list of edges of "from" vertex
        Postcondition:
            - The forward edge from the "from" vertex to "to" vertex is appended in the list of edges of "from" vertex

        Input
            fro: An integer that denotes the index of the Vertex of the start edge
            to: An integer that denotes the index of the Vertex of the end edge
            weight: An integer that denotes the weight of the edge
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving the accessing of attributes and
                appending an Edge instance to the edges list which takes constant time
                complexity
            Worst case analysis: O(1), where the computations are only involving the accessing of attributes and
                appending an Edge instance to the edges list which takes constant time
                complexity

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be using the
                self.vertices to access the Vertices and their respective methods / attributes
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """
        self.vertices[fro].add_edges(self.vertices[to], weight)

    def graph_add_reverse_edges(self, fro, to, weight):
        """
        This is a method that is called for the given fro vertex and to vertex, where we will add an edge with the given
        weight to these vertices. But in comparison to previous method, the index values of fro and to received by this
        function is reversed, where for the previous, if we call graph_add_edges(1, 2, 5), for this method we would call
        graph_add_reverse_edges(2, 1, 5), indicating we are adding both forward edges into a edges list (with the
        previous method) and reversed edges into the reversed_edges list (the current method). This is done by calling
        the add_reverse_edges function from the instance of the fro Vertex and add a new instance of edge with
        u = fro Vertex, v = to Vertex and w = weight into the list of edges of the fro Vertex.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The reverse edge from the "from" vertex to "to" vertex is not in the list of edges of "from" vertex
        Postcondition:
            - The reverse edge from the "from" vertex to "to" vertex is appended in the list of edges of "from" vertex

        Input
            fro: An integer that denotes the index of the Vertex of the start edge
            to: An integer that denotes the index of the Vertex of the end edge
            weight: An integer that denotes the weight of the edge

        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving the accessing of attributes and
                appending an Edge instance to the reverse_edges list which takes constant time
                complexity
            Worst case analysis: O(1), where the computations are only involving the accessing of attributes and
                appending an Edge instance to the reverse_edges list which takes constant time
                complexity

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be using the
                self.vertices to access the Vertices and their respective methods / attributes
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """
        self.vertices[fro].add_reverse_edges(self.vertices[to], weight)

    def dijkstra(self, source):  # source is the starting vertex instance
        """
        This is a dijkstra method that finds the shortest time from the source to all possible vertices. For my
        dijkstra code, First i will initialize a minHeap with the parameter of self.vertices. Upon initliazation in the
        minHeap, all the vertices will be set with a time of math.inf which will be changed upon the update operation
        with the smallest time. So, after initialization of minHeap with time and vertex tuple, we will update the
        time of the source to be "0" which will also perform an upheap/rise making the first index in the MinHeap to
        be the smallest time which is the source. Next I made a while loop which will loop until thare is no vertex
        to be served from the minHeap. Next we will serve the vertex with the smallest time from the MinHeap,
        followed by setting the visited and discovered for the vertex served to be True which indicates that the
        time for the served vertex is finalized and optimized. Next we will set the edges list to be either the
        vertex edges or vertex reverse edges based on the start_Mode variable to be True or False respectively.

        This is done so as my approach for this assignment is to run dijkstra twice, one with forward edges and one with
        reversed edges and find the shortest time for all the Solulu trees where the sum of time of start to start
        Solulu, weight to break the Solulu and sum of end Solulu to exit tree is the absolute minimum, where the time
        from start to start Solulu is obtained from forward dijkstra, end Solulu to exit tree is obtained from the
        reversed dijkstra and weight is obtained from the time taken to break the Solulu tree. Hence, why I set 2 edge
        list, edges and reversed_edges.

        Once we get the edge list, we will check if the time of the served_vertex is math.inf. If it is math,inf,
        this indicates that the vertex has not been visited or discovered before by any other vertices and there is no
        path from the source to the served vertex, so we will not do an edge relaxation for these vertex, thus
        we have an if condition to do the edge relaxation only if the time of the served_vertex's time != math.inf

        Next if the served_vertex's time != math.inf we will loop through each of the edges of the served_vertex. If
        it is already discovered,  set discovered to True, update the time to the time from the served vertex to the
        vertex from the edge (served vertex's time from source + edge weight). If the visited for the
        vertex_from_initial_edge from the "to" edge of served_vertex is False (indicating we have discovered this vertex
        before but there is a new time from another vertex to this vertex)  I will check if the previous time from
        another vertex is greater than the current time from the served vertex plus the edge weight, we set discovered
        to True, update the time
        Written by Sarviin Hari (32885741)

        Precondition:
            - The time attribute for each and every vertex instances is 0
            - The visited and discovered for all vertices are set to False
            - The graph is connected, weighted, directed graph with non-negative edge weight
            - The starting vertex is given as a parameter source
        Postcondition:
            - The reverse edge from the "from" vertex to "to" vertex is appended in the list of edges of "from" vertex
            - The algorithm computes the smallest time taken from the start vertex to all other vertex in the graph
            and stores in the variable time
            - The algorithm also computes the past of each vertex indicating which vertex is the shortest distance
            connected to which will loop to the source vertex in the end

        Input
            source: An instance of the start vertex where will start running the dijkstra from
        Return:
            self.vertices: List of vertices with the updated shortest distance and updated past from dijkstra

        Time complexity:
            Best case analysis: The best case complexity is similar to the worse case complexity where it is set to be
                O(E log V), where V is the number of vertices in the graph and E denotes the number of edges in the
                graph
            Worst case analysis: To analyze the worst case complexity, let us look at each operation complexity.
                First we have the MinHeap initialization and update of the source index. The MinHeap initialization has
                a worse case complexity of O(V), where V is the number of vertices in the minHeap and update has a worse
                case complexity of O(log V), where V is the number of vertices in the minHeap. This gives a complexity
                of O(V) + O(V log V)

                Next we have the while (minHeap.final_non_served_index()) > 0 loop, which has a complexity of O(V) where
                V is the number of vertices in the minHeap. In the while loop, we have:
                    - serve operation from minHeap which has a worse case complexity of O(log V), where V is the number
                    of vertices in the minHeap
                    - setting visited, discovered to True and storing a pre-defined list in a new variable edges, which
                    all takes O(1) complexity
                    - for loop for each and every edge which itself takes a O(V-1) complexity where V is the number of
                    Vertex and there is a possibility in the worse case secnario where the vertex can have V-1 number of
                    edges. We can simplify the time complexity, O(V-1) to O(V) where V is the number of vertices in the
                    minHeap. In the for loop, we have:
                        - setting visited or discovered to True, setting the past to served_vertex instance and setting
                        the time to the served_vertex time + weight which all takes O(1) complexity
                        - minHeap update operation which has a worse case complexity of O(log V), where V is the number
                        of vertices in the minHeap. This gives a complexity of O(V) + O(V log V)

                Thus, we can summarise the complexity to be O(V log V) + O(V*(log V + 1 + V*(1 + log V)))
                = O(V log V) + O(V*(log V + 1 + V log V)) = O(V log V) + O(V*(V log V)) = O(V log V) + O(V^2 log V)
                = O(V^2 log V) = O(E log V), where V is the number of vertices in the graph and E denotes the number of
                edges in the graph

        Space complexity:
            Input space analysis: O(V), where V is the number of vertices in self.vertices as we will be using the
                self.vertices to access the Vertices and their respective methods / attributes for update
            Aux space analysis: O(V) where V is the number of vertices in self.vertices which is required for the
                instantiation of minHeap
        """
        source.time = 0
        minHeap = MinHeap(self.vertices)  # use a list to make it easy
        minHeap.update((source.time, source))

        # O(V)
        while (minHeap.final_non_served_index()) > 0:

            # remove the first elem from the minHeap list, and append the last item from the heap to first and
            # make a down heap
            served_vertex = minHeap.serve()

            # I have visited served_vertex and time is finalized
            served_vertex[1].visited = True
            served_vertex[1].discovered = True

            # Set the edges list to access based on forward or reverse mode
            if self.start_Mode:
                edges = served_vertex[1].edges
            else:
                edges = served_vertex[1].reverse_edges

            # Dont do edge relaxation if time==math.inf, suggesting that the vertex was never in the
            # minHeap and does not have an edge from the previous vertex from source
            if served_vertex[0] != math.inf:

                # O(V-1) = O(V)
                for edge in edges:
                    vertex_from_initial_edge = edge.v  # corresponding 'to' vertex

                    # When the vertex is not seen before, time = math.inf
                    if vertex_from_initial_edge.discovered == False:
                        vertex_from_initial_edge.discovered = True
                        vertex_from_initial_edge.time = served_vertex[1].time + edge.w
                        # set which past to update based on froward or reverse mode
                        if self.start_Mode == True:
                            vertex_from_initial_edge.start_time = served_vertex[1].time + edge.w
                            vertex_from_initial_edge.past = served_vertex[1]
                        else:
                            vertex_from_initial_edge.reverse_past = served_vertex[1]
                        # O(log V) for update
                        minHeap.update((vertex_from_initial_edge.time, vertex_from_initial_edge))

                    # When the vertex has been seen before, but seen again to comapre the new path and prev path to get the one with the smallest time
                    elif vertex_from_initial_edge.visited == False:
                        # If the new set of time is smaller, update
                        if vertex_from_initial_edge.time > served_vertex[1].time + edge.w:
                            vertex_from_initial_edge.discovered = True
                            # update the new time
                            vertex_from_initial_edge.time = served_vertex[1].time + edge.w
                            # set which past to update based on froward or reverse mode
                            if self.start_Mode == True:
                                vertex_from_initial_edge.start_time = served_vertex[1].time + edge.w
                                vertex_from_initial_edge.past = served_vertex[1]
                            else:
                                vertex_from_initial_edge.reverse_past = served_vertex[1]
                            # O(log V) for update
                            minHeap.update((vertex_from_initial_edge.time, vertex_from_initial_edge))  # update vertex vertex_from_initial_edge in heap with time vertex_from_initial_edge.time (smaller) -> so remove prev and add new -> perform upheap


        return self.vertices


class Vertex:
    def __init__(self, id: int):
        """
        This is an __init__ method where I will initialize variables required for the computation of vertex by other
        methods. Here I will create variables which are id (identity of vertex), edges and reverse_edges (stores the
        forward and reversed edges from vertex), discovered and visited (to denote the state of variable in dijkstra),
        time (denotes the time for vertex to move), past and reverse_past (to store the instance of past vertex),
        pointer to store the current index of vertex in minHeap, is_end_tree and is_final_vertex (stores the states
        of vertex whether it is an exit or final end tree respectively)
        Written by Sarviin Hari (32885741)

        Precondition:
            - The input id is an unique integer denoting the id of the Vertex instance
            - It must have a list for edges and reverse edges, including variables to store the index values, time, past
            vertex and the state of vertex
        Postcondition:
            - The Vertex object is initialized with an integer id
            - An empty list for reverse and forward edges is instantiated as well as the pointer variable to denote the
            position in minHeap, time to store the shortest time, past to store the instance of previous vertex and
            variables such as discovered, visited, is_end_tree and is_final_vertex  which have a default state of False

        Input
            id: An integer denoting the id of vertex
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving storing values in variable
            Worst case analysis: O(1), where the computations are only involving storing values in variable

        Space complexity:
            Input space analysis: O(1), where the input is just an integer value
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
                and empty list
        """
        self.id = id  # the Vertex identity (basically the key)
        self.edges = []  # the value that stores the corresponding edges of the key
        self.reverse_edges = []  # the value that stores the corresponding edges of the key

        # for traversal (almost like maintaining 2 lists. So basically if discovered is False that means you have never even approached the vertex knowingly/unknowingly ; if visited is false that means we might have discovered but we have not gone in and look into the respective vertex's edges)
        self.discovered = False
        self.visited = False  # instead of maintaining them in a list, we can just maintain them by looking at these variables to see if we have looked into them or not to save aux space

        # time
        self.start_time = 0
        self.time = 0

        # past
        self.past = None

        # reverse past
        self.reverse_past = None

        # current index
        self.pointer = None

        # for exit
        self.is_end_tree = False
        self.is_final_vertex = False


    def add_edges(self, to, weight):
        """
        This is a method that a new instance of edge with u = self Vertex, v = to Vertex and w = weight into the list of
        edges of the current Vertex
        Written by Sarviin Hari (32885741)

        Precondition:
            - The forward edge from the current vertex to "to" vertex is not in the list of edges of current vertex
        Postcondition:
            - The forward edge from the current vertex to "to" vertex is appended in the list of edges of current vertex

        Input
            to: An integer that denotes the index of the Vertex of the end edge
            weight: An integer that denotes the weight of the edge

        Return:
            None

        Time complexity:
            Best case analysis: O(1), appending an Edge instance to the self.edges list which takes constant time
                complexity
            Worst case analysis: O(1), appending an Edge instance to the self.edges list which takes constant time
                complexity

        Space complexity:
            Input space analysis: O(E), where E is the number of edges in self.edges as we will be using the
                self.edges to append an Edge instance
            Aux space analysis: O(1) as there is no additional memory required since we are only appending to a
                pre-existing list
        """
        self.edges.append(Edges(self, to, weight))

    def add_reverse_edges(self, to, weight):
        """
        This is a method that a new instance of a reversed edge with u = self Vertex, v = to Vertex and w = weight into
        the list of reverse_edges of the current Vertex.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The reverse edge from the current vertex to "to" vertex is not in the list of edges of current vertex
        Postcondition:
            - The reverse edge from the current vertex to "to" vertex is appended in the list of edges of current vertex

        Input
            to: An integer that denotes the index of the Vertex of the end edge
            weight: An integer that denotes the weight of the edge

        Return:
            None

        Time complexity:
            Best case analysis: O(1), appending an Edge instance to the self.reverse_edges list which takes constant
                time complexity
            Worst case analysis: O(1), appending an Edge instance to the self.reverse_edges list which takes constant
                time complexity

        Space complexity:
            Input space analysis: O(E), where E is the number of edges in self.reverse_edges as we will be using the
                self.reverse_edges to append an Edge instance
            Aux space analysis: O(1) as there is no additional memory required since we are only appending to a
                pre-existing list
        """
        self.reverse_edges.append(Edges(self, to, weight))

    # def __str__(self):
    #     return "Vertex Id: " + str(self.id) + ", Time: " + str(self.time)

    # def __repr__(self):
    #     return "Vertex Id: " + str(self.id) + ", Time: " + str(self.time)


class Edges:
    def __init__(self, u: Vertex, v: Vertex, w):
        """
        This is an __init__ method where I will initialize variables required for the computation of edges by other
        methods. Here I will create 3 instance variables u (instance of "from" Vertex), v (instance of "to" Vertex),
        w (weight of edge)
        Written by Sarviin Hari (32885741)


        Precondition:
            - The input must consists of "from", "to" and "weight"
        Postcondition:
            - 3 instance variable of u, v, and w are initialized to store "from" vertex instance, "to" vertex instance
            and "weight" of the edge

        Input
            u: An instance of "from" vertex
            v: An instance of "to" vertex
            w: An integer denoting the weight of the edge

        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving storing values in variable
            Worst case analysis: O(1), where the computations are only involving storing values in variable

        Space complexity:
            Input space analysis: O(1), where the input is just an integer value and instance variables
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
                and instance variables
        """
        self.u = u
        self.v = v
        self.w = w

    # def __str__(self):
    #     return "From: " + str(self.u) + " To: " + str((self.v)) + " Weight: " + str(self.w)

    # def __repr__(self):
    #     return "From: " + str(self.u.id) + " To: " + str((self.v.id)) + " Weight: " + str(self.w)

class MinHeap:
    def __init__(self, v_list):
        """
        This is an __init__ method where I will initialize the self.heap with the length of the vertex list + 1 (as
        we will have None + N elements), followed by substituting the index of 1 to N-1 with a tuple consisting of
        math.inf denoting the time and an object which is the instance of a Vertex. I also set the pointer of the
        Vertex to be the current index of the element in the heap when instantiated. Then I instantiate 2 variables
        start_index (index that the heap's element starts from) and num_of_removed_nodes (denoting the number of nodes
        that are not served remaining in the heap)
        Written by Sarviin Hari (32885741)

        Precondition:
            - The v_list denotes the vertex instances to be used in min heap and the vertex instances must be valid
            - The min heap must store the time value and the vertex instances
        Postcondition:
            - A tuple of time and vertex instance is stored in the self.heap
            - The time for all the vertex instances is set to math.inf
            - A self.heap instance is initialized with all the vertices and the 0th index being None

        Input
            v_list: A list consisting of Vertex instances
        Return:
            None

        Time complexity:
            Best case analysis: O(N), where N is the number of elements in v_list
            Worst case analysis: O(N), where N is the number of elements in v_list

        Space complexity:
            Input space analysis: O(N), where N is the length of the v_list
            Aux space analysis: O(N), as the additional memory for temporary elements required is to instantiate a new
                list, self.heap to store the (time, Vertex) tuple of elemenets from the v_list
        """

        self.heap = [None]*(len(v_list) + 1)

        for i in range(1, len(self.heap)):
            self.heap[i] = (math.inf, v_list[i-1])
            self.heap[i][1].pointer = i

        self.start_index = 1
        self.num_of_removed_nodes = 0

    def serve(self):
        """
        This is a serve operation, where I will first get the min element from the min heap at index 1, then I will swap
        the element of the first index with the final index of the heap (which is the final index of the list of
        un-served elements). Next I will increase the num_of_removed_nodes by 1 and call the down heap function
        on the swapped element at index 1.
        Written by Sarviin Hari (32885741)

        Precondition:
            - heap is in the correct heap order where the value of each parent node is less than its child nodes
            - The served index must be 1, denoting the smallest node with the smallest value in the heap
        Postcondition:
            - The minimum element is removed from the heap (swapped with the last node and decrease the number of
            non-served elements in the heap by 1 which ensures that the swapped position from the start index will not
            be considered for the subsequent heap)
            - Min heap property where parent node is smaller than or equal to the child node remains
            - The length of heap remains the same
            - The number of elements not served from the heap decrease by 1 (denoted by self.final_non_served_index())

        Input
            index: An integer denoting the index of the parent node
        Return:
            minimum: A tuple consisting of an integer denoting the time and an object which is the
                instance of a Vertex

        Time complexity:
            Best case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity
            Worst case analysis: O(log N), where N is the number of elements in the min heap, when the parent node
                is smaller than or equal to the child node for every iteration until the reaching the end of the heap,
                where we will have log N number of iteration and swaps

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """

        # get the Min form index 1
        minimum = self.heap[self.start_index]

        # swap first and last
        self.swap_values(self.start_index, self.final_non_served_index())
        self.num_of_removed_nodes += 1

        # perform sink operation
        self.down_heap(self.start_index)

        return minimum

    def final_non_served_index(self):
        """
        This is a method to return the index of the last element in the heap. As we are restoring the served elements
        at the end of the list, heap_length ensures that the index always denotes the index of the heap to be the
        element that has not been served
        Written by Sarviin Hari (32885741)

        Precondition:
            - self.heap and self.num_of_removed_nodes must have beem initialized
        Postcondition:
            - The method returns the number of elements in the self.heap excluding the served nodes (appended at the end
            of the list)
            - There is no changes done to heap through this method

        Input
            None
        Return:
            len(self.heap) - self.num_of_removed_nodes - 1: The final index in the heap excluding the served vertex

        Time complexity:
            Best case analysis: O(1), where the computations are only return statement of the length
            Worst case analysis: O(1), where the computations are only return statement of the length

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap to get the
                length of the heap
            Aux space analysis: O(1), as there is no additional memory required
        """
        return len(self.heap) - self.num_of_removed_nodes - 1

    def update (self, pos_instance_tuple):
        """
        This is method to update the time of the specified (ind, Vertex) tuple, where we will get the index of the
        Vertex to be updated from the pointer, then set the value of that position in the list with the new updated
        time tuple, followed by an up_heap operation
        Written by Sarviin Hari (32885741)

        Precondition:
            - heap is in the correct heap order where the value of each parent node is less than its child nodes
            - the pos_instance_tuple must consists of the updated time and the vertex instance to be updated
        Postcondition:
            - The time of the vertex instance is updated and the min heap is in the correct heap order where the parent
            node is smaller than or equal to the child node

        Input
            pos_instance_tuple: A tuple consisting of an integer denoting the time and an object which is the
                instance of a Vertex
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity
            Worst case analysis: O(log N), where N is the number of elements in the min heap, when the parent node
                is smaller than or equal to the child node for every iteration until reaching the end of the heap,
                where we will have log N number of iteration and swaps

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element and for swapping of elements
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """
        # get the current index of the vertex
        index = pos_instance_tuple[1].pointer

        # change the tuple value of prev large value to new small value
        self.heap[index] = pos_instance_tuple

        # rise operation on the current index of the min elem
        self.up_heap(index)

    def size(self):
        """
        This is a method to return the number of elements in the heap
        Written by Sarviin Hari (32885741)

        Precondition:
            - self.heap must have beem initialized
        Postcondition:
            - The method returns the number of elements in the self.heap
            - There is no changes done to heap through this method

        Input
            None
        Return:
            len(self.heap): Number of elements in the heap

        Time complexity:
            Best case analysis: O(1), where the computations are only return statement of the length
            Worst case analysis:  O(1), where the computations are only return statement of the length

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap to get the
                length of the heap
            Aux space analysis: O(1), as there is no additional memory required
        """
        return len(self.heap)

    def swap_values(self, i, j):
        """
        This is method to swap the elements of the given parent and child index values, where we will swap the positions
        of the nodes. Next we will also update the pointers of the nodes to be the new positions of the nodes
        Written by Sarviin Hari (32885741)

        Precondition:
            - The i and j integer index must be within the range of 1 and self.final_non_served_index(), where the
            self.final_non_served_index() denotes the last index of elements in the heap
        Postcondition:
            - The nodes at index i and j are swapped to their new positions
            - the pointers in the vertex instance is updated to the index position

        Input
            i: An integer denoting the index of the parent node
            j: An integer denoting the index of the child node
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity
            Worst case analysis:  O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element and swapping the elements from one index to another
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """
        # swap the elements
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        # update pointers for each vertex
        self.heap[i][1].pointer = i
        self.heap[j][1].pointer = j

    def up_heap(self, index):
        """
        This is a recursive up heap / rise operation, where we will first get the index of the element to rise from
        which is the parent node which can be found by integer division of the current index with 2. Then we will check
        if the parent node is bigger than index 1 and if the parent node is bigger than the child node. If that's the
        Written by Sarviin Hari (32885741)

        Precondition:
            - The index must be within the range of 1 and self.final_non_served_index(), where the
            self.final_non_served_index() denotes the last index of elements in the heap
        Postcondition:
            - Heap property is restored where the elements in the heap are stored in the correct increasing heap order
            with parent node being smaller than the child nodes

        Input
            index: An integer denoting the index of the parent node
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity
            Worst case analysis: O(log N), where N is the number of elements in the min heap, when the parent node
                is smaller than or equal to the child node for every iteration until the reaching the end of the heap,
                where we will have log N number of iteration and swaps

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element and swapping the elements from one index to another
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """
        # get the parent node
        main_index = (index) // 2

        # if the parent > node swap and upheap
        if main_index >= 1:
            if self.heap[main_index][0] > self.heap[index][0]:
                self.swap_values(main_index, index)
                self.up_heap(main_index)

    def smallest_child(self, index):
        """
        This is a method to find the smallest child of a parent node, where we will first compute the index values for
        the 2 child nodes of a parent node by computing the index of the child which are 2*index and 2*index+1. Then
        we will check if the index value is more than the length of heap list (since I am not removing the items from
        the heap, I will use the heap_length which decreases as each node is served as the length of heap list) I will
        return None as the parent node does not have any child nodes. Next out of the left and right child, if the left
        and right are within the heap length I will set the t_ind to be the smallest element of them and only one of the
        childs are within heap length then that child will be set to t_ind. Then finally I will compare the parent
        node and the smallest child node. If the parent node is smaller than or equal to the smallest child node, I
        return None and if otherwise I will return the smallest child node index itself.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The index must be within the range of 1 and self.final_non_served_index(), where the
            self.final_non_served_index() denotes the last index of elements in the heap
            - The return index must be a valid index
        Postcondition:
            - The return value is a valid index within the range of 1 and self.final_non_served_index(), where the
            self.final_non_served_index() denotes the last index of elements in the heap and the return value is either
            the smallest child of the parent node or None

        Input
            index: An integer denoting the index of the parent node
        Return:
            None: None value denoting the index is the smallest among the child nodes
            index: An integer denoting the index of the smallest child node


        Time complexity:
            Best case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity
            Worst case analysis: O(1), where the computations are only involving comparison operation and accessing
                operations in a list which has a O(1) complexity

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """
        l_child = 2*index
        r_child = 2*index+1

        # both are off limits
        if l_child > self.final_non_served_index() and r_child > self.final_non_served_index():
            return None

        # if both left and right are within limits, choose the smallest value
        # if either within the limit choose it
        t_ind = index
        if l_child <= self.final_non_served_index() and r_child <= self.final_non_served_index():
            if self.heap[l_child][0] < self.heap[r_child][0]:
                t_ind = l_child
            else:
                t_ind = r_child
        elif l_child <= self.final_non_served_index():
            t_ind = l_child
        elif r_child <= self.final_non_served_index():
            t_ind = r_child

        # compare the values between the smallest child and the parent node
        # if it is smaller, then return the index, else return None
        if self.heap[index][0] > self.heap[t_ind][0]:
            return t_ind
        else:
            return None

    def down_heap(self, index):
        """
        This is a recursive down heap / sink operation, where we will first get the index of the element to sink from
        the input variable (index), where we will first find the child nodes of the index of the heap. If the
        smallest child function returns None, we will not down heap again, but if it returns an index value of the
        left/right child which has the smallest value, of them both, we will swap the values of the parent and the child
        and recurse the down heap again with the index of the swapped parent node
        Written by Sarviin Hari (32885741)

        Precondition:
            - The index must be within the range of 1 and self.final_non_served_index(), where the
            self.final_non_served_index() denotes the last index of elements in the heap
        Postcondition:
            - Heap property is restored where the elements in the heap are stored in the correct increasing heap order
            with parent node being smaller than or equal to the child nodes

        Input:
            index: An integer denoting the index of the parent node
        Return:
            None

        Time complexity:
            Best case analysis: O(1), when the child nodes are bigger than the parent node at which we will not have to
                recurse to reorder the nodes as it is already in the correct position
            Worst case analysis: O(log N), where N is the number of elements in the min heap, when the parent node
                is smaller than or equal to the child node for every iteration until the reaching the end of the heap,
                where we will have log N number of iteration and swaps

        Space complexity:
            Input space analysis: O(N), where N is the length of the self.heap as we will be using the heap for element
                access to get the element and swapping the elements from one index to another
            Aux space analysis: O(1), as the additional memory for temporary elements required are only integer values
        """
        min_distance_index = self.smallest_child(index)

        if min_distance_index is not None:
            self.swap_values(index, min_distance_index)
            self.down_heap(min_distance_index)


if __name__ == '__main__':

    # The roads represented as a list of tuples
    roads = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    # The solulus represented as a list of tuples
    solulus = [(5, 10, 0), (6, 1, 6), (7, 5, 7), (0, 5, 2), (8, 4, 8)]
    # Creating a TreeMap object based on the given roads
    myforest = TreeMap(roads, solulus)

    # Shortest time from start vertex 1 to exit vertex 7, 2 or 4
    start = 1
    exits = [7, 2, 4]
    print(myforest.escape(start, exits))