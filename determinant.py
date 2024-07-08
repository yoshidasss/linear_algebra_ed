import tkinter as tk
from tkinter import ttk

class determinant:
    def __init__(self, root):
        self.root = root
        self.root.title("Determinant App")

        # ウィンドウのサイズを取得
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()

        # Canvasを作成
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.X)

        # スケールの定義
        self.scale = 50  # ピクセル単位で1単位とする

        # マトリクスを表示
        self.draw_matrix()
        # 基底ベクトルを表示
        self.draw_basis_vectors()
        # ベクトルの繋ぐ点線を描画
        self.draw_dotted_lines()
        # 行列式を表示
        self.draw_determinant()
        # 行列式を計算
        self.calculate_determinant()

if __name__ == '__main__':
    root = tk.Tk()
    app = determinant(root)
    root.mainloop()