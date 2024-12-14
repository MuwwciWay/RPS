# tree_sort.py
import random

def generate_numbers():
    numbers = []
    for _ in range(10):
        numbers.append(random.randint(0, 100))
    return numbers

def tree_sort(A):
    if len(A) <= 1:
        return A

    mid = len(A) // 2
    left = tree_sort(A[:mid])
    right = tree_sort(A[mid:])

    result = []
    i = j = 0
    while i < len(left) or j < len(right):
        if i == len(left):
            result.append(right[j])
            j += 1
        elif j == len(right):
            result.append(left[i])
            i += 1
        else:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    return result

def save_array(filename, array, encoding='Windows-1251'):
    with open(filename, 'w', encoding=encoding) as file:
        for item in array:
            file.write(str(item) + '\n')
