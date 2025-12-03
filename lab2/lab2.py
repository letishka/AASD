from enum import Enum
import random
import math
import matplotlib.pyplot as plt


class Color(Enum):
    BLACK = 0
    RED = 1


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.color = Color.BLACK

    def __str__(self) -> str:
        return str(self.key) if self.key is not None else "NIL"


class BST:
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.NIL.height = 0
        self.NIL.color = Color.BLACK
        self.root = self.NIL

    def _is_nil(self, node):
        return node is self.NIL

    def __str__(self, node=None, level=0, prefix="root: ") -> str:
        if node is None:
            node = self.root
            if self._is_nil(node):
                return "Empty tree"

        res = "   " * level + prefix + str(node)

        if self._is_nil(node):
            res += "\n"
            return res

        res += "\n"
        res += self.__str__(node.left, level + 1, "L: ")
        res += self.__str__(node.right, level + 1, "R: ")

        return res

    def insert(self, key):
        if not self._is_nil(self.find(key)):
            return None

        x = Node(key)
        x.left = self.NIL
        x.right = self.NIL
        x.parent = self.NIL

        if self._is_nil(self.root):
            self.root = x
            return x

        current = self.root
        parent = self.NIL

        while not self._is_nil(current):
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        x.parent = parent
        if key < parent.key:
            parent.left = x
        else:
            parent.right = x

        return x

    def find(self, key):
        current = self.root

        while not self._is_nil(current):
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current

        return self.NIL

    def _transplant(self, u, v):
        if self._is_nil(u.parent):
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        if not self._is_nil(v):
            v.parent = u.parent

    def _minimum(self, node):
        while not self._is_nil(node.left):
            node = node.left
        return node

    def _maximum(self, node):
        while not self._is_nil(node.right):
            node = node.right
        return node

    def find_min(self):
        if self._is_nil(self.root):
            return None
        return self._minimum(self.root).key

    def find_max(self):
        if self._is_nil(self.root):
            return None
        return self._maximum(self.root).key

    def _delete(self, node_to_delete):
        if self._is_nil(node_to_delete):
            return self.NIL

        if self._is_nil(node_to_delete.left):
            self._transplant(node_to_delete, node_to_delete.right)
        elif self._is_nil(node_to_delete.right):
            self._transplant(node_to_delete, node_to_delete.left)
        else:
            y = self._minimum(node_to_delete.right)

            if y.parent != node_to_delete:
                self._transplant(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y

            self._transplant(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y

        return node_to_delete.parent

    def delete(self, key):
        z = self.find(key)
        if self._is_nil(z):
            return self.NIL
        return self._delete(z)

    def preorder(self, node=None, result=None):
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        result.append(node.key)
        self.preorder(node.left, result)
        self.preorder(node.right, result)

        return result

    def inorder(self, node=None, result=None):
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        self.inorder(node.left, result)
        result.append(node.key)
        self.inorder(node.right, result)

        return result

    def postorder(self, node=None, result=None):
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        self.postorder(node.left, result)
        self.postorder(node.right, result)
        result.append(node.key)

        return result

    def levelorder(self):
        if self._is_nil(self.root):
            return []

        result = []
        queue = [self.root]

        while queue:
            current = queue.pop(0)

            if not self._is_nil(current):
                result.append(current.key)
                queue.append(current.left)
                queue.append(current.right)

        return result

    def levelorder_with_levels(self):
        if self._is_nil(self.root):
            return []

        result = []
        queue = [(self.root, 0)]

        while queue:
            current, level = queue.pop(0)

            if not self._is_nil(current):
                if len(result) <= level:
                    result.append([])
                result[level].append(current.key)
                queue.append((current.left, level + 1))
                queue.append((current.right, level + 1))

        return result

    def height(self, node=None):
        if node is None:
            node = self.root

        if self._is_nil(node):
            return 0

        left_height = self.height(node.left)
        right_height = self.height(node.right)

        return max(left_height, right_height) + 1


class AVL(BST):
    def __init__(self):
        super().__init__()

    def _height(self, node):
        if self._is_nil(node):
            return 0
        return node.height

    def _update_height(self, node):
        if self._is_nil(node):
            return 0
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return node.height

    def _balance_factor(self, node):
        if self._is_nil(node):
            return 0
        return self._height(node.right) - self._height(node.left)

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        y.parent = x.parent
        x.parent = y
        if not self._is_nil(T2):
            T2.parent = x

        if self._is_nil(y.parent):
            self.root = y
        elif y.parent.left == x:
            y.parent.left = y
        else:
            y.parent.right = y

        self._update_height(x)
        self._update_height(y)

        return y

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        x.parent = y.parent
        y.parent = x
        if not self._is_nil(T2):
            T2.parent = y

        if self._is_nil(x.parent):
            self.root = x
        elif x.parent.left == y:
            x.parent.left = x
        else:
            x.parent.right = x

        self._update_height(y)
        self._update_height(x)

        return x

    def _balance(self, node):
        if self._is_nil(node):
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance < -1:
            if self._balance_factor(node.left) <= 0:
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)

        if balance > 1:
            if self._balance_factor(node.right) >= 0:
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

        return node

    def insert(self, key):
        node = super().insert(key)
        if node is None:
            return None

        current = node
        while not self._is_nil(current):
            current = self._balance(current)
            current = current.parent

        if self._is_nil(self.root) and node.parent is self.NIL:
            self.root = node

        return node

    def _delete(self, z):
        if self._is_nil(z):
            return self.NIL

        y = z
        y_original_height = y.height

        if self._is_nil(z.left):
            x = z.right
            self._transplant(z, z.right)
        elif self._is_nil(z.right):
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_height = y.height
            x = y.right

            if y.parent != z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.height = z.height

        current = z.parent if not self._is_nil(z.parent) else x.parent
        while not self._is_nil(current):
            self._update_height(current)
            current = self._balance(current)
            current = current.parent

        if self._is_nil(self.root) and not self._is_nil(x):
            self.root = x

        return z.parent


class RB(BST):
    def __init__(self):
        super().__init__()
        self.NIL.color = Color.BLACK

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        y.parent = x.parent
        x.parent = y
        if not self._is_nil(T2):
            T2.parent = x

        if self._is_nil(y.parent):
            self.root = y
        elif y.parent.left == x:
            y.parent.left = y
        else:
            y.parent.right = y

        return y

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        x.parent = y.parent
        y.parent = x
        if not self._is_nil(T2):
            T2.parent = y

        if self._is_nil(x.parent):
            self.root = x
        elif x.parent.left == y:
            x.parent.left = x
        else:
            x.parent.right = x

        return x

    def _balance_insert(self, z):
        while z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._left_rotate(z.parent.parent)

        self.root.color = Color.BLACK

    def _balance_delete(self, x):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right

                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left

                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = Color.BLACK

    def insert(self, key):
        node = super().insert(key)
        if node is None:
            return None

        node.color = Color.RED
        self._balance_insert(node)

        return node

    def _rb_delete(self, z):
        y = z
        y_original_color = y.color

        if self._is_nil(z.left):
            x = z.right
            self._transplant(z, z.right)
        elif self._is_nil(z.right):
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent != z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == Color.BLACK:
            self._balance_delete(x)

        return z.parent

    def delete(self, key):
        z = self.find(key)
        if self._is_nil(z):
            return self.NIL
        return self._rb_delete(z)


def avl_theoretical_lower_bound(n):
    if n == 0:
        return 0
    return math.log2(n + 1)


def avl_theoretical_upper_bound(n):
    if n == 0:
        return 0
    return 1.44 * math.log2(n + 2)


def rb_theoretical_lower_bound(n):
    if n == 0:
        return 0
    return math.log2(n + 1)


def rb_theoretical_upper_bound(n):
    if n == 0:
        return 0
    return 2 * math.log2(n + 1)


def bst_experiment_random_keys(max_n=39856, step=100):
    n_values = []
    heights = []

    all_keys = list(range(max_n))
    random.shuffle(all_keys)

    for n in range(0, max_n + 1, step):
        n_values.append(n)

        if n == 0:
            height = 0
        else:
            tree = BST()
            for i in range(n):
                tree.insert(all_keys[i])
            height = tree.height()

        heights.append(height)

    return n_values, heights


def avl_experiment_random_keys(max_n=38767, step=100):
    n_values = []
    heights = []
    lower_bounds = []
    upper_bounds = []

    all_keys = list(range(max_n))
    random.shuffle(all_keys)

    for n in range(0, max_n + 1, step):
        n_values.append(n)

        if n == 0:
            height = 0
        else:
            tree = AVL()
            for i in range(n):
                tree.insert(all_keys[i])
            height = tree.height()

        heights.append(height)
        lower_bounds.append(avl_theoretical_lower_bound(n))
        upper_bounds.append(avl_theoretical_upper_bound(n))

    return n_values, heights, lower_bounds, upper_bounds


def rb_experiment_random_keys(max_n=32345, step=100):
    n_values = []
    heights = []
    lower_bounds = []
    upper_bounds = []

    all_keys = list(range(max_n))
    random.shuffle(all_keys)

    for n in range(0, max_n + 1, step):
        n_values.append(n)

        if n == 0:
            height = 0
        else:
            tree = RB()
            for i in range(n):
                tree.insert(all_keys[i])
            height = tree.height()

        heights.append(height)
        lower_bounds.append(rb_theoretical_lower_bound(n))
        upper_bounds.append(rb_theoretical_upper_bound(n))

    return n_values, heights, lower_bounds, upper_bounds


def avl_experiment_sorted_keys(max_n=23455, step=100):
    n_values = []
    heights = []
    lower_bounds = []
    upper_bounds = []

    for n in range(0, max_n + 1, step):
        n_values.append(n)

        if n == 0:
            height = 0
        else:
            tree = AVL()
            for i in range(n):
                tree.insert(i)
            height = tree.height()

        heights.append(height)
        lower_bounds.append(avl_theoretical_lower_bound(n))
        upper_bounds.append(avl_theoretical_upper_bound(n))

    return n_values, heights, lower_bounds, upper_bounds


def rb_experiment_sorted_keys(max_n=32123, step=100):
    n_values = []
    heights = []
    lower_bounds = []
    upper_bounds = []

    for n in range(0, max_n + 1, step):
        n_values.append(n)

        if n == 0:
            height = 0
        else:
            tree = RB()
            for i in range(n):
                tree.insert(i)
            height = tree.height()

        heights.append(height)
        lower_bounds.append(rb_theoretical_lower_bound(n))
        upper_bounds.append(rb_theoretical_upper_bound(n))

    return n_values, heights, lower_bounds, upper_bounds


def plot_bst_results():
    n_values, heights = bst_experiment_random_keys()

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, heights, 'b-', label='Экспериментальная высота BST', linewidth=2, alpha=0.7)

    log_n = [math.log2(n + 1) if n > 0 else 0 for n in n_values]
    sqrt_n = [math.sqrt(n) for n in n_values]

    plt.plot(n_values, log_n, 'g--', label='log₂(n+1)', linewidth=1.5, alpha=0.7)
    plt.plot(n_values, sqrt_n, 'r--', label='√n', linewidth=1.5, alpha=0.7)

    plt.xlabel('Количество ключей (n)')
    plt.ylabel('Высота дерева')
    plt.title('Зависимость высоты BST от количества ключей\n(случайные ключи, равномерное распределение)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, max(n_values))
    plt.show()


def plot_avl_rb_random_results():
    n_avl, h_avl, lb_avl, ub_avl = avl_experiment_random_keys()
    n_rb, h_rb, lb_rb, ub_rb = rb_experiment_random_keys()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(n_avl, h_avl, 'b-', label='Экспериментальная высота', linewidth=2, alpha=0.7)
    ax1.plot(n_avl, lb_avl, 'r--', label='Нижняя оценка: log₂(n+1)', linewidth=1.5)
    ax1.plot(n_avl, ub_avl, 'g--', label='Верхняя оценка: 1.44*log₂(n+2)', linewidth=1.5)
    ax1.set_xlabel('Количество ключей (n)')
    ax1.set_ylabel('Высота дерева')
    ax1.set_title('Зависимость высоты AVL-дерева от n\n(случайные ключи)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, max(n_avl))

    ax2.plot(n_rb, h_rb, 'b-', label='Экспериментальная высота', linewidth=2, alpha=0.7)
    ax2.plot(n_rb, lb_rb, 'r--', label='Нижняя оценка: log₂(n+1)', linewidth=1.5)
    ax2.plot(n_rb, ub_rb, 'g--', label='Верхняя оценка: 2*log₂(n+1)', linewidth=1.5)
    ax2.set_xlabel('Количество ключей (n)')
    ax2.set_ylabel('Высота дерева')
    ax2.set_title('Зависимость высоты RB-дерева от n\n(случайные ключи)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(n_rb))

    plt.tight_layout()
    plt.show()


def plot_avl_rb_sorted_results():
    n_avl, h_avl, lb_avl, ub_avl = avl_experiment_sorted_keys()
    n_rb, h_rb, lb_rb, ub_rb = rb_experiment_sorted_keys()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(n_avl, h_avl, 'b-', label='Экспериментальная высота', linewidth=2, alpha=0.7)
    ax1.plot(n_avl, lb_avl, 'r--', label='Нижняя оценка: log₂(n+1)', linewidth=1.5)
    ax1.plot(n_avl, ub_avl, 'g--', label='Верхняя оценка: 1.44*log₂(n+2)', linewidth=1.5)
    ax1.set_xlabel('Количество ключей (n)')
    ax1.set_ylabel('Высота дерева')
    ax1.set_title('Зависимость высоты AVL-дерева от n\n(монотонно возрастающие ключи)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, max(n_avl))

    ax2.plot(n_rb, h_rb, 'b-', label='Экспериментальная высота', linewidth=2, alpha=0.7)
    ax2.plot(n_rb, lb_rb, 'r--', label='Нижняя оценка: log₂(n+1)', linewidth=1.5)
    ax2.plot(n_rb, ub_rb, 'g--', label='Верхняя оценка: 2*log₂(n+1)', linewidth=1.5)
    ax2.set_xlabel('Количество ключей (n)')
    ax2.set_ylabel('Высота дерева')
    ax2.set_title('Зависимость высоты RB-дерева от n\n(монотонно возрастающие ключи)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(n_rb))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    Tree = BST()

    random_numbers = random.sample(range(-10, 26), 20)
    print(f"Вставляем: {random_numbers}")
    for i in random_numbers:
        Tree.insert(i)
    print("Дерево после вставок:")
    print(Tree)
    print()

    test_key = random_numbers[3]
    found = Tree.find(test_key)
    print(f"Поиск ключа {test_key}: {'Найден' if not Tree._is_nil(found) else 'Не найден'}")
    print()

    delete_key = random_numbers[5]
    print(f"Удаление ключа {delete_key}")
    Tree.delete(delete_key)
    print("Дерево после удаления:")
    print(Tree)
    print()

    print("=== ОБХОДЫ ДЕРЕВА ===")

    print("Прямой обход (pre-order):")
    print(Tree.preorder())
    print()

    print("Центрированный обход (in-order):")
    print(Tree.inorder())
    print()

    print("Обратный обход (post-order):")
    print(Tree.postorder())
    print()

    print("Обход в ширину (level-order):")
    print(Tree.levelorder())
    print()

    print("Обход в ширину с уровнями:")
    levels = Tree.levelorder_with_levels()
    for i, level in enumerate(levels):
        print(f"{i}: {level}")
    print()

    print("=== ХАРАКТЕРИСТИКИ ДЕРЕВА ===")
    print(f"Высота дерева: {Tree.height()}")
    print(f"Минимальный ключ: {Tree.find_min()}")
    print(f"Максимальный ключ: {Tree.find_max()}")

    print("\n=== ТЕСТ AVL ДЕРЕВА ===")
    avl_tree = AVL()
    avl_values = [10, 20, 30, 40, 50, 25]
    for val in avl_values:
        avl_tree.insert(val)
    print("AVL дерево после вставки 10, 20, 30, 40, 50, 25:")
    print(avl_tree)
    print(f"Высота AVL: {avl_tree.height()}")
    print(f"In-order AVL: {avl_tree.inorder()}")

    avl_tree.delete(50)
    print("\nAVL дерево после удаления 50:")
    print(avl_tree)
    print(f"Высота AVL после удаления: {avl_tree.height()}")

    print("\n=== ТЕСТ RB ДЕРЕВА ===")
    rb_tree = RB()
    rb_values = [7, 3, 18, 10, 22, 8, 11, 26]
    for val in rb_values:
        rb_tree.insert(val)
    print("RB дерево после вставки значений:")
    print(rb_tree)
    print(f"Высота RB: {rb_tree.height()}")
    print(f"In-order RB: {rb_tree.inorder()}")

    rb_tree.delete(10)
    print("\nRB дерево после удаления 10:")
    print(rb_tree)
    print(f"Высота RB после удаления: {rb_tree.height()}")

    print("\n=== ЗАПУСК ЭКСПЕРИМЕНТОВ ===")

    print("Эксперимент 1: BST со случайными ключами...")
    plot_bst_results()
    print("Эксперимент 2: AVL и RB со случайными ключами...")
    plot_avl_rb_random_results()
    print("Эксперимент 3: AVL и RB с монотонно возрастающими ключами...")
    plot_avl_rb_sorted_results()