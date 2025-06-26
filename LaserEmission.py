from manim import *

class LaserEmission(Scene):
    def construct(self):
        #onderdelen laser        
        n_layer = Rectangle(width=5, height=1.2, fill_color=BLUE, fill_opacity=0.5).shift(UP * 1.5)
        p_layer = Rectangle(width=5, height=1.2, fill_color=RED, fill_opacity=0.5).shift(DOWN * 1.5)
        active_layer = Rectangle(width=5, height=0.6, fill_color=WHITE, fill_opacity=0.2)

        layers = VGroup(n_layer, active_layer, p_layer)
        self.play(FadeIn(layers))

        n_label = Text("n-type halfgeleider", font_size=24).next_to(n_layer, UP)
        p_label = Text("p-type halfgeleider", font_size=24).next_to(p_layer, DOWN)
        active_label = Text("actieve laag", font_size=24).next_to(active_layer, UP)
        self.play(Write(n_label), Write(p_label), Write(active_label))

        #spiegels
        left_mirror = Line(start=LEFT * 2.6 + DOWN * 2, end=LEFT * 2.6 + UP * 2, color=GREY)
        right_mirror = Line(start=RIGHT * 2.6 + DOWN * 2, end=RIGHT * 2.6 + UP * 2, color=GREY)
        left_label = Text("Volledig reflecterende spiegel", font_size=20).next_to(left_mirror, LEFT)
        right_label = Text("Halfdoorlatende spiegel", font_size=20).next_to(right_mirror, RIGHT)
        self.play(Create(left_mirror), Create(right_mirror), Write(left_label), Write(right_label))

        #spontane emissie
        electron = Dot(color=BLUE).move_to(n_layer.get_center() + RIGHT * 1)
        minus = Text("-", font_size=24).move_to(electron.get_center())
        hole = Circle(radius=0.15, color=RED).move_to(p_layer.get_center() + RIGHT * 1)
        gap = Text("gap", font_size=16).next_to(hole, DOWN, buff=0.1)
        self.play(FadeIn(electron, minus, hole, gap))

        #samenkomen gap en elektron
        merge_point = active_layer.get_center() + RIGHT * 0.5
        self.play(electron.animate.move_to(merge_point), hole.animate.move_to(merge_point), minus.animate.move_to(merge_point))
        self.play(FadeOut(gap))
        self.wait(0.5)

        #foton ontstaat en beweegt naar links
        photon1 = Arrow(start=ORIGIN, end=LEFT * 0.8, color=YELLOW, buff=0).move_to(merge_point)
        photon_label = Text("Foton", font_size=20).next_to(photon1, DOWN)
        spont_label = Text("Spontane emissie", font_size=30).to_edge(UP)
        self.play(Create(photon1), Write(photon_label), Write(spont_label))
        self.wait(1)

        self.play(FadeOut(photon_label))

        self.play(FadeOut(electron), FadeOut(hole), FadeOut(minus))
        self.wait(0.5)

        #gestimuleerde emissie
        self.play(FadeOut(spont_label))

        #foton raakt spiegel
        bounce_point = left_mirror.get_center()
        self.play(photon1.animate.move_to(bounce_point))

        #tweede elektron-gat combinatie komt
        electron2 = Dot(color=BLUE).move_to(active_layer.get_center() + LEFT * 0.5)
        minus2 = Text("-", font_size=24).move_to(electron2.get_center())
        hole2 = Circle(radius=0.15, color=RED).move_to(electron2.get_center())
        gap2 = Text("gap met aangeslagen elektron", font_size=16).next_to(hole2, DOWN, buff=0.1)
        self.play(FadeIn(electron2, minus2, hole2, gap2))
        self.wait(0.5)

        #foton draait om en beweegt naar rechts tot het paar
        photon1.rotate(PI)  
        target_point = active_layer.get_center() + LEFT * 0.5
        self.play(photon1.animate.move_to(target_point))

        self.play(FadeOut(photon1))

        #twee coherente fotonen ontstaan en bewegen naar rechts
        photon2 = Arrow(start=ORIGIN, end=RIGHT * 0.8, color=YELLOW, buff=0).move_to(hole2.get_center())
        photon3 = Arrow(start=ORIGIN, end=RIGHT * 0.8, color=YELLOW, buff=0).move_to(hole2.get_center() + DOWN * 0.2)
        coh_label = Text("twee coherente fotonen", font_size=20).next_to(photon2, UP)
        stim_label = Text("Gestimuleerde emissie", font_size=30).to_edge(UP)
        self.play(Create(photon2), Create(photon3), Write(coh_label), Write(stim_label))
        self.play(photon2.animate.shift(RIGHT * 3), photon3.animate.shift(RIGHT * 3))

        self.play(FadeOut(electron2), FadeOut(hole2), FadeOut(minus2), FadeOut(gap2))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
