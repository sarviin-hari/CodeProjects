"""
SARVIIN A/L HARI
32885741
Version 3
"""
import math

# ==========
# Search for substring between start and end with Suffix Trie

class Node:
    def __init__(self, data=None, level=None):
        """
        This is an __init__ method to define the internal structure of a Node instance with a list to indicate the
            next direct branch (Leaf/A/B/C/D) from the Node and also a list to store all the index of the current
            branches that can be branched from that node.

        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - Initialize a list of size 5, where the subsequent linking nodes can be stored
            - Initialize an empty list that stores index of the branches from the current node

        Input
            data: A char value that indicates the identity of the node
            level: An integer indicating the depth of the node level
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the operation involves the assignment of instance variables with the inputs
                and initialization of a list of a fixed size of 5 with a complexity of O(5) = O(1)
            Worst case analysis: O(1), where the operation involves the assignment of instance variables with the inputs
                and initialization of a list of a fixed size of 5 with a complexity of O(5) = O(1)

        Space complexity:
            Input space analysis: O(1), where the input consists of a char and a string which has a complexity of O(1)
            Aux space analysis: O(1), where the auxiliary space is used for initialization of a list of a fixed size of
                5 with a complexity of O(5) = O(1)
        """
        self.node_size = 5
        self.link = [None] * self.node_size
        # stores the char of node
        self.data = data

        # stores the index of the current node based on original suffix
        self.index_of_element = None
        self.index = None

        # stores the index of branches on the current node
        self.down_branch = []

        # level of the node
        self.level = level

    # def __str__(self):
    #     return "(" + str(self.data) + ", " + str(self.index_of_element)+ ", " + str(self.index) + ")"

    # def __repr__(self):
    #     return "(" + str(self.data) + ", " + str(self.index_of_element)+ ", " + str(self.index) + ")"

