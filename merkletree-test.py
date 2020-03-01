import hashlib
import unittest
import merkletree

class MerkleTest(unittest.TestCase):
    
    @unittest.expectedFailure
    def test_unable_to_build_from_empty_collection(self):
        tree_fail = merkletree.MerkleTree([])
        self.assertIsNone(tree_fail) # This is only for the linter :()

    def test_merkle_no_digest(self):
        
        tree_even = merkletree.MerkleTree([1,2,3,4,5,6])
        tree_odd = merkletree.MerkleTree([1,2,3,4,5])
        
        even_error_feedback = \
            'Incorrect root: Expected - {0}, Received - {1}'.format('12345656', tree_even.root.value)
        odd_error_feedback = \
            'Incorrect root: Expected - {0}, Received - {1}'.format('12345555', tree_odd.root.value)

        self.assertEqual(tree_even.root.value, '12345656', even_error_feedback)
        self.assertEqual(tree_odd.root.value, '12345555', odd_error_feedback)
        
    def test_merkle_with_cryptographic_digest(self):
        
        even_sequence = ['tx1', 'tx2', 'tx3', 'tx4']
        odd_sequence = [1, 2, 3, 8, 9, 9, 9, 9]

        def H(element):
            H = hashlib.sha256()

            if type(element) == str:
                H.update(element.encode('utf-8'))
            elif type(element) == int:
                H.update(bytes([element]))
            else:
                H.update(element)

            return H.digest()    

        tree_even = merkletree.MerkleTree(even_sequence, digest_delegate=H)
        tree_odd = merkletree.MerkleTree(odd_sequence, digest_delegate=H)

        even_digest = [H(x) for x in even_sequence]
        odd_digest = [H(x) for x in odd_sequence]

        root_even = H(H(even_digest[0] + even_digest[1]) + H(even_digest[2] + even_digest[3]))

        root_odd_left = H(H(odd_digest[0] + odd_digest[1]) + H(odd_digest[2] + odd_digest[3]))
        root_odd_right = H(H(odd_digest[4] + odd_digest[5]) + H(odd_digest[6] + odd_digest[7]))
        root_odd = H(root_odd_left + root_odd_right)
        
        even_error_feedback = \
            'Incorrect root: Expected - {0}, Received - {1}'.format(root_even, tree_even.root.value)
        odd_error_feedback = \
            'Incorrect root: Expected - {0}, Received - {1}'.format(root_odd, tree_odd.root.value)

        self.assertEqual(tree_even.root.value, root_even, even_error_feedback)
        self.assertEqual(tree_odd.root.value, root_odd, odd_error_feedback)


if __name__ == '__main__':
    unittest.main(verbosity=2)