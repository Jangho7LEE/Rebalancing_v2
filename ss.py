# import matplotlib.pyplot as plt
# # 데이터셋 생성
# x = [1, 2, 3, 4, 5]
# y1 = [2, 3, 5, 7, 11]
# y2 = [1, 4, 6, 8, 10]

# # 산점도 그리기
# plt.scatter([x[0]] , y1[0], color='blue', label='Y1')
# plt.scatter([x[0]] * len(y2), y2, color='red', label='Y2')

# # 그래프 제목과 축 레이블 추가
# plt.title('Scatter Plot Example')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')

# # 범례 추가
# plt.legend()

# # 그래프 표시
# plt.show()


import matplotlib.pyplot as plt

# 데이터셋 생성
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]
y1 = [2, 4,11 , 17, 111]

# 선 그래프 그리기
plt.figure()
plt.plot(x, y, color='skyblue', linewidth=2, linestyle='--', marker='o', markersize=8, label='Line Plot')
plt.plot(x, y1, color='skyblue', linewidth=2, linestyle='--', marker='o', markersize=8, label='Line Plot')

# 그래프 제목과 축 레이블 추가
plt.title('Line Plot Example')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()