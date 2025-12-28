from manimlib import *


class WarpReduceVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Warp-Level Reduction: warpReduce()", font_size=36)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.5)

        # =====================================================================
        # PART 1: Show instruction pipeline horizontally
        # =====================================================================
        code_lines = [
            ("sdata[tid]", "+=", "sdata[tid + 32];"),
            ("sdata[tid]", "+=", "sdata[tid + 16];"),
            ("sdata[tid]", "+=", "sdata[tid + 8];"),
            ("sdata[tid]", "+=", "sdata[tid + 4];"),
            ("sdata[tid]", "+=", "sdata[tid + 2];"),
            ("sdata[tid]", "+=", "sdata[tid + 1];"),
        ]

        # Create instruction boxes horizontally
        inst_boxes = VGroup()
        inst_texts = VGroup()
        for i, (line1, line2, line3) in enumerate(code_lines):
            box = RoundedRectangle(width=2.1, height=1.5, corner_radius=0.1)
            box.set_stroke(WHITE, width=1.5)
            box.set_fill(BLUE_E, opacity=0.3)

            # Three lines of text
            t1 = Text(line1, font_size=18, font="Consolas")
            t2 = Text(line2, font_size=18, font="Consolas", color=YELLOW)
            t3 = Text(line3, font_size=18, font="Consolas")
            text_group = VGroup(t1, t2, t3).arrange(DOWN, buff=0.1)
            text_group.move_to(box.get_center())

            inst_boxes.add(box)
            inst_texts.add(text_group)

        inst_group = VGroup(*[VGroup(inst_boxes[i], inst_texts[i]) for i in range(6)])
        inst_group.arrange(RIGHT, buff=0.15)
        inst_group.move_to(ORIGIN)

        # Thin arrows between instructions
        arrows = VGroup()
        for i in range(5):
            arrow = Line(
                inst_boxes[i].get_right() + LEFT * 0.05,
                inst_boxes[i + 1].get_left() + RIGHT * 0.05,
                color=YELLOW,
                stroke_width=1.5
            )
            arrow_tip = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            arrow_tip.scale(0.08)
            arrow_tip.rotate(-PI/2)
            arrow_tip.next_to(arrow, RIGHT, buff=0)
            arrows.add(VGroup(arrow, arrow_tip))

        pipeline_label = Text("Instruction Pipeline (executed sequentially per thread)", font_size=20, color=YELLOW)
        pipeline_label.next_to(inst_group, UP, buff=0.4)

        parallel_note = Text("But ALL 32 threads execute each instruction in PARALLEL!", font_size=18, color=GREEN)
        parallel_note.next_to(inst_group, DOWN, buff=0.4)

        # Animate pipeline appearance (slower)
        self.play(
            LaggedStartMap(FadeIn, inst_boxes, lag_ratio=0.15),
            run_time=2
        )
        self.play(
            LaggedStartMap(Write, inst_texts, lag_ratio=0.15),
            run_time=2.5
        )
        self.play(
            LaggedStartMap(ShowCreation, arrows, lag_ratio=0.15),
            run_time=1.5
        )
        self.play(Write(pipeline_label), run_time=1)
        self.play(Write(parallel_note), run_time=1)
        self.wait(2)

        # =====================================================================
        # PART 2: Fade out pipeline, show memory visualization
        # =====================================================================
        pipeline_all = VGroup(inst_group, arrows, pipeline_label, parallel_note)
        self.play(FadeOut(pipeline_all), run_time=1)

        # Initialize shared memory with 64 elements (values 1-64)
        sdata = list(range(1, 65))

        # Create shared memory boxes - two rows for better visibility
        box_width = 0.35
        box_height = 0.5

        # Row 1: indices 0-31
        row1_boxes = VGroup()
        row1_labels = VGroup()
        start_x = -5.5
        row1_y = 0.8

        for i in range(32):
            box = Rectangle(width=box_width, height=box_height)
            box.set_stroke(WHITE, width=1)
            box.set_fill(BLUE_E, opacity=0.3)
            box.move_to([start_x + i * (box_width + 0.02), row1_y, 0])
            row1_boxes.add(box)

            if i % 4 == 0:
                label = Text(f"{i}", font_size=10)
                label.next_to(box, DOWN, buff=0.05)
                row1_labels.add(label)

        # Row 2: indices 32-63
        row2_boxes = VGroup()
        row2_labels = VGroup()
        row2_y = -0.3

        for i in range(32, 64):
            box = Rectangle(width=box_width, height=box_height)
            box.set_stroke(WHITE, width=1)
            box.set_fill(GREEN_E, opacity=0.3)
            box.move_to([start_x + (i - 32) * (box_width + 0.02), row2_y, 0])
            row2_boxes.add(box)

            if i % 4 == 0:
                label = Text(f"{i}", font_size=10)
                label.next_to(box, DOWN, buff=0.05)
                row2_labels.add(label)

        # Thread arrows above row 1 (thinner)
        thread_arrows = VGroup()
        thread_labels_group = VGroup()
        for i in range(0, 32, 4):
            arrow = Line(
                row1_boxes[i].get_top() + UP * 0.35,
                row1_boxes[i].get_top() + UP * 0.08,
                color=YELLOW,
                stroke_width=1.5
            )
            arrow_tip = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            arrow_tip.scale(0.06)
            arrow_tip.next_to(arrow, DOWN, buff=0)
            thread_arrows.add(VGroup(arrow, arrow_tip))

            t_label = Text(f"T{i}", font_size=9, color=YELLOW)
            t_label.next_to(arrow, UP, buff=0.02)
            thread_labels_group.add(t_label)

        # Labels
        row1_label = Text("sdata[0-31]", font_size=16, color=BLUE)
        row1_label.next_to(row1_boxes, LEFT, buff=0.2)

        row2_label = Text("sdata[32-63]", font_size=16, color=GREEN)
        row2_label.next_to(row2_boxes, LEFT, buff=0.2)

        # Show memory (slower)
        self.play(
            LaggedStartMap(FadeIn, row1_boxes, lag_ratio=0.03),
            LaggedStartMap(FadeIn, row2_boxes, lag_ratio=0.03),
            run_time=1.5
        )
        self.play(
            Write(row1_labels), Write(row2_labels),
            Write(row1_label), Write(row2_label),
            run_time=1
        )
        self.play(
            LaggedStartMap(ShowCreation, thread_arrows, lag_ratio=0.08),
            LaggedStartMap(FadeIn, thread_labels_group, lag_ratio=0.08),
            run_time=1
        )
        self.wait(1)

        # =====================================================================
        # PART 3: Instruction-by-instruction with pipeline shown each time
        # =====================================================================

        def show_instruction_and_execute(inst_num, offset, note_text):
            nonlocal sdata

            # Bring instruction back (small, at top right) - 3 lines
            line1, line2, line3 = code_lines[inst_num - 1]
            t1 = Text(line1, font_size=16, font="Consolas", color=YELLOW)
            t2 = Text(line2, font_size=16, font="Consolas", color=WHITE)
            t3 = Text(line3, font_size=16, font="Consolas", color=YELLOW)
            inst_display = VGroup(t1, t2, t3).arrange(DOWN, buff=0.05)
            inst_display.to_edge(RIGHT, buff=0.3).shift(UP * 2.5)
            inst_box = SurroundingRectangle(inst_display, color=YELLOW, buff=0.1)
            inst_label = Text(f"Instruction {inst_num}", font_size=14, color=WHITE)
            inst_label.next_to(inst_box, UP, buff=0.1)

            self.play(
                FadeIn(inst_display),
                ShowCreation(inst_box),
                Write(inst_label),
                run_time=0.8
            )

            # Execute the summation animation
            if inst_num == 1:
                # Thin arrows from row2 to row1 (pointing down to row1)
                arrows = VGroup()
                for i in [0, 8, 16, 24, 31]:
                    # Line from row2 bottom to row1 top
                    line = Line(
                        row2_boxes[i].get_bottom(),
                        row1_boxes[i].get_top(),
                        color=ORANGE,
                        stroke_width=1.5
                    )
                    # Arrow tip pointing down (into row1)
                    tip = Triangle(fill_color=ORANGE, fill_opacity=1, stroke_width=0)
                    tip.scale(0.07)
                    tip.next_to(line, DOWN, buff=0)
                    arrows.add(VGroup(line, tip))

                self.play(
                    *[row1_boxes[i].animate.set_fill(RED, opacity=0.6) for i in range(32)],
                    *[row2_boxes[i].animate.set_fill(ORANGE, opacity=0.6) for i in range(32)],
                    run_time=0.6
                )
                self.play(ShowCreation(arrows), run_time=0.8)

                # Update values
                for i in range(32):
                    sdata[i] = sdata[i] + sdata[i + 32]

                # Show note
                note = Text(note_text, font_size=16, color=TEAL)
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.8)
                self.wait(1)

                # Reset and cleanup
                self.play(
                    *[row1_boxes[i].animate.set_fill(BLUE_E, opacity=0.3) for i in range(32)],
                    *[row2_boxes[i].animate.set_fill(GREEN_E, opacity=0.15) for i in range(32)],
                    FadeOut(arrows),
                    FadeOut(note),
                    run_time=0.6
                )
            else:
                # Within row1 reduction - arrows curve down into destination
                arrows = VGroup()
                sample = [0, offset//2, offset-1] if offset > 2 else list(range(min(offset, 2)))
                for i in sample:
                    if i + offset < 32:
                        # Curved arrow going from source down into destination
                        arrow = CurvedArrow(
                            row1_boxes[i + offset].get_bottom() + DOWN * 0.05,
                            row1_boxes[i].get_bottom() + DOWN * 0.05,
                            angle=TAU/5,  # Positive angle curves below
                            color=ORANGE,
                            stroke_width=1.5
                        )
                        arrows.add(arrow)

                # Highlight active boxes
                self.play(
                    *[row1_boxes[i].animate.set_fill(RED, opacity=0.6) for i in range(min(offset, 32))],
                    *[row1_boxes[i].animate.set_fill(ORANGE, opacity=0.6) for i in range(offset, min(offset*2, 32))],
                    run_time=0.6
                )
                self.play(ShowCreation(arrows), run_time=0.8)

                # Update values
                for i in range(32):
                    if i + offset < 32:
                        sdata[i] = sdata[i] + sdata[i + offset]

                note = Text(note_text, font_size=16, color=TEAL)
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.8)
                self.wait(1)

                self.play(
                    *[row1_boxes[i].animate.set_fill(BLUE_E, opacity=0.3) for i in range(32)],
                    FadeOut(arrows),
                    FadeOut(note),
                    run_time=0.6
                )

            # Fade out instruction display
            self.play(
                FadeOut(inst_display),
                FadeOut(inst_box),
                FadeOut(inst_label),
                run_time=0.5
            )
            self.wait(0.3)

        # Execute all 6 instructions
        show_instruction_and_execute(1, 32, "After inst 1: sdata[0-31] now holds sums from both halves")
        show_instruction_and_execute(2, 16, "After inst 2: sdata[0-15] contains sums of 4 elements each")
        show_instruction_and_execute(3, 8, "After inst 3: sdata[0-7] contains sums of 8 elements each")
        show_instruction_and_execute(4, 4, "After inst 4: sdata[0-3] contains sums of 16 elements each")
        show_instruction_and_execute(5, 2, "After inst 5: sdata[0-1] contains sums of 32 elements each")
        show_instruction_and_execute(6, 1, "After inst 6: sdata[0] = FINAL SUM of all 64 elements!")

        # =====================================================================
        # PART 4: Final highlight
        # =====================================================================
        self.play(
            row1_boxes[0].animate.set_fill(GREEN, opacity=0.9).set_stroke(GREEN, width=3),
            run_time=1
        )

        final_text = Text(f"sdata[0] = {sdata[0]}", font_size=32, color=GREEN)
        final_text.move_to(DOWN * 2.2)

        final_note = Text("Sum of 1 + 2 + ... + 64 = 2080", font_size=20, color=WHITE)
        final_note.next_to(final_text, DOWN, buff=0.2)

        self.play(Write(final_text), run_time=1)
        self.play(Write(final_note), run_time=0.8)

        # Show pipeline one more time as summary
        self.wait(1)

        # Smaller pipeline at bottom
        small_inst_boxes = VGroup()
        small_inst_texts = VGroup()
        for i, (line1, line2, line3) in enumerate(code_lines):
            box = RoundedRectangle(width=1.8, height=0.7, corner_radius=0.05)
            box.set_stroke(WHITE, width=1)
            box.set_fill(BLUE_E, opacity=0.3)

            # Three lines
            t1 = Text(line1, font_size=7, font="Consolas")
            t2 = Text(line2, font_size=7, font="Consolas", color=YELLOW)
            t3 = Text(line3, font_size=7, font="Consolas")
            text_group = VGroup(t1, t2, t3).arrange(DOWN, buff=0.02)
            text_group.move_to(box.get_center())

            small_inst_boxes.add(box)
            small_inst_texts.add(text_group)

        small_inst_group = VGroup(*[VGroup(small_inst_boxes[i], small_inst_texts[i]) for i in range(6)])
        small_inst_group.arrange(RIGHT, buff=0.08)
        small_inst_group.to_edge(DOWN, buff=0.1)

        # Thin arrows for small pipeline
        small_arrows = VGroup()
        for i in range(5):
            line = Line(
                small_inst_boxes[i].get_right() + LEFT * 0.02,
                small_inst_boxes[i + 1].get_left() + RIGHT * 0.02,
                color=YELLOW,
                stroke_width=1
            )
            tip = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            tip.scale(0.05)
            tip.rotate(-PI/2)
            tip.next_to(line, RIGHT, buff=0)
            small_arrows.add(VGroup(line, tip))

        self.play(
            FadeOut(final_text),
            FadeOut(final_note),
            run_time=0.6
        )

        self.play(
            LaggedStartMap(FadeIn, small_inst_boxes, lag_ratio=0.08),
            LaggedStartMap(Write, small_inst_texts, lag_ratio=0.08),
            run_time=1.5
        )
        self.play(
            LaggedStartMap(ShowCreation, small_arrows, lag_ratio=0.08),
            run_time=0.8
        )

        # Final summary
        summary = Text("6 sequential instructions, 32 parallel threads = O(log n) reduction",
                       font_size=18, color=GREEN)
        summary.next_to(small_inst_group, UP, buff=0.3)
        self.play(Write(summary), run_time=1)

        self.wait(3)
