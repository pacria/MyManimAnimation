from manimlib.imports import *


class VertexMap(VGroup):
    CONFIG={
        "pos_list":[(2.1, 3.2), (.9, 1.1), (-2.1, 0), (1.5, -1.4), (-1.3, 1.7)],
        "radius":.3,
        "stroke_color":YELLOW_C,
        "fill_color":YELLOW_B,
        "fill_opacity":1
    }
    def __init__(self, pos_list=None, dis_m = None, vertex_map=None, **kwargs):
        digest_config(self, kwargs)

        self.pos_list = self.pos_list if pos_list is None else pos_list
        self.vertex_count = len(self.pos_list)

        self.dis_m = dis_m

        self.vertex_array = [
            Circle(radius=self.radius, 
            stroke_color=self.stroke_color, 
            fill_color=self.fill_color,
            fill_opacity=self.fill_opacity).move_to(x*RIGHT+y*UP) for x, y in self.pos_list]        

        VGroup.__init__(self, *self.vertex_array)

        self.numbering_vertex(vertex_map=vertex_map)
    
    def full_generation(self, number_config=dict(), link_config=dict(), distance_num_config={}):
        number_config = merge_dicts_recursively(
            dict(font="Consolas", stroke_width=.2, color=GREY),
            number_config
        )
        link_config = merge_dicts_recursively(
            dict(stroke_width=1.4, stroke_color=YELLOW_D),
            link_config
        )
        distance_num_config = merge_dicts_recursively(
            dict(font="Consolas", stroke_width=.2, color=LIGHT_GREY, opacity=.8),
            distance_num_config
        )
        self.get_vertex_numbering(**number_config)
        self.generate_links(**link_config)
        self.show_all_link_label(**distance_num_config)

        return self

    def shape_generation(self, link_config=dict(), vertex_map=None):
        link_config = merge_dicts_recursively(
            dict(stroke_width=1.4, stroke_color=YELLOW_D),
            link_config
        )
        self.generate_links(vertex_map=vertex_map, **link_config)

        return self
    
    def generate_rect_border(self, buff=SMALL_BUFF, **kwargs):
        if hasattr(self, "radius"):
            buff += self.radius
        x_pos, y_pos = [x for x, _ in self.pos_list], [y for _, y in self.pos_list]
        x_min, x_max = min(x_pos), max(x_pos)
        y_min, y_max = min(y_pos), max(y_pos)

        rect = Rectangle(width=abs(x_min)+x_max+2*buff, height=abs(y_min)+y_max+2*buff, **kwargs)
        rect.shift((x_min+x_max)/2*RIGHT+(y_min+y_max)/2*UP)

        # self.submobjects.append(rect)

        self.submobjects.append(rect)

        self.border = rect

        return self

    def numbering_vertex(self, vertex_map=None):
        self.vertex_map = list(range(self.vertex_count)) if vertex_map is None else vertex_map

        self.vertex_dict = {vertex_num:vertex for vertex, vertex_num in zip(self.vertex_array, self.vertex_map)}

    def get_vertex_numbering(self, vertex_map=None, add_to_group=True, **kwargs):
        if not hasattr(self, "vertex_map") or vertex_map is not None:
            self.numbering_vertex(vertex_map)

        
        self.number_array = [Text('%d'%i, **kwargs) for i in self.vertex_map]

        for number, vertex in zip(self.number_array, self.vertex_array):
            number.match_height(vertex).scale(.6)
            number.next_to(vertex, UP, buff=-vertex.get_height()*.7)
        
        if add_to_group:
            self.submobjects += self.number_array

        return self.number_array

    def generate_links(self, add_to_group=True, vertex_map=None, **kwargs):
        if not hasattr(self, "vertex_map") or vertex_map is not None:
            self.numbering_vertex(vertex_map)
        link_m = ~np.isinf(self.dis_m)

        self.links = dict()

        for number, vertex in self.vertex_dict.items():
            for other_vertex_number in range(number+1, self.vertex_count):
                if link_m[number, other_vertex_number]:
                    link = Line(vertex, self.vertex_dict[other_vertex_number], **kwargs)
                    self.links['%d%d'%(number, other_vertex_number)] = link

        link_gro = list(self.links.values())
        if add_to_group:
            self.submobjects += link_gro
        
        return link_gro

    def generate_path(self, vertex_list, **kwargs):
        path = []
        for i in range(len(vertex_list)-1):
            link = Line(self.vertex_dict[vertex_list[i]].get_center(), self.vertex_dict[vertex_list[i+1]].get_center(), **kwargs)
            path.append(link)
        
        return VGroup(*path)

    def show_link_label(self, v1, v2, **kwargs):
        # v1, v2 vertex_number
        try:
            v1, v2 = min(v1, v2), max(v1, v2)
            num_label = Text('%d'%self.dis_m[v1, v2], **kwargs)
            link = self.links['%d%d'%(v1, v2)]

            num_label.scale(.4)
            num_label.move_to(link.get_center())

            self.submobjects.append(num_label)

            return num_label
        except OverflowError or KeyError:
            return 
    
    def show_all_link_label(self, **kwargs):
        
        labels = []
        for i in range(self.vertex_count):
            for j in range(i+1, self.vertex_count):
                num_label = self.show_link_label(i, j, **kwargs)
                if num_label is None:
                    continue
                labels.append(num_label)
        
        return labels

    def set_dis_m(self, dis_m):
        self.dis_m = dis_m 
    
    def get_dis_m(self, dis_m):
        return self.dis_m


