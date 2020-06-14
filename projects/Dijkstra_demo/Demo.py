from Dijkstra_demo.Effects import SizeOutAndSizeIn
from Dijkstra_demo.VertexMap import VertexMap, Table, NumberedCircle
from Dijkstra_demo.func import dijkstra, point_to_pos

from manimlib.imports import *


# 前言
class PreZero(Scene):
    def construct(self):
        dis_m1 = np.array([
            [0, 1, 4, 2, np.inf],
            [1, 0, 2, np.inf, 5],
            [4, 2, 0, 1, np.inf],
            [2, np.inf, 1, 0, 3],
            [np.inf, 5, np.inf, 3, 0]
        ])

        v_map = VertexMap(dis_m=dis_m1).shape_generation()

        v2_map = VertexMap(dis_m=dis_m1).shape_generation(vertex_map=[2, 3, 0, 4, 1])

        v3_map = VertexMap(dis_m=dis_m1).shape_generation(vertex_map=[3, 1, 0, 4, 2])

        v4_map = VertexMap(dis_m=dis_m1).shape_generation(vertex_map=[4, 2, 3, 0, 1])
        
        self.play(ShowCreation(v_map))

        self.wait()

        self.play(
            Succession(
                Transform(v_map, v2_map),
                Transform(v_map, v3_map),
                Transform(v_map, v4_map),
                run_time=3,
                rate_func=smooth
            )
        )


class DemoONE(Scene):
    CONFIG={
        "start_point":(-3.5, .2),
        "end_point":(3.5, -.2),
        "through_point":[(-2.3, -1.8), (1.7, 2.6), (-1.5, .7), (2.6, .8), (1.9, -.8)],
        "dis_m":np.array([
            [0, 1, np.inf, 1, np.inf, np.inf, np.inf],
            [1, 0, 1, np.inf, 3, np.inf, np.inf],
            [np.inf, 1, 0, np.inf, 3, np.inf, np.inf],
            [1, np.inf, np.inf, 0, np.inf, 4, 2],
            [np.inf, 3, 3, np.inf, 0, 2, 3],
            [np.inf, np.inf, np.inf, 4, 2, 0, 5],
            [np.inf, np.inf, np.inf, 2, 3, 5, 0]
        ])
    }
    def construct(self):
        flag = SVGMobject('flag').scale(.4).set_color(RED_A).set_opacity(.7)

        home = SVGMobject('home2').scale(.4).set_color(YELLOW_A).set_opacity(.7)

        doubt = SVGMobject('doubt').scale(.4).set_color(LIGHT_GREY).set_opacity(1)

        flag.move_to(point_to_pos(self.start_point))

        home.move_to(point_to_pos(self.end_point))

        v_map = VertexMap(
            pos_list=[self.start_point, *self.through_point, self.end_point],
            dis_m=self.dis_m,
            fill_opacity=.8
            )

        path_list = [v_map.generate_path(vertex_list, stroke_width=3, stroke_color=YELLOW_D) 
            for vertex_list in [(0, 3, 6), (0, 1, 2,  4, 6), (0, 1, 3, 5, 6)]]

        self.play(
            LaggedStart(
                Write(flag),
                Write(home),
                lag_ratio=.4,
                run_time=1.2),
                )

        self.add_foreground_mobject(flag)
        self.add_foreground_mobject(home)

        self.play(
            LaggedStart(
                *[
                    Succession(
                        ShowCreation(path, run_time=.8),
                        ApplyMethod(path.fade, .5, run_tim=.2)
                    )
                for path in path_list],
                lag_ratio=.5,
                rate_func=smooth
            )
        )

        self.wait()

        self.play(
            Succession(
                *[
                    ApplyMethod(path.set_opacity, .9, run_time=1.2, rate_func=there_and_back)
                     for path in path_list
                ]
            )
        )

        self.play(
            AnimationGroup(
                FadeOutAndShift(flag, LEFT, run_time=.8),
                FadeOutAndShift(home, run_time=.8),
                ApplyMethod(VGroup(*path_list).set_color, LIGHT_GREY, run_time=.4),
                ApplyMethod(VGroup(*path_list).fade, .3, run_time=.4),
                Transform(VGroup(*path_list).copy(), v_map, run_time=1.2)
            )
            
        )

        self.wait(.6)

        link_gro = v_map.generate_links(stroke_width=1.4, stroke_color=YELLOW_D)


        self.play(
            FadeOut(VGroup(*path_list)),
            LaggedStart(
                *[ShowCreation(link) for link in link_gro], 
                lag_ratio=.2
            )
        )



