# File: data_structures.py
from typing import TypeVar, List, Tuple
import heapq

# Định nghĩa các kiểu dữ liệu
GridLocation = Tuple[int, int]  # (x, y)
Location = TypeVar('Location')  # Generic type cho location

# Class PriorityQueue - Hàng đợi ưu tiên
class PriorityQueue:
    def __init__(self):
        # Khởi tạo list rỗng để lưu các phần tử (priority, location)
        self.elements: List[Tuple[float, Location]] = []
    
    def empty(self) -> bool:
        # Kiểm tra hàng đợi có rỗng không
        return not self.elements
    
    def put(self, item: Location, priority: float):
        # Thêm item vào hàng đợi với độ ưu tiên priority
        # Sử dụng heapq để tự động sắp xếp theo priority
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> Location:
        # Lấy ra và xóa item có priority thấp nhất
        # [1] để lấy location, bỏ qua priority
        return heapq.heappop(self.elements)[1]

# Class GridWithWeights - Lưới 2D có trọng số
class GridWithWeights:
    def __init__(self, width: int, height: int):
        self.width = width      # Chiều rộng lưới
        self.height = height    # Chiều cao lưới
        self.walls = []         # List các ô tường không đi qua được
        self.weights = {}       # Dict lưu trọng số của mỗi ô
    
    def in_bounds(self, id: GridLocation) -> bool:
        # Kiểm tra tọa độ id có nằm trong lưới không
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        # Kiểm tra có thể đi qua ô id không (không phải tường)
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> List[GridLocation]:
        # Trả về list các ô kề có thể đi tới từ ô id
        (x, y) = id
        # Xét 4 ô kề theo 4 hướng
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        # Lọc ra các ô hợp lệ (trong lưới và không phải tường)
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)
    
    def cost(self, from_id: GridLocation, to_id: GridLocation) -> float:
        # Trả về chi phí di chuyển từ from_id đến to_id
        # Nếu to_id có trong weights thì lấy giá trị đó
        # Nếu không thì chi phí mặc định là 1
        return self.weights.get(to_id, 1)
