print('Лабораторная N°1')
print('Ротару Ксения Алексеевна. Гр.4354\n\n')

n = int(input('Введите кол-во элементов в массиве: '))
A = []
print('Введите элементы массива через enter:')
for i in range(n):
    A.append(int(input(f'{i}: ')))

def Selection_Sort(arr, n):
    print('\n\nСОРТИРОВКА ВЫБОРОМ:')
    comparisons = 0
    swaps = 0
    cur = 0
    print(arr)
    while cur < n - 1:
        mn = cur
        for i in range(cur + 1, n):
            comparisons += 1
            if arr[mn] > arr[i]:
                mn = i
        if mn != cur:
            swaps += 1
            arr[cur], arr[mn] = arr[mn], arr[cur]
        cur += 1
        print(arr)
    
    print(f"\nСравнения: {comparisons}, Обмены: {swaps}")
    print("Временная сложность: O(n²) в худшем, среднем и лучшем случае")
    return arr

def Insertion_Sort(arr, n):
    print('\n\nСОРТИРОВКА ВСТАВКАМИ:')
    comparisons = 0
    swaps = 0
    print(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                swaps += 1
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
        print(arr)
    
    print(f"\nСравнения: {comparisons}, Сдвиги: {swaps}")
    print("Временная сложность: O(n²) в худшем и среднем случае, O(n) в лучшем случае")
    return arr

def Merge_Sort(arr, n):
    print('\n\nСОРТИРОВКА СЛИЯНИЕМ:')
    comparisons = [0]
    print(arr)
    
    def merge_sort_util(lst):
        if len(lst) <= 1:
            return lst
            
        mid = len(lst) // 2
        left = merge_sort_util(lst[:mid])
        right = merge_sort_util(lst[mid:])
        
        merged = merge(left, right)
        print("Слияние:", left, "и", right, "->", merged)
        return merged
        
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
        
    sorted_arr = merge_sort_util(arr)
    for i in range(n):
        arr[i] = sorted_arr[i]
    
    print(f"\nСравнения: {comparisons[0]}")
    print("Временная сложность: O(n log n) во всех случаях")
    return arr

def Heap_Sort(arr, n):
    print('\n\nСОРТИРОВКА КУЧЕЙ:')
    comparisons = [0]
    swaps = [0]
    print(arr)
    
    def heapify(heap_size, root_index):
        largest = root_index
        left_child = 2 * root_index + 1
        right_child = 2 * root_index + 2

        if left_child < heap_size:
            comparisons[0] += 1
            if arr[left_child] > arr[largest]:
                largest = left_child

        if right_child < heap_size:
            comparisons[0] += 1
            if arr[right_child] > arr[largest]:
                largest = right_child

        if largest != root_index:
            swaps[0] += 1
            arr[root_index], arr[largest] = arr[largest], arr[root_index]
            print("Перестройка кучи:", arr)
            heapify(heap_size, largest)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    
    for i in range(n-1, 0, -1):
        swaps[0] += 1
        arr[0], arr[i] = arr[i], arr[0]
        print("Извлечение максимума:", arr)
        heapify(i, 0)
    
    print(f"\nСравнения: {comparisons[0]}, Обмены: {swaps[0]}")
    print("Временная сложность: O(n log n) во всех случаях")
    return arr

A_copy1 = A.copy()
A_copy2 = A.copy()
A_copy3 = A.copy()
A_copy4 = A.copy()

print('\nОтсортированный массив выбором:', Selection_Sort(A_copy1, n))
print('\nОтсортированный массив вставками:', Insertion_Sort(A_copy2, n))
print('\nОтсортированный массив слиянием:', Merge_Sort(A_copy3, n))
print('\nОтсортированный массив кучей:', Heap_Sort(A_copy4, n))
