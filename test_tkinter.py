import tkinter as tk
from tkinter import ttk
import math

class AxisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Axis Display App")

        # ウィンドウのサイズを取得
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()

        # Canvasを作成
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height / 2)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.X)

        # スケールの定義
        self.scale = 50  # ピクセル単位で1単位とする

        # x軸とy軸を描画
        self.draw_axes()
        # マトリクスを表示
        self.draw_matrix()
        # 基底ベクトルを表示
        self.draw_basis_vectors()
        # ベクトルの繋ぐ点線を描画
        self.draw_dotted_lines()
        # 行列の入力フォームを作成
        self.create_matrix_input_form()
        # グリッドを描画
        self.draw_grid()

        # イベントバインディング
        self.canvas.tag_bind("i_vector", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("i_vector", "<B1-Motion>", self.drag)
        self.canvas.tag_bind("i_vector", "<ButtonRelease-1>", self.stop_drag)
        self.canvas.tag_bind("j_vector", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("j_vector", "<B1-Motion>", self.drag)
        self.canvas.tag_bind("j_vector", "<ButtonRelease-1>", self.stop_drag)
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.j_text = self.canvas.create_text(0, 0, text="j", anchor=tk.NW)

    def draw_axes(self):
        # x軸を画面の下半分に描画
        self.canvas.create_line(0, self.window_height / 4, self.window_width, self.window_height / 4, arrow=tk.LAST)
        
        # y軸を画面の下半分に描画（上向きにする）
        self.canvas.create_line(self.window_width / 2, self.window_height / 2, self.window_width / 2, 0, arrow=tk.LAST)
        
        # 原点に0を表示
        self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 + 10, text="0", anchor=tk.NW)

    def draw_matrix(self):
        # x軸に1刻みで目盛りを描画
        for i in range(1, int(self.window_width / 2 / self.scale)):
            # 正の方向
            self.canvas.create_line(self.window_width / 2 + i * self.scale, self.window_height / 4 - 5, self.window_width / 2 + i * self.scale, self.window_height / 4 + 5)
            self.canvas.create_text(self.window_width / 2 + i * self.scale, self.window_height / 4 + 10, text=str(i), anchor=tk.N)

            # 負の方向
            self.canvas.create_line(self.window_width / 2 - i * self.scale, self.window_height / 4 - 5, self.window_width / 2 - i * self.scale, self.window_height / 4 + 5)
            self.canvas.create_text(self.window_width / 2 - i * self.scale, self.window_height / 4 + 10, text=str(-i), anchor=tk.N)

        # y軸に1刻みで目盛りを描画
        for i in range(1, int(self.window_height / 4 / self.scale)):
            # 正の方向
            self.canvas.create_line(self.window_width / 2 - 5, self.window_height / 4 - i * self.scale, self.window_width / 2 + 5, self.window_height / 4 - i * self.scale)
            self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 - i * self.scale, text=str(i), anchor=tk.W)

            # 負の方向
            self.canvas.create_line(self.window_width / 2 - 5, self.window_height / 4 + i * self.scale, self.window_width / 2 + 5, self.window_height / 4 + i * self.scale)
            self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 + i * self.scale, text=str(-i), anchor=tk.W)

    def draw_basis_vectors(self):
        # 基底ベクトルを描画（太線で赤色）
        self.basis_vector_length = self.scale  # 基底ベクトルの長さをスケールに基づいて設定

        # x軸の基底ベクトル（iベクトル）
        self.i_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                 self.window_width / 2 + self.basis_vector_length, self.window_height / 4,
                                                 arrow=tk.LAST, fill='red', width=3, tags="i_vector")
        self.i_text = self.canvas.create_text(self.window_width / 2 + self.basis_vector_length + 10, self.window_height / 4 - 10,
                                text="i", fill='red', anchor=tk.NW)

        # y軸の基底ベクトル（jベクトル）
        self.j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                 self.window_width / 2, self.window_height / 4 - self.basis_vector_length,
                                                 arrow=tk.LAST, fill='red', width=3, tags="j_vector")
        self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 - self.basis_vector_length - 10,
                                text="j", fill='red', anchor=tk.NW)

        # 基底ベクトルの和を示すベクトル（i + j）
        self.i_j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                   self.window_width / 2 + self.basis_vector_length, self.window_height / 4 - self.basis_vector_length,
                                                   arrow=tk.LAST, fill='green', width=3, tags="i_j_vector")
        self.i_j_text = self.canvas.create_text(self.window_width / 2 + self.basis_vector_length + 10, self.window_height / 4 - self.basis_vector_length - 10,
                                                 text="i + j", fill='green', anchor=tk.NW)

    def draw_dotted_lines(self):
        # ベクトルiの終点からベクトルi+jの終点への点線を描画
        x1, y1 = self.canvas.coords(self.i_vector)[2], self.canvas.coords(self.i_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.i_dotted_line = self.canvas.create_line(x1, y1, x2, y2, fill='blue', dash=(3, 3), tags="i_dotted_line")

        # ベクトルjの終点からベクトルi+jの終点への点線を描画
        x1, y1 = self.canvas.coords(self.j_vector)[2], self.canvas.coords(self.j_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.j_dotted_line = self.canvas.create_line(x1, y1, x2, y2, fill='blue', dash=(3, 3), tags="j_dotted_line")

        # 紫の点線を描画
        self.draw_purple_dotted_lines()


    def update_dotted_lines(self):
        # ベクトルiの終点からベクトルi+jの終点への点線を更新
        x1, y1 = self.canvas.coords(self.i_vector)[2], self.canvas.coords(self.i_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.canvas.coords(self.i_dotted_line, x1, y1, x2, y2)

        # ベクトルjの終点からベクトルi+jの終点への点線を更新
        x1, y1 = self.canvas.coords(self.j_vector)[2], self.canvas.coords(self.j_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.canvas.coords(self.j_dotted_line, x1, y1, x2, y2)

        # 紫の点線を更新
        self.draw_purple_dotted_lines

    def create_matrix_input_form(self):
        # マトリクスの入力フォームを作成
        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.pack(side=tk.TOP, pady=10)

        # 入力フィールドを作成
        self.matrix_entries = []
        for i in range(2):
            row_entries = []
            for j in range(2):
                entry = ttk.Entry(self.matrix_frame, width=10)
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        # Submitボタン
        self.submit_button = ttk.Button(self.matrix_frame, text="Submit", command=self.submit_matrix)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def draw_grid(self):
        # グリッドを描画
        for i in range(1, int(self.window_width / (2 * self.scale))):
            # 第一象限
            x = self.window_width / 2 + i * self.scale
            self.canvas.create_line(x, 0, x, self.window_height / 2, dash=(1, 2), fill='gray')
            # 第二象限
            x = self.window_width / 2 - i * self.scale
            self.canvas.create_line(x, 0, x, self.window_height / 2, dash=(1, 2), fill='gray')

        self.draw_purple_dotted_lines()

    def draw_purple_dotted_lines(self):
        # 既存の紫の点線を削除
        for item in self.canvas.find_withtag("purple_dotted_line"):
            self.canvas.delete(item)

        # 紫の点線をx軸と平行に描画
        num_lines = int(self.window_height / (2 * self.scale))  # 描画する紫の点線の数
        for i in range(-num_lines, num_lines + 1):
            y = self.window_height / 4 + i * self.scale
            self.canvas.create_line(0, y, self.window_width, y, fill='purple', dash=(3, 3), tags="purple_dotted_line")

    def start_drag(self, event):
        # ドラッグの開始
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        # ドラッグ中の動作
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        # ドラッグ対象がi_vectorの終点の場合
        if self.drag_data["item"] == self.i_vector:
            x1, y1 = self.canvas.coords(self.i_vector)[:2]
            x2, y2 = self.canvas.coords(self.i_vector)[2:]
            self.canvas.coords(self.i_vector, x1, y1, x2 + dx, y2 + dy)
            self.canvas.coords(self.i_text, x2 + dx + 10, y2 + dy - 10)

            # i+jベクトルの終点を更新
            x_j, y_j = self.canvas.coords(self.j_vector)[2], self.canvas.coords(self.j_vector)[3]
            self.canvas.coords(self.i_j_vector, x1, y1, x2 + dx + (x_j - self.window_width / 2), y2 + dy + (y_j - self.window_height / 4))
            self.canvas.coords(self.i_j_text, x2 + dx + 10 + (x_j - self.window_width / 2), y2 + dy - 10 + (y_j - self.window_height / 4))
            self.update_dotted_lines()

        # ドラッグ対象がj_vectorの終点の場合
        elif self.drag_data["item"] == self.j_vector:
            x1, y1 = self.canvas.coords(self.j_vector)[:2]
            x2, y2 = self.canvas.coords(self.j_vector)[2:]
            self.canvas.coords(self.j_vector, x1, y1, x2 + dx, y2 + dy)
            self.canvas.coords(self.j_text, x2 + dx + 10, y2 + dy - 10)

            # i+jベクトルの終点を更新
            x_i, y_i = self.canvas.coords(self.i_vector)[2], self.canvas.coords(self.i_vector)[3]
            self.canvas.coords(self.i_j_vector, x1, y1, x_i + dx + (x2 - self.window_width / 2), y_i + dy + (y2 - self.window_height / 4))
            self.canvas.coords(self.i_j_text, x_i + dx + 10 + (x2 - self.window_width / 2), y_i - 10 + (y2 - self.window_height / 4))
            self.update_dotted_lines()

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        # ドラッグの終了
        self.drag_data["item"] = None

    def submit_matrix(self):
        # 行列を取得して表示
        matrix = []
        for row_entries in self.matrix_entries:
            row = []
            for entry in row_entries:
                row.append(float(entry.get()))
            matrix.append(row)
        print("Submitted Matrix:", matrix)

if __name__ == "__main__":
    root = tk.Tk()
    app = AxisApp(root)
    root.mainloop()



