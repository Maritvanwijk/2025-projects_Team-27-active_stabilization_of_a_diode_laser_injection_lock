from manim import *

class Laser(Scene):
    def construct(self):
        # --- 0. Algemene instellingen en kleuren ---
        default_run_time = 1.5 # Duur van de meeste animaties
        short_run_time = 0.3 # Duur voor snellere acties (bijv. flash)
        default_wait_time = 0.5 # Pauze tussen stappen
        long_wait_time = 1.0 # Langere pauze voor belangrijke momenten

        laser_color = BLUE_D
        feedback_color_laser = YELLOW_B # Kleur van de laser bij feedback
        flash_color = WHITE # Voor de flash animatie
        beam_feedback_color = RED_B # Nieuwe kleur voor de feedback straal
        beam_spectrometer_color = RED_A # Nieuwe kleur voor de spectrometer straal
        case_color = GRAY_B
        opening_color = BLACK
        component_color = WHITE
        label_color = WHITE

        # --- 1. Elementen definiëren en stapsgewijs introduceren ---

        # 1.1 Laser
        laser = Rectangle(width=1.8, height=0.7, color=laser_color, fill_opacity=1).shift(DOWN * 3.5 + RIGHT * 4)
        laser_label = Text("Laser (LDM56/M en L638P150)", font_size=20, color=label_color).next_to(laser, LEFT, buff=0.2)
        self.play(Create(laser), Create(laser_label), run_time=default_run_time)
        self.wait(default_wait_time)

        # 1.2 Eerste Grating (direct boven de laser, omgedraaid)
        grating1_center = laser.get_top() + UP * 1.5 # Direct boven de laser
        grating1 = Line(grating1_center + LEFT * 1, grating1_center + RIGHT * 1).set_stroke(width=5, color=component_color).rotate(-PI/4) # Nu -PI/4
        grating1_label = Text("Grating (Feedback)", font_size=20, color=label_color).next_to(grating1, UP, buff=0.2)
        self.play(Create(grating1), Create(grating1_label), run_time=default_run_time)
        self.wait(default_wait_time)

        # 1.3 Spectrometer behuizing (Case)
        case_width = 8
        case_height = 6
        case_center = LEFT * 2
        case = Rectangle(width=case_width, height=case_height, color=case_color, fill_opacity=0.7).move_to(case_center)

        opening_width = 0.2
        opening_height = 0.8
        opening_pos_x = case.get_right()[0] # Aan de rechterkant van de case
        target_horizontal_y = grating1.get_center()[1] # Y-coördinaat voor de horizontale straal
        opening_pos = np.array([opening_pos_x, target_horizontal_y, 0])
        opening = Rectangle(width=opening_width, height=opening_height, color=opening_color, fill_opacity=1).move_to(opening_pos)

        spectrometer_case_group = VGroup(case, opening)
        self.play(Create(spectrometer_case_group), run_time=default_run_time)
        self.wait(default_wait_time)

        # 1.4 Spectrometer onderdelen binnen de case
        # Mirror 1 (nu een lijn, op dezelfde hoogte als de opening/horizontale straal)
        mirror1_center = case.get_left() + RIGHT * 0.5 # Iets naar rechts van de linkerkant van de case
        mirror1_center[1] = target_horizontal_y # Dezelfde hoogte als de opening en grating1
        mirror1 = Line(mirror1_center + UP * 0.5, mirror1_center + DOWN * 0.5).set_stroke(width=5, color=component_color)
        mirror1_label = Text("Mirror 1", font_size=20, color=label_color).next_to(mirror1, UP, buff=0.2)
        # Controleer en pas positie label aan om overlap te voorkomen
        if mirror1_label.get_bottom()[1] < mirror1.get_top()[1]: # Als label te laag is
            mirror1_label.next_to(mirror1, UP, buff=0.5) # Meer ruimte
        self.play(Create(mirror1), Create(mirror1_label), run_time=default_run_time)
        self.wait(default_wait_time)

        # Grating 2 (Blazed)
        grating2_center = case_center + RIGHT * 2 + UP * 1.5 # Binnen de case, rechterboven
        grating2 = Line(grating2_center + UP * 0.75 + LEFT * 0.75, grating2_center + DOWN * 0.75 + RIGHT * 0.75).set_stroke(width=5, color=component_color).rotate(PI) # Gedraaid
        grating2_label = Text("Grating (Blazed)", font_size=20, color=label_color).next_to(grating2, RIGHT, buff=0.2)
        if grating2_label.get_left()[0] < grating2.get_right()[0]: # Als label te veel overlapt
             grating2_label.next_to(grating2, RIGHT, buff=0.5)
        self.play(Create(grating2), Create(grating2_label), run_time=default_run_time)
        self.wait(default_wait_time)

        # Mirror 2 (onder Grating 2 en tussen M1 en G2 horizontaal, gericht op CCD)
        mirror2_center = (grating2_center + mirror1_center) / 2 # Horizontaal tussen G2 en M1
        mirror2_center[1] = case.get_bottom()[1] + 1.0 # Lager in de case
        mirror2 = Line(mirror2_center + LEFT * 0.7, mirror2_center + RIGHT * 0.7).set_stroke(width=5, color=component_color).rotate(PI) # Gericht naar boven/links voor CCD
        mirror2_label = Text("Mirror 2", font_size=20, color=label_color).next_to(mirror2, DOWN, buff=0.2)
        if mirror2_label.get_top()[1] > mirror2.get_bottom()[1]:
            mirror2_label.next_to(mirror2, DOWN, buff=0.5)
        self.play(Create(mirror2), Create(mirror2_label), run_time=default_run_time)
        self.wait(default_wait_time)

        # CCD (boven alles in de top van de case, nu meer gecentreerd bovenin)
        ccd_width = 1.8
        ccd_height = 0.5
        ccd_center = case.get_top() + DOWN * 0.5 + LEFT * 0.5 # Bovenin de case, meer gecentreerd
        ccd = Rectangle(width=ccd_width, height=ccd_height, color=component_color, fill_opacity=1).move_to(ccd_center)
        ccd_label = Text("CCD", font_size=20, color=label_color).next_to(ccd, UP, buff=0.2)
        if ccd_label.get_bottom()[1] < ccd.get_top()[1]:
            ccd_label.next_to(ccd, UP, buff=0.5)
        self.play(Create(ccd), Create(ccd_label), run_time=default_run_time)
        self.wait(long_wait_time)


        # --- 2. Laserstraal animeren (Propagatie en Feedback) ---

        # 2.1 Straal van laser naar Grating 1 (rechte lijn omhoog)
        beam_laser_start = laser.get_top() + UP * 0.1
        beam_laser_end_grating1 = grating1.get_center()
        beam_to_grating1 = Line(beam_laser_start, beam_laser_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_grating1.animate.put_start_and_end_on(beam_laser_start, beam_laser_end_grating1),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(default_wait_time)

        # 2.2 Feedback straal met flash en kleurverandering
        feedback_beam_start = grating1.get_center()
        feedback_beam_end = laser.get_center() + UP * 0.2
        beam_feedback = Line(feedback_beam_start, feedback_beam_start, color=beam_feedback_color, stroke_width=7)

        flash_circle = Circle(radius=0.1, color=flash_color, fill_opacity=1).move_to(feedback_beam_end)

        self.play(
            beam_feedback.animate.put_start_and_end_on(feedback_beam_start, feedback_beam_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(short_run_time)

        self.play(
            FadeIn(flash_circle, run_time=short_run_time),
            flash_circle.animate.set_stroke(opacity=0).scale(3),
            laser.animate.set_color(feedback_color_laser),
            laser_label.animate.set_color(feedback_color_laser),
            run_time=short_run_time
        )
        self.wait(default_wait_time) # Even wachten met de feedbackstraal die blijft staan

        # 2.3 De straal van Grating 1 naar de opening (horizontaal)
        beam_to_opening_start = grating1.get_center()
        beam_to_opening_end = opening.get_center()
        beam_to_opening = Line(beam_to_opening_start, beam_to_opening_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_opening.animate.put_start_and_end_on(beam_to_opening_start, beam_to_opening_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(default_wait_time)

        # 2.4 Straal van opening naar Mirror 1 (horizontaal)
        beam_to_mirror1_start = opening.get_center()
        beam_to_mirror1_end = mirror1.get_center()
        beam_to_mirror1 = Line(beam_to_mirror1_start, beam_to_mirror1_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_mirror1.animate.put_start_and_end_on(beam_to_mirror1_start, beam_to_mirror1_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(default_wait_time)

        # 2.5 Straal van Mirror 1 naar Grating 2 (Blazed)
        beam_to_grating2_start = mirror1.get_center()
        beam_to_grating2_end = grating2.get_center()
        beam_to_grating2 = Line(beam_to_grating2_start, beam_to_grating2_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_grating2.animate.put_start_and_end_on(beam_to_grating2_start, beam_to_grating2_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(default_wait_time)

        # 2.6 Straal van Grating 2 naar Mirror 2
        beam_to_mirror2_start = grating2.get_center()
        beam_to_mirror2_end = mirror2.get_center()
        beam_to_mirror2 = Line(beam_to_mirror2_start, beam_to_mirror2_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_mirror2.animate.put_start_and_end_on(beam_to_mirror2_start, beam_to_mirror2_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(default_wait_time)

        # 2.7 Straal van Mirror 2 naar CCD
        beam_to_ccd_start = mirror2.get_center()
        beam_to_ccd_end = ccd.get_center()
        beam_to_ccd = Line(beam_to_ccd_start, beam_to_ccd_start, color=beam_spectrometer_color, stroke_width=7)

        self.play(
            beam_to_ccd.animate.put_start_and_end_on(beam_to_ccd_start, beam_to_ccd_end),
            run_time=default_run_time, rate_func=linear
        )
        self.wait(long_wait_time * 2)