class NumberedCircle(VGroup):
    CONFIG={
        "circle_config":{"radius":.3,
        "stroke_color":YELLOW_C,
        "fill_color":YELLOW_B,
        "fill_opacity":1},
        "number_config":{"font":"Consolas", "stroke_width":.2, "color":GREY}
    }
    def __init__(self, number, **kwargs):
        digest_config(self, kwargs)
        circle = Circle(**self.circle_config)
        number = Text('%s'%repr(number), **self.number_config)
        number.match_height(circle).scale(.6)
        number.next_to(circle, UP, buff=-circle.get_height()*.7)

        VGroup.__init__(self, circle, number)


class Table:
    CONFIG = {
        "col_buff":.4,
        "row_buff":.2,
        "height":1.2,
        "width":1.4,
        "col_direction":RIGHT,
        "row_direction":DOWN,
        "base":ORIGIN,
        "col_num":6,
        "row_num":4,
        "row_title":False,
        "col_title":False,
        "size":.6
    }
    def __init__(self, mobj_matrix, **kwargs):
        digest_config(self, kwargs)

        self.mobj_matrix = mobj_matrix

        self.row_num, self.col_num = np.shape(self.mobj_matrix)

        if not isinstance(mobj_matrix[0, 0], VMobject):
            self.mobj_matrix = VGroup(
                *[VGroup(*[TextMobject('%s'%repr(self.mobj_matrix[i, j]), **kwargs).scale(self.size) for j in range(self.col_num)]) for i in range(self.row_num)]
            )

        if self.row_title:
            self.row_num += 1
        
        if self.col_title:
            self.col_num += 1

        self.get_height(*self.mobj_matrix[0])

        self.get_width(*self.mobj_matrix[0])

        self.generate_grids()

    
    def get_height(self, *mobjs):
        self.height = max(mobj.get_height() for mobj in mobjs)
    
    def get_width(self, *mobjs):
        self.width = max(mobj.get_width() for mobj in mobjs)

    def generate_grids(self):
        self.grid_matrix = []
        for i in range(self.row_num):
            row_list = []
            for j in range(self.col_num):
                row_stand = i*(self.width+self.row_buff)*self.row_direction 
                row_list.append(ORIGIN + j*(self.height+self.col_buff)*self.col_direction + row_stand)
            self.grid_matrix.append(row_list)
        
        self.grid_matrix = np.array(self.grid_matrix)
        return self.grid_matrix
    
    def set_positon(self, r, c):
        # print(np.shape(self.mobj_matrix), np.shape(self.grid_matrix))
        gr = r+1 if self.row_title else r
        gc = c+1 if self.col_title else c
        self.mobj_matrix[r][c].move_to(self.grid_matrix[gr][gc])

        return self

    def set_all_pos(self):
        r, c, *m = np.shape(self.mobj_matrix)
        for i in range(r):
            for j in range(c):
                self.set_positon(i, j)

        return self

    def set_row_title(self, row_mobjs):
        if not self.row_title:
            return

        for mobj, pos in zip(row_mobjs, self.grid_matrix[0][1:]):
            mobj.move_to(pos)

        return row_mobjs

    def set_col_title(self, col_mobjs):
        if not self.col_title:
            return

        for mobj, pos in zip(col_mobjs, self.grid_matrix[1:, 0]):
            mobj.move_to(pos)

        return col_mobjs


    def get_sample(self):
        return self.mobj_matrix[0][0]