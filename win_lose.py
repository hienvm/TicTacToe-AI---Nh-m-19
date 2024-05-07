from collections import deque
from typing import Iterable, Literal


def can_lose(board: list[list[str]], k: int, role: Literal['x', 'o']) -> bool:
    '''Sliding window kích thước k cho từng hàng, cột và đường chéo. Check xem có window nào ko chứa role.'''
    m = len(board)
    n = len(board[0])

    # Check các hàng
    if n >= k:
        for i in range(m):
            if can_lose_ln(k, role,
                           [board[i][j] for j in range(n)]):
                return True

    # Check các cột
    if m >= k:
        for j in range(n):
            if can_lose_ln(k, role,
                           [board[i][j] for i in range(m)]):
                return True

    # Check các đường chéo xuống từ trái sang i - j = c
    for c in range(- n + 1, m - 1):
        # Ta có: 0 <= i < m && i = j + c && 0 <= j < n
        # Suy ra: 0 <= j + c < m && 0 <= j < n
        low = max(0, -c)
        upper = min(m - c, n)
        if upper - low >= k:
            if can_lose_ln(k, role,
                           [board[j + c][j] for j in range(low, upper)]):
                return True

    # Check các đường chéo lên từ trái sang i + j = c
    for c in range(0, m + n - 1):
        # Ta có: 0 <= i < m && i = c - j && 0 <= j < n
        # Suy ra: 0 <= c - j < m && 0 <= j < n
        # Suy ra: c - m < j && j <= c && 0 <= j < n
        low = max(0, c - m + 1)
        upper = min(c + 1, n)
        if upper - low >= k:
            if can_lose_ln(k, role,
                           [board[c - j][j] for j in range(low, upper)]):
                return True

    return False


def can_lose_ln(k: int, role: Literal['x', 'o'], ln: Iterable[str]):
    window = deque(maxlen=k)    # window: một dãy k ô liên tiếp
    # đếm sl các ô của mỗi bên trong window
    op_cnt: int = 0

    # Duyệt từng ô
    for cell in ln:
        # Thêm ô tiếp theo vào cuối window
        window.append(cell)
        if cell == role:
            op_cnt += 1

        if len(window) == k:
            # Check xem có thể win ko
            if op_cnt == 0:
                return True

            # loại bỏ phần tử đầu khi window đã đạt đủ kích thước k
            first = window.popleft()
            if first == role:
                op_cnt -= 1

    return False
