import cv2 as cv
import numpy as np
import sys

class ISODATA:
    def __init__(self,image_array,K):
        if isinstance(image_array,np.ndarray) == False:
            raise ValueError("Sai giá trị ảnh đầu vào")
        try:
            K = int(K)
        except ValueError:
            print("Sai giá trị vùng")
            sys.exit()
        self.gray = cv.cvtColor(image_array,cv.COLOR_BGR2GRAY)
        self.height,self.width = self.gray.shape
        #--Khai báo từng phần tử sử dụng trong chương trình
        self.areas_array = [] #List chứa các vùng (các lớp) có kích thước bằng kích thước ảnh
        self.current_threshold = np.zeros(shape=K+1) #Mảng chứa các ngưỡng hiện tại
        self.previous_threshold = np.zeros(shape=K+1) #Mảng chứa các ngưỡng quá khứ
        self.current_means = np.zeros(shape=K) #Mảng chứa giá trị trung bình hiện tại
        self.previous_means = np.zeros(shape=K) #Mảng chứa giá trị trung bình quá khứ
        self.max_threshold = np.max(self.gray) #Phần tử ngưỡng cao nhất của ảnh
        self.min_threshold = np.min(self.gray) #Phần tử ngưỡng thấp nhất của ảnh
        self.K = K #Số vùng
        #--Khởi tạo giá trị ban đầu cho các phần tử
        #Khởi tạo số vùng ở trạng thái trống
        for x in range(K):
            self.areas_array.append(np.zeros((self.height,self.width)))
        #Khởi tạo ngưỡng quá khứ (x : 0->K)
        for x in range(K+1):
            if x == 0:
                self.previous_threshold[x] = self.min_threshold
            elif x == K:
                self.previous_threshold[x] = self.max_threshold
            else:
                self.previous_threshold[x] = x*((self.max_threshold-self.min_threshold)/K) + self.min_threshold
    def compare2Array(self,arr_1,arr_2):
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
                return False
        else:
            return False
    def execute_ISODATA_Algorithm(self):
        while True:
            #- Khởi tạo lại Mảng chứa ngưỡng hiện tại
            self.current_threshold = np.zeros(shape=self.K+1)
            #- Khởi tạo lại số vùng ở trạng thái trống
            for x in range(self.K+1):
                self.areas_array.append(np.zeros((self.height,self.width)))
            #- Khởi tạo lại mảng chứa giá trị trung bình hiện tại
            self.current_means = np.zeros(shape=self.K) #Mảng chứa giá trị trung bình hiện tại
            #- Thực hiện tìm các điểm ảnh thuộc các phân vùng khác nhau
            for y in range(self.height):
                for x in range(self.width):
                    for z in range(len(self.previous_threshold)-1):
                        if self.gray[y][x] >= self.previous_threshold[z] and self.gray[y][x] <= self.previous_threshold[z+1]:
                            #Do số thứ tự của z cũng tương ứng với là số thứ tự của vùng
                            (self.areas_array[z])[y][x] = self.gray[y][x]
            #- Thực hiện tính mức xám trung bình và cho vào mảng trung bình
            for x in range(self.K):
                self.current_means[x] = np.mean(self.areas_array[x])
            #- Tính giá trị ngưỡng của các lớp theo giá trị trung bình
            for x in range(self.K + 1):
                if x == 0:
                    self.current_threshold[x] = self.min_threshold
                elif x == self.K:
                    self.current_threshold[x] = self.max_threshold
                else:
                    self.current_threshold[x] = (self.current_means[x-1]+self.current_means[x])/2
            #- Thực hiện so sánh giá trị giữa mảng ngưỡng hiện tại và mảng ngưỡng quá khứ, đồng thời cả mảng giá trị trung bình hiện tại và quá khứ
            if self.compare2Array(self.current_threshold,self.previous_threshold):
                print('\n\n')
                print(f'Current threshold : {self.current_threshold}')
                print(f'Previous threshold: {self.previous_threshold}')
                print(f'Current means : {self.current_means}')
                print(f'Previous means: {self.previous_means}')
                print('Executing ISODATA Completed')
                break
            #-Cập nhật giá trị ngưỡng hiện tại = qúa khứ phòng trường hợp giá trị trung bình 2 bên bằng nhau
            #- Chỉ khi cập nhật giá trị ngưỡng thì điều kiện lặp method detectTheMoon mới không xảy ra vĩnh viễn
            elif self.compare2Array(self.current_means,self.previous_means):
                print("\n\nBecause the previous means are equal to the current means, we update the current threshold equal to the previous threshold ")
                print(f'Last Result: {self.previous_threshold}')
                self.current_threshold = self.previous_threshold
                print('Executing ISODATA Completed')
                break
            else:
                print('\n\n')
                print(f'Current threshold : {self.current_threshold}')
                print(f'Previous threshold: {self.previous_threshold}')
                print('\n')
                print(f'Current means : {self.current_means}')
                print(f'Previous means: {self.previous_means}')
                self.previous_means = self.current_means
                self.previous_threshold = self.current_threshold
        # print(self.current_means)
    def detectTheMoon(self):
        self.execute_ISODATA_Algorithm()
        #Trong khi ngưỡng lớn thứ nhì và ngưỡng lớn thứ nhất có độ chênh lệch mức sáng là 10 (do ánh trăng sáng)
        while np.abs(self.current_threshold[self.K]-self.current_threshold[self.K-1]) >=20:
            #-Cập nhật giá trị T0 bằng với giá trị lớn thứ nhì trong mảng ngưỡng hiện tại 
            self.min_threshold = self.current_threshold[self.K-1]
            #-Reset giá trị ngưỡng quá khứ
            self.previous_means = np.zeros(shape=self.K) #Mảng chứa giá trị trung bình quá khứ
            #Khởi tạo lại ngưỡng quá khứ theo giá trị T0 mới 
            for x in range(self.K+1):
                if x == 0:
                    self.previous_threshold[x] = self.min_threshold
                elif x == self.K:
                    self.previous_threshold[x] = self.max_threshold
                else:
                    self.previous_threshold[x] = x*((self.max_threshold-self.min_threshold)/self.K) + self.min_threshold
            self.execute_ISODATA_Algorithm()
        print('\n\n')
        print(f'Final Current threshold : {self.current_threshold}')
        return self.current_threshold,self.current_means,self.areas_array

if __name__ == "__main__":
    app = ISODATA(cv.imread('./photos/trang.jpg'),15)
    arr_threshold,arr_means,arr_areas = app.detectTheMoon()
    arr_threshold = arr_threshold.tolist()
    gray = cv.imread('./photos/trang.jpg',0)
    #Ta cần ảnh của mặt trăng, do đó ta sẽ sử dụng lớp cuối cùng để biến đổi về thành ảnh nhị phân (do giá trị giữa 2 khoảng ngưỡng đó là lớn nhất và mặt trăng lại sáng nhất)
    thres,binary_image = cv.threshold(gray,int(arr_threshold[app.K-1]),int(arr_threshold[app.K]),cv.THRESH_BINARY)
    cv.imshow('Image',binary_image)
    if cv.waitKey(0) == ord('q'):
        print('Quit')
        sys.exit()
    
            
        