class DemoTWO(Scene):
    CONFIG={
        "start_point":(-3.5, .2),
        "end_point":(3.5, -.2),
        "through_point":[(-2.3, -1.8), (1.7, 2.6), (-1.5, .7), (2.6, .8), (1.9, -.8)],
        "dis_m":np.array([
            [0, 1, np.inf, 1, np.inf, np.inf, np.inf],
            [1, 0, 1, np.inf, 3, np.inf, np.inf],
            [np.inf, 1, 0, np.inf, 3, np.inf, np.inf],
            [1, np.inf, np.inf, 0, np.inf, 4, 2],
            [np.inf, 3, 3, np.inf, 0, 2, 3],
            [np.inf, np.inf, np.inf, 4, 2, 0, 5],
            [np.inf, np.inf, np.inf, 2, 3, 5, 0]
        ])
    }
    def construct(self):
        v_map = VertexMap(
            pos_list=[self.start_point, *self.through_point, self.end_point],
            dis_m=self.dis_m,
            fill_opacity=.8
            )
        v_map.shape_generation()

        self.add(v_map)
        self.wait()
        
        number_array = v_map.get_vertex_numbering(
            add_to_group = True, 
            font="Consolas", 
            stroke_width=.2, 
            color=DARK_GREY)
        self.play(
            LaggedStart(
                *[Write(number, run_time=.7) for number in number_array], 
                lag_ratio=.2
            )
        )

        new_number_array = v_map.get_vertex_numbering(
            add_to_group=False, vertex_map=[1, 2, 0, 4, 3, 6, 5], 
            font="Consolas", 
            stroke_width=.2, 
            color=DARK_GREY
        )

        self.play(
            FadeOutAndShiftDown(VGroup(*number_array)),
            FadeInFrom(VGroup(*new_number_array), UP),
            run_time=.8
        )
        # 不同的标号方式对整个图不会造成实质性的影响

        self.wait()

        self.play(
            FadeOutAndShiftDown(VGroup(*new_number_array)),
            FadeInFrom(VGroup(*number_array), UP),
            run_time=.4
        )

        self.wait()

        labels = v_map.show_all_link_label(font="Consolas", stroke_width=.2, \
            color=LIGHT_GREY, stroke_color=YELLOW)

        self.play(
            LaggedStart(
                *[Write(label, run_time=.7) for label in labels], 
                lag_ratio=.2,
                run_time=1.8
            )
        )


class DemoTHREE(Scene):
    CONFIG={
        "start_point":(-3.5, .2),
        "end_point":(3.5, -.2),
        "through_point":[(-2.3, -1.8), (1.7, 2.6), (-1.5, .7), (2.6, .8), (1.9, -.8)],
        "dis_m":np.array([
            [0, 1, np.inf, 1, np.inf, np.inf, np.inf],
            [1, 0, 1, np.inf, 3, np.inf, np.inf],
            [np.inf, 1, 0, np.inf, 3, np.inf, np.inf],
            [1, np.inf, np.inf, 0, np.inf, 4, 2],
            [np.inf, 3, 3, np.inf, 0, 2, 3],
            [np.inf, np.inf, np.inf, 4, 2, 0, 5],
            [np.inf, np.inf, np.inf, 2, 3, 5, 0]
        ])
    }
    def construct(self):
        v_map = VertexMap(
            pos_list=[self.start_point, *self.through_point, self.end_point],
            dis_m=self.dis_m,
            fill_opacity=.8
            )
        v_map.shape_generation()
        
        number_array = v_map.get_vertex_numbering(
            add_to_group = True, 
            font="Consolas", 
            stroke_width=.2, 
            color=DARK_GREY)

        labels = v_map.show_all_link_label(font="Consolas", stroke_width=.2, \
            color=LIGHT_GREY, stroke_color=YELLOW)
        
        print(len(labels))
        
        self.add(v_map)
        v_map_copy = v_map.copy()

        circle0 = VGroup(v_map.vertex_dict[0], number_array[0]).copy()
        circle1 = VGroup(v_map.vertex_dict[1], number_array[1]).copy()
        link01 = v_map.links['01'].copy()
        link01.generate_target()
        link01.target.set_stroke(width=8)
        label01 = labels[0].copy()
        label01.generate_target()
        label01.target.scale(2.1)
        label01.target.shift(2*SMALL_BUFF)

        circle4 = VGroup(v_map.vertex_dict[4], number_array[4]).copy()
        link14 = v_map.links['14'].copy()
        link14.generate_target()
        link14.target.set_stroke(width=8)
        label14 = labels[3].copy()
        label14.generate_target()
        label14.target.scale(2.1)
        label14.target.shift(2*SMALL_BUFF)
        


        self.add(circle0, circle1, link01, label01)
        self.wait()

        self.play(
            ApplyMethod(v_map.fade, .7, run_time=2.2)
        )

        self.play(
            SizeOutAndSizeIn(circle0),
            SizeOutAndSizeIn(circle1),
            run_time=1.4
        )

        self.play(
            LaggedStart(
                MoveToTarget(link01),
                MoveToTarget(label01)
            )
        )

        self.add(circle4, label14, link14)
        self.play(
            LaggedStart(
                MoveToTarget(link14),
                MoveToTarget(label14)
            )
        )


        self.wait()
        self.clear()
        self.play(ShowCreation(v_map_copy), run_time=1.4)

        v_map.generate_rect_border(color=YELLOW_A, stroke_width=1.2, buff=SMALL_BUFF*3)
        self.play(ShowCreation(v_map.border))

        self.play(
            v_map_copy.scale, .6, 
            v_map_copy.shift, 3.2*LEFT,
            v_map.scale, .6, 
            v_map.shift, 3.2*LEFT, run_time=1.5
        )
        self.wait()

