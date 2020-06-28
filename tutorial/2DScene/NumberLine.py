from manimlib.imports import *
from SelfTutorial.ScreenGrid.screen_grid import ScreenGrid
from SelfTutorial.DemoClass.DemoClass import DemoClass
from collections import defaultdict


class Scene(Scene):
    CONFIG = {
        "camera_config":{"background_color":"#161616"},
        "include_grid":True
    }
    def setup(self):
        if self.include_grid:
            self.add(ScreenGrid().fade(0.7))


class BasicNumberLine(Scene):
    def construct(self):
        nb_line = NumberLine()

        self.play(ShowCreation(nb_line))


"""
Config of NumberLine

CONFIG = {
        "color": LIGHT_GREY,
        "x_min": -FRAME_X_RADIUS,
        "x_max": FRAME_X_RADIUS,
        "unit_size": 1,
        "include_ticks": True,
        "tick_size": 0.1,
        "tick_frequency": 1,
        # Defaults to value near x_min s.t. 0 is a tick
        # TODO, rename this
        "leftmost_tick": None,
        # Change name
        "numbers_with_elongated_ticks": [0],
        "include_numbers": False,
        "numbers_to_show": None,
        "longer_tick_multiple": 2,
        "number_at_center": 0,
        "number_scale_val": 0.75,
        "label_direction": DOWN,
        "line_to_number_buff": MED_SMALL_BUFF,
        "include_tip": False,
        "tip_width": 0.25,
        "tip_height": 0.25,
        "decimal_number_config": {
            "num_decimal_places": 0,
        },
        "exclude_zero_from_default_numbers": False,
    }
"""

class XminandXmax(Scene):
    def construct(self):
        nb_line_demo = DemoClass(
            NumberLine().set_color(YELLOW),
            attrs={
                "x_min":(-4, 2.01),
                "x_max":(-2, 4.01)
            },
            show_text = False
        )

        print(repr(nb_line_demo))

        self.add(nb_line_demo.group)

        self.play(
            *nb_line_demo.get_anim(run_time=5)
        )


# tick, tips, numbers
"""
self.init_leftmost_tick()
        if self.include_tip:
            self.add_tip()
        if self.include_ticks:
            self.add_tick_marks()
        if self.include_numbers:
            self.add_numbers()
"""
class IncludeOrNot(Scene):
    CONFIG={
        "default_setting":{
            "include_tip": False,
            "include_ticks": True,
            "include_numbers": False
        }
    }
    def construct(self):
        nb_line0 = NumberLine(include_tip=False, include_ticks=False, include_numbers=False).set_color(LIGHT_GREY)
        nb_line1 = NumberLine(include_tip=True, include_ticks=False, include_numbers=False).set_color(LIGHT_GREY)
        nb_line2 = NumberLine(include_tip=False, include_ticks=True, include_numbers=False).set_color(LIGHT_GREY)
        nb_line3 = NumberLine(include_tip=False, include_ticks=False, include_numbers=True).set_color(LIGHT_GREY)

        tip_text = Text("TIP", font="Verdana").move_to(2*UP).set_color_by_gradient([YELLOW_D, RED_B]).set_sheen_direction(RIGHT)

        self.play(
            LaggedStart(
                    Transform(nb_line0, nb_line1, run_time=2),
                    Write(tip_text, run_time=1.4),
                    lag_ratio=.4
                )
        )

        ticks_text = Text("TICKS", font="Verdana").move_to(2*UP).set_color_by_gradient([YELLOW_D, RED_B]).set_sheen_direction(RIGHT)

        self.play(
            LaggedStart(
                    
                    Transform(nb_line0, nb_line2, run_time=2),
                    FadeOutAndShift(tip_text, LEFT, run_time=.2), 
                    FadeInFrom(ticks_text, RIGHT, run_time=.2),
                )
        )

        number_text = Text("NUMBER", font="Verdana").move_to(2*UP).set_color_by_gradient([YELLOW_D, RED_B]).set_sheen_direction(RIGHT)

        self.play(
            LaggedStart(
                    
                    Transform(nb_line0, nb_line3, run_time=2),
                    FadeOutAndShift(ticks_text, LEFT, run_time=.2), 
                    FadeInFrom(number_text, RIGHT, run_time=.2),
                )
        )


