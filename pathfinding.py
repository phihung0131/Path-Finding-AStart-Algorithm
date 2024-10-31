# File: pathfinding.py
from typing import Dict, List, Optional, Tuple
from data_structures import GridLocation, GridWithWeights, PriorityQueue, Location

def heuristic(a: GridLocation, b: GridLocation) -> float:
    """Hàm ước lượng khoảng cách Manhattan giữa 2 điểm"""
    (x1, y1) = a  # Tọa độ điểm a
    (x2, y2) = b  # Tọa độ điểm b
    return abs(x1 - x2) + abs(y1 - y2)  # Tổng khoảng cách theo 2 trục x và y

def a_star_search(
    graph: GridWithWeights,  # Lưới 2D có trọng số
    start: GridLocation,     # Điểm xuất phát
    goal: GridLocation       # Điểm đích
) -> Tuple[Dict[GridLocation, Optional[GridLocation]], Dict[GridLocation, float]]:
    """
    Thuật toán A* tìm đường đi ngắn nhất:
    1. Input:
        - graph: Lưới 2D chứa thông tin về tường và trọng số
        - start: Tọa độ điểm xuất phát
        - goal: Tọa độ điểm đích
    2. Output:
        - came_from: Dict lưu node cha của mỗi node (dùng để tái tạo đường đi)
        - cost_so_far: Dict lưu chi phí thực tế để đến mỗi node từ start
    """
    # Khởi tạo frontier (danh sách các node cần xét) với node xuất phát
    frontier = PriorityQueue()  # Hàng đợi ưu tiên sắp xếp theo f = g + h
    frontier.put(start, 0)      # Thêm start vào frontier với priority = 0
    
    # Khởi tạo 2 dict để lưu thông tin đường đi
    came_from: Dict[GridLocation, Optional[GridLocation]] = {}  # Lưu node cha
    cost_so_far: Dict[GridLocation, float] = {}                # Lưu chi phí đến node
    came_from[start] = None     # Node start không có node cha
    cost_so_far[start] = 0      # Chi phí đến start = 0
    
    # Lặp cho đến khi frontier rỗng
    while not frontier.empty():
        current: GridLocation = frontier.get()  # Lấy node có priority thấp nhất
        
        # Nếu đã đến đích thì dừng
        if current == goal:
            break
        
        # Xét tất cả các node kề với node hiện tại
        for next in graph.neighbors(current):
            # Tính chi phí mới để đến next
            new_cost = cost_so_far[current] + graph.cost(current, next)
            
            # Nếu chưa đến next hoặc tìm được đường ngắn hơn
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # Priority = chi phí thực + heuristic
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def reconstruct_path(
    came_from: Dict[Location, Optional[Location]],
    start: Location,
    goal: Location
) -> List[Location]:
    """
    Tái tạo đường đi từ came_from
    Input:
        came_from: Dict lưu parent của mỗi node
        start: Location xuất phát
        goal: Location đích
    Output:
        path: List các location tạo thành đường đi
    """
    current: Location = goal
    path: List[Location] = []
    
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path