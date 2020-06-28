from SteppedTutorial.ScreenGrid.ScreenGrid import ScreenGrid
from SteppedTutorial.DemoClass.DemoClass import DemoClass
from manimlib.imports import *


class BasicPlot1(GraphScene):
    CONFIG = {
        "y_max" : 50,
        "y_min" : 0,
        "x_max" : 7,
        "x_min" : 0,
        "y_tick_frequency" : 5, 
        "x_tick_frequency" : 0.5, 
        "axes_color" : BLUE, 
        "y_labeled_nums": range(0,60,10),
        "x_labeled_nums": list(np.arange(2, 7.0+0.5, 0.5)),
        "x_label_decimal":1,
        "y_label_direction": LEFT,
        "x_label_direction": DOWN,
        "y_label_decimal":3
    }
    def construct(self):
        self.setup_axes(animate=True)
        graph = self.get_graph(lambda x : x**2,  
                                    color = GREEN,
                                    x_min = 2, 
                                    x_max = 4
                                    )
        self.play(
        	ShowCreation(graph),
            run_time = 2
        )
        self.wait()


from math import sin

# def interpolate(start, end, alpha):
#     return (1 - alpha) * start + alpha * end

"""
class ParametricFunction(VMobject):
    CONFIG = {
        "t_min": 0,
        "t_max": 1,
        "step_size": 0.01,  # Use "auto" (lowercase) for automatic step size
        "dt": 1e-8,
        # TODO, be smarter about figuring these out?
        "discontinuities": [],
    }

    def __init__(self, function=None, **kwargs):
        # either get a function from __init__ or from CONFIG
        self.function = function or self.function
        VMobject.__init__(self, **kwargs)

    def get_function(self):
        return self.function

    def get_point_from_function(self, t):
        return self.function(t)

    def get_step_size(self, t=None):
        if self.step_size == "auto":
            
            # for x between -1 to 1, return 0.01
            # else, return log10(x) (rounded)
            # e.g.: 10.5 -> 0.1 ; 1040 -> 10
            
            if t == 0:
                scale = 0
            else:
                scale = math.log10(abs(t))
                if scale < 0:
                    scale = 0

                scale = math.floor(scale)

            scale -= 2
            return math.pow(10, scale)
        else:
            return self.step_size

    def generate_points(self):
        t_min, t_max = self.t_min, self.t_max
        dt = self.dt

        discontinuities = filter(
            lambda t: t_min <= t <= t_max,
            self.discontinuities
        )
        discontinuities = np.array(list(discontinuities))
        boundary_times = [
            self.t_min, self.t_max,
            *(discontinuities - dt),
            *(discontinuities + dt),
        ]
        boundary_times.sort()
        for t1, t2 in zip(boundary_times[0::2], boundary_times[1::2]):
            t_range = list(np.arange(t1, t2, self.get_step_size(t1)))
            if t_range[-1] != t2:
                t_range.append(t2)
            points = np.array([self.function(t) for t in t_range])
            valid_indices = np.apply_along_axis(
                np.all, 1, np.isfinite(points)
            )
            points = points[valid_indices]
            if len(points) > 0:
                self.start_new_path(points[0])
                self.add_points_as_corners(points[1:])
        self.make_smooth()
        return self

"""

class Zflag(VMobject):
    CONFIG = {
        "points":(UL, UR, DL, DR)
    }
    def __init__(self, *p, **kwargs):
        digest_config(self, kwargs)
        points = p or self.points 

        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners(points)
        self.make_smooth()

    # def generate_points(self):
    #     self.set_anchors_and_handles
    #     self.make_smooth()
    #     return self

class TestZflag(Scene):
    def construct(self):
        z = Zflag()
        self.write(z)
        self.wait()


class BasicPlotAdd1(GraphScene):
    CONFIG = {
        "y_max" : -5,
        "y_min" : 5,
        "x_max" : 5,
        "x_min" : -5,
        "y_tick_frequency" : 5, 
        "x_tick_frequency" : 0.5, 
        "graph_origin": ORIGIN
    }
    def construct(self):
        self.setup_axes(invisiable=False)
        theta = ValueTracker(0)
        graph = self.get_graph(lambda x : sin(x),  
                                    color = GREEN,
                                    x_min = -5, 
                                    x_max = 5
                                    )
        graph.add_updater(lambda mobj: mobj.become(
            self.get_graph(
                lambda x: sin(x+theta.get_value()),
                color = GREEN,
                x_min = -5,
                x_max = 5
            )
        ))
        self.play(
        	ShowCreation(graph),
            run_time = 2
        )
        self.wait()
        self.play(theta.increment_value, 2*PI)
        self.wait()

        
class BasicPlot2(GraphScene):
    CONFIG = {
        "y_max" : 100,
        "y_min" : -100,
        "x_max" : 10,
        "x_min" : -10,
        "y_tick_frequency" : 10, 
        "x_tick_frequency" : 1, 
        "axes_color" : BLUE, 
        "graph_origin" : np.array((0,0,0))
    }
    def construct(self):
        self.setup_axes(animate=True)

        # ParametricFunction
        graph = self.get_graph(lambda x : x**2,  
                                    color = LIGHT_GREY,
                                    x_min = -9, 
                                    x_max = 9
                                    )
        
        label = self.get_graph_label(graph)

        self.play(
            LaggedStart(
                ShowCreation(graph),
                ShowCreation(label),
                lag_ratio=.5
            ),               
            run_time = 2
        )
        self.wait()


class BasicPlot2v2(GraphScene):
    # The version without axes
    CONFIG = {
        "y_max" : 100,
        "y_min" : -100,
        "x_max" : 10,
        "x_min" : -10,
        "y_tick_frequency" : 10, 
        "x_tick_frequency" : 1, 
        "axes_color" : BLUE, 
        "graph_origin" : np.array((0,0,0))
    }
    def construct(self):
        self.setup_axes(invisiable=True)

        # ParametricFunction
        graph = self.get_graph(lambda x : x**2,  
                                    color = LIGHT_GREY,
                                    x_min = -9, 
                                    x_max = 9
                                    )
        
        label = self.get_graph_label(graph)

        self.play(
            LaggedStart(
                ShowCreation(graph),
                ShowCreation(label),
                lag_ratio=.5
            ),               
            run_time = 2
        )
        self.wait()