class Trie:
    def __init__(self, ori_string, reverse=False):
        """
        This is an __init__ method to define the internal structure of a Trie that stores an instance of a Node which
            is a root Node and the state of the trie (forward / reverse) to indicaate how the internal structure of
            insert operation works.

        Written by Sarviin Hari (32885741)

        Precondition:
            - The state of the current Trie (reverse or forward) has to be indicated peoperly
        Postcondition:
            - a root instance is cerated with a Node class

        Input
            ori_string: A string value that indicates the string for the suffix trie
            reverse: A boolean value indicating if the suffix trie is normal or reverse suffix
        Return:
            None

        Time complexity:
            Best case analysis: O(1), where the operation involves the assignment of instance variables with the inputs
                and initialization of a Node instance with a complexity of O(1)
            Worst case analysis: O(1), where the operation involves the assignment of instance variables with the inputs
                and initialization of a Node instance with a complexity of O(1)

        Space complexity:
            Input space analysis: O(1), where the input consists of a boolean and string which has a complexity of O(1)
            Aux space analysis: O(1), where the auxiliary space is used for initialization of instance variables and a
                Node instance with a complexity of O(1)
        """
        self.root = Node()  # an empty node as the root

        self.reverse = reverse  # boolean value to determine if its for

        self.genome = ori_string

        self.genome_max_index = len(self.genome) - 1  # last index

    def insert_recur(self, index):
        """
        This is a insert recursive call method that sets the current value to be the root instance and calls the
            auxiliary recursive function with the base case being the current index matching the last index of the
            genome and the recurrence relation being the subsequent recursive call to the next node based on the
            order of the char in the genome string. If the base case is not met, the index of the next node is
            obtained based on the char value and if the index has no element, a new element is created, the current
            is resetted to the new node and stored in the index and the index of the current char is resetted. If
            the index has an element the current is resetted to the next node. Next I will append the index of the
            char into to the corresponding node visited or created and call the recursive call on the new current
            while increasing the current index by 1

        Written by Sarviin Hari (32885741)

        Precondition:
            - The index value is an integer indicating the subsequent index of the genome where the index will be
                between 0 and len(genome)
        Postcondition:
            - The suffix from the starting index inputted to the end of the string is added to the suffix trie

        Input
            index: An integer indicating the index that the suffix has to start from
        Return:
            None


        Time complexity:
            Best case analysis: Same as the worse case complexity
            Worst case analysis: O(N), where N is the length of the genome string to be added to the suffix trie (from
                the index value, until the end of the genome string). This is because, the recursive adding of the
                elements into the suffix trie for each node instance only takes a time complexity of O(1) as the
                operations involved are only if checks, appending value into a list, or mathematical operations which
                takes O(1) complexity. Thus, since the recursion runs N times (the length of genome), O(N)*O(1)
                will give a complexity of O(N)

            Worst case analysis after completion of addition of all suffix of genome in suffix trie:
                O(N^2), where N is the length of the genome string. This is because to create a suffix trie, all the
                suffixes of the current string, genome, has to be added to the trie. For a genome of length, N, there is
                N possible suffixes that has to be traversed and added to the suffix trie. The complexity of adding a
                single suffix to the trie takes O(N) complexity, where N is the length of the genome string to be added
                to the suffix trie (from the index value, until the end of the genome string). Since we have to add N
                suffixes and adding a suffix has a complexity of O(N), the total complexity of adding all suffixes to
                the trie will be O(N)*O(N) = O(N^2)

        Space complexity:
            Input space analysis: O(1), where the input consists of index as an integer with complexity of O(1)
            Aux space analysis: O(N), where N is the length of the genome string to be added to the suffix trie (from
                the index value, until the end of the genome string). This is because upon the addition of a suffix
                to the suffix trie the index of the current suffix node will be appended into the nodes visited or
                created when traversing through the length of the genome string which increases the dimension of the
                list by N

            Aux space analysis after completion of addition of all suffix of genome in suffix trie:
                O(N^2), where N is the length of the genome string. This is because upon adding each suffix, to
                the suffix trie, the index of the current suffix node is appended into the nodes visited or created. The
                number of possible elements that has to be appended to the lists in total given the length of the genome
                goes from N to N-1 to N-2 ... 1 for each iteration will be O(N) and the subsequent iteration will be
                O(N-1), O(N-2), ... O(1). So we calculate the complexity using the formula O(N)*O(N-1)*O(N-2) ... O(1),
                which can test_given_cases simplified to O(N^2)
        """
        curr = self.root  # set current to root
        ini_index = index
        key_index = index
        self.aux_insert_recur(curr, ini_index, key_index)  # call teh recursive aux function

    def aux_insert_recur(self, current, ini_index, key_index):
        """
        This is a aux recursive call method with the base case being the current index matching the last index of the
            genome and the recurrence relation being the subsequent recursive call to the next node based on the
            order of the char in the genome string. If the base case is not met, the index of the next node is
            obtained based on the char value and if the index has no element, a new element is created, the current
            is resetted to the new node and stored in the index and the index of the current char is resetted. If
            the index has an element the current is resetted to the next node. Next I will append the index of the
            char into to the corresponding node visited or created and call the recursive call on the new current
            while increasing the current index by 1

        Written by Sarviin Hari (32885741)

        Precondition:
            - The current must be a node instance or None
        Postcondition:
            - The suffix from the starting index inputted to the end of the string is added to the suffix trie

        Input
            current: A node instance for the current node that is being visited
            ini_index: An integer indicating the current index for the node in the suffix trie
            key_index: An integer indicating the initial index (the starting index value of the genome)
        Return:
            None

        Time complexity:
            Best case analysis: Same as the worse case complexity
            Worst case analysis: O(N), where N is the length of the genome string to be added to the suffix trie (from
                the index value, until the end of the genome string). This is because, the recursive adding of the elements into the suffix trie
                for each node instance only takes a time complexity of O(1) as the operations involved are only
                if checks, appending value into a list, or mathematical operations which takes O(1) complexity. Thus,
                since the recursion runs N times (the length of genome), O(N)*O(1) will give a complexity of O(N)

            Worst case analysis after completion of addition of all suffix of genome in suffix trie:
                O(N^2), where N is the length of the genome string. This is because to create a suffix trie, all the
                suffixes of the current string, genome, has to be added to the trie. For a genome of length, N, there is
                N possible suffixes that has to be traversed and added to the suffix trie. The complexity of adding a
                single suffix to the trie takes O(N) complexity, where N is the length of the genome string to be added
                to the suffix trie (from the index value, until the end of the genome string). Since we have to add N
                suffixes and adding a suffix has a complexity of O(N), the total complexity of adding all suffixes to
                the trie will be O(N)*O(N) = O(N^2)


        Space complexity:
            Input space analysis: O(1), where the input consists of a node instance and integer with complexity of O(1)
            Aux space analysis: O(N), where N is the length of the genome string to be added to the suffix trie (from
                the index value, until the end of the genome string). This is because upon the addition of a suffix
                to the suffix trie the index of the current suffix node will be appended into the nodes visited or
                created when traversing through the length of the genome string which increases the dimension of the
                list by N

            Aux space analysis after completion of addition of all suffix of genome in suffix trie:
                O(N^2), where N is the length of the genome string. This is because upon adding each suffix, to
                the suffix trie, the index of the current suffix node is appended into the nodes visited or created. The
                number of possible elements that has to be appended to the lists in total given the length of the genome
                goes from N to N-1 to N-2 ... 1 for each iteration will be O(N) and the subsequent iteration will be
                O(N-1), O(N-2), ... O(1). So we calculate the complexity using the formula O(N)*O(N-1)*O(N-2) ... O(1),
                which can test_given_cases simplified to O(N^2)
        """
        # base case when the length of the string = the index of the genome after every recursion
        if len(self.genome) == ini_index:
            return

        else:
            char = self.genome[ini_index]
            index = ord(char) - 65 + 1  # to accommodate terminal at first index

            # if current path exists, change the current to the next based on the char,
            if current.link[index] is not None:
                current = current.link[index]
                node = current
            # else create path - create new Node,  change the current to the new node based on the char
            else:
                node = Node(data=char, level=ini_index - key_index + 1)
                current.link[index] = node
                current = current.link[index]

                # set the current index of the node
                if self.reverse:
                    current.index_of_element = self.genome_max_index - ini_index
                else:
                    current.index_of_element = ini_index

            # append the index into the list in each node
            if self.reverse:
                # print(char, self.genome_max_index - ini_index, key_index)
                node.down_branch.append(self.genome_max_index - ini_index)
            else:
                # print(char, ini_index, key_index, node, node.index, node.down_branch)
                node.down_branch.append(ini_index)

            ini_index += 1

            # recursively call the function again
            self.aux_insert_recur(current, ini_index, key_index)

            return

    def rev_search(self, reverse_end):
        """
        This is an reverse search of end string method, where the code will traverse through each char in the end string
            and get the node instance of the first char of the end string. If no such Node exists in the suffix trie
            None is returned suggesting such end string representation is not valid

        Written by Sarviin Hari (32885741)

        Precondition:
            - The reverse suffix trie has already been initialized
        Postcondition:
            - The node of the start of end string is returned or None is returned if no such Node exist for the char

        Input
            reverse_end: A string which is the end of the genome required for searching
        Return:
            current: An instance of a Node that refers to the first char of the reverse_end string
            None: A None value indicating such end string does not exist in the suffix trie

        Time complexity:
            Best case analysis: O(1), when the first char of the  end string does not exist in the root node
                thus no traversal is required
            Worst case analysis: O(U), where U is the length of the end string. This is because the for loop in this
                code that traverse through the elements from the root of the reversed genome suffix trie will traverse
                from the last char to the end char of the end string which has a length of U at the worst case ensuring
                the complexity is maintained

        Space complexity:
            Input space analysis: O(U), where U is the length of the end string.
            Aux space analysis: O(1), where the auxiliary space is used for initialization of variables to store the
                Node instance which has a complexity of O(1)

        """
        # loop through from root to the node where the reversed end string matches and get the node on the suffix trie
        # if such string does not exist return None
        current = self.root
        for char in reverse_end:
            index = ord(char) - 65 + 1  # to accommodate terminal at first index
            # print(char, current.link, current.index_of_element)
            if current.link[index] is not None:
                current = current.link[index]
            else:
                # print("Cut off one")
                return None

        # if the current value is None, return None else return current
        if current is not None:
            return current
        else:
            # print("Cut off two")
            return None

    def front_search(self, start, end, end_val):
        """
        This is a front search of start string method and traversal to find all possible combinations of strings that
            start as the prefix and end as the suffix provided. First a forward search is done where the code will
            traverse through each char in the start string and get the node instance of the last char of the start
            string. If no such Node exists in the suffix trie an empty list is returned indicating no such combination
            exists. Next when both the start and end exists we will get the list of branches of nodes from the
            node of the start trie and end trie to find all the possible combinations of substring as long as the
            start index < end index

        Written by Sarviin Hari (32885741)

        Precondition:
            - The suffix trie has already been initialized
        Postcondition:
            - The suffix trie must not be altered
            - All possible combinations of strings between start and end is returned in a list

        Input
            start: A string value for the start of the genome required
            end: A string value for the end of the genome required
            end_val: A node instance of the last
        Return:
            ret_lst: A list of strings of all possible combinations of the substring from the start of prefix to end of
                suffix
            []: n empty list when the start or the ned or both strings do not exist

        Time complexity:
            Best case analysis: O(1). The best case complexity occurs when the start string does not exist in the root
                of suffix trie, thus, an empty list will be returned with no traversal required
            Worst case analysis: O(T + V) where T is the length of the start string and V is the number of
                characters in the output list, where for loop in this code traverse through the elements from the
                root of the genome suffix trie will traverse from the first char to the end char of the start string
                which has a length of T.

                Next, the second for loop will traverse through the start_list, which consists of the indexes of the
                branches from the end of the start char's node and the end_list, which consists of the indexes of the
                branches from the start of the end char's node. So, the for loop in a for loop will traverse through
                each possible combinations of start and end string and store the all possible string within the start
                and end strings in the list where the length of traversal, K , is the substring in between the start
                and end string for each possible combinations. Thus this results in the complexity being V where V is
                the length of all possible substrings between the start and end strings. In the worse case where for
                the start and end strings the code has to traverse through all possible combinations of start to end,
                the complexity of V = O(N^2), where the traversal has to go through N^2 possible combinations of genomes
                (i.e. genome = N/2*A's and N/2*B's and given the start string is A and end string is B, for each
                possible genomes all A's has to be traversed for all the B's which goes up to O(N^2))


        Space complexity:
            Input space analysis: O(T + U), where T is the length of the start string and U is the length of the
                end string
            Aux space analysis: O(V), where V is the sum of the number of char in the list of the return substrings
                for all combinations from the start string and the end string.  This is because the size of the
                output list is scaled based on the length of all the return substring of the genome's start and end.
                In that case in the worse scenario the aux space will be O(N^2), N is the length of the initial genome
                string. This is because, when there is repetition of single values >= N/2 times for either the start or
                the end string or both, the number of output required will increase to N^2 possible combination for the
                traversal required to traverse from all the indexes of the start string from the first occurrence to
                the last occurrence of the end string which makes the number of string elements to be stored in the
                list to increase to N^2. This results in all possible combinations of start to end, to be V = O(N^2),
                which requires a list of length of O(N^2) in the worst case. In best case where the start and end
                string does not exist, no traversal is required and an empty list is returned resulting in a complexity
                of O(1)

        """
        # loop through from root to the node where the start string matches and get the node on the suffix trie
        # if such string does not exist return None
        current = self.root
        for char in start:
            index = ord(char) - 65 + 1  # to accommodate terminal at first index
            if current.link[index] is not None:
                current = current.link[index]
            else:
                # print("Cut off three")
                return []

        start_list = current.down_branch
        end_list = end_val.down_branch

        ret_lst = []

        # for each of the elements in the start_list and for each of the element in the end list, as long as the
        # start_index < end_index, there exists a substring and add the substring in the list
        for i in range(len(start_list)):
            # print("Loop " + str(i+1))
            for j in range(len(end_list)):
                # print("Traversal")
                if start_list[i] >= end_list[j]:
                    break
                # print(" ", start_list[i], end_list[j])
                string = ""
                for k in range(start_list[i]+1, end_list[j]):
                    string += self.genome[k]
                    # print("   ", self.genome[k])
                ret_lst.append(start + string + end)

        return ret_lst


