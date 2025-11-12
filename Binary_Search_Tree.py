class Binary_Search_Tree:
    class __BST_Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.__root = None

    # Helper function to update node height
    # Time Complexity: O(1), because it calculates the height of a node by directly accessing 
    # the heights of its left and right children, which are stored as attributes.
    def __update_height(self, node):
        if node is None:
            return 0
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        node.height = max(left_height, right_height) + 1

    # Helper function to get the balance factor
    # Time Complexity: O(1), because it directly calculates the balance factor by accessing 
    # the heights of the left and right children, which are stored as attributes.
    def __get_balance(self, node):
        if not node:
            return 0
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height

    # Time Complexity: O(log(n)), because the insertion involves a traversal down the height
    # of the AVL tree (which is balanced and has height log(n)), and balancing operations are O(1).
    def insert_element(self, value): 
        self.__root = self.__recursive_insert(self.__root, value)

    # Private recursive insertion helper method
    # Time Complexity: O(log(n)), because the method recursively traverses the height of the AVL tree
    # to find the correct position for the new value. Since the AVL tree is balanced, its height is O(log(n)).
    # Each comparison and assignment operation during traversal is O(1).
    def __recursive_insert(self, node, value):
        if node is None:
            return self.__BST_Node(value)
        if value < node.value:
            node.left = self.__recursive_insert(node.left, value)
        elif value > node.value:
            node.right = self.__recursive_insert(node.right, value)
        else:
            raise ValueError("Duplicate values are not allowed.")

        # Update height of the current node
        self.__update_height(node)

        # Balance the node if needed
        return self.__balance(node)

    # Time Complexity: O(log(n)), because the method calls __recursive_remove, which traverses
    # the height of the AVL tree to locate the node to be removed. Since the AVL tree is balanced,
    # the height of the tree is O(log(n)).
    def remove_element(self, value): 
        self.__root = self.__recursive_remove(self.__root, value)

    # Private recursive removal helper method
    # Time Complexity: O(log(n)), because the method traverses the height of the AVL tree to locate 
    # the node to be removed, which takes O(log(n)) in a balanced tree. 
    def __recursive_remove(self, node, value):
        if node is None:
            raise ValueError("Value not found.")
        if value < node.value:
            node.left = self.__recursive_remove(node.left, value)
        elif value > node.value:
            node.right = self.__recursive_remove(node.right, value)
        else:
            # Node with one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: get the inorder successor (smallest in the right subtree)
            temp = self.__min_value_node(node.right)
            node.value = temp.value
            node.right = self.__recursive_remove(node.right, temp.value)

        # Update height of the current node
        self.__update_height(node)

        # Balance the node if needed
        return self.__balance(node)

    # Helper method to find the node with the minimum value
    # Time Complexity: O(log(n)), because the method traverses the leftmost path of a subtree to find
    # the node with the minimum value. In an AVL tree, the height of the tree is O(log(n)),
    # so the traversal is limited to the height of the tree.
    def __min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Balancing the AVL tree
    # Time Complexity: O(1)
    def __balance(self, node):
        balance = self.__get_balance(node)

        # Left-heavy case
        if balance > 1:
            if self.__get_balance(node.left) < 0:
                # Left-Right case: Left rotate on left child before right rotate
                node.left = self.__rotate_left(node.left)
            # Left-Left case: Right rotate
            node = self.__rotate_right(node)

        # Right-heavy case
        elif balance < -1:
            if self.__get_balance(node.right) > 0:
                # Right-Left case: Right rotate on right child before left rotate
                node.right = self.__rotate_right(node.right)
            # Right-Right case: Left rotate
            node = self.__rotate_left(node)

        # Update height after balancing
        self.__update_height(node)

        return node

    # Helper method to rotate the subtree rooted at y to the right
    # Time Complexity: O(1)
    def __rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights in correct order
        self.__update_height(y)
        self.__update_height(x)

        return x

    # Helper method to rotate the subtree rooted at x to the left
    # Time Complexity: O(1)
    def __rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights in correct order
        self.__update_height(x)
        self.__update_height(y)

        return y
    # Time Complexity: O(n), because the method visits each node exactly once during the traversal.
    # For each node, it performs constant-time operations: a recursive call for the left subtree,
    # appending the node's value, and a recursive call for the right subtree.
    # Since there are n nodes in the tree, the total complexity is O(n).
    def in_order(self):
        if self.__root is None:
            return "[ ]" #if the tree is empty
        else:
            result = []
            self.__in_order(self.__root, result)
            return "[ " + ", ".join(str(x) for x in result) + " ]"

    def __in_order(self, node, result):
        if node:
            self.__in_order(node.left, result)# Traverse the left subtree
            result.append(node.value)# Append the value of the current node
            self.__in_order(node.right, result) # Traverse the right subtree

    # Time Complexity: O(n), For the worst-case scenario, pre_order runs at linear time because it only touches each
    # node once which is similar to the other two sorting methods. The method call to
    # __subtree_pre_order first concatenates the value of the root of the tree to the string being
    # returned. Then, it concatenates the value of the nodes on the left side of the tree which will be
    # followed by the right side of the tree. Both of which only requires the method to travel to each
    # node once, leading to linear time performance.
    def pre_order(self):
        if self.__root is None:
            return "[ ]"
        else:
            result = []
            self.__pre_order(self.__root, result)
            return "[ " + ", ".join(str(x) for x in result) + " ]"

    def __pre_order(self, node, result):
        if node:
            result.append(node.value)# Append the value of the current node
            self.__pre_order(node.left, result) # Traverse the right subtree
            self.__pre_order(node.right, result)# Traverse the left subtree

    # Time Complexity: O(n), post_order has linear time performance at the worst-case scenario because it also
    # touches each node of the binary tree once like the other two sorting methods. The method call
    # to __subtree_post_order concatenates the value of the nodes on the left side of the tree
    # followed by the right side of the tree. After going through the nodes on both sides once, the
    # method concatenates the value of the root of the tree to the string being returned, leading to
    # linear time performance.
    def post_order(self):
        if self.__root is None:
            return "[ ]"
        else:
            result = []
            self.__post_order(self.__root, result) # perform post order traversal
            return "[ " + ", ".join(str(x) for x in result) + " ]"

    def __post_order(self, node, result):
        if node:
            self.__post_order(node.left, result)# Traverse the left subtree
            self.__post_order(node.right, result)# Traverse the right subtree
            result.append(node.value)# Append the value of the current node

    def to_list(self): # O(n) complexity as each node is visited once
        result = []
        self.__in_order(self.__root, result)
        return result

    # Time Complexity: O(1), because it directly accesses the height attribute of the root node.
    # No traversal or computation is required.
    def get_height(self):
        return self.__root.height if self.__root else 0 # retrieved height from the root node if exist

    def __str__(self):
        return self.in_order()

if __name__ == '__main__':
    pass
