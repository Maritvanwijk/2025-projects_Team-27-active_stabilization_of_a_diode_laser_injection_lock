from manim import *
import numpy as np

class CorrectLittrowConfig(Scene):
    def construct(self):
        # Parameters
        incident_angle_deg = 30
        incident_angle_rad = incident_angle_deg * DEGREES

        # Positions
        grating_pos = ORIGIN
        emitter_pos = LEFT * 4 + DOWN * np.tan(incident_angle_rad) * 4
        emitter = Rectangle(height=0.4, width=0.2, color=BLUE).move_to(emitter_pos)

        # Grating visual
        grating = VGroup(*[
            Line(UP * 0.5, DOWN * 0.5, color=GRAY)
            for _ in range(20)
        ]).arrange(RIGHT, buff=0.05).move_to(grating_pos)

        # Incident beam (red, toward grating)
        incident_beam = Line(
            start=emitter_pos,
            end=grating_pos,
            color=RED
        ).set_stroke(width=6)

        # 1st order diffraction (Littrow) – back to diode (yellow now)
        first_order_beam = Line(
            start=grating_pos,
            end=emitter_pos,
            color=YELLOW
        ).set_stroke(width=6)

        # 0th order reflection – mirrored over the normal (upward direction)
        zero_order_direction = np.array([
            np.cos(2),
            np.sin(2),  # upward
            0
        ])
        zeroth_beam = Line(
            start=grating_pos,
            end=grating_pos + zero_order_direction * 6,
            color=YELLOW
        ).set_stroke(width=4)

        # Animate
        self.play(FadeIn(emitter), run_time=0.5)
        self.play(Create(incident_beam), run_time=1)
        self.wait(0.3)

        self.play(FadeIn(grating), run_time=0.5)
        self.wait(0.3)

        self.play(Create(first_order_beam), Create(zeroth_beam), run_time=0.8
                  )
        self.wait(2)

        lasdgawegab
        test
        self.play(*[FadeOut(mob) for mob in [emitter, grating, incident_beam, first_order_beam, zeroth_beam]])
