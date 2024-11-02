# 라이브러리
import math as m
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LissajousApp: # GUI
    def __init__(self, master): # GUI 선언
        self.master = master 
        self.master.title("오실로스코프-함수발생기 모형 프로그램") # GUI 제목
        self.master.geometry("1280x720") # GUI 초기 해상도

        # 실수형 데이터 선언 (초깃값)
        self.A = tk.DoubleVar(value=1.0) # 진폭
        self.a = tk.DoubleVar(value=1.0) # 주파수
        self.i1 = tk.DoubleVar(value=0.0) # 위상차
        self.k1 = tk.DoubleVar(value=0.0) # 수직이동
        self.B = tk.DoubleVar(value=1.0) 
        self.b = tk.DoubleVar(value=1.0)
        self.i2 = tk.DoubleVar(value=0.0)
        self.k2 = tk.DoubleVar(value=0.0)

        # 슬라이더 생성
        self.create_sliders_frame()
        
        # 직교좌표계 선언
        self.fig, self.ax = plt.subplots(figsize=(8, 8)) # 직교좌표계 정의
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master) # 그래프를 GUI에 통합
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) # 직접 표기

        # 업데이트 호출 (실시간 표기)
        self.update_plot()

        # 클립보드에 복사하기 버튼 추가
        self.copy_button = tk.Button(self.master, text="클립보드에 데이터 복사하기", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.BOTTOM, padx=10)

    def create_sliders_frame(self): # 
        slider_frame = tk.Frame(self.master)
        slider_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # GUI 요소 지정
        tk.Label(slider_frame, text="x축 진폭 (m) [float]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=0.1, variable=self.A, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="x축 주파수 (rad/s) [int]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=1, variable=self.a, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="x축 위상차 (degrees°) [int]").pack()
        tk.Scale(slider_frame, from_=0, to=360, resolution=1, variable=self.i1, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="x축 수직이동 (m) [float]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=0.1, variable=self.k1, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="y축 진폭 (m) [float]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=0.1, variable=self.B, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="y축 주파수 (rad/s) [int]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=1, variable=self.b, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="y축 위상차 (degrees°) [int]").pack()
        tk.Scale(slider_frame, from_=0, to=360, resolution=1, variable=self.i2, orient='horizontal', command=self.update_plot, length=300).pack()

        tk.Label(slider_frame, text="y축 수직이동 (m) [float]").pack()
        tk.Scale(slider_frame, from_=-10, to=10, resolution=0.1, variable=self.k2, orient='horizontal', command=self.update_plot, length=300).pack()

    def lissajous(self, a, b, A, B, i1, i2, k1, k2):
        t_values = np.linspace(0, 2 * np.pi, 1000) # 균일 분포값 생성
        x = A * np.sin(a * t_values + m.radians(i1)) + k1  # 그래프에 대해 균일 함숫값 추출
        y = B * np.sin(b * t_values + m.radians(i2)) + k2 # 또 다른 그래프에 대해 균일 함숫값 추출
        return x, y # 임의의 두 그래프 합성

    def update_plot(self, event=None): # 업데이트 함수 (실시간 변환)
        x, y = self.lissajous(self.a.get(), self.b.get(), self.A.get(), self.B.get(), self.i1.get(), self.i2.get(), self.k1.get(), self.k2.get()) 
        
        self.ax.clear() # 초기화
        if abs(self.k1.get())+abs(self.k2.get())>0: # 좌표 지정
            self.ax.plot(x, y, label='Lissajous Curve', color='red') # 수직이동 시 홍색 개형
        else:
            if abs(self.a.get())-abs(self.b.get())==0:
                self.ax.plot(x, y, label='Lissajous Curve', color='green') # 주파수의 절댓값이 동일할 때 녹색 개형
            else: 
                self.ax.plot(x, y, label='Lissajous Curve', color='blue') # 보편적인 청색 개형
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--') # x축 직선 지정
        self.ax.axvline(0, color='black', linewidth=0.5, linestyle='--') # y축 직선 지정
        self.ax.set_title("Lissajous Curve", fontsize=16) # 그래프 이름 지정
        self.ax.grid() # 격자 표시 지정
        self.ax.set_aspect('equal', 'box') # 좌표계 비율 지정

        max_amplitude = max(abs(self.A.get())+abs(self.k1.get()), abs(self.B.get())+abs(self.k2.get())) # 매개변수에 의한 좌표 표시 가중치 (표시 최적화)
        limit = max_amplitude * 1.2 # 25%의 여유분 지정 (표시 최적화)
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        
        # 범례 생성
        self.ax.legend()
        
        # 그래프 생성
        self.canvas.draw()

    def copy_to_clipboard(self): # 클립보드 복사 함수
        x, y = self.lissajous(self.a.get(), self.b.get(), self.A.get(), self.B.get(), self.i1.get(), self.i2.get(), self.k1.get(), self.k2.get())
        data = "x,y\n" + "\n".join(f"{xi},{yi}" for xi, yi in zip(x, y))  # 데이터 포맷
        self.master.clipboard_clear()  # 클립보드 비우기
        self.master.clipboard_append(data)  # 클립보드에 데이터 추가
        self.master.update()  # 클립보드에 반영

# 루프를 무시하고 우선되는 작업
if __name__ == '__main__':
    root = tk.Tk() # GUI 생성
    app = LissajousApp(root) # 앱 생성
    root.mainloop() # 창 생성