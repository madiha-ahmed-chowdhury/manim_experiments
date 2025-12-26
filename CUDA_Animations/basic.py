from manimlib import *

class SerialVsParallelSum(Scene):
    def construct(self):
        # Configuration
        n = 8  # Number of elements (power of 2 for clean parallel reduction)
        values = [3, 7, 2, 5, 1, 4, 6, 8]  # Example values

        # ============== PART 1: SETUP ==============

        # Main title
        main_title = Text("Vector Summation: Serial vs Parallel")
        main_title.scale(0.6)
        main_title.to_edge(UP, buff=0.2)
        self.play(Write(main_title))
        self.wait(0.5)

        # Create two side panels
        serial_title = Text("Serial (CPU)", color=BLUE)
        serial_title.scale(0.5)
        serial_title.move_to([-3.5, 2.5, 0])

        parallel_title = Text("Parallel (GPU)", color=GREEN)
        parallel_title.scale(0.5)
        parallel_title.move_to([3.5, 2.5, 0])

        # Dividing line
        divider = Line([0, 3, 0], [0, -3, 0], color=WHITE, stroke_width=2)

        self.play(
            Write(serial_title),
            Write(parallel_title),
            ShowCreation(divider)
        )
        self.wait(0.5)

        # ============== SERIAL SIDE (LEFT) ==============

        # Create serial vector boxes - centered on left side
        serial_box_width = 0.45
        serial_box_height = 0.35
        serial_boxes = VGroup()
        serial_value_texts = VGroup()

        # Center the boxes on the left half
        serial_total_width = n * serial_box_width
        serial_start_x = -3.5 - serial_total_width / 2 + serial_box_width / 2

        for i in range(n):
            box = Rectangle(width=serial_box_width, height=serial_box_height, stroke_color=BLUE)
            box.move_to([serial_start_x + i * serial_box_width, 1.8, 0])
            serial_boxes.add(box)

            val_text = Text(str(values[i]))
            val_text.scale(0.3)
            val_text.move_to(box.get_center())
            serial_value_texts.add(val_text)

        # Serial accumulator - positioned below vector
        serial_acc_label = Text("Sum:")
        serial_acc_label.scale(0.3)
        serial_acc_label.move_to([-4.5, 0.3, 0])

        serial_acc_box = Rectangle(width=0.7, height=0.45, stroke_color=YELLOW)
        serial_acc_box.next_to(serial_acc_label, RIGHT, buff=0.15)

        serial_acc_value = Text("0", color=YELLOW)
        serial_acc_value.scale(0.35)
        serial_acc_value.move_to(serial_acc_box.get_center())

        # Serial step counter
        serial_step_label = Text("Steps:")
        serial_step_label.scale(0.3)
        serial_step_label.move_to([-4.5, -0.3, 0])

        serial_step_value = Text("0", color=RED)
        serial_step_value.scale(0.35)
        serial_step_value.next_to(serial_step_label, RIGHT, buff=0.15)

        # ============== PARALLEL SIDE (RIGHT) ==============

        # Create parallel vector boxes
        parallel_box_width = 0.45
        parallel_box_height = 0.35
        parallel_boxes_level0 = VGroup()
        parallel_value_texts_level0 = VGroup()

        # Center the boxes on the right half
        parallel_total_width = n * parallel_box_width
        parallel_start_x = 3.5 - parallel_total_width / 2 + parallel_box_width / 2

        for i in range(n):
            box = Rectangle(width=parallel_box_width, height=parallel_box_height, stroke_color=GREEN)
            box.move_to([parallel_start_x + i * parallel_box_width, 1.8, 0])
            parallel_boxes_level0.add(box)

            val_text = Text(str(values[i]))
            val_text.scale(0.3)
            val_text.move_to(box.get_center())
            parallel_value_texts_level0.add(val_text)

        # Parallel step counter
        parallel_step_label = Text("Steps:")
        parallel_step_label.scale(0.3)
        parallel_step_label.move_to([1.3, -0.3, 0])

        parallel_step_value = Text("0", color=RED)
        parallel_step_value.scale(0.35)
        parallel_step_value.next_to(parallel_step_label, RIGHT, buff=0.15)

        # Show both vectors
        self.play(
            LaggedStart(*[ShowCreation(box) for box in serial_boxes], lag_ratio=0.05),
            LaggedStart(*[ShowCreation(box) for box in parallel_boxes_level0], lag_ratio=0.05),
            run_time=1
        )
        self.play(
            LaggedStart(*[Write(vt) for vt in serial_value_texts], lag_ratio=0.05),
            LaggedStart(*[Write(vt) for vt in parallel_value_texts_level0], lag_ratio=0.05),
            run_time=1
        )

        # Show accumulators and step counters
        self.play(
            Write(serial_acc_label), ShowCreation(serial_acc_box), Write(serial_acc_value),
            Write(serial_step_label), Write(serial_step_value),
            Write(parallel_step_label), Write(parallel_step_value),
        )
        self.wait(0.5)

        # ============== ZOOM INTO SERIAL SIDE ==============

        serial_focus_text = Text("First: Serial Processing", color=BLUE)
        serial_focus_text.scale(0.4)
        serial_focus_text.move_to([-3.5, -2.5, 0])
        self.play(Write(serial_focus_text))

        # Zoom into serial side
        self.play(
            self.camera.frame.animate.move_to([-3.5, 0.5, 0]).set_height(5),
            FadeOut(parallel_title),
            FadeOut(parallel_boxes_level0),
            FadeOut(parallel_value_texts_level0),
            FadeOut(parallel_step_label),
            FadeOut(parallel_step_value),
            FadeOut(divider),
            FadeOut(main_title),
            run_time=1.5
        )
        self.wait(0.3)

        # Serial process explanation
        serial_explain = Text("CPU: One element at a time", color=ORANGE)
        serial_explain.scale(0.3)
        serial_explain.move_to([-3.5, -1.2, 0])
        self.play(Write(serial_explain))

        # Run serial summation with moving dot
        current_sum = 0
        serial_steps = 0

        for i in range(n):
            # Highlight current element
            self.play(
                serial_boxes[i].animate.set_fill(YELLOW, opacity=0.5),
                serial_boxes[i].animate.set_stroke(YELLOW, width=2),
                run_time=0.2
            )

            serial_steps += 1
            current_sum += values[i]

            # Create moving dot from element to accumulator
            moving_dot = Dot(color=YELLOW, radius=0.08)
            moving_dot.move_to(serial_boxes[i].get_center())
            self.add(moving_dot)

            # Animate dot moving to accumulator
            self.play(
                moving_dot.animate.move_to(serial_acc_box.get_center()),
                run_time=0.4
            )

            # Update step counter
            new_step = Text(str(serial_steps), color=RED)
            new_step.scale(0.35)
            new_step.next_to(serial_step_label, RIGHT, buff=0.15)

            # Update accumulator
            new_acc = Text(str(current_sum), color=YELLOW)
            new_acc.scale(0.35)
            new_acc.move_to(serial_acc_box.get_center())

            self.play(
                FadeOut(moving_dot),
                Transform(serial_step_value, new_step),
                Transform(serial_acc_value, new_acc),
                run_time=0.2
            )

            # Mark as processed
            self.play(
                serial_boxes[i].animate.set_fill(BLUE, opacity=0.3),
                serial_boxes[i].animate.set_stroke(BLUE, width=1),
                run_time=0.15
            )

        # Show serial result
        serial_result = Text(f"Result: {current_sum}", color=GREEN)
        serial_result.scale(0.35)
        serial_result.move_to([-3.5, -1.7, 0])

        serial_complexity = Text("Time: O(n) = 8 steps", color=RED)
        serial_complexity.scale(0.3)
        serial_complexity.next_to(serial_result, DOWN, buff=0.1)

        self.play(FadeOut(serial_explain))
        self.play(Write(serial_result), Write(serial_complexity))
        self.wait(0.8)

        # ============== ZOOM OUT ==============

        self.play(FadeOut(serial_focus_text))

        # Recreate parallel side elements
        parallel_boxes_level0_new = VGroup()
        parallel_value_texts_level0_new = VGroup()

        for i in range(n):
            box = Rectangle(width=parallel_box_width, height=parallel_box_height, stroke_color=GREEN)
            box.move_to([parallel_start_x + i * parallel_box_width, 1.8, 0])
            parallel_boxes_level0_new.add(box)

            val_text = Text(str(values[i]))
            val_text.scale(0.3)
            val_text.move_to(box.get_center())
            parallel_value_texts_level0_new.add(val_text)

        parallel_step_value_new = Text("0", color=RED)
        parallel_step_value_new.scale(0.35)
        parallel_step_value_new.next_to(parallel_step_label, RIGHT, buff=0.15)

        # Zoom out to show both
        self.play(
            self.camera.frame.animate.move_to([0, 0, 0]).set_height(7),
            FadeIn(main_title),
            FadeIn(parallel_title),
            FadeIn(divider),
            FadeIn(parallel_boxes_level0_new),
            FadeIn(parallel_value_texts_level0_new),
            FadeIn(parallel_step_label),
            FadeIn(parallel_step_value_new),
            run_time=1.5
        )
        self.wait(0.5)

        # ============== ZOOM INTO PARALLEL SIDE ==============

        parallel_focus_text = Text("Now: Parallel Processing", color=GREEN)
        parallel_focus_text.scale(0.4)
        parallel_focus_text.move_to([3.5, -2.5, 0])
        self.play(Write(parallel_focus_text))

        # Zoom into parallel side
        self.play(
            self.camera.frame.animate.move_to([3.5, 0, 0]).set_height(5.5),
            FadeOut(serial_title),
            FadeOut(serial_boxes),
            FadeOut(serial_value_texts),
            FadeOut(serial_acc_label),
            FadeOut(serial_acc_box),
            FadeOut(serial_acc_value),
            FadeOut(serial_step_label),
            FadeOut(serial_step_value),
            FadeOut(serial_result),
            FadeOut(serial_complexity),
            FadeOut(divider),
            FadeOut(main_title),
            run_time=1.5
        )

        # Parallel process explanation
        parallel_explain = Text("GPU: Multiple elements simultaneously", color=ORANGE)
        parallel_explain.scale(0.28)
        parallel_explain.move_to([3.5, 2.3, 0])
        self.play(Write(parallel_explain))
        self.wait(0.3)

        # ============== PARALLEL REDUCTION ==============

        # Level 0 -> Level 1: 8 -> 4
        level1_values = []
        level1_boxes = VGroup()
        level1_texts = VGroup()
        arrows_0_to_1 = VGroup()

        level1_y = 0.8
        level1_spacing = 0.9

        for i in range(4):
            new_val = values[2*i] + values[2*i + 1]
            level1_values.append(new_val)

            box = Rectangle(width=0.5, height=0.4, stroke_color=GREEN)
            box_x = parallel_start_x + (2*i + 0.5) * parallel_box_width
            box.move_to([box_x, level1_y, 0])
            level1_boxes.add(box)

            val_text = Text(str(new_val))
            val_text.scale(0.3)
            val_text.move_to(box.get_center())
            level1_texts.add(val_text)

            # Arrows from two parents
            arrow1 = Line(
                parallel_boxes_level0_new[2*i].get_bottom(),
                box.get_top(),
                buff=0.05,
                stroke_width=1
            )
            arrow2 = Line(
                parallel_boxes_level0_new[2*i + 1].get_bottom(),
                box.get_top(),
                buff=0.05,
                stroke_width=1
            )
            arrows_0_to_1.add(arrow1, arrow2)

        # Step 1: Show all 4 parallel additions
        step1_text = Text("Step 1: 4 parallel additions", color=YELLOW)
        step1_text.scale(0.28)
        step1_text.move_to([3.5, -2, 0])

        self.play(Write(step1_text))

        # Highlight all pairs simultaneously
        self.play(
            *[parallel_boxes_level0_new[i].animate.set_fill(YELLOW, opacity=0.5) for i in range(n)],
            run_time=0.3
        )

        # Show arrows and new boxes
        self.play(
            LaggedStart(*[ShowCreation(arrow) for arrow in arrows_0_to_1], lag_ratio=0.02),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[ShowCreation(box) for box in level1_boxes], lag_ratio=0.05),
            LaggedStart(*[Write(txt) for txt in level1_texts], lag_ratio=0.05),
            run_time=0.5
        )

        # Update parallel step counter
        new_parallel_step = Text("1", color=RED)
        new_parallel_step.scale(0.35)
        new_parallel_step.next_to(parallel_step_label, RIGHT, buff=0.15)
        self.play(Transform(parallel_step_value_new, new_parallel_step), run_time=0.2)

        # Mark level 0 as processed
        self.play(
            *[parallel_boxes_level0_new[i].animate.set_fill(GREEN, opacity=0.3) for i in range(n)],
            run_time=0.2
        )

        self.play(FadeOut(step1_text))

        # Level 1 -> Level 2: 4 -> 2
        level2_values = []
        level2_boxes = VGroup()
        level2_texts = VGroup()
        arrows_1_to_2 = VGroup()

        level2_y = -0.2

        for i in range(2):
            new_val = level1_values[2*i] + level1_values[2*i + 1]
            level2_values.append(new_val)

            box = Rectangle(width=0.55, height=0.45, stroke_color=GREEN)
            # Position between pairs of level1 boxes
            box_x = (level1_boxes[2*i].get_center()[0] + level1_boxes[2*i + 1].get_center()[0]) / 2
            box.move_to([box_x, level2_y, 0])
            level2_boxes.add(box)

            val_text = Text(str(new_val))
            val_text.scale(0.32)
            val_text.move_to(box.get_center())
            level2_texts.add(val_text)

            arrow1 = Line(level1_boxes[2*i].get_bottom(), box.get_top(), buff=0.05, stroke_width=1)
            arrow2 = Line(level1_boxes[2*i + 1].get_bottom(), box.get_top(), buff=0.05, stroke_width=1)
            arrows_1_to_2.add(arrow1, arrow2)

        # Step 2
        step2_text = Text("Step 2: 2 parallel additions", color=YELLOW)
        step2_text.scale(0.28)
        step2_text.move_to([3.5, -2, 0])

        self.play(Write(step2_text))

        self.play(
            *[level1_boxes[i].animate.set_fill(YELLOW, opacity=0.5) for i in range(4)],
            run_time=0.3
        )

        self.play(
            LaggedStart(*[ShowCreation(arrow) for arrow in arrows_1_to_2], lag_ratio=0.02),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[ShowCreation(box) for box in level2_boxes], lag_ratio=0.05),
            LaggedStart(*[Write(txt) for txt in level2_texts], lag_ratio=0.05),
            run_time=0.5
        )

        new_parallel_step2 = Text("2", color=RED)
        new_parallel_step2.scale(0.35)
        new_parallel_step2.next_to(parallel_step_label, RIGHT, buff=0.15)
        self.play(Transform(parallel_step_value_new, new_parallel_step2), run_time=0.2)

        self.play(
            *[level1_boxes[i].animate.set_fill(GREEN, opacity=0.3) for i in range(4)],
            run_time=0.2
        )

        self.play(FadeOut(step2_text))

        # Level 2 -> Level 3: 2 -> 1 (Final)
        final_value = level2_values[0] + level2_values[1]
        level3_y = -1.2

        final_box = Rectangle(width=0.65, height=0.5, stroke_color=YELLOW, stroke_width=3)
        final_box_x = (level2_boxes[0].get_center()[0] + level2_boxes[1].get_center()[0]) / 2
        final_box.move_to([final_box_x, level3_y, 0])

        final_text = Text(str(final_value), color=YELLOW)
        final_text.scale(0.4)
        final_text.move_to(final_box.get_center())

        arrow_final_1 = Line(level2_boxes[0].get_bottom(), final_box.get_top(), buff=0.05, stroke_width=1)
        arrow_final_2 = Line(level2_boxes[1].get_bottom(), final_box.get_top(), buff=0.05, stroke_width=1)

        # Step 3
        step3_text = Text("Step 3: 1 final addition", color=YELLOW)
        step3_text.scale(0.28)
        step3_text.move_to([3.5, -2, 0])

        self.play(Write(step3_text))

        self.play(
            *[level2_boxes[i].animate.set_fill(YELLOW, opacity=0.5) for i in range(2)],
            run_time=0.3
        )

        self.play(
            ShowCreation(arrow_final_1),
            ShowCreation(arrow_final_2),
            run_time=0.5
        )
        self.play(
            ShowCreation(final_box),
            Write(final_text),
            run_time=0.5
        )

        new_parallel_step3 = Text("3", color=RED)
        new_parallel_step3.scale(0.35)
        new_parallel_step3.next_to(parallel_step_label, RIGHT, buff=0.15)
        self.play(Transform(parallel_step_value_new, new_parallel_step3), run_time=0.2)

        self.play(
            *[level2_boxes[i].animate.set_fill(GREEN, opacity=0.3) for i in range(2)],
            run_time=0.2
        )

        # Parallel result
        parallel_result = Text(f"Result: {final_value}", color=GREEN)
        parallel_result.scale(0.32)
        parallel_result.next_to(final_box, RIGHT, buff=0.3).shift(DOWN * 0.3)

        parallel_complexity = Text("Time: O(log n) = 3 steps", color=RED)
        parallel_complexity.scale(0.28)
        parallel_complexity.next_to(parallel_result, DOWN, buff=0.1)

        self.play(
            FadeOut(step3_text),
            Write(parallel_result),
            Write(parallel_complexity)
        )
        self.wait(0.8)

        self.play(FadeOut(parallel_focus_text), FadeOut(parallel_explain))

        # ============== FINAL ZOOM OUT - COMPARISON ==============

        # Recreate serial side for final comparison
        serial_boxes_final = VGroup()
        serial_value_texts_final = VGroup()

        for i in range(n):
            box = Rectangle(width=serial_box_width, height=serial_box_height, stroke_color=BLUE)
            box.set_fill(BLUE, opacity=0.3)
            box.move_to([serial_start_x + i * serial_box_width, 1.8, 0])
            serial_boxes_final.add(box)

            val_text = Text(str(values[i]))
            val_text.scale(0.3)
            val_text.move_to(box.get_center())
            serial_value_texts_final.add(val_text)

        serial_result_final = Text(f"Result: {current_sum}", color=GREEN)
        serial_result_final.scale(0.35)
        serial_result_final.move_to([-3.5, -1.5, 0])

        serial_complexity_final = Text("O(n) = 8 steps", color=RED)
        serial_complexity_final.scale(0.32)
        serial_complexity_final.next_to(serial_result_final, DOWN, buff=0.1)

        parallel_complexity_final = Text("O(log n) = 3 steps", color=RED)
        parallel_complexity_final.scale(0.32)
        parallel_complexity_final.move_to([3.5, -2.2, 0])

        # Zoom out
        self.play(
            self.camera.frame.animate.move_to([0, 0, 0]).set_height(7),
            FadeIn(main_title),
            FadeIn(serial_title),
            FadeIn(serial_boxes_final),
            FadeIn(serial_value_texts_final),
            FadeIn(serial_result_final),
            FadeIn(serial_complexity_final),
            FadeIn(divider),
            FadeOut(parallel_result),
            FadeOut(parallel_complexity),
            FadeIn(parallel_complexity_final),
            run_time=1.5
        )

        self.wait(0.5)

        # ============== SPEEDUP COMPARISON ==============

        comparison_title = Text("Performance Comparison", color=YELLOW)
        comparison_title.scale(0.45)
        comparison_title.move_to([0, -2.3, 0])

        speedup_text = Text("Speedup: 8/3 = 2.67x faster!", color=YELLOW)
        speedup_text.scale(0.4)
        speedup_text.move_to([0, -2.7, 0])

        self.play(Write(comparison_title))
        self.wait(0.2)
        self.play(Write(speedup_text))

        # Flash the speedup
        flash_rect = Rectangle(width=4, height=0.5, stroke_color=YELLOW, stroke_width=3)
        flash_rect.move_to(speedup_text.get_center())

        self.play(ShowCreation(flash_rect), run_time=0.4)
        self.play(FadeOut(flash_rect), run_time=0.4)

        # Final note about scalability
        scale_note = Text("For n=1M: Parallel is 50,000x faster!", color=ORANGE)
        scale_note.scale(0.35)
        scale_note.move_to([0, -3.1, 0])

        self.play(Write(scale_note))

        self.wait(3)
