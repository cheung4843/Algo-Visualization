from heapq import heappop, heappush

from manim import *
from random import shuffle, seed

config.background_color = "#3B4252"

red = "#BF616A"
orange = "#D08770"
yellow = "#EBCB8B"
green = "#A3BE8C"
purple = "#B48EAD"
gray = "#D8DEE9"
white = "#ECEFF4"

seed(4843)


class Cell(VGroup):
    def __init__(self, i: int, j: int, cell_size: float = 1, **kwargs):
        super().__init__(**kwargs)
        self.x, self.y = i, j
        self.wall = {"Top": True, "Right": True, "Down": True, "Left": True}
        self.wall_lines = {"Top": None, "Right": None, "Down": None, "Left": None}
        self.visited = False
        # for tracing back the path
        self.prev_cell = None

        # Create the square and edges based on the specified properties
        self.square = Square(side_length=cell_size, stroke_opacity=0, fill_color="#3B4252",
                             fill_opacity=0.5).set_z_index(
            -1)
        self.add(self.square)

        half_size = cell_size / 2

        top_left = self.square.get_top() + half_size * LEFT
        # self.add(Dot(top_left, color=RED)).set_z(1)
        top_right = self.square.get_top() + half_size * RIGHT
        # self.add(Dot(top_right, color=RED)).set_z(1)
        bottom_left = self.square.get_bottom() + half_size * LEFT
        # self.add(Dot(bottom_left, color=RED)).set_z(1)
        bottom_right = self.square.get_bottom() + half_size * RIGHT
        # self.add(Dot(bottom_right, color=RED)).set_z(1)

        # Create the edges
        if self.wall["Top"]:
            top_edge = Line(top_left, top_right, color=white)
            self.wall_lines["Top"] = top_edge
            self.add(top_edge).set_z_index(1)
        if self.wall["Right"]:
            right_edge = Line(top_right, bottom_right, color=white)
            self.wall_lines["Right"] = right_edge
            self.add(right_edge).set_z_index(1)
        if self.wall["Down"]:
            bottom_edge = Line(bottom_right, bottom_left, color=white)
            self.wall_lines["Down"] = bottom_edge
            self.add(bottom_edge).set_z_index(1)
        if self.wall["Left"]:
            left_edge = Line(bottom_left, top_left, color=white)
            self.wall_lines["Left"] = left_edge
            self.add(left_edge).set_z_index(1)

    def remove_edge(self, edge: str):
        self.wall[edge] = False
        self.remove(self.wall_lines[edge])
        self.wall_lines[edge] = None


class Maze:

    def __init__(self, rows: int, cols: int, cell_size: float = 1):
        self.rows = rows
        self.cols = cols
        self.offset = {"Right": (0, 1), "Down": (1, 0), "Left": (0, -1), "Top": (-1, 0)}
        self.offset_reverse = {"Right": "Left", "Down": "Top", "Left": "Right", "Top": "Down"}
        self.maze = [[Cell(i, j, cell_size) for j in range(self.cols)] for i in range(self.rows)]
        self.maze_display = None
        self.action_steps = []
        self.solution_steps = []
        self.trace_back_steps = []

    def recursive_backtracker(self):
        self.action_steps.clear()
        st = [(0, 0, None)]
        self.maze[0][0].visited = True

        while st:
            cur_x, cur_y, prev_cell_wall_to_remove = st.pop()
            if prev_cell_wall_to_remove:
                self.destroy_wall(cur_x, cur_y, prev_cell_wall_to_remove)

            available_neighbors = []
            for direction in self.offset:
                offset_x, offset_y = self.offset[direction]
                next_x, next_y = cur_x + offset_x, cur_y + offset_y
                if 0 <= next_x < self.rows and 0 <= next_y < self.cols and not self.maze[next_x][next_y].visited:
                    available_neighbors.append((next_x, next_y, direction))
            shuffle(available_neighbors)
            for next_x, next_y, direction in available_neighbors:
                self.maze[next_x][next_y].visited = True
                st.append((next_x, next_y, direction))

    def destroy_wall(self, cur_x, cur_y, prev_direction):
        prev_x, prev_y = cur_x - self.offset[prev_direction][0], cur_y - self.offset[prev_direction][1]
        self.maze[prev_x][prev_y].wall[prev_direction] = False
        cur_direction = self.offset_reverse[prev_direction]
        self.maze[cur_x][cur_y].wall[cur_direction] = False
        self.action_steps.append(((prev_x, prev_y, prev_direction), (cur_x, cur_y, cur_direction)))

    def A_star(self, star_x=0, star_y=0, end_x=None, end_y=None):
        self.solution_steps.clear()
        dis_from_start = [[float("inf") for _ in range(self.cols)] for _ in range(self.rows)]
        # (f_val, (x, y, dis_from_start[x][y]))
        pq = [(0, (star_x, star_y, 0))]

        while pq:
            f_val, (cur_x, cur_y, cur_dis) = heappop(pq)
            dis_from_start[cur_x][cur_y] = cur_dis
            self.solution_steps.append((cur_x, cur_y, cur_dis, self.maze[cur_x][cur_y].prev_cell))
            if cur_x == end_x and cur_y == end_y:
                return
            for direction in self.offset:
                offset_x, offset_y = self.offset[direction]
                next_x, next_y = cur_x + offset_x, cur_y + offset_y
                if 0 <= next_x < self.rows and 0 <= next_y < self.cols and not self.maze[cur_x][cur_y].wall[direction]:
                    if dis_from_start[next_x][next_y] > cur_dis + 1:
                        self.maze[next_x][next_y].prev_cell = (cur_x, cur_y)
                        g, h = cur_dis + 1, (self.rows - 1 - next_x) ** 2 + (self.cols - 1 - next_y) ** 2
                        f = g + h
                        dis_from_start[next_x][next_y] = g
                        heappush(pq, (f, (next_x, next_y, g)))

    def get_maze(self):
        self.recursive_backtracker()
        self.maze_display = VGroup(*[self.maze[i][j] for i in range(self.rows) for j in range(self.cols)])
        self.maze_display.arrange_in_grid(self.rows, self.cols, buff=0)
        return self.maze_display

    def get_action_steps(self):
        return self.action_steps

    def get_solution_steps(self):
        return self.solution_steps

    def get_trace_back_steps(self):
        prev_cell = (self.rows - 1, self.cols - 1)
        while prev_cell:
            self.trace_back_steps.append(prev_cell)
            prev_cell = self.maze[prev_cell[0]][prev_cell[1]].prev_cell
        return self.trace_back_steps


class Figure(ImageMobject):
    def __init__(self, size_scale, file_name, **kwargs):
        ImageMobject.__init__(self, file_name, **kwargs)
        self.scale(size_scale)
        self.current_direction = "Right"
        self.set_z_index(1)
        self.direction = {"Right": 0, "Down": 270 * DEGREES, "Left": 180 * DEGREES, "Top": 90 * DEGREES}

    def set_direction(self, target_direction: str):
        if self.current_direction != target_direction:
            self.rotate(self.direction[target_direction] - self.direction[self.current_direction])
            self.current_direction = target_direction


class Test(Scene):
    def construct(self):
        SIZE = 0.6
        # Maze Animation
        graph = Maze(12, 20, cell_size=SIZE)
        maze_display = graph.get_maze()
        self.play(Create(maze_display), run_time=graph.rows * graph.cols * 0.025)
        self.wait()

        action_steps = graph.get_action_steps()
        with open('action_steps.txt', 'w') as f:
            for action in action_steps:
                f.write(str(action) + '\n')

        # Maze Generation Animation
        pac_man = Figure(SIZE * 0.1, "images\\pacman.png").move_to(graph.maze[0][0].get_center())
        self.add(pac_man)

        for action in action_steps:
            cur_x, cur_y, cur_edge_to_be_remove = action[0]
            next_x, next_y, next_edge_to_be_remove = action[1]
            pac_man.move_to(graph.maze[cur_x][cur_y].get_center())
            pac_man.set_direction(cur_edge_to_be_remove)
            self.play(FadeOut(graph.maze[cur_x][cur_y].wall_lines[cur_edge_to_be_remove]),
                      FadeOut(graph.maze[next_x][next_y].wall_lines[next_edge_to_be_remove]),
                      run_time=0.1)
            graph.maze[cur_x][cur_y].remove_edge(cur_edge_to_be_remove)
            graph.maze[next_x][next_y].remove_edge(next_edge_to_be_remove)

        self.wait(2)
        self.play(FadeOut(pac_man), run_time=1)
        self.wait(2)

        # A* Animation
        graph.A_star(end_x=graph.rows - 1, end_y=graph.cols - 1)
        solution_steps = graph.get_solution_steps()
        solution_steps_VGroup = VGroup()
        for step in solution_steps:
            x, y, dis, _ = step
            dis_tex = Tex(str(dis)).set_color(white).scale(0.8).move_to(graph.maze[x][y].get_center())
            solution_steps_VGroup.add(dis_tex)
            self.play(Create(dis_tex), run_time=0.1)

        self.wait(2)

        # Trace Back Animation
        graph.maze[-1][-1].square.set_color(orange)
        red_ghost = Figure(0.25 * SIZE, "images\\red_ghost.png").move_to(graph.maze[0][0].get_center())
        self.add(red_ghost)
        trace_back_steps = graph.get_trace_back_steps()
        for step in trace_back_steps[::-1]:
            x, y = step
            graph.maze[x][y].square.set_color(red)
            red_ghost.move_to(graph.maze[x][y].get_center())
            self.play(graph.maze[x][y].square.animate.scale(0.8), run_time=0.1)

        self.wait(2)
        self.play(FadeOut(maze_display), FadeOut(solution_steps_VGroup), FadeOut(red_ghost), run_time=2)
        self.wait(2)

        # Code Animation
        full_code = '''
        def recursive_backtracker(self):
            st = [(0, 0, None)]
            self.maze[0][0].visited = True
    
            while st:
                cur_x, cur_y, prev_cell_wall_to_remove = st.pop()
                if prev_cell_wall_to_remove:
                    self.destroy_wall(cur_x, cur_y, prev_cell_wall_to_remove)
    
                available_neighbors = []
                for direction in self.offset:
                    offset_x, offset_y = self.offset[direction]
                    next_x, next_y = cur_x + offset_x, cur_y + offset_y
                    if 0 <= next_x < self.rows and 0 <= next_y < self.cols and not self.maze[next_x][next_y].visited:
                        available_neighbors.append((next_x, next_y, direction))
                shuffle(available_neighbors)
                for next_x, next_y, direction in available_neighbors:
                    self.maze[next_x][next_y].visited = True
                    st.append((next_x, next_y, direction))

        def destroy_wall(self, cur_x, cur_y, prev_direction):
            prev_x, prev_y = cur_x - self.offset[prev_direction][0], cur_y - self.offset[prev_direction][1]
            self.maze[prev_x][prev_y].wall[prev_direction] = False
            cur_direction = self.offset_reverse[prev_direction]
            self.maze[cur_x][cur_y].wall[cur_direction] = False
            self.action_steps.append(((prev_x, prev_y, prev_direction), (cur_x, cur_y, cur_direction)))
    
        def A_star(self, star_x=0, star_y=0, end_x=None, end_y=None):
            self.solution_steps.clear()
            dis_from_start = [[float("inf") for _ in range(self.cols)] for _ in range(self.rows)]
            # (f_val, (x, y, dis_from_start[x][y]))
            pq = [(0, (star_x, star_y, 0))]
    
            while pq:
                f_val, (cur_x, cur_y, cur_dis) = heappop(pq)
                dis_from_start[cur_x][cur_y] = cur_dis
                self.solution_steps.append((cur_x, cur_y, cur_dis, self.maze[cur_x][cur_y].prev_cell))
                if cur_x == end_x and cur_y == end_y:
                    return
                for direction in self.offset:
                    offset_x, offset_y = self.offset[direction]
                    next_x, next_y = cur_x + offset_x, cur_y + offset_y
                    if 0 <= next_x < self.rows and 0 <= next_y < self.cols and not self.maze[cur_x][cur_y].wall[direction]:
                        if dis_from_start[next_x][next_y] > cur_dis + 1:
                            self.maze[next_x][next_y].prev_cell = (cur_x, cur_y)
                            g, h = cur_dis + 1, (self.rows - 1 - next_x) ** 2 + (self.cols - 1 - next_y) ** 2
                            f = g + h
                            dis_from_start[next_x][next_y] = g
                            heappush(pq, (f, (next_x, next_y, g)))
        '''
        rendered_code = Code(code=full_code, style="monokai", language="python",
                             tab_width=4,
                             background="window", font="Monospace", insert_line_no=False,
                             line_spacing=0.4).scale(0.4).to_corner(UL)

        self.play(Write(rendered_code), run_time=10)

        maze_generation_tex = Tex("Maze Generation", color=green).scale(0.8).move_to(
            rendered_code.get_right() + RIGHT * 2 + UP * 1.5)
        recursive_backtracker_tex = Tex("Recursive Backtracker", color=yellow).scale(0.5).next_to(maze_generation_tex,
                                                                                                  DOWN)
        maze_generation_VGroup = VGroup(maze_generation_tex, recursive_backtracker_tex)
        self.play(Write(maze_generation_VGroup), run_time=2)

        maze_solution_tex = Tex("Maze Solution", color=green).scale(0.8).move_to(
            rendered_code.get_right() + RIGHT * 2 + DOWN * 1.5)
        a_star_tex = Tex("A* Search", color=yellow).scale(0.5).next_to(maze_solution_tex, DOWN)

        maze_solution_VGroup = VGroup(maze_solution_tex, a_star_tex)
        self.play(Write(maze_solution_VGroup), run_time=2)

        self.play(Circumscribe(maze_generation_VGroup, color=yellow, fade_out=True), run_time=0.5)
        self.play(Circumscribe(maze_solution_VGroup, color=yellow, fade_out=True), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(rendered_code), FadeOut(maze_generation_VGroup), FadeOut(maze_solution_VGroup), run_time=2)
        self.wait(2)