class BasicTips(Scene):
    def construct(self):
        nb_line_demo = DemoClass(
            NumberLine().set_color(YELLOW),
            attrs={
                "tick_size":(.1, .3),

                "tick_frequency":(2, .5),
                "unit_size":(1, 2)
            },
            get_text_anim=False
        )

        print(repr(nb_line_demo))

        self.add(nb_line_demo.group)

        nb_line_demo.text.to_edge(UP, buff=2*SMALL_BUFF)

        additional_config = (
            {"run_time":4},
            {"run_time":1.7}
        )

        self.play(
            Succession(*nb_line_demo.get_anim(*additional_config, run_time=3))
        )


"""
self.shift(-self.number_to_point(self.number_at_center))
"""
class CenterNumber(Scene):
    def construct(self):
        nb_line_demo = DemoClass(
            NumberLine().set_color(YELLOW),
            attrs={
                "number_at_center":(-2.01, 2.01),
            },
            mobj_config={
                "x_min":-3,
                "x_max":3,
                "include_numbers":True,
                "numbers_to_show":range(-2, 2)
            }
        )

        print(repr(nb_line_demo))

        

        nb_line_demo.text.to_edge(UP, 2*SMALL_BUFF)

        # dot
        center_dot = Dot(stroke_width=3).move_to(ORIGIN).set_color_by_gradient([YELLOW_D, RED_A])

        self.add(nb_line_demo.group, center_dot)

        self.play(
            *nb_line_demo.get_anim(run_time=3, rate_func=there_and_back)
        )



class NumberesWithLine(Scene):
    def construct(self):
        nb_line0 = NumberLine()
        nb_line1 = NumberLine(include_numbers=True)
        nb_line2 = NumberLine(include_numbers=True, numbers_to_show=[1, 2, 3])
        nb_line3 = NumberLine(include_numbers=True,
                        numbers_to_show=[2.5, 3.5], 
                        decimal_number_config={
                            "num_decimal_places": 1,
                            },)

        self.play(
            Succession(
                Write(nb_line0),
                Transform(nb_line0, nb_line1, run_time=3),
                Transform(nb_line0, nb_line2, run_time=2),
                Transform(nb_line0, nb_line3, run_time=2)
            )
        )


class StemNumberLine(NumberLine):
    CONFIG={
        "include_stem": True,
        "include_dot":True,
        "x_val":[0, 1, 2],
        "y_val":[1, 2, 3],
        "stem_config":{
            "stroke_color":BLUE
        },
        "stem_dot_config":{
            "fill_color":BLUE
        }
    }
    def __init__(self, x_val=None, y_val=None, **kwargs):
        digest_config(self, kwargs)

        self.x_val = x_val or self.x_val
        self.y_val = y_val or self.y_val

        NumberLine.__init__(self)

        if self.include_stem:
            self.add_stem_marks()

        if self.include_dot:
            self.add_stem_dots()

    def set_x_val(self, x_val):
        self.x_val = x_val
    
    def set_y_val(self, y_val):
        self.y_val = y_val
    
    def get_x_val(self):
        return self.x_val
    
    def get_y_val(self):
        return self.y_val

    def add_stem_marks(self, **kwargs):
        self.stem = [self.get_stem(x, y, **kwargs) for x, y in zip(self.x_val, self.y_val)]
        self.add(
            VGroup(*self.stem)
        )

    def get_stem(self, x_val, y_val, **kwargs):
        stem = self.get_tick(x_val, size=y_val/2)
        stem.shift(self.n2p(x_val)-stem.points[0])
        self.stem_config = merge_dicts_recursively(self.stem_config, kwargs)
        if hasattr(self, 'stem_config'):
            stem.set_style(**self.stem_config)
        return stem

    def add_stem_dots(self, **kwargs):
        self.stem_dot_config = merge_dicts_recursively(self.stem_dot_config, kwargs)
        dot = Circle(radius=DEFAULT_DOT_RADIUS, **self.stem_dot_config)
        self.stem_dots = [dot.copy().shift(x*RIGHT + y*UP) for x, y in zip(self.x_val, self.y_val)]
        self.add(
            VGroup(*self.stem_dots)
        )

    # def get_stem_dot(self, x_val, y_val, **kwargs):
        
    #     dot = Circle(radius=DEFAULT_DOT_RADIUS, **self.stem_dot_config).move_to
    #     return dot


class TestStemLine(Scene):
    def construct(self):
        sn_line = StemNumberLine()

        self.play(Write(sn_line))

        self.wait()

        self.play(Rotate(sn_line, PI/2, ORIGIN))
        
        self.wait()