class DemoFOUR(Scene):
    CONFIG={
        "start_point":(-3.5, .2),
        "end_point":(3.5, -.2),
        "through_point":[(-2.3, -1.8), (1.7, 2.6), (-1.5, .7), (2.6, .8), (1.9, -.8)],
        "dis_m":np.array([
            [0, 1, np.inf, 1, np.inf, np.inf, np.inf],
            [1, 0, 1, np.inf, 3, np.inf, np.inf],
            [np.inf, 1, 0, np.inf, 3, np.inf, np.inf],
            [1, np.inf, np.inf, 0, np.inf, 4, 2],
            [np.inf, 3, 3, np.inf, 0, 2, 3],
            [np.inf, np.inf, np.inf, 4, 2, 0, 5],
            [np.inf, np.inf, np.inf, 2, 3, 5, 0]
        ])
    }
    def construct(self):
        v_map = VertexMap(
            pos_list=[self.start_point, *self.through_point, self.end_point],
            dis_m=self.dis_m,
            fill_opacity=.8
            )
        v_map.full_generation()

        
        v_map.generate_rect_border(color=YELLOW_A, stroke_width=1.2, buff=SMALL_BUFF*3)
        v_map.scale(.6)
        v_map.shift(2.6*LEFT)

        self.add(v_map)


        text = TextMobject("Distance\nMap", font="Courier New").scale(1.3).shift(2*RIGHT).set_color(YELLOW_A)

        self.play(
            v_map.fade, .6,
            ReplacementTransform(v_map.copy(), text)
        )

        self.wait()

        # 那么什么是距离矩阵呢

        dis_m_table = Table(self.dis_m, col_title=True, row_title=True).set_all_pos()

        self.play(
            ShowCreation(dis_m_table.mobj_matrix),
            text.shift, 2.6*UP,
            dis_m_table.mobj_matrix.shift, 2*UP
            )

        row_mobjs = [NumberedCircle(i) for i in range(v_map.vertex_count)]
        row_mobjs = dis_m_table.set_row_title(row_mobjs)
        VGroup(*row_mobjs).shift(2*UP)

        col_mobjs = [NumberedCircle(i) for i in range(v_map.vertex_count)]
        col_mobjs = dis_m_table.set_col_title(col_mobjs)
        VGroup(*col_mobjs).shift(2*UP)

        self.wait()

        self.play(
            ReplacementTransform(dis_m_table.mobj_matrix.copy(), VGroup(*row_mobjs)),
            ReplacementTransform(dis_m_table.mobj_matrix.copy(), VGroup(*col_mobjs)),
            ApplyMethod(text.shift, .4*UP),
            run_time=2.2
        )


class DemoFIVE(Scene):
    CONFIG={
        "start_point":(-3.5, .2),
        "end_point":(3.5, -.2),
        "through_point":[(-2.3, -1.8), (1.7, 2.6), (-1.5, .7), (2.6, .8), (1.9, -.8)],
        "dis_m":np.array([
            [0, 1, np.inf, 1, np.inf, np.inf, np.inf],
            [1, 0, 1, np.inf, 3, np.inf, np.inf],
            [np.inf, 1, 0, np.inf, 3, np.inf, np.inf],
            [1, np.inf, np.inf, 0, np.inf, 4, 2],
            [np.inf, 3, 3, np.inf, 0, 2, 3],
            [np.inf, np.inf, np.inf, 4, 2, 0, 5],
            [np.inf, np.inf, np.inf, 2, 3, 5, 0]
        ])
    }
    def construct(self):
        v_map = VertexMap(
            pos_list=[self.start_point, *self.through_point, self.end_point],
            dis_m=self.dis_m,
            fill_opacity=.8
            )
        v_map.full_generation()

        
        v_map.generate_rect_border(color=YELLOW_A, stroke_width=1.2, buff=SMALL_BUFF*3)
        v_map.scale(.6)
        v_map.shift(2.6*LEFT)








        

