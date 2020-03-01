import hashlib
import unittest
import merkletree


class MerkleProofTest(unittest.TestCase):

    def setUp(self):
        
        def H(element):
            H = hashlib.sha256()
            if type(element) == str:
                H.update(element.encode('utf-8'))
            elif type(element) == int:
                H.update(bytes([element]))
            else:
                H.update(element)
            return H.digest()

        self.H = H
        self.tree = merkletree.MerkleTree(["somedata", "trx1", "trx2", "trx4", "trx5"], digest_delegate=H)

    
    def test_merkle_should_contain_items(self):
        should_be_true = self.tree.contains("somedata")
        should_be_false = "non-existing data" in self.tree
        
        self.assertFalse(should_be_false)
        self.assertTrue(should_be_true)

    def test_merkle_should_return_correct_proof_when_leaf_is_left_child(self):
        
        proof_branch = self.tree.request_proof("trx4")
        
        root = self.tree.root.value
        root_from_proof_branch = self.__build_root(proof_branch)

        on_error = "The proof you provided was invalid. Expected: {0}, Got: {1}" \
            .format(root, root_from_proof_branch)

        self.assertEqual(root, root_from_proof_branch, on_error)

    def test_merkle_should_return_correct_proof_when_leaf_is_right_child(self):

        proof_branch = self.tree.request_proof("trx1")

        root = self.tree.root.value
        root_from_proof_branch = self.__build_root(proof_branch)

        on_error = "The proof you provided was invalid. Expected: {0}, Got: {1}" \
            .format(root, root_from_proof_branch)

        self.assertEqual(root, root_from_proof_branch, on_error)

    def test_merkle_should_return_correct_proof_on_edge_case(self):
        proof_branch = self.tree.request_proof("trx5")
        root = self.tree.root.value
        root_from_proof_branch = self.__build_root(proof_branch)

        on_error = "The proof you provided was invalid. Expected: {0}, Got: {1}" \
            .format(root, root_from_proof_branch)

        self.assertEqual(root, root_from_proof_branch, on_error)    

    @unittest.expectedFailure
    def test_merkle_should_throw_on_requesting_proof_for_non_existing_element(self):
        proof_branch = self.tree.request_proof("I have to raise an exception here")

    def __build_root(self, collection, left_child=True):
        """
            `__build_root is used as an internal recursive call to compute
            the root of the tree using the data that was provided as an argument`

            Args:
                collection (list): The hashed collection of items that you we will use for the root
        """

        size = len(collection)

        # When size is 1 the root is the only node that is left
        if(size == 0):
            raise Exception()

        result = collection[0][1]

        for i in range(1, size):
            left_child = collection[i][0]
            val = collection[i][1]
            result = self.H(val + result) if left_child else self.H(result + val)

        return result

if __name__ == '__main__':
    unittest.main(verbosity=2)