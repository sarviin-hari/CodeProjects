"""
SARVIIN A/L HARI
32885741
Version 3
"""
import math

# ==========
# Security Schedule Allocation with Ford Fulkerson

class ResidualNetwork:
    def __init__(self):
        """
        This is an __init__ method of a ResidualNetwork class which is used to define the residual network of a Flow
            Network. In this method I defined the instance variables security (vertex of all securities), company
            (vertex of all companies), sec_day_shift (vertex of all securities and respective shifts for each day),
            comp_day_shift (vertex of all companies and respective shifts for each day), day  (vertex of all securities
            and days) as an empty list and variables begin, source, end, sink as None as well as setting the initial
            sum to 0.
        I decided to use a Residual Network with the Flow Network as it can keep track of the flows and capacities for
            the network by finding the augmented paths with final max flow from the source and sink using an efficient
            algorithm, bfs using the approach of ford fulkerson.
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - Initialize an empty list for security, company, sec_day_shift, comp_day_shift, day
            - Initialize instance variables begin, source, end, and sink to None

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the operation involves the assignment of instance variables with None
                and initialization of empty lists
            Worst case analysis: O(1), where the operation involves the assignment of instance variables with None
                and initialization of empty lists
        Space complexity:
            Input space analysis: O(1), where the input consists of a char and a string which has a complexity of O(1)
            Aux space analysis: O(1), where the auxiliary space is used for initialization of an empty lists and
                instance variables
        """
        # initialize lists for vertices
        self.security = []
        self.company = []
        self.sec_day_shift = []
        self.comp_day_shift = []
        self.day = []

        # initialize the start and end indexes
        self.begin = None
        self.source = None
        self.end = None
        self.sink = None

        self.sum = 0

    def bfs(self, source, target=None):  # source is the starting vertex instance
        """
        This is a bfs method of a ResidualNetwork class which finds the shortest path from the source to the target
            of the residual network, sink. Once the shortest path is obtained the bfs is terminated. This method
            is called from the ford fulkerson method of the flow network to find the augmenting path from the source to
            sink such that the max flow from the source to sink can be identified. Since bfs uses the shortest path
            approach, this ensures that the augmenting path always have the minimum number of edges thus assisting
            in ensuring the complexity of ford fulkerson remains efficient. The augmented shortest path are identified
            by storing the previous edges from the source in the variables special_edges which can be used to back track
            from the sink to obtain the augmented path
        Written by Sarviin Hari (32885741)

        Precondition:
            - The vertex and edges for the residual network has already been added
        Postcondition:
            - terminate when the target is reached from the source
            - update the distance variable of the residual network

        Input
            - source: The node instance for the source of the flow network
            - target: The node instance for the sink of the flow network
        Return:
            True/False indicating if the bfs has reached the target or not respectively

        Time complexity:
            Best case analysis: Same as the worst case
            Worst case analysis: O(V+E), where V is the number of vertices and E is the number of edges. This is because
            in the worst case, we will traverse through all the vertices from source to sink and since each vertex has
            its own corresponding edges, so for each vertex each of the edges are traversed to get the corresponding
            "to" vertex. Since in our network flow, in total for all the Vertices, we have E edges and the edges will
            be traversed E times in the worse case when all vertices are traversed, the complexity becomes an addition
            of V and E

        Space complexity:
            Input space analysis: O(1), where the input consists of the instances of the source and target instances
            Aux space analysis: O(V), where V is the number of vertices in the flow network. This is because the bfs
                can run form the source to the sink through all vertices in the worst case, and since we are appending
                the vertices discovered into a list, in worse case we can have  V vertices in the list

        """

        # discovered = Queue() # ADT
        discovered = [source]

        # loop through each of the elements in the discovered list as long as its not empty
        while len(discovered) > 0:
            discovered_vertex = discovered.pop(0)  # remove the first elem from the discovered list
            discovered_vertex.visited = True
            discovered_vertex.discovered = True

            # for each of the edges in the current vertex loop through all the edges and add the vertex in discovered
            # if there is a flow
            for edge in discovered_vertex.edges:
                if (edge.flow != 0):
                    visiting_vertex = edge.v  # corresponding 'to' vertex

                    # if the visiting vertex from the discovered vertex is not discovered and not visited, add it to the
                    # discovered list
                    if visiting_vertex.visited == False:
                        if visiting_vertex.discovered == False:  # put the 'to' vertex in the discovered list, set it to TRue
                            # print("  visited and discovered = yes", discovered_vertex.id, visiting_vertex.id)
                            visiting_vertex.special_edge = edge
                            visiting_vertex.distance = discovered_vertex.distance + 1
                            visiting_vertex.past = discovered_vertex
                            discovered.append(visiting_vertex)
                            visiting_vertex.discovered = True

            # if the target is reached return True (successful bfs)
            if discovered_vertex == target:
                return True

        return False


