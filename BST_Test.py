import unittest
from Binary_Search_Tree import Binary_Search_Tree
from Fraction import Fraction

class BSTTester(unittest.TestCase):

    def setUp(self):
        self.__BST = Binary_Search_Tree()
        self.__fraction1 = Fraction(1, 2)
        self.__fraction2 = Fraction(1, 4)
        self.__fraction3 = Fraction(2, 4)

    # Empty BST string representation should be []
    def test_empty_tree(self):
        self.assertEqual('[ ]', str(self.__BST))
        
    # Empty Tree should have a height of 0
    def test_empty_tree_height(self):
        self.assertEqual(0, self.__BST.get_height())
    
    # Empty Tree should have an in-order and pre-order traversal of [] 
    def test_empty_tree_traversal(self):
        self.assertEqual('[ ]', self.__BST.pre_order())
        self.assertEqual('[ ]', self.__BST.in_order())
        self.assertEqual('[ ]', self.__BST.post_order())

    # Insert single element (height , traversal and string representation)
    def test_insert_single_element(self):
        self.__BST.insert_element(10)
        self.assertEqual('[ 10 ]', str(self.__BST)) #string representation should be [10]
        self.assertEqual(1, self.__BST.get_height()) # height of a single element should be 1
        self.assertEqual('[ 10 ]', self.__BST.pre_order())
        self.assertEqual('[ 10 ]', self.__BST.in_order())
        self.assertEqual('[ 10 ]', self.__BST.post_order())

    # Inserting multiple elements and test string representation, traversal and height
    def test_insert_multiple_elements(self):
        self.__BST.insert_element(20)
        self.__BST.insert_element(10)
        self.__BST.insert_element(30)
        self.assertEqual('[ 10, 20, 30 ]', str(self.__BST)) #string representation
        self.assertEqual(2, self.__BST.get_height()) #height
        self.assertEqual('[ 10, 20, 30 ]', self.__BST.in_order()) # in-order traversal
        self.assertEqual('[ 20, 10, 30 ]', self.__BST.pre_order()) # pre_order traversal
        self.assertEqual('[ 10, 30, 20 ]', self.__BST.post_order()) # post_order traversal
    
    #test trees with different heights
    def test_heights(self):
        self.assertEqual(0, self.__BST.get_height()) #empty tree should have a height of 0
        self.__BST.insert_element(20)
        self.assertEqual(1, self.__BST.get_height()) #tree with just the root node should have a height of 1
        self.__BST.insert_element(10)
        self.assertEqual(2, self.__BST.get_height()) #2 nodes should result a height of 2
        self.__BST.insert_element(30)
        self.assertEqual(2, self.__BST.get_height()) #3 nodes should also result in a height of 2
        self.__BST.insert_element(33)
        self.__BST.insert_element(34)
        self.__BST.insert_element(35)
        self.__BST.insert_element(36)
        self.assertEqual(3, self.__BST.get_height())# 7 nodes should result in height of 3
        self.__BST.insert_element(96)
        self.assertEqual(4, self.__BST.get_height()) # 8 nodes should result in a height of 4
        
        
    # insert element not in order and check balance
    def test_insent_not_in_order_check_balance(self):
        self.__BST.insert_element(20)
        self.__BST.insert_element(7)
        self.__BST.insert_element(22)
        self.__BST.insert_element(60)
        self.__BST.insert_element(99)
        self.__BST.insert_element(18) 
        self.assertEqual('[ 7, 18, 20, 22, 60, 99 ]', self.__BST.in_order())
        
    #  remove root node check balance
    def test_remove_root_node_check_balance(self):
        self.__BST.insert_element(20)
        self.__BST.insert_element(7)
        self.__BST.insert_element(22)
        self.__BST.insert_element(60)
        self.__BST.insert_element(99)
        self.__BST.insert_element(18) 
        self.__BST.remove_element(20)
        self.assertEqual('[ 7, 18, 22, 60, 99 ]', self.__BST.in_order())

    # Remove an existing element
    def test_insert_5_remove_1(self):
        self.__BST.insert_element(20)
        self.__BST.insert_element(10)
        self.__BST.insert_element(30)
        self.__BST.insert_element(40)
        self.__BST.insert_element(50)
        self.__BST.remove_element(30)
        self.assertEqual('[ 10, 20, 40, 50 ]', str(self.__BST))

    # Remove non-existent value should raise ValueError
    def test_remove_unexist_value(self):
        self.__BST.insert_element(20)
        with self.assertRaises(ValueError):
            self.__BST.remove_element(30)
        self.assertEqual('[ 20 ]', str(self.__BST))

    # In-order traversal verification
    def test_in_order_traversals(self):
        self.__BST.insert_element(50)
        self.__BST.insert_element(30)
        self.__BST.insert_element(70)
        self.__BST.insert_element(20)
        self.__BST.insert_element(40)
        self.__BST.insert_element(60)
        self.__BST.insert_element(80)
        self.assertEqual('[ 20, 30, 40, 50, 60, 70, 80 ]', self.__BST.in_order())

    # Pre-order traversal verification
    def test_pre_order_traversals(self):
        self.__BST.insert_element(50)
        self.__BST.insert_element(30)
        self.__BST.insert_element(70)
        self.__BST.insert_element(20)
        self.__BST.insert_element(40)
        self.__BST.insert_element(60)
        self.__BST.insert_element(80)
        self.assertEqual('[ 50, 30, 20, 40, 70, 60, 80 ]', self.__BST.pre_order())

    # Post-order traversal verification
    def test_post_order_traversals(self):
        self.__BST.insert_element(50)
        self.__BST.insert_element(30)
        self.__BST.insert_element(70)
        self.assertEqual('[ 30, 70, 50 ]', self.__BST.post_order())

    # Duplicate insertion
    def test_duplicate_insertion(self):
        self.__BST.insert_element(10)
        with self.assertRaises(ValueError):
            self.__BST.insert_element(10)

    # Insert one node and remove it to achieve empty tree
    def test_insert_a_node_and_remove_it(self):
        self.__BST.insert_element(10)
        self.assertEqual('[ 10 ]', self.__BST.in_order())
        self.__BST.remove_element(10)
        self.assertEqual('[ ]', self.__BST.in_order())
        
    # Insert one node and remove it should have height of 0
    def test_insert_a_node_and_remove_it_height(self):
        self.__BST.insert_element(10)
        self.assertEqual(1, self.__BST.get_height())
        self.__BST.remove_element(10)
        self.assertEqual(0, self.__BST.get_height())

    # Remove an element on an empty tree
    def test_remove_on_emptyTree(self):
        with self.assertRaises(ValueError):
            self.__BST.remove_element(1)
        self.assertEqual('[ ]', self.__BST.post_order())

    # Test balancing with AVL property
    def test_AVL_balancing(self):
        self.__BST.insert_element(10)
        self.__BST.insert_element(20)
        self.__BST.insert_element(30)
        self.__BST.insert_element(40)
        self.__BST.insert_element(50)
        self.__BST.insert_element(25)
        self.assertEqual('[ 10, 20, 25, 30, 40, 50 ]', self.__BST.in_order())
        self.__BST.remove_element(20)
        self.assertEqual('[ 10, 25, 30, 40, 50 ]', self.__BST.in_order())


    # Test height after operations
    def test_height_after_operations(self):
        # Insert elements
        self.__BST.insert_element(60)
        self.__BST.insert_element(50)
        self.__BST.insert_element(70)
        self.__BST.insert_element(30)
        self.__BST.insert_element(55)
        self.__BST.insert_element(80)

        # Remove elements
        self.__BST.remove_element(30)
        self.__BST.remove_element(70)
        self.__BST.remove_element(80)

        # Calculate expected height dynamically
        current_height = self.__BST.get_height()

        # Asserting height is within a reasonable range (given AVL balancing)
        self.assertTrue(current_height > 1, f"Height should be greater than 1. Got: {current_height}")
        self.assertTrue(current_height <= 3, f"Height should be less than or equal to 3. Got: {current_height}")
        

    # Testing Fraction comparisons
    def test_less_than_for_Fraction(self):
        self.assertEqual(False, self.__fraction1 < self.__fraction2, 'It should return False because 1/2 is not less than 1/4')

    def test_less_than_for_Fraction2(self):
        self.assertEqual(True, self.__fraction2 < self.__fraction1, 'It should return True because 1/4 is less than 1/2')

    def test_greater_than_for_Fraction(self):
        self.assertEqual(True, self.__fraction1 > self.__fraction2, 'It should return True because 1/2 is greater than 1/4')

    def test_greater_than_for_Fraction2(self):
        self.assertEqual(False, self.__fraction2 > self.__fraction1, 'It should return False because 1/4 is not greater than 1/2')

    def test_equals_for_Fraction(self):
        self.assertEqual(True, self.__fraction1 == self.__fraction3, 'It should return True because 1/2 is equal to 2/4')

    def test_equals_for_Fraction2(self):
        self.assertEqual(False, self.__fraction1 == self.__fraction2, 'It should return False because 1/2 is not equal to 1/4')

if __name__ == '__main__':
    unittest.main()
