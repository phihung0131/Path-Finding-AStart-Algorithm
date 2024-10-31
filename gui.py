import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from data_structures import GridWithWeights
from pathfinding import a_star_search, reconstruct_path

class PathfindingGUI:
    def __init__(self, root):
        # Thiết lập cửa sổ chính
        self.root = root
        self.root.title("A* Pathfinding")
        
        # Khởi tạo các thuộc tính
        self.grid_size = 10
        self.cell_size = 50
        self.grid = GridWithWeights(self.grid_size, self.grid_size)
        self.start = None
        self.goal = None
        self.path = None
        self.came_from = {}

        # Tạo frame chứa các điều khiển kích thước
        self._setup_size_controls()
        
        # Tạo canvas để vẽ lưới
        self.canvas = tk.Canvas(root, width=self.grid_size * self.cell_size, 
                              height=self.grid_size * self.cell_size)
        self.canvas.pack(side="left")
        
        # Tạo panel chứa các nút điều khiển
        self._setup_control_panel()
        
        # Vẽ lưới ban đầu
        self.draw_grid()

    def _setup_size_controls(self):
        """Tạo các điều khiển để thay đổi kích thước lưới"""
        size_frame = ttk.LabelFrame(self.root, text="Kích thước lưới")
        size_frame.pack(side="top", padx=5, pady=5)

        # Input chiều rộng, cao
        for i, text in enumerate(["Rộng:", "Cao:"]):
            ttk.Label(size_frame, text=text).grid(row=0, column=i*2, padx=5)
            var = tk.StringVar(value="10")
            setattr(self, f"{'width' if i==0 else 'height'}_var", var)
            ttk.Entry(size_frame, textvariable=var, width=10).grid(row=0, column=i*2+1)

        # Nút áp dụng
        ttk.Button(size_frame, text="Áp dụng", command=self.apply_size).grid(row=0, column=4, padx=5)

    def _setup_control_panel(self):
        """Tạo panel chứa các nút điều khiển"""
        panel = ttk.Frame(self.root)
        panel.pack(side="right", fill="y", padx=5)

        # Tạo các nút điều khiển
        buttons = [
            ("Đặt điểm đầu", self.set_start),
            ("Đặt điểm đích", self.set_goal),
            ("Thêm tường", self.add_wall),
            ("Đặt trọng số", self.set_weight),
            ("Tìm đường", self.find_path)
        ]
        
        for text, command in buttons:
            ttk.Button(panel, text=text, command=command).pack(pady=2)

    def get_cell_color(self, cell):
        """Xác định màu sắc cho mỗi ô trong lưới"""
        if cell == self.start:
            return "green"
        elif cell == self.goal:
            return "red"
        elif cell in self.grid.walls:
            return "gray"
        elif self.path and cell in self.path:
            return "yellow"
        else:
            return "white"
        
    def _draw_arrow(self, cell, x1, y1, x2, y2):
        """Vẽ mũi tên chỉ hướng đi cho ô"""
        if self.came_from and cell in self.came_from:
            next_cell = self.came_from[cell]
            if next_cell:
                # Tính hướng di chuyển
                dx = next_cell[0] - cell[0]
                dy = next_cell[1] - cell[1]
                
                # Xác định ký tự mũi tên
                arrow = ""
                if dx == 1: arrow = "→"
                elif dx == -1: arrow = "←"
                elif dy == 1: arrow = "↓"
                elif dy == -1: arrow = "↑"
                
                # Vẽ mũi tên lên canvas
                if arrow:
                    self.canvas.create_text(
                        (x1 + x2)/2,
                        (y1 + y2)/2,
                        text=arrow,
                        font=('Arial', 12, 'bold')
                    )
        
    def draw_grid(self):
        """Vẽ lưới với các thành phần"""
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Tính toạ độ cho mỗi ô
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                cell = (i, j)

                # Vẽ ô với màu tương ứng
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=self.get_cell_color(cell))

                # Hiển thị trọng số nếu có
                if cell in self.grid.weights:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2,
                                          text=str(self.grid.weights[cell]))

                # Hiển thị mũi tên chỉ hướng nếu có
                self._draw_arrow(cell, x1, y1, x2, y2)

    def setup_grid(self):
        """Khởi tạo lưới mới với kích thước đã chọn"""
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            
            # Cập nhật kích thước grid
            self.grid = GridWithWeights(width, height)
            self.grid_size = max(width, height)
            
            # Cập nhật kích thước canvas
            canvas_width = width * self.cell_size
            canvas_height = height * self.cell_size
            self.canvas.configure(width=canvas_width, height=canvas_height)
            
            # Reset các giá trị
            self.start = None
            self.goal = None
            self.path = None
            self.came_from = None  # Thêm dòng này
            
            # Vẽ lại grid
            self.draw_grid()
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid grid dimensions!")

    def apply_size(self):
        """Áp dụng kích thước mới cho lưới"""
        # Xóa hết nội dung cũ
        self.canvas.delete("all")
        # Khởi tạo lưới mới
        self.setup_grid()

    def set_start(self):
        def on_click(event):
            # Chuyển đổi tọa độ click sang tọa độ grid
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            self.start = (x, y)
            self.canvas.unbind("<Button-1>")
            self.draw_grid()
        
        self.canvas.bind("<Button-1>", on_click)

    def set_goal(self):
        def on_click(event):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            self.goal = (x, y)
            self.canvas.unbind("<Button-1>")
            self.draw_grid()
        
        self.canvas.bind("<Button-1>", on_click)

    def add_wall(self):
        def on_click(event):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            cell = (x, y)
            if cell in self.grid.walls:
                self.grid.walls.remove(cell)
            else:
                self.grid.walls.append(cell)
            self.draw_grid()
        
        self.canvas.bind("<Button-1>", on_click)

    def set_weight(self):
        """Thiết lập trọng số cho ô"""
        def on_click(event):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            cell = (x, y)
            
            # Tạo dialog để nhập trọng số
            weight = tk.simpledialog.askfloat("Set Weight", 
                                            "Enter weight for cell ({}, {}):".format(x, y),
                                            minvalue=1)
            if weight:
                self.grid.weights[cell] = weight
            else:
                self.grid.weights.pop(cell, None)
            
            self.draw_grid()
            
        self.canvas.bind("<Button-1>", on_click)
        
    def show_result(self, path, cost_so_far):
        """Hiển thị kết quả trong cửa sổ mới"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Path Result")

        # Tổng chi phí
        total_cost = cost_so_far[self.goal] if self.goal in cost_so_far else 0
        ttk.Label(result_window, 
                 text=f"Total Cost: {total_cost:.2f}",
                 font=('Arial', 12, 'bold')).pack(pady=5)

        # Hiển thị đường đi
        path_text = "Path: " + " -> ".join([f"({x},{y})" for x, y in path])
        ttk.Label(result_window, text=path_text, wraplength=400).pack(pady=5)

        # Canvas để vẽ lưới kết quả
        result_canvas = tk.Canvas(
            result_window,
            width=self.grid_size * 30,  # Kích thước nhỏ hơn
            height=self.grid_size * 30
        )
        result_canvas.pack(pady=5)

        # Vẽ lưới kết quả
        cell_size = 30
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                x1 = i * cell_size
                y1 = j * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                cell = (i, j)
                
                # Màu sắc và hiển thị tương tự như draw_grid
                fill_color = self.get_cell_color(cell)
                result_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
                
                # Hiển thị chi phí
                if cell in cost_so_far:
                    result_canvas.create_text(
                        (x1 + x2)/2,
                        (y1 + y2)/2,
                        text=f"{cost_so_far[cell]:.1f}",
                        font=('Arial', 8)
                    )

    def find_path(self):
        if not hasattr(self, 'start') or not hasattr(self, 'goal'):
            return

        self.came_from, cost_so_far = a_star_search(self.grid, self.start, self.goal)
        
        if self.goal in self.came_from:
            self.path = reconstruct_path(self.came_from, self.start, self.goal)
            self.draw_grid()
            # Hiển thị cửa sổ kết quả
            self.show_result(self.path, cost_so_far)
        else:
            tk.messagebox.showinfo("No Path", "No path found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()