class Vertex:
    def __init__(self, id: int):
        """
        This is an __init__ method where I will initialize variables required for the residual network vertex. The
        variables initialized for the vertex are id (identity of vertex), edges (edges corresponding to the vertex),
        identity (vertex category), discovered and visited (for bfs), distance, past (prev vertex) and special_edges
        (previous edge of the residual network).
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - required isntaxnce variables id, edge, idnetity, dicoeverd, visisted, distance, past and special_edges
            are created

        Input
            id: An integer indicating the vertex's id
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
        self.id = id  # the Vertex identity (basically the start)
        self.edges = []  # the value that stores the corresponding edges of the start
        self.identity = ""

        # for traversal (almost like maintaining 2 lists. So basically if discovered is False that means you have never
        # even approached the vertex knowingly/unknowingly ; if visited is false that means we might have discovered
        # but we have not gone in and look into the respective vertex's edges)
        self.discovered = False
        self.visited = False

        # distance
        self.distance = 0

        # past vertex
        self.past = None

        # the edge the current vertex originated from
        self.special_edge = None

    def add_edges(self, to, flow, capacity, flowNetworkEdge):
        """
        This is a method to add an Edge instance to the vertex with the given flow and capacity as well as
            the corresponding flow network edge for the edge
        Written by Sarviin Hari (32885741)

        Precondition:
            - There is no edge from the current vertex to the "to" vertex
        Postcondition:
            - There is an edge from the current vertex to the "to" vertex
            - The reverse_edge is added from "to" vertex to "self" vertex
            - The flowNetworkEdge is added for the forward and reverse edges

        Input
            to: An instance of vertex to add an edge to
            flow: An integer indicating the flow value of the edge
            capacity: An integer indicating the capacity value of the edge
            flowNetworkEdge: An instance of an Edge of a FlowNetwork corresponding to the Residual Network

        Return:
            None

        Time complexity:
            Best case analysis: O(1), adding an Edge instance takes a constant time complexity to append to the
                self.edges list
            Worst case analysis: O(1), adding an Edge instance takes a constant time complexity to append to the
                self.edges list

        Space complexity:
            Input space analysis: O(E), where E is the number of edges in self.edges as we will be using the
                self.edges list to append an Edge instance
            Aux space analysis: : O(1), as the additional memory for temporary elements required are only integer values
                and instance variables creation
        """


        # create normal and opposite edge and set opposite's back to True
        forward_edge = Edges(self, to, capacity - flow)
        reverse_edge = Edges(to, self, flow)
        reverse_edge.setBack()

        # add forward and reverse edge for residual graph
        forward_edge.add_Edge(reverse_edge)
        reverse_edge.add_Edge(forward_edge)

        # add the flowNetwork into forward and reverse edge
        forward_edge.add_flowNetwork(flowNetworkEdge)
        reverse_edge.add_flowNetwork(flowNetworkEdge)

        # add the edges to their respective vertices
        self.edges.append(forward_edge)
        to.edges.append(reverse_edge)

    # def __str__(self):
    #     return "Vertex Id: " + str(self.id) + ", Distance: " + str(self.distance)

    # def __repr__(self):
    #     return self.identity + str(self.id)

class Edges:
    def __init__(self, u, v, flow, capacity=None):
        """
        This is an __init__ method where I will initialize variables required for the residual and the flow network
            edges (Same Edge class for both residual and flow network).
        First I initialize common variable u (instance of "from" Vertex), v (instance of "to" Vertex), flow (current
            flow of the edges), capacity (capacity of the edge - default to None for Residual).
        Next, for the Residual network, I define variables my_opposite, flowNetwork and back to store the reverse edge
            instance, flownetwork edge instance of the current edge and true/false boolean to determine if the current
            edge is a reverse of residual edge or not

        Written by Sarviin Hari (32885741)

        Precondition:
            - The input must consist of "from", "to" and "flow"
            - The capacity parameter is optional and default as None (for Residual Network)
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
        # create instances for the from and to and flow and capacity
        self.u = u
        self.v = v
        self.flow = flow
        self.capacity = capacity

        # set the opposite edge and the corresponding flowNetwork edge
        self.my_opposite = None
        self.flowNetwork = None

        # indicate the state of the edge to be forward or reverse
        self.back = False

    def add_Edge(self, instance):
        """
        The add_Edge add an instance of the reversed edge in the instance variable my_opposite
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - None

        Input
            instance: An instance of an Edge of the reverse edge corresponding to the forward edge Residual Network

        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving storing values in variable
            Worst case analysis: O(1), where the computations are only involving storing values in variable

        Space complexity:
            Input space analysis: O(1), where the input is just an integer value and instance variables
            Aux space analysis: O(1), as no new auxiliary input is created
        """
        self.my_opposite = instance

    def setBack(self):
        """
        The setBack sets the back instance variable to True indicating the current edge is the reverse of the residual
            edge
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - None

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving storing values in variable
            Worst case analysis: O(1), where the computations are only involving storing values in variable

        Space complexity:
            Input space analysis: O(1), where the input is just an integer value and instance variables
            Aux space analysis: O(1), as no new auxiliary input is created
        """
        self.back = True

    def add_flowNetwork(self, instance):
        """
        The add_flowNetwork stores the Flow Network instance in the flowNetwork variable
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - None

        Input
            instance: An instance of an Edge of the Flow Network corresponding to the Residual Network

        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the computations are only involving storing values in variable
            Worst case analysis: O(1), where the computations are only involving storing values in variable

        Space complexity:
            Input space analysis: O(1), where the input is just an integer value and instance variables
            Aux space analysis: O(1), as no new auxiliary input is created
        """
        self.flowNetwork = instance

    # def __str__(self):
    #     return "(" + str(self.u.identity) + str(self.u.id) + ", " + str(self.v.identity) + str(self.v.id) + ", " + str(self.flow) + ", " + str(self.flowNetwork.flow) + "/" + str(self.flowNetwork.capacity) + ") " + str(self.back)[0]

    # def __repr__(self):
    #     return "(" + str(self.u.identity) + str(self.u.id) + ", " + str(self.v.identity) + str(self.v.id) + ", " + str(self.flow) + "/" + str(self.capacity) + ")"

