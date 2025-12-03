class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1

    def __str__(self) -> str:
        return str(self.key) if self.key is not None else "NIL"


class BST:
    def __init__(self):
        # Создаём единый NIL-узел
        self.NIL = Node(None)  # Ключ None для NIL
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        # Корень изначально указывает на NIL
        self.root = self.NIL

    def _is_nil(self, node):
        return node is self.NIL or node.key is None

    def __str__(self, node=None, level=0, prefix="Root: ") -> str:
        if node is None:
            node = self.root
            if self._is_nil(node):
                return "Empty tree"

        res = "  " * level + prefix + str(node) + "\n"

        # Если узел не NIL и есть хотя бы один потомок
        if not self._is_nil(node):
            # Левый потомок
            if not self._is_nil(node.left):
                res += self.__str__(node.left, level + 1, "L: ")
            else:
                res += "  " * (level + 1) + "L: NIL\n"

            # Правый потомок
            if not self._is_nil(node.right):
                res += self.__str__(node.right, level + 1, "R: ")
            else:
                res += "  " * (level + 1) + "R: NIL\n"

        return res

    def insert(self, key):
        # Проверяем, существует ли ключ
        if not self._is_nil(self.find(key)):
            return None

        # Создаём новый узел
        x = Node(key)
        x.left = self.NIL
        x.right = self.NIL
        x.parent = self.NIL

        # Если дерево пустое
        if self._is_nil(self.root):
            self.root = x
            return x

        # Ищем место для вставки
        current = self.root
        parent = self.NIL

        while not self._is_nil(current):
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        # Вставляем узел
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
                return current  # Найден

        return self.NIL  # Не найден - возвращаем NIL

    def _transplant(self, u, v):
        """Заменяет поддерево u на поддерево v"""
        if self._is_nil(u.parent):
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        if not self._is_nil(v):
            v.parent = u.parent

    def _minimum(self, node):
        """В поддереве"""
        while not self._is_nil(node.left):
            node = node.left
        return node
    def _maximum(self, node):
        """В поддереве"""
        while not self._is_nil(node.right):
            node = node.right
        return node
    def find_min(self):
        """Во всём дереве"""
        if self._is_nil(self.root):
            return None
        return self._minimum(self.root).key
    def find_max(self):
        """Во всём дереве"""
        if self._is_nil(self.root):
            return None
        return self._maximum(self.root).key

    def _delete(self, node):
        if self._is_nil(node):
            return self.NIL

        if self._is_nil(node.left):
            # Нет левого потомка или оба потомка NIL
            self._transplant(node, node.right)
        elif self._is_nil(node.right):
            # Нет правого потомка
            self._transplant(node, node.left)
        else:
            # Есть оба потомка
            y = self._minimum(node.right)

            if y.parent != node:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y

        return node.parent

    def delete(self, node):
        z = self.find(node)
        if self._is_nil(z):
            return self.NIL
        return self._delete(z)

    def preorder(self, node=None, result=None):
        """Прямой обход (Pre-order): Корень → Лево → Право"""
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        result.append(node.key)  # Корень
        self.preorder(node.left, result)  # Лево
        self.preorder(node.right, result)  # Право

        return result

    def inorder(self, node=None, result=None):
        """Центрированный обход (In-order): Лево → Корень → Право"""
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        self.inorder(node.left, result)  # Лево
        result.append(node.key)  # Корень
        self.inorder(node.right, result)  # Право

        return result

    def postorder(self, node=None, result=None):
        """Обратный обход (Post-order): Лево → Право → Корень"""
        if result is None:
            result = []
            node = self.root

        if self._is_nil(node):
            return result

        self.postorder(node.left, result)  # Лево
        self.postorder(node.right, result)  # Право
        result.append(node.key)  # Корень

        return result

    def levelorder(self):
        """Обход в ширину (Level-order)"""
        if self._is_nil(self.root):
            return []

        result = []
        queue = [self.root]  # Очередь для BFS

        while queue:
            current = queue.pop(0)  # Берем первый элемент

            if not self._is_nil(current):
                result.append(current.key)

                # Добавляем детей в очередь
                if not self._is_nil(current.left):
                    queue.append(current.left)
                if not self._is_nil(current.right):
                    queue.append(current.right)

        return result

    # Обход в ширину с уровнями
    def levelorder_with_levels(self):
        """Обход в ширину с указанием уровней"""
        if self._is_nil(self.root):
            return []

        result = []
        queue = [(self.root, 0)]  # (узел, уровень)

        while queue:
            current, level = queue.pop(0)

            if not self._is_nil(current):
                # Добавляем результат с указанием уровня
                if len(result) <= level:
                    result.append([])
                result[level].append(current.key)

                # Добавляем детей
                if not self._is_nil(current.left):
                    queue.append((current.left, level + 1))
                if not self._is_nil(current.right):
                    queue.append((current.right, level + 1))

        return result


    #AVLAVLAVLAVLAVLVALVALAVLAVLVALAVLAVLAVLAVLAVLAVLAVLAVLAVLAVLAVLAVLAVLAVLAVL

    class AVL(BST):
        def __init__(self):
            super().__init__()

        def insert(self):
            super().insert()

        def _delete(self):
            super()._delete()

        def _height(self, node):
            if self._is_nil(node):
                return 0
            return node.height

        def _left_rotate (self, node):
            #левый поворот

        def _right_rotate(self, node):
            #правый поворот

        def _balance_factor(self, node):
            if self._is_nil(node):
                return 0
            return self._height(node.right) - self._height(node.left)

        def _balance(self):
            #балансировка

        def AVL_insert(self, key):
            super().insert(key)
            _balance(self)
            pass

        def _AVL_delete(self, key):
            super()._delete(key)
            _balance(self)
            pass

#RBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRBRB

    class RB(BST):
        def __init__(self):
            super().__init__()

        def insert(self):
            super().insert()

        def _delete(self):
            super()._delete()

        def _left_rotate(self, node):

        # левый поворот

        def _right_rotate(self, node):

        # правый поворот

        def _balance_insert(self, node):

        # балансировка полсе вставки

        def _balance_delete(self, node):

        # балансировка полсе удаления

        def insert(self, key):

            self._balance_insert()
            pass

        def _delete(self, key):

            self._balance_delete()
            pass

if __name__ == "__main__":
    Tree = BST()
    import random

    # Тест 2: Вставка нескольких элементов
    random_numbers = random.sample(range(-10, 26), 10)
    print(f"Вставляем: {random_numbers}")
    for i in random_numbers:
        Tree.insert(i)
    print("Дерево после вставок:")
    print(Tree)
    print()

    # Тест 3: Поиск
    test_key = random_numbers[3]
    found = Tree.find(test_key)
    print(f"Поиск ключа {test_key}: {'Найден' if not Tree._is_nil(found) else 'Не найден'}")
    print()

    # Тест 4: Удаление
    delete_key = random_numbers[5]
    print(f"Удаление ключа {delete_key}")
    Tree.delete(delete_key)
    print("Дерево после удаления:")
    print(Tree)
    print()

    # Тест 5: Обходы
    print("=== ОБХОДЫ ДЕРЕВА ===")

    print("Прямой обход (Pre-order):")
    print(Tree.preorder())
    print("Ожидаемый результат: [50, 30, 20, 10, 25, 40, 35, 45, 70, 60, 80]")
    print()

    print("Центрированный обход (In-order):")
    print(Tree.inorder())
    print("Ожидаемый результат: [10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80]")
    print("(отсортированные ключи для BST)")
    print()

    print("Обратный обход (Post-order):")
    print(Tree.postorder())
    print("Ожидаемый результат: [10, 25, 20, 35, 45, 40, 30, 60, 80, 70, 50]")
    print()

    print("Обход в ширину (Level-order):")
    print(Tree.levelorder())
    print("Ожидаемый результат: [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]")
    print()

    print("Обход в ширину с уровнями:")
    levels = Tree.levelorder_with_levels()
    for i, level in enumerate(levels):
        print(f"Уровень {i}: {level}")
    print()

    print("=== ХАРАКТЕРИСТИКИ ДЕРЕВА ===")
    #print(f"Высота дерева: {Tree.height()}")
    #print(f"Количество узлов: {Tree.size()}")
    print(f"Минимальный ключ: {Tree.find_min()}")
    print(f"Максимальный ключ: {Tree.find_max()}")
