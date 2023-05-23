

list1 = [1, 2, 3]
list2 = [1, 2, 3, 4,7,8]

elements_not_in_list2 = set(list1) - set(list2)

result = list(elements_not_in_list2)
print(result)


if len(result)==0:
    print("rong")