class FlowVertex:
    def __init__(self, id: int):
        """
        This is an __init__ method where I will initialize variables required for the residual network vertex. The
        variables initialized for the vertex are id (identity of vertex), edges (edges corresponding to the vertex),
        identity (vertex category), and edges_present (to determine if the vertex has an edge or not)
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - None

        Input
            id: An integer indicating the vertex's id
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

        self.id = id  # the Vertex identity (basically the start)
        self.edges = []  # the value that stores the corresponding edges of the start

        self.identity = ""

        # set whether if the vertex has an edge or nor (based on preferences)
        self.edge_present = False

    def add_edges(self, to, flow, capacity):
        """
        This is a method to add an Edge instance to the vertex with the given flow and capacity to ensure the link from the
            "from" vertex to the "to"vertex
        Written by Sarviin Hari (32885741)

        Precondition:
            - There is no edge from the current vertex to the "to" vertex
        Postcondition:
            - There is an edge from the current vertex to the "to" vertex

        Input
            to: An instance of vertex to add an edge to
            flow: An integer indicating the flow value of the edge
            capacity: An integer indicating the capacity value of the edge

        Return:
            None

        Time complexity:
            Best case analysis: O(1), adding an Edge instance takes a constant time complexity to append to the
                self.edges list
            Worst case analysis: O(1), adding an Edge instance takes a constant time complexity to append to the
                self.edges list

        Space complexity:
            Input space analysis: O(E), where E is the number of edges in self.edges as we will be using the
                self.edges list to append an Edge instance
            Aux space analysis: : O(1), as the additional memory for temporary elements required are only integer values
                and instance variables creation
        """

        # add an edge to flownetwork
        forward_edge_to_flow_network = Edges(self, to, flow, capacity)
        self.edges.append(forward_edge_to_flow_network)

        return forward_edge_to_flow_network

    # def __str__(self):
    #     return self.identity + str(self.id)

    # def __repr__(self):
    #     return self.identity + str(self.id)


class newFlowNetwork:
    def reset(self):
        """
        This is a method to reset the state of the instances of past, visited, discovered in each and every vertex
            to either False or None. This is done to ensure that there is no complications in computation when I run
            the bfs for the subsequent iterations to get the flow from source to sink the visited or discovered edges
            can be traversed again
        Written by Sarviin Hari (32885741)

        Precondition:
            - The elements in the list are all the Vertex class
        Postcondition:
            - the variables in vertices are reset to None or False to ensure the bfs works properly for next bfs
            iteration

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: O(m + n), where m is the number of companies and n is the number of securities as we
                will be looping through the list to reset the values
            Worst case analysis: O(m + n), where m is the number of companies and n is the number of securities as we
                will be looping through the list to reset the values


        Space complexity:
            Input space analysis: O(m + n), where m is the number of companies and n is the number of securities in
                self.g.security, self.g.day, self.g.sec_day_shift, self.g.company, and self.g.comp_day_shift as we will
                traverse on all these vertices to reset their visited, discovered and past states to False or None
                looping through each of these vertices to reset their state to their original values
                looping through each of these vertices to reset their state to their original values
            Aux space analysis: O(1) as there is no additional memory required since we are changing the states of the
                variables only
        """

        # reset the security list
        for i in range(len(self.security)):
            self.g.security[i].visited = False
            self.g.security[i].discovered = False
            self.g.security[i].past = None

        # reset the security days list
        for i in range(len(self.sec_days)):
            self.g.day[i].visited = False
            self.g.day[i].discovered = False
            self.g.day[i].past = None

        # reset the security days-shift list
        for i in range(len(self.sec_day_shift)):
            self.g.sec_day_shift[i].visited = False
            self.g.sec_day_shift[i].discovered = False
            self.g.sec_day_shift[i].past = None

        # reset the company list
        for i in range(len(self.company)):
            self.g.company[i].visited = False
            self.g.company[i].discovered = False
            self.g.company[i].past = None

        # reset the company shift list
        for i in range(len(self.comp_day_shift)):
            self.g.comp_day_shift[i].visited = False
            self.g.comp_day_shift[i].discovered = False
            self.g.comp_day_shift[i].past = None

        # reset the begin vertex
        self.g.begin.visited = False
        self.g.begin.discovered = False
        self.g.begin.past = None

        # reset the end vertex
        self.g.end.visited = False
        self.g.end.discovered = False
        self.g.end.past = None

        # reset the source vertex
        self.g.source.visited = False
        self.g.source.discovered = False
        self.g.source.past = None

        # reset the sink vertex
        self.g.sink.visited = False
        self.g.sink.discovered = False
        self.g.sink.past = None

    def __init__(self, pref, off, min_s, max_s):
        """
        This is a __init__ method that creates a flownetwork and the subsequent residual network instance related
            to teh flownetwork. First I will make a validation check for the __init__ method where I will check if the
            demand of the companies matches the maximum securities available followed by checking if the number of min
            securities working days can match the company demand (check if number of securities required per company is
            lesser than the number of securities available per day) and return None if either conditions are met as they
            are non-feasible. Next this method creates the instances for the source, start, sink and end of the
            flownetwork. Next, a list is created for each security followed by days for a security, followed by
            shifts for a security based on days followed by the shift for the companies and finally a list for the
            companies. Following that edges are created for the flownetwork from the source to the securities (based
            on their min-shift lower bound) and source to the start (based on additional requirement of securities by
            the companies). Next subsequent edges are added between the securities to days, the days to security shifts
            , the security shifts to company shifts and the company shifts to company. Finally, edges with 0 capacity
            from the company is added to the end vertex and edges with capacity of total demand for a company for 30
            days is added to the sink vertex. This creates a complete flownetwork for the problem to determine if the
            allocation is feasible or not and what will the allocation be using ford fulkerson
        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - The flownetwork is created with all vertices and edges connecting from source to sink with a flow and
            capacity with the corresponding residual network

        Input
            pref: A list of list where the outer list represents the number of securities and the inner list represents
                the preference of the securities shifts
            off: A list of list where the outer list represents the number of companies and the inner list represents
                the number of securities required per shift
            min_s: An integer indicating the minimum shifts a security has to work in 30 days
            max_s: An integer indicating the maximum shifts a security can work in 30 days
        Return:
            None

        Time complexity:
            Best case analysis: O(m), where m is the number of companies. This occurs when the minimum number of
                securities shifts is bigger than the companies requirement (where there are securities that
                have not been allocated with their min shifts, but the company has matched the requirements already).
                This results in an early termination where there is no need to create the vertex and edge insstances.
            Worst case analysis: O(m * n), where m is the number of companies and n is the number of securities.
                This is because to create edges between the shifts of the security and the shifts of the company,
                I have to traverse for each of the security to each of the shifts in each company which results in
                the complexity being O(m)*O(n) = O(mn). Although the complexity is O(30*3*n) for each security and
                O(30*3*m) for each company, since 30*3 is a constant value which can be amortized to O(1) these
                complexities will be O(n) and O(m) respectively. Although there are multiple other loop functions, these
                functions either run O(m) times or O(n) times where O(mn) is a dominating complexity


        Space complexity:
            Input space analysis: O(m + n), where m is the number of companies and n is the number of securities.
                Although we have a list in a list for all the companies and securities, but since the internal list is
                a constant value of 3, the complexity will be O(m*3) + O(n*3) = O(3m+3n) = O(m+n)
            Aux space analysis: O(m * n), where m is the number of companies and n is the number of securities.
                This is because after creating the edges between the shifts of the security and the shifts of the
                company, the edges has to be stored in the edges list for each vertex of the shifts of the security.
                Since there will be m*n number of edges in total scaled by a constant 30 or 3*30, so the
                auxiliary space complexity remains as O(mn) as the constants will have a complexity of O(1).
                Furthermore, since creating an edge for vertices in flow network and residual network takes the same
                auxiliary space for each, the auxiliary space will be 2*O(mn) = O(2mn) = O(mn)

        """


        self.num_of_days = 30

        # the minimum shifts of securities can or cant be fulfilled by the given companies
        self.max_demand_for_30_days = 0
        for dem in off:
            self.max_demand_for_30_days += sum(dem) * self.num_of_days
        self.num_of_shift_security = len(pref)*min_s

        # get the maximum number of securities that can work
        self.pref_count = len(pref)*max_s

        # gets the sum of all the number of officers for 30 days
        self.sums = 0
        for i in range(len(off)):
            self.sums += sum(off[i])*30

        # print(self.pref_count, self.sums, self.num_of_shift_security, self.max_demand_for_30_days)
        # print(self.max_demand_for_30_days - min_s * len(pref))

        # when the number of securities required per company is lesser than the number of securities available per day
        if self.pref_count < self.sums:
            return

        # when the minimum number of security shifts is bigger than the companies requirement
        if self.num_of_shift_security > self.max_demand_for_30_days:
            # print("in")
            return
        # create a residual plot instance
        self.g = ResidualNetwork()
        self.total_sum = 0

        ## For addition of vertices, we will add vertices for both the flow network and residual network

        # create list of security, company, days for security and shifts for security for flow network and residual
        self.security = [None]*len(pref)
        self.g.security = [None]*len(pref)
        self.company = [None]*len(off)
        self.g.company = [None]*len(off)

        # create vertex for securities
        for i in range(len(pref)):
            v = FlowVertex(i + 1)
            v.identity = "s"
            self.security[i] = v
            self.g.security[i] = Vertex(i+1)

        # create vertex for security days
        self.sec_days = []
        index = 1
        for i in range(len(pref)*30):
            if i == 30*index:
                index += 1
                d_index = 0

            v = FlowVertex(i%30 + 1)
            v.identity = "s" + str(index) + "_D" + str(i%30 + 1) + " "
            self.sec_days.append(v)

            v2 = Vertex(i%30 + 1)
            v2.identity = "s" + str(index) + "_D" + str(i%30+ 1) + " "
            self.g.day.append(v2)

        # create vertex for security shifts - O(n*30*3) = O(n)
        num_of_vertex = len(pref)*30*3
        working_shifts = 30*3
        index = 1
        d_index = 1
        self.sec_day_shift = []
        for i in range(num_of_vertex):
            shift_index = i % 3
            if i == working_shifts*index:
                index += 1
                d_index = 0
            if i % 3 == 0 and i != 0:
                d_index += 1

            v = FlowVertex(shift_index + 1)
            v.identity = "s" + str(index) + "_D" + str(d_index) + "_S"

            v2 = Vertex(shift_index + 1)
            v2.identity = "s" + str(index) + "_D" + str(d_index) + "_S"

            self.sec_day_shift.append(v)
            self.g.sec_day_shift.append(v2)
        # print(self.sec_day_shift)

        # create vertex for companies
        for i in range(len(off)):
            v = FlowVertex(i + 1)
            v.identity = "c"
            self.company[i] = v
            self.g.company[i] = Vertex(i+1)

        # create vertex for company shifts - O(m*30*3) = O(m)
        num_of_vertex = len(off)*30*3
        working_shifts = 30*3
        index = 1
        d_index = 1
        self.comp_day_shift = []
        for i in range(num_of_vertex):
            shift_index = i % 3
            if i == working_shifts*index:
                index += 1
                d_index = 0
            if i % 3 == 0 and i != 0:
                d_index += 1
            # if i ==
            v = FlowVertex(shift_index + 1)
            v.identity = "c" + str(index) + "_D" + str(d_index) + "_S"

            v2 = Vertex(shift_index + 1)
            v2.identity = "c" + str(index) + "_D" + str(d_index) + "_S"

            self.comp_day_shift.append(v)
            self.g.comp_day_shift.append(v2)

        # create the start and end vertex
        self.begin = FlowVertex(1000)
        self.end = FlowVertex(1001)
        self.source = FlowVertex(1002)
        self.sink = FlowVertex(1003)
        self.g.begin = Vertex(1000)
        self.g.end = Vertex(1001)
        self.g.source = Vertex(1002)
        self.g.sink = Vertex(1003)

        ## For addition of edges, we will add edges for both the flow network and residual network

        # add edge from source to start
        e_s = self.source.add_edges(self.begin, 0, self.max_demand_for_30_days - min_s * len(self.security))  # - incoming + outgoing, demand = max_demand_for_30_days, incoming = 0, outgoing = lb * len(self.security)
        e_e = self.end.add_edges(self.sink, 0, 0)
        self.g.source.add_edges(self.g.begin, 0, (self.max_demand_for_30_days - min_s * len(self.g.security)), e_s)  # - incoming + outgoing, demand = max_demand_for_30_days, incoming = 0, outgoing = lb * len(self.security)
        self.g.end.add_edges(self.g.sink, 0, 0, e_e)

        # add edge from source to security with demand as capacity and begin to security - O(n)
        for i in range(len(self.security)):
            # add the lb from source
            e_s = self.source.add_edges(self.security[i], 0, min_s)
            # add the additional remains
            e_b = self.begin.add_edges(self.security[i], 0, max_s - min_s)

            self.g.source.add_edges(self.g.security[i], 0, min_s, e_s)
            self.g.begin.add_edges(self.g.security[i], 0, max_s - min_s, e_b)

        # add edge from security to days - O(n*30) = O(n)
        index = 0
        for i in range(len(self.security)):
            for j in range(30):
                e_sd = self.security[i].add_edges(self.sec_days[index], 0, 1)
                self.g.security[i].add_edges(self.g.day[index], 0, 1, e_sd)
                # print(i+1, index+1)
                index += 1

        # add edges from days to shifts of each security - O(n*30*3) = O(n)
        index = 0
        num_sec = 0
        for i in range(len(self.sec_days)):
            if i % 30 == 0 and i != 0:
                # print("in")
                num_sec +=1

            for j in range(3):
                if pref[num_sec][j] == 1:
                    sec_days = self.sec_days[i].add_edges(self.sec_day_shift[index], 0, 1)
                    self.g.day[i].add_edges(self.g.sec_day_shift[index], 0, 1, sec_days)
                    self.sec_day_shift[index].edge_present = True

                # print(i%30+1, self.sec_day_shift[index], pref[num_sec][j])
                index += 1

        # add edges from security shifts to company shifts - O(m*n) = O(mn)
        sec_num = 1
        for i in range(len(self.sec_day_shift)):
            if i % (30*3) == 0:
                sec_num += 1
            index = i % (30*3)
            for j in range(len(off)):
                if  self.sec_day_shift[i].edge_present == True:
                    e_sds_cds = self.sec_day_shift[i].add_edges(self.comp_day_shift[index], 0, 1)
                    self.g.sec_day_shift[i].add_edges(self.g.comp_day_shift[index], 0, 1, e_sds_cds)
                index += 30*3

        # add edge from company shift to company - O(m*30*3) = O(m)
        index = 0
        for i in range(len(self.company)):
            for j in range(30*3):

                weight = off[i][j%3]

                e_cds = self.comp_day_shift[index].add_edges(self.company[i], 0, weight)
                self.g.comp_day_shift[index].add_edges(self.g.company[i], 0, weight, e_cds)

                index += 1

        # add edge from company to sink - O(m)
        for i in range(len(self.company)):
            required_officers_per_day = sum(off[i])
            required_officers_for_all_days = required_officers_per_day * self.num_of_days

            # self.company[i].add_edge(self.end, required_officers_for_all_days,required_officers_for_all_days)
            e_ce = self.company[i].add_edges(self.end, 0, 0)
            e_cs = self.company[i].add_edges(self.sink, 0, required_officers_for_all_days)

            self.g.company[i].add_edges(self.g.end, 0, 0, e_ce)
            self.g.company[i].add_edges(self.g.sink, 0, required_officers_for_all_days, e_cs)

    def ford_fulkerson(self):
        """
        This is a ford fulkerson method on the residual network. For a ford fulkerson method, I use the bfs defined in
            the residual network to find the augmenting path continuously to get the flow for the flow network until no
            flows exists from the source to sink. Once there is no available augmenting path from the source to sink, we
            can identify that the ford ferkuson method is complete with the max flow of the network flow.
        To run this method, first we will get an augmenting path from the bfs, next, I will find the minimum distance
            within the augmenting path and update the flownetwork and the residual network with the minimum flow
            identified. Following that I will reset the visited, discovered and past states of the residual network to
            default then I will run the bfs again. The bfs will run again and again until there is no augmenting path.
        Written by Sarviin Hari (32885741)

        Precondition:
            - The Residual Network and Flow Network has been defined with respective edges from each vertex
        Postcondition:
            - The flow network is updated with the max flow from source to sink

        Input
            None
        Return:
            None

        Time complexity:
            Best case analysis: Same as the worst case
            Worst case analysis: O(m * n * n), where m is the number of companies and n is the number of securities.
                The worst case complexity of a ford fulkerson is O(VE^2), where V is the number of vertices and E is the
                number of edges. Although for our flow network, E should be approximately V^2, but not in this case,
                where the E will not be V^2 since most of the edges are scaled between the companies and the securities,
                and there is no connection between companies to companies or securities to securities. This ensures that
                the number of edges is dependent on the preferences of the securities, which is why we can see that for
                the edges, it is dominated by the number of securities, n. As for the number of vertices, the dominant
                factor for the number of vertices traversed is the companies themselves as the requirement of the
                companies is what we are trying to fulfill as the demand for the securities. In this case, since the
                dominant factor is the number of companies, the number of vertices visited is scaled by the number of
                companies. This ensures that the worse case time complexity lies between O(mnn). The ford fulkerson has
                to run O(mnn) times since to run bfs, the complexity will O(V + E) = O(m + n), and since a bfs is being
                used to identify the number of times being run, the complexity will be O(VE) = O(mn). Thus, in total,
                since the dominating factor for bfs is scaled by the number of edges, the total complexity = O(mnn).

        Space complexity:
            Input space analysis: O(1), since there is no inputs and the self input values retieved are methods instead
                of variable of lists
            Aux space analysis: O(m), where m is the number of companies. The space complexity of O(m) is required in
                the bfs to store the discovered list that has been traversed and since the remaining operations in ford
                fulkerson involves updating the values only.
        """

        ### Ford_fulkerson
        # find the first augmenting path with bfs
        bfs_value = self.g.bfs(self.g.source, self.g.sink)

        # loop through as long as the bfs_value returned is True indicating the presence of an augmenting path
        while bfs_value:
            initial = self.g.sink
            minimum = math.inf

            # get the maximum possible flow (the smallest value possible based on the current capacity and flow)
            while initial is not None:
                if initial.past != None:
                    minimum = min(minimum, initial.special_edge.flow)

                initial = initial.past

            self.total_sum += minimum

            # update the flow for flowNetwork, normal edge and reverse edge
            initial = self.g.sink
            while initial is not None:
                if initial.past == None:
                    break

                if not initial.special_edge.back:
                    initial.special_edge.flow -= minimum
                    initial.special_edge.my_opposite.flow += minimum
                    initial.special_edge.flowNetwork.flow += minimum
                else:
                    initial.special_edge.flow -= minimum
                    initial.special_edge.my_opposite.flow += minimum
                    initial.special_edge.flowNetwork.flow -= minimum
                initial = initial.past

            # for all vertices reset the visited and discovered
            self.reset()

            # run the bfs again to get the next augmenting path
            bfs_value = self.g.bfs(self.g.source, self.g.sink)

def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
    This is a allocate method that creates a flownetwork and the subsequent residual network instance related
        to the flownetwork to define the structure of the graph path from the security to the companies. After
        creating the flow and teh residual network, the ford fulkerson method will be run to find the maximum
        flow from teh source to the sink and the update is done on the flow network itself. Next, the edges from the
        source is checked if they have a max flow, if yes then the problem is feasible and we will update the allocation
        list, else, the problem is not feasible and None is returned

        The approach I am planning to use for this assignment is to create a Flow Network based on the Circular Lower
            Bound Flows and the corresponding Residual Network for the Flow Network. The Residual Network is initialized
            upon the creation of the FlowNetwork, where I will initialize the Residual Network as an instance variable
            of the Flow Network.The Flow Network is created by creating the vertices for start, source, sink and end as
            well as lists for securities, security_days, security_Shifts, company_shifts and companies while adding
            edges with a flow and capacity to determine the maximum flow through each edge. I will add the edges from
            the vertex of the security to days then days to sec_day_shift then sec_day_shift to comp_day_shift then
            comp_day_shift to company as well as edges from source to security, start to security and companies to sink.
            These edges will also be created concurrently while creating the Residual Network with the instance of
            FlowNetwork passed in as a parameter for the Edges to store these instances. Next I will run the ford
            fulkerson on the residual network which will run the bfs of the Residual Network to get an augmenting path
            continuously to get the flow until no flows exists from the source to sink. This indicates the completion
            of the ford fulkerson method and following that, I will check if the flow is complete (feasible) by
            observing the edges from the source to the securities to check if the flow = capacity for all the edges. If
            they are all equal then it is feasible, else it is not feasible. Finally, based on the resulting flow
            network I will create a list of a list for the allocation of the securities for the companies. For the
            approach of this question, although we will be using n*30*3 number of vertices for the shifts of security and
            m*30*3 number of vertices for the shifts of companies, but since, 30 and 3 are constants, they can be
            considered to be of  O(1) complexity, thus bringing the complexity of creating these vertices to O(n) and
            O(m) respectively

    Written by Sarviin Hari (32885741)

    Precondition:
        - The preferences for the security must be at least one of the shifts
        - The min shift <= max shift and are bounded by 0 and 30 inclusive
    Postcondition:
        - The feasibility of the flow network is identified, if yes, allocation returned, else None returned

    Input
        preferences: A list of list where the outer list represents the number of securities and the inner list
            represents the preference of the securities shifts
        officers_per_org: A list of list where the outer list represents the number of companies and the inner list
            represents the number of securities required per shift
        min_shifts: An integer indicating the minimum shifts a security has to work in 30 days
        max_shifts: An integer indicating the maximum shifts a security can work in 30 days
    Return:
        lst: A list of allocation for each security for each company for each day and each shift
        None: When no allocation exists or the ford fulkerson is not feasible

    Time complexity:
        Best case analysis: O(m), where m is the number of companies. This occurs when the minimum number of
            securities shifts is bigger than the companies requirement (where there are securities that
            have not been allocated with their min shifts, but the company has matched the requirements already).
            This results in an early termination where there is no need to create the vertex and edge instances.
        Worst case analysis: O(m * n * n), where m is the number of companies and n is the number of securities.
            The worst case complexity of a ford fulkerson is O(VE^2), where V is the number of vertices and E is the
            number of edges. Although for our flow network, E should be approximately V^2, but not in this case,
            where the E will not be V^2 since most of the edges are scaled between the companies and the securities,
            and there is no connection between companies to companies or securities to securities. This ensures that
            the number of edges is dependent on the preferences of the securities, which is why we can see that for
            the edges, it is dominated by the number of securities, n. As for the number of vertices, the dominant
            factor for the number of vertices traversed is the companies themselves as the requirement of the
            companies is what we are trying to fulfill as the demand for the securities. In this case, since the
            dominant factor is the number of companies, the number of vertices visited is scaled by the number of
            companies. This ensures that the worse case time complexity of ford fulkerson lies between O(mnn). Since
            the other operations takes a lesser time complexity where creation of vertices takes O(m+n), creation of
            edges taken O(mn), the feasibility checking takes O(n) and the process of creating the allocation list
            takes O(mn), the worst case complexity will be the dominant one which is O(mnn)


    Space complexity:
        Input space analysis: O(m + n), where m is the number of companies and n is the number of securities.
            Although we have a list in a list for all the companies and securities, but since the internal list is
            a constant value of 3, the complexity will be O(m*3) + O(n*3) = O(3m+3n) = O(m+n)
        Aux space analysis: O(m * n), where m is the number of companies and n is the number of securities.
            This is because after creating the edges between the shifts of the security and the shifts of the
            company, the edges has to be stored in the edges list for each vertex of the shifts of the security.
            Since there will be m*n number of edges in total scaled by a constant of 3 or 30, so the
            auxiliary space complexity remains as O(mn)

    """
    # create a flow network
    flowNetwork = newFlowNetwork(preferences, officers_per_org, min_shifts, max_shifts)

    # check if the conditions of securities meeting the company demands and vice versa
    if flowNetwork.num_of_shift_security > flowNetwork.max_demand_for_30_days:
        return None

    if flowNetwork.pref_count < flowNetwork.sums:
        return None

    # create the allocation list
    lst = []
    for i in range(len(preferences)):
        sec = []
        for j in range(len(officers_per_org)):
            comp = []
            for k in range(flowNetwork.num_of_days):
                day = []
                for l in range(3):
                    day.append(0)
                comp.append(day)
            sec.append(comp)
        lst.append(sec)

    # run the ford_fulkerson
    flowNetwork.ford_fulkerson()

    # check if the flow == capacity for all the edges from the source to securities
    # if it's not, the problem is not feasible and return None
    for i in range(len(flowNetwork.source.edges)):
        if flowNetwork.source.edges[i].flow != flowNetwork.source.edges[i].capacity:
            # print("None")
            return None

    # loop through the security shift list (that has edges from the security to companies) to update the allocation list
    security_num = 0
    day = 0
    for i in range(len(flowNetwork.sec_day_shift)):
        # update the day and security number index after every 30 days and 3 shifts
        if i%(30*3) == 0 and i != 0:
            day = 0
            security_num += 1

        # upfdate the days and shifts
        if i%3 == 0 and i%(30*3) != 0:
            day += 1
        shift_num = i%3

        # loop through each companies and update the list
        for j in range(len(flowNetwork.company)):
            if len(flowNetwork.sec_day_shift[i].edges) != 0:
                # print("Security: ", security_num+1, "Day: ", day+1, "Shift: ", shift_num+1, "Company: ", j+1, "Flow: ", flowNetwork.sec_day_shift[i].edges[j].flow)
                lst[security_num][j][day][shift_num] = flowNetwork.sec_day_shift[i].edges[j].flow

    return lst

if __name__ == "__main__":

    preferences = [[1, 1, 1], [1, 0, 1], [1, 1, 0], [0, 1, 0]]
    officer = [[1, 0, 2], [0, 1, 0]]
    min_shift = 1
    max_shift = 5
    
    print(allocate(preferences, officer, min_shift, max_shift))
    