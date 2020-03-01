import hashlib


class MerkleTree:
    """
        `The Merkle Tree is a special kind of Binary Tree that allows the user to prevent
        information malleability and preserve integrity by using cryptographically secure
        hash functions. By providing leaves you create a root by concatination and hashingself.
        If the root is mutated it means that the data inside the leaves was changed. You can also
        derive cryptographic proofs that a piece of data is inside the tree`

        Comments:
           Complexities - This part can be improved by doing couple of modifications
    """


    class __Node:

        def __init__(self, item=None, left=None, right=None):
            """
            `Merkle Node constructor. Used for storing the left and right node pointersself.`

            Args:
                item (bytes): Bytes object that represents the hashed value that resides in the current node
                left (Node): Reference to the left subtree or a None value if current node is leaf
                right (Node): Reference to the right subtree or a None value if current node is leaf
            """
            self.left = left
            self.right = right
            self.__value = item

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, value):
            self.__value = value

        def __str__(self):
            return 'Value: {0}'.format(self.value)

        def __repr__(self):
            return self.__str__() + '\n\t' + self.left.__repr__() + '\n\t' + self.right.__repr__()


    def __init__(self,
                 iterable,
                 digest_delegate=lambda x: str(x)):
        """
            `Merkle Tree constructor`

            Args:
                iterable (list_iterator): The collection you want to create the root from
                digest_delegate (function): ~
                  ~ A delegate (reference to function) that returns the digest of a passed in argument
        """
        self.digest = digest_delegate
        self.__root = self.build_root(iterable)

    @property
    def root(self):
        return self.__root



    def build_root(self, iterable):
        """
            `This method builds a Merkle Root from the passed in iterable.
             After the data is preprocessed, it calls the internal __build_root
             function to build the actual Merkle Root.`

            Args:
                iterable (list_iterator): The collection you want to create the root from

            Returns:
                Node: The newly built root of the Merkle Tree
        """
        # TODO: Implement this method
        # Try implementing this method yourself


        # When size is 1 the root is the only node that is left


        # Double the last node if the size is odd


        # Iterate over the collection and create the upper layers till the root is reached
        # Keep references for each node to its children


        # Return the root

        collection = list(iterable)

        assert(len(collection) != 0)

        if len(collection) % 2 != 0:
            collection.extend(collection[-1:])

        collection = [self.__Node(self.digest(x)) for x in collection]

        return self.__build_root(collection)

    def __build_root(self, collection):

        size = len(collection)
        if size == 1:
            return collection[0]

        if size % 2 != 0:
            collection.append(self.__Node(collection[-1].value, left=collection[-1].left, right=collection[-1].right))

        next_level = []


        i = 0
        while i < size:
            if isinstance(collection[i], self.__Node):
                digest = self.digest(collection[i].value + collection[i+1].value)
                node = self.__Node(digest, left=collection[i], right=collection[i+1])
                next_level.append(node)

            else:
                hashed_left = self.digest(collection[i])
                hashed_right = self.digest(collection[i+1])
                digest = self.digest(hashed_left.value + hashed_right.value)
                node = self.__Node(digest, None, None)
                next_level.append(node)
            i += 2

        return self.__build_root(next_level)

    def contains(self, value):
        """
            `The contains method checks whether the item passed in as an argument is in the
            tree and returns True/False. It is used only externally. It's internal equivalent
            is __find`

            Args:
                value (object): The value you are searching for

            Returns:
                bool: The result of the search

            Complexity:
                O(n)
        """
        if value is None or self.root is None:
            return False

        hashed_value = self.digest(value)

        return self.__find(self.root, hashed_value) is not None


    def __find(self, node, value):
        """
            `Find is the internal equivalent of the contains method`

            Args:
                value (object): The value you are searching for

            Returns:
                bool: The result of the search

            Complexity:
                O(n)
        """
        if node is None:
            return None

        if node.value == value:
            return node

        return self.__find(node.left, value) or self.__find(node.right, value)

    def request_proof(self, value):
        """
            `The request_proof method provides to the caller a merkle branch in order to prove
            that the integrity of the data is in tact. The caller can use the same digest and
            verify it himself`

            Args:
               value (object) - The item you want proof for

            Returns:
               list - Python list containing the merkle branch (proof) in the form of tuples

            Throws:
                Exception - On invalid value or one that is not contained in the tree
        """
        # TODO: Implement this method
        # Try implementing this method yourself. It is not mandatory though. There is a
        # step by step solution in the exercise document

        # Hash the value

        # Check if it is contained within the tree

        # Start building the proof

        # Traverse left and right to find the correct leaf node

        # If the leaf was found in the left subtree -> add the right node to the proof list

        # If it was both found on the left and on the right -> it means that left and right values are identical
        # Do not add to the list

        # Create tuple with the node value and the position it was found on
        # 0 for right node and 1 for left node e.g (1, node.left)

        # Append to the list

        hashed_value = self.digest(value)

        if self.__find(self.root, hashed_value) is None:
            raise Exception('This argument is not contained in the tree.')

        proof = []
        self.__build_valid_proof(self.root, hashed_value, proof)

        if len(proof) != 0:
            proof.insert(0, (0 if proof[1][0] else 1, hashed_value))

        return proof


    def __build_valid_proof(self, node, value, proof_list):
        if node is None:
            return False

        if node.value == value:
            return True

        found_left = self.__build_valid_proof(node.left, value, proof_list)
        found_right = self.__build_valid_proof(node.right, value, proof_list)

        if not found_left and not found_right:
            return False

        if found_left and found_right and (0, node.left.value) in proof_list:
            return False

        n = (0, node.right.value) if found_left else (1, node.left.value)

        proof_list.append(n)

        return True


    def dump(self, indent=0):

        if self.root is None:
            return

        self.__print(self.root, indent)

    def __print(self, node, indent):

        if node is None:
            return

        print('{0}Node: {1}'.format(' '*indent, node.value))
        self.__print(node.left, indent+2)
        self.__print(node.right, indent+2)

    def __contains__(self, value):
        hashed_value = self.digest(value)
        return self.__find(self.root, hashed_value)

    """
    def build_root(self, iterable):

        collection = list(iterable)

        assert(len(collection) != 0)

        if len(collection) % 2 != 0:
            collection.append(collection[-1])

        collection = [self.__Node(self.digest(x)) for x in collection]

        return self.__build_root(collection)

    def __build_root(self, collection):

        size = len(collection)
        if size == 1:
            return collection[0]

        if size % 2 == 0:
            collection.append(self.__Node(collection[-1].value, left=collection[-1].left, right=collection[-1].right))

        next_level = []

        for i in range(0, size - 1, 2):
            digest = self.digest(collection[i].value + collection[i+1].value)
            node = self.__Node(digest, left=collection[i], right=collection[i+1])
            next_level.append(node)

        return self.__build_root(next_level)

    """