class OrfFinder:
    def __init__(self, genome):
        """
        This is an __init__ method to define the creation of 2 suffix tries where the first suffix trie is of the normal
            order of the genome and the second suffix trie is of the reversed order of the genome.  To create the suffix
            tries I will create an instance of trie with normal mode and reverse mode and loop through each possible
            combinations of genome suffix to recursively add the strings into the trie

        The approach I am planning to use for this assignment is to create 2 suffix trie. The first suffix trie will be
            all the suffixes of the string genome from the start to the end of the string where the string genome is in
            normal order. The second suffix trie will be the reverse suffix trie of all the suffixes of the reversed
            string of genome from the start to the end of the reversed string of genome where the string genome is in
            the reversed order. While the creation of the suffix trie, the indexes of the suffixes passing through each
            branch is appended into the list to ensure that all the branches stemming from the current node is stored.
            With both these suffix trees, first I will traverse through the start string to get the node of the end of
            the start sting with the normal suffix and also traverse through the end string to get the node of the start
            of the end sting with the reversed suffix. Both these nodes will give me the possible starting branches and
            ending branches for each of the possible combinations of start and ends. With these lists, I can traverse
            through all possible combinations of start and end (given that the start <= end) to get the K string which
            is the strings in between of start and end for all possible combinations and add them to the list to be
            returned

        Written by Sarviin Hari (32885741)

        Precondition:
            - None
        Postcondition:
            - 2 suffix tries created one of normal order of the genome and the second is of the reversed order of the
            genome

        Input
            genome: A string value the initial genome in normal order
        Return:
            None

        Time complexity:
            Best case analysis: Same as the worse case complexity
            Worst case analysis: O(N^2), where N is the length of the genome string. This is because to create a suffix
                trie, all the suffixes of the current string, genome, has to be added to the trie. For a genome of
                length, N, there is N possible suffixes that has to be traversed and added to the suffix trie. The
                complexity of adding a single suffix to the trie takes O(N) complexity, where N is the length of the
                genome string to be added to the suffix trie (from the index value, until the end of the genome string).
                Since we have to add N suffixes and adding a suffix has a complexity of O(N), the total complexity of
                adding all suffixes to the trie will be O(N)*O(N) = O(N^2)

        Space complexity:
            Input space analysis: O(N), where N is the length of the string genome
            Aux space analysis: O(N^2), where N is the length of the genome string. This is because upon adding each
                suffix, to the suffix trie, the index of the current suffix node is appended into the nodes visited or
                created. The number of possible elements that has to be appended to the lists in total given the length
                of the genome goes from N to N-1 to N-2 ... 1 for each iteration will be O(N) and the subsequent
                iteration will be O(N-1), O(N-2), ... O(1). So we calculate the complexity using the formula
                O(N)*O(N-1)*O(N-2) ... O(1), which can be simplified to O(N^2)

        """
        self.genome = genome

        # create a suffix trie for the string genome
        self.trie = Trie(genome)
        for i in range(len(genome)):
            self.trie.insert_recur(i)

        # reverse the string genome
        string = ""
        for i in range(len(genome)-1, -1, -1):
            string += genome[i]

        # create a suffix trie for the reversed string of genome
        self.trie_rev = Trie(string, reverse=True)
        for i in range(len(string)):
            self.trie_rev.insert_recur(i)

    def find(self, start, end):
        """
        This is a find method to find the list of all possible substrings of the start and the end. For that we will
            first get the node of the start of the end string form the reverse suffix trie and the end of the start
            string from the forward suffix trie. Then from the nodes I will get all the possible branches from the
            current node for start and end and traverse through each possible branch combination ofn start and end
            to get the substrings as long as the start index < end index

        The approach I am planning to use for this assignment is to create 2 suffix trie. The first suffix trie will be
            all the suffixes of the string genome from the start to the end of the string where the string genome is in
            normal order. The second suffix trie will be the reverse suffix trie of all the suffixes of the reversed
            string of genome from the start to the end of the reversed string of genome where the string genome is in
            the reversed order. While the creation of the suffix trie, the indexes of the suffixes passing through each
            branch is appended into the list to ensure that all the branches stemming from the current node is stored.
            With both these suffix trees, first I will traverse through the start string to get the node of the end of
            the start sting with the normal suffix and also traverse through the end string to get the node of the start
            of the end sting with the reversed suffix. Both these nodes will give me the possible starting branches and
            ending branches for each of the possible combinations of start and ends. With these lists, I can traverse
            through all possible combinations of start and end (given that the start <= end) to get the K string which
            is the strings in between of start and end for all possible combinations and add them to the list to be
            returned

        Written by Sarviin Hari (32885741)

        Precondition:
            - 2 suffix tries created one of normal order of the genome and the second is of the reversed order of the
            genome
        Postcondition:
            - A list of all possible string combinations is returned

        Input
            start: A string value for the start of the genome required
            end: A string value for the end of the genome required
        Return:
            A list of all possible combinations of strings between teh start and end of the genome
            An empty list when there is no combinations of genome for start and end exist

        Time complexity:
            Best case analysis: O(U), where U is the length of the end string. The best case complexity occurs
                when the start string does not exist in the suffix trie and the end string does not exist in the reverse
                suffix trie's root from first char itself which ensures that there is no traversal required to search
                for the node instance and an empty list will be returned. Since no traversal required at all, constant
                complexity remains for the traversal and since we have to reverse the list at any cost at the start,
                this takes a complexity of the length of the end string, U
            Worst case analysis: O(T+U+V), where T is the length of the start string, U is the length of end string,
                and V is the sum of the number of char in the list of the return substrings
                for all combinations from the start string and the end string, where the code will traverse through
                the start string and end strings to get their index list and traverse through V possible number of
                strings to create a list of strings.  The worse case scenario occurs when
                the start and end strings the code has to traverse through all possible combinations of start to end,
                the complexity of V = O(N^2), where the traversal has to go through N^2 possible combinations of genomes
                (i.e. genome = N/2*A's and N/2*B's and given the start string is A and end string is B, for each
                possible genomes all A's has to be traversed for all the B's which goes up to O(N^2))

        Space complexity:
            Input space analysis: O(T+U), where T is the length the start string and U is the length of the end string
            Aux space analysis: O(V), where V is the sum of the number of char in the list of the return substrings
                for all combinations from the start string and the end string.  This is because the size of the
                output list is scaled based on the length of all the return substring of the genome's start and end.
                In that case in the worse scenario the aux space will be O(N^2), N is the length of the initial genome
                string. This is because, when there is repetition of single values >= N/2 times for either the start or
                the end string or both, the number of output required will increase to N^2 possible combination for the
                traversal required to traverse from all the indexes of the start string from the first occurrence to
                the last occurrence of the end string which makes the number of string elements to be stored in the
                list to increase to N^2. This results in all possible combinations of start to end, to be V = O(N^2),
                which requires a list of length of O(N^2) in the worst case. In best case where the start and end
                string does not exist, no traversal is required and an empty list is returned resulting in a complexity
                of O(1)

        """
        # Reverse the string of end
        end_string = ""
        for i in range(len(end)-1,-1,-1):
            end_string += end[i]

        # get the latest node of the current
        curr = self.trie_rev.rev_search(end_string)

        # if the end node doesn't exist, return empty list
        if curr is None:
            return []

        # traverse from the start to all possible ends to get the strings
        return self.trie.front_search(start, end, curr)

if __name__ == "__main__":
    genome = OrfFinder('CCDDBBACABBBBBCDC')
    assert sorted(genome.find('B', 'A')) == sorted(['BA', 'BACA', 'BBA', 'BBACA'])
    genome = OrfFinder('ACBBCCCBBAABDCCBDDAC')
    assert sorted(genome.find('D', 'C')) == sorted(['DAC', 'DC', 'DCC', 'DCCBDDAC', 'DDAC'])
