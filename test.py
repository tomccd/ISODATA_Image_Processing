import numpy as np


# arr_1 = np.array([1,2,3,4,5])

# arr_2 = np.array([4,5,6,7,8])

# list = []
# list.append(arr_1)
# list.append(arr_2)
# string = 'A'
# a = int(string)
# print(a)
# print(np.isclose([27.0,28.0], [26.99999,27.99999]))
# print(np.zeros((2,3)).shape)
def compare2Array(arr_1,arr_2):
        if isinstance(arr_1,np.ndarray)  and isinstance(arr_2,np.ndarray):
            count = 0
            for x in range(len(arr_1)):
            #- Nếu trị tuyệt đối của hiệu 2 phần từ nằm trong dải từ 0.1 đến 0.9, ta coi như là 2 số đó bằng nhau
                condition1 = np.abs(arr_1[x]-arr_2[x]) >= 0
                condition2 = np.abs(arr_1[x]-arr_2[x]) <= 0.999999999999999
                #- I dunno why I used this thing. Link : https://numpy.org/doc/stable/reference/generated/numpy.logical_and.html
                if np.logical_and(condition1,condition2):
                    count+=1
            if count == len(arr_1):
                return True
            else:
                print(count)
                return False
        else:
            return False

print(compare2Array(np.array([1,2,3,4]),np.array([1,2,3,4])))