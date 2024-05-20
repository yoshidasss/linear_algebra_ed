import tkinter as tk
from tkinter import ttk

class AxisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Axis Display App")

        # ウィンドウのサイズを取得
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()

        # Canvasを作成
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height/1.7)
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
        self.draw_extra_grid()

        # イベントバインディング
        """ self.canvas.tag_bind("i_vector", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("i_vector", "<B1-Motion>", self.drag)
        self.canvas.tag_bind("i_vector", "<ButtonRelease-1>", self.stop_drag)
        self.canvas.tag_bind("j_vector", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("j_vector", "<B1-Motion>", self.drag)
        self.canvas.tag_bind("j_vector", "<ButtonRelease-1>", self.stop_drag) """
        #self.drag_data = {"x": 0, "y": 0, "item": None}

    # x軸とy軸の描画
    def draw_axes(self):
        self.canvas.create_line(0, self.window_height / 4, self.window_width, self.window_height / 4, arrow=tk.LAST)
        self.canvas.create_line(self.window_width / 2, self.window_height / 2, self.window_width / 2, 0, arrow=tk.LAST)
        self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 + 10, text="0", anchor=tk.NW)
        # y軸の描画
        self.canvas.create_line(self.window_width / 2, 0, self.window_width / 2, self.window_height, arrow=tk.LAST)
        self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 * 3 + 10, text="0", anchor=tk.NW)

    # 行列の目盛りの描画
    def draw_matrix(self):
        for i in range(1, int(self.window_width / 2 / self.scale)):
            self.canvas.create_line(self.window_width / 2 + i * self.scale, self.window_height / 4 - 5,
                                    self.window_width / 2 + i * self.scale, self.window_height / 4 + 5)
            self.canvas.create_text(self.window_width / 2 + i * self.scale, self.window_height / 4 + 10,
                                    text=str(i), anchor=tk.N)
            self.canvas.create_line(self.window_width / 2 - i * self.scale, self.window_height / 4 - 5,
                                    self.window_width / 2 - i * self.scale, self.window_height / 4 + 5)
            self.canvas.create_text(self.window_width / 2 - i * self.scale, self.window_height / 4 + 10,
                                    text=str(-i), anchor=tk.N)
        for i in range(1, int(self.window_height / 4 / self.scale)):
            self.canvas.create_line(self.window_width / 2 - 5, self.window_height / 4 - i * self.scale,
                                    self.window_width / 2 + 5, self.window_height / 4 - i * self.scale)
            self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 - i * self.scale,
                                    text=str(i), anchor=tk.W)
            self.canvas.create_line(self.window_width / 2 - 5, self.window_height / 4 + i * self.scale,
                                    self.window_width / 2 + 5, self.window_height / 4 + i * self.scale)
            self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 + i * self.scale,
                                    text=str(-i), anchor=tk.W)

    # 基底ベクトルの描画
    def draw_basis_vectors(self):
        self.basis_vector_length = self.scale
        self.i_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                self.window_width / 2 + self.basis_vector_length, self.window_height / 4,
                                                arrow=tk.LAST, fill='red', width=3, tags="i_vector")
        self.i_text = self.canvas.create_text(self.window_width / 2 + self.basis_vector_length + 10,
                                              self.window_height / 4 - 10, text="i", fill='red', anchor=tk.NW)
        self.j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                self.window_width / 2, self.window_height / 4 - self.basis_vector_length,
                                                arrow=tk.LAST, fill='red', width=3, tags="j_vector")
        self.j_text = self.canvas.create_text(self.window_width / 2 + 10, self.window_height / 4 - self.basis_vector_length - 10,
                                              text="j", fill='red', anchor=tk.NW)
        self.i_j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4,
                                                  self.window_width / 2 + self.basis_vector_length,
                                                  self.window_height / 4 - self.basis_vector_length,
                                                  arrow=tk.LAST, fill='green', width=3, tags="i_j_vector")
        self.i_j_text = self.canvas.create_text(self.window_width / 2 + self.basis_vector_length + 10,
                                                self.window_height / 4 - self.basis_vector_length - 10, text="i + j",
                                                fill='green', anchor=tk.NW)

    # 点線の描画
    def draw_dotted_lines(self):
        x1, y1 = self.canvas.coords(self.i_vector)[2], self.canvas.coords(self.i_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.i_dotted_line = self.canvas.create_line(x1, y1, x2, y2, fill='blue', dash=(3, 3), tags="i_dotted_line")
        x1, y1 = self.canvas.coords(self.j_vector)[2], self.canvas.coords(self.j_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.j_dotted_line = self.canvas.create_line(x1, y1, x2, y2, fill='blue', dash=(3, 3), tags="j_dotted_line")

    def update_dotted_lines(self):
        x1, y1 = self.canvas.coords(self.i_vector)[2], self.canvas.coords(self.i_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.canvas.coords(self.i_dotted_line, x1, y1, x2, y2)
        x1, y1 = self.canvas.coords(self.j_vector)[2], self.canvas.coords(self.j_vector)[3]
        x2, y2 = self.canvas.coords(self.i_j_vector)[2], self.canvas.coords(self.i_j_vector)[3]
        self.canvas.coords(self.j_dotted_line, x1, y1, x2, y2)

    # 行列入力フォームの作成
    def create_matrix_input_form(self):
        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.pack(side=tk.TOP, pady=10)
        self.matrix_entries = []
        for i in range(2):
            row_entries = []
            for j in range(2):
                entry = ttk.Entry(self.matrix_frame, width=10)
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
        self.submit_button = ttk.Button(self.matrix_frame, text="Submit", command=self.submit_matrix)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    # グリッドの描画
    def draw_grid(self):
        self.canvas.delete("grid_line")
        i_vector_coords = self.canvas.coords(self.i_vector)
        j_vector_coords = self.canvas.coords(self.j_vector)
        i_x, i_y = i_vector_coords[2] - i_vector_coords[0], i_vector_coords[3] - i_vector_coords[1]
        j_x, j_y = j_vector_coords[2] - j_vector_coords[0], j_vector_coords[3] - j_vector_coords[1]
        grid_range = 20
        origin_x = self.window_width / 2
        origin_y = self.window_height / 4

        for j in range(-grid_range, grid_range + 1):
            # 横向き(第1,4象限)
            start_x = origin_x + j * j_x
            start_y = origin_y + j * j_y
            end_x = start_x + grid_range * i_x
            end_y = start_y + grid_range * i_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", dash=(2, 2), tags="grid_line")
            # 横向き(第2,3象限)
            start_x = origin_x - j * j_x
            start_y = origin_y - j * j_y
            end_x = start_x - grid_range * i_x
            end_y = start_y - grid_range * i_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", dash=(2, 2), tags="grid_line")
            # 縦向き(第3,4象限)
            start_x = origin_x + j * i_x
            start_y = origin_y + j * i_y
            end_x = start_x - grid_range * j_x
            end_y = start_y - grid_range * j_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", dash=(2, 2), tags="grid_line")
            # 縦向き(第1,2象限)
            start_x = origin_x - j * i_x
            start_y = origin_y - j * i_y
            end_x = start_x + grid_range * j_x
            end_y = start_y + grid_range * j_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", dash=(2, 2), tags="grid_line")
    
    # グリッドを描画する別のメソッド
    ## 次にこのメソッドをグラフの最後尾に表示させる
    def draw_extra_grid(self):
        self.canvas.delete("extra_grid_line")
        grid_spacing = 1  # グリッドの間隔を1とする
        x_origin = self.window_width / 2
        y_origin = self.window_height / 4

        # より薄い色を設定
        hex_gray = '#767676'

        # x軸に平行なグリッドを描画
        for i in range(int(-x_origin / self.scale), int(x_origin / self.scale) + 1):
            x = x_origin + i * self.scale
            self.canvas.create_line(x, 0, x, self.window_height, fill=hex_gray, dash=(3, 3), tags="extra_grid_line")

        # y軸に平行なグリッドを描画
        for j in range(int(-y_origin / self.scale), int(y_origin / self.scale) + 1):
            y = y_origin + j * self.scale
            self.canvas.create_line(0, y, self.window_width, y, fill=hex_gray, dash=(3, 3), tags="extra_grid_line")


    """ # ドラッグ開始
    def start_drag(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    # ドラッグ中
    def drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        if self.drag_data["item"] in [self.i_vector, self.j_vector]:
            self.update_dotted_lines()
            self.draw_grid()

    # ドラッグ終了
    def stop_drag(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
 """
    def submit_matrix(self):
        try:
            a = float(self.matrix_entries[0][0].get())
            b = float(self.matrix_entries[0][1].get())
            c = float(self.matrix_entries[1][0].get())
            d = float(self.matrix_entries[1][1].get())
        except ValueError:
            return
        self.canvas.delete(self.i_vector)
        self.canvas.delete(self.i_text)
        self.canvas.delete(self.j_vector)
        self.canvas.delete(self.j_text)
        self.canvas.delete(self.i_j_vector)
        self.canvas.delete(self.i_j_text)
        i_vector_end_x = self.window_width / 2 + a * self.scale
        i_vector_end_y = self.window_height / 4 - b * self.scale
        j_vector_end_x = self.window_width / 2 + c * self.scale
        j_vector_end_y = self.window_height / 4 - d * self.scale
        self.i_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4, i_vector_end_x,
                                                i_vector_end_y, arrow=tk.LAST, fill='red', width=3, tags="i_vector")
        self.i_text = self.canvas.create_text(i_vector_end_x + 10, i_vector_end_y - 10, text="i", fill='red', anchor=tk.NW)
        self.j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4, j_vector_end_x,
                                                j_vector_end_y, arrow=tk.LAST, fill='red', width=3, tags="j_vector")
        self.j_text = self.canvas.create_text(j_vector_end_x + 10, j_vector_end_y - 10, text="j", fill='red', anchor=tk.NW)
        i_j_vector_end_x = i_vector_end_x + c * self.scale
        i_j_vector_end_y = i_vector_end_y - d * self.scale
        self.i_j_vector = self.canvas.create_line(self.window_width / 2, self.window_height / 4, i_j_vector_end_x,
                                                  i_j_vector_end_y, arrow=tk.LAST, fill='green', width=3, tags="i_j_vector")
        self.i_j_text = self.canvas.create_text(i_j_vector_end_x + 10, i_j_vector_end_y - 10, text="i + j",
                                                fill='green', anchor=tk.NW)
        self.update_dotted_lines()
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = AxisApp(root)
    root.mainloop()