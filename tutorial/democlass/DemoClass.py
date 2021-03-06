from manimlib.imports import *


# At least now. function factory is indeed.
class UpdaterFactory:
    # TODO: Shall I extend its functions as a general function factory?
    def __init__(self, tracker, func):
        self.tracker = tracker
        # func MUST return an UPDATER(FUNC) with argument tracker
        self.func = func
    
    def __call__(self):
        return self.func(self.tracker)

class DemoClass(VGroup):
    CONFIG={
        "float_func":float,
        "mobj_config":{},
        "dec_config":{"size":1.2},
        "text_config":{"font":"Courier New", 'size': .6, "stroke_width":.8, "height":4},
        "anim_config":{},
        "mobj_updater":None,
        "val_dec_updater":None,
        "text_updater":None,
        "sep_buff":2*SMALL_BUFF,
        "performance":True # Set this to True may take too many resources.

    }

    

    def __init__(self, mobj=None, attrs=None, add_updater=True, **kwargs):
        digest_config(self, kwargs)

        self.seperate_attrs(attrs)

        # self.value_trackers
        self.value_trackers = [ValueTracker(init_value) for init_value in self.init_values]
        

        # val_dec
        # 将不同的updater 加到value_dec上并不是一件容易的事，保险起见，作 is 检测
        self.value_decos = [DecimalNumber(init_value, **self.dec_config) for init_value in self.init_values]

        # val_dec_updater
        def val_dec_updater(tracker):
            return lambda mobj: mobj.set_value(tracker.get_value())

        # func_list = [lambda mobj: mobj.set_value(tracker.get_value()) for tracker in self.value_trackers]
        # You will find func_list[0] is func_list[-1] == False

        # text

        self.text = self.get_text()

        # text_array = [VGroup(
        #         Text("{}=".format(attr_name), **self.text_config),
        #         val_dec.scale_in_place(self.dec_config["size"])).arrange(buff=SMALL_BUFF, aligned_edge=DOWN)
        #     for attr_name, val_dec in zip(self.attr_list, self.value_decos)]
        
        
        text_updater = self.get_text_updater()


        # mobj
        self.mobj_class = mobj.__class__

        self.mobj_config = merge_dicts_recursively(
            mobj.get_style(),
            self.mobj_config
        )

        cls_config = merge_dicts_recursively(
            self.mobj_config, 
            {attr:val for attr, val in zip(self.attr_list, self.init_values)}
            )

        self.mobj = self.mobj_class(**cls_config)

        def mobj_updater(mobj):
            tracked_vals = [tracker.get_value() for tracker in self.value_trackers]
            cls_config = {attr:val for attr, val in zip(self.attr_list, tracked_vals)}

            if self.performance:
                cls_config = merge_dicts_recursively(self.mobj_config, cls_config)

            new_mobj = self.mobj_class(**cls_config)
            # new_mobj.match_style(mobj)

            mobj.become(new_mobj)

        # add_updater
        self.mobj_updater = mobj_updater if self.mobj_updater is None else self.mobj_updater
        self.val_dec_updater = val_dec_updater if self.val_dec_updater is None else self.val_dec_updater
        self.text_updater = text_updater if self.text_updater is None else self.text_updater
        if add_updater:
            self._add_updater()

        # group
        self.group = VGroup(self.mobj, self.text)
    
    def seperate_attrs(self, attrs):
        self.attr_list = list(attrs.keys())
        self.init_values, self.end_values = [pre for pre, _ in attrs.values()]\
            , [end  for _, end in attrs.values()]

        self.init_values = list(map(self.float_func, self.init_values))
        self.end_values = list(map(self.float_func, self.end_values))

    def get_text(self):
        explain_text = VGroup(
            *[Text("{}=".format(attr_name), **self.text_config)for attr_name in self.attr_list]
        )

        for dec, text in zip(self.value_decos, explain_text):
            dec.match_height(text)

        dec_text = VGroup(
            *self.value_decos
        ).arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)

        explain_text.arrange(DOWN, buff=SMALL_BUFF, aligned_edge=RIGHT)
        
        dec_text.next_to(explain_text, RIGHT, buff=self.sep_buff, aligned_edge=DOWN)

        return VGroup(explain_text, dec_text)
        # print(self.text.get_boundary_point(RIGHT))

        # right_boarder, up_limit = self.text.get_boundary_point(RIGHT)[0], 5

        

        # invis_line = Line([right_boarder, up_limit, 0], [right_boarder, -up_limit, 0]).fade(0)

        # for part in self.text:
        #     part[1].next_to(invis_line, LEFT, buff=SMALL_BUFF)

    def get_text_updater(self):
        # TODO: Should there be a text_updater?(Moving around can be bells and whistles)
        return None 

        
    
    def get_anim(self, **kwargs):
        anim_config = merge_dicts_recursively(self.anim_config, kwargs)
        anim = [ApplyMethod(tracker.set_value, end_val, **anim_config) 
            for tracker, end_val in zip(self.value_trackers, self.end_values)]

        # TODO: reutrn anim(list) or AnimationGroup(*anim, **kwargs) or LaggedStart(*anim, **kwargs)?
        return anim

    def _add_updater(self):
        if self.mobj_updater:
            self.mobj.add_updater(self.mobj_updater)
        if self.val_dec_updater:
            for value_dec, tracker in zip(self.value_decos, self.value_trackers):
                value_dec.add_updater(UpdaterFactory(tracker, self.val_dec_updater)())
        if self.text_updater:
            self.text.add_updater(self.text_updater)
    
    def __repr__(self):
        fmt_str = "Attribute:{attr:>10}\t Ranging{init:.2f}~{end:.2f}"
        output = '\n'.join(fmt_str.format(attr=attr_name, init=init_val, end=end_val) 
            for attr_name, init_val, end_val in zip(self.attr_list, self.init_values, self.end_values))
        return output


class SquareDemo(Scene):
    def construct(self):
        square = Square(side_length=2).set_fill(color=WHITE, opacity=.6).set_color_by_gradient([YELLOW_A, RED_B])
        square_demo = DemoClass(
            square,
            {"side_length":(1, 5)}
        )

        print(square_demo.group)

        self.add(square_demo.group)

        print(square_demo.get_anim())

        self.play(AnimationGroup(
            *square_demo.get_anim(run_time=3)
        ))


class ArcDemo(Scene):
    def construct(self):
        arc = Arc().set_color_by_gradient([GOLD_D, RED_B, YELLOW_A, RED_D])
        arc_demo = DemoClass(
            arc,
            { 
            "angle":(TAU/4, 2*PI),
            "radius":(2, 4),
            "stroke_width":(2, 22)}
        )

        print(repr(arc_demo))

        self.add(arc_demo.group)

        self.play(AnimationGroup(
            *arc_demo.get_anim(run_time=3)
        ))
