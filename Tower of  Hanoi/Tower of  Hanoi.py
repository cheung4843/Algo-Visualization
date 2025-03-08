from manim import *
from numpy import array
from math import log2

config.background_color = "#3B4252"

red = "#BF616A"
orange = "#D08770"
yellow = "#EBCB8B"
green = "#A3BE8C"
purple = "#B48EAD"
gray = "#D8DEE9"
white = "#ECEFF4"


class Test(Scene):
    def construct(self):
        self.add_sound("sound/relaxing.mp3")
        b_peg = Rectangle(height=6, width=0.5, color=gray, fill_color=gray,
                          fill_opacity=0.1).set_z_index(0.5)
        a_peg = Rectangle(height=6, width=0.5, color=gray, fill_color=gray,
                          fill_opacity=0.1).set_z_index(0.5)
        c_peg = Rectangle(height=6, width=0.5, color=gray, fill_color=gray,
                          fill_opacity=0.1).set_z_index(0.5)
        pegs = VGroup(a_peg, b_peg, c_peg)
        self.play(Create(pegs), run_time=2)
        self.play(a_peg.animate.move_to(b_peg.get_center() + LEFT * 4),
                  c_peg.animate.move_to(b_peg.get_center() + RIGHT * 4))

        src_tex = MathTex("\\text{Source}").next_to(a_peg.get_bottom(), DOWN)
        aux_tex = MathTex("\\text{Auxiliary}").next_to(b_peg.get_bottom(), DOWN)
        tar_tex = MathTex("\\text{Target}").next_to(c_peg.get_bottom(), DOWN)

        name = VGroup(src_tex, aux_tex, tar_tex)
        self.play(Write(name), run_time=2)

        self.wait(1)

        disk_1 = RoundedRectangle(height=1, width=2, color=red, fill_color=red, fill_opacity=0.1,
                                  stroke_opacity=1).move_to(a_peg.get_top() + DOWN * 0.5)
        disk_2 = RoundedRectangle(height=1, width=2.5, color=orange, fill_color=orange, fill_opacity=0.1,
                                  stroke_opacity=1).next_to(disk_1,
                                                            DOWN)
        disk_3 = RoundedRectangle(height=1, width=3, color=yellow, fill_color=yellow, fill_opacity=0.1,
                                  stroke_opacity=1).next_to(disk_2,
                                                            DOWN)
        disk_4 = RoundedRectangle(height=1, width=3.5, color=green, fill_color=green, fill_opacity=0.1,
                                  stroke_opacity=1).next_to(disk_3,
                                                            DOWN)
        disk_5 = RoundedRectangle(height=1, width=4, color=purple, fill_color=purple, fill_opacity=0.1,
                                  stroke_opacity=1).next_to(disk_4,
                                                            DOWN)

        disks = VGroup(disk_1, disk_2, disk_3, disk_4, disk_5)
        self.play(Create(disks), run_time=2)

        # from the bottom to the top
        a_disk_pos = list(map(lambda x: x.get_center(), (disk_5, disk_4, disk_3, disk_2, disk_1)))
        # print(a_disk_pos)
        b_disk_pos = [array([0., -2.5, 0.]), array([0., -1.25, 0.]), array([0., 0., 0.]), array([0., 1.25, 0.]),
                      array([0., 2.5, 0.])]
        c_disk_pos = [array([4., -2.5, 0.]), array([4., -1.25, 0.]), array([4., 0., 0.]), array([4., 1.25, 0.]),
                      array([4., 2.5, 0.])]

        disk_pos = {'A': a_disk_pos, 'B': b_disk_pos, 'C': c_disk_pos}
        towers = {'A': [disk_5, disk_4, disk_3, disk_2, disk_1], 'B': [], 'C': []}

        msg = Tex().to_edge(UR)
        status = Tex().to_edge(UL)
        steps = Tex().move_to(tar_tex.get_right())
        text = VGroup(msg, status, steps)

        def move_to(src, tar, step):
            top = towers[src].pop()
            towers[tar].append(top)
            self.play(top.animate.move_to(disk_pos[tar][len(towers[tar]) - 1]),
                      Transform(msg, Tex(f'{src} to {tar}').to_edge(UR)),
                      Transform(status,
                                Tex(f'{len(towers["A"])}, {len(towers["B"])}, {len(towers["C"])}').to_edge(UL)),
                      Transform(steps, Tex(f'{step}').move_to(tar_tex.get_right() + RIGHT * 1.3)))

        operations = [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C'), ('A', 'B'),
                      ('C', 'B'), ('C', 'A'), ('B', 'A'), ('C', 'B'), ('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'),
                      ('B', 'A'), ('B', 'C'), ('A', 'C'), ('B', 'A'), ('C', 'B'), ('C', 'A'), ('B', 'A'), ('B', 'C'),
                      ('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]

        for i in range(len(operations)):
            s, t = operations[i]
            move_to(s, t, i + 1)

        self.wait(2)
        self.play(Uncreate(pegs), Unwrite(name), Uncreate(disks), Unwrite(text), run_time=2)
        self.wait(1)

        code = '''
                def Hanoi(n, src, aux, tar):
                    if n == 0:
                        return
                    Hanoi(n - 1, src, tar, aux)
                    print(f'{src} -> {tar})
                    Hanoi(n - 1, aux, src, tar)

                Hanoi(k, 'A', 'B', 'C')
                '''
        rendered_code = Code(code=code, tab_width=4, background="rectangle",
                             language="Python", font="Monospace", style="monokai", insert_line_no=False).scale(0.7)
        self.play(Write(rendered_code), run_time=3)
        self.play(rendered_code.animate.move_to(LEFT * 3.5 + UP * 1.5))
        code_title = MathTex("\\text{Code}").next_to(rendered_code, UP)
        self.play(Write(code_title))
        self.wait(1)

        t1 = MathTex("\\text{T}(1)=1", font_size=30)
        self.play(Write(t1))
        t2 = MathTex("\\text{T}(2)=2\\text{T}(1)+1=2+1}", font_size=30).align_to(t1.get_left(), LEFT).shift(
            DOWN * 0.6)
        self.play(Write(t2))
        t3 = MathTex("\\text{T}(3)=2\\text{T}(2)+1=2^{2}+2+1", font_size=30).align_to(t1.get_left(), LEFT).shift(
            DOWN * 1.2)
        self.play(Write(t3))
        dots = MathTex("\\vdots", font_size=30).shift(DOWN * 1.8)
        self.play(Write(dots))
        tn = MathTex(
            r"\text{T}(n) &= 2\text{T}(n-1)+1=2^{n-1}+2^{n-2}+\cdots +1 \\ &= \frac{(2^{n}-1)}{2-1} \\ &= 2^{n}-1",
            font_size=30).align_to(t2.get_left(),
                                   LEFT).shift(
            DOWN * 3)
        self.play((Write(tn)))
        equations = VGroup(t1, t2, t3, dots, tn)
        box = SurroundingRectangle(equations, color=white, corner_radius=0.2, buff=MED_SMALL_BUFF - 0.1)
        self.play(Create(box))
        step_title = MathTex("\\text{Formula}").move_to([-code_title.get_x(), code_title.get_y(), 0])
        eq_block = equations + box
        self.play(Write(step_title))
        self.play(eq_block.animate.next_to(step_title, DOWN))
        self.wait(1)

        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 32, 4],
            tips=False,
            axis_config={"include_numbers": True},
            x_length=5,
            y_length=5
        ).scale(0.6).next_to(rendered_code, DOWN * 3)
        self.play(DrawBorderThenFill(ax))

        graph1 = ax.plot(lambda x: 2 ** x, x_range=[0, 5], use_smoothing=False, color=red)
        graph2 = ax.plot(lambda x: x, x_range=[0, 5], use_smoothing=False, color=yellow)
        graph3 = ax.plot(lambda x: x * log2(x), x_range=[1, 5], use_smoothing=False, color=green)
        graph = VGroup(graph1, graph3, graph2)
        self.play(Create(graph))

        fun_lab1 = MathTex("\\mathcal{O}(2^{n})", color=red).next_to(graph1, UP)
        fun_lab2 = MathTex("\\mathcal{O}(n)", color=yellow).next_to(graph2, RIGHT)
        fun_lab3 = MathTex("\\mathcal{O}(n\\log{n})", color=green).next_to(graph3, UR)
        label = VGroup(fun_lab1, fun_lab3, fun_lab2).scale(0.6)
        self.play(Write(label))

        self.wait(2)
        self.play(FadeOut(code_title), FadeOut(rendered_code), FadeOut(step_title), FadeOut(eq_block), FadeOut(ax),
                  FadeOut(graph), FadeOut(label))
        self.wait(1)