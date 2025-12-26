from manimlib import *


class BankConflictFullExplanation(Scene):
    """Run this to see all scenes in sequence"""

    def construct(self):
        self.scene1_shared_memory_bank_layout()
        self.scene2_warp_execution_model()
        self.scene3_single_thread_instruction()
        self.scene4_warp_level_conflict()
        self.scene5_two_accesses_not_problem()
        self.scene6_sequential_addressing()
        self.scene7_final_comparison()

    def clear_scene(self):
        """Clear all objects from the scene"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

    def scene1_shared_memory_bank_layout(self):
        # Title
        title = Text("Scene 1: Shared Memory Bank Layout", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        # Create 32 bank columns
        num_banks = 32
        bank_width = 0.35
        bank_height = 3.5
        banks = VGroup()

        total_width = num_banks * bank_width + (num_banks - 1) * 0.05
        start_x = -total_width / 2

        for i in range(num_banks):
            bank = Rectangle(width=bank_width, height=bank_height)
            bank.set_stroke(WHITE, width=1)
            bank.set_fill(BLUE_E, opacity=0.3)
            bank.move_to([start_x + i * (bank_width + 0.05), -0.3, 0])
            banks.add(bank)

        bank_labels = VGroup()
        for i in range(0, num_banks, 4):
            label = Text(f"B{i}", font_size=14)
            label.next_to(banks[i], DOWN, buff=0.1)
            bank_labels.add(label)

        self.play(LaggedStartMap(FadeIn, banks, lag_ratio=0.02), run_time=1.5)
        self.play(Write(bank_labels))

        rule_text = Text("bank_id = index % 32", font_size=28, color=YELLOW)
        rule_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(rule_text))
        self.wait(0.5)

        row1_elements = VGroup()
        for i in range(num_banks):
            elem = Text(f"[{i}]", font_size=10)
            bank_idx = i % 32
            elem.move_to(banks[bank_idx].get_top() + DOWN * 0.3)
            row1_elements.add(elem)

        self.play(LaggedStartMap(FadeIn, row1_elements, lag_ratio=0.01), run_time=1.5)

        mapping_text = VGroup(
            Text("Bank 0 → sdata[0], sdata[32], sdata[64], ...", font_size=20),
            Text("Bank 1 → sdata[1], sdata[33], sdata[65], ...", font_size=20),
            Text("Bank 2 → sdata[2], sdata[34], sdata[66], ...", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        mapping_text.to_edge(LEFT).shift(DOWN * 3.5)

        self.play(Write(mapping_text), run_time=2)
        self.wait()

        row2_elements = VGroup()
        for i in range(num_banks):
            elem = Text(f"[{i+32}]", font_size=10)
            bank_idx = (i + 32) % 32
            elem.move_to(banks[bank_idx].get_top() + DOWN * 0.6)
            row2_elements.add(elem)

        self.play(LaggedStartMap(FadeIn, row2_elements, lag_ratio=0.01), run_time=1.5)

        highlight_box = SurroundingRectangle(
            VGroup(row1_elements[0], row2_elements[0]), color=RED, buff=0.05
        )
        note = Text("Multiple elements in same bank!", font_size=22, color=RED)
        note.next_to(highlight_box, UP, buff=0.2).shift(RIGHT * 2)

        self.play(ShowCreation(highlight_box), Write(note))
        self.wait(2)
        self.clear_scene()

    def scene2_warp_execution_model(self):
        title = Text("Scene 2: Warp Execution Model", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        threads = VGroup()
        thread_labels = VGroup()
        num_threads = 32
        thread_size = 0.4

        for i in range(num_threads):
            thread_box = Square(side_length=thread_size)
            thread_box.set_stroke(WHITE, width=1)
            thread_box.set_fill(GREEN_E, opacity=0.5)

            row = i // 16
            col = i % 16
            thread_box.move_to([
                (col - 7.5) * (thread_size + 0.1),
                1 - row * (thread_size + 0.3),
                0
            ])
            threads.add(thread_box)

            label = Text(f"T{i}", font_size=12)
            label.move_to(thread_box.get_center())
            thread_labels.add(label)

        warp_label = Text("Warp (32 threads)", font_size=28)
        warp_label.next_to(threads, UP, buff=0.3)

        self.play(Write(warp_label))
        self.play(
            LaggedStartMap(FadeIn, threads, lag_ratio=0.02),
            LaggedStartMap(FadeIn, thread_labels, lag_ratio=0.02),
            run_time=1.5
        )

        lockstep_text = Text("All 32 threads execute the same instruction in lockstep",
                            font_size=24, color=YELLOW)
        lockstep_text.next_to(threads, DOWN, buff=0.5)
        self.play(Write(lockstep_text))

        for _ in range(2):
            self.play(*[t.animate.set_fill(YELLOW, opacity=0.8) for t in threads], run_time=0.3)
            self.play(*[t.animate.set_fill(GREEN_E, opacity=0.5) for t in threads], run_time=0.3)

        key_text = Text("Bank conflicts are checked per instruction, per warp",
                       font_size=28, color=RED)
        key_text.to_edge(DOWN, buff=0.5)
        box = SurroundingRectangle(key_text, color=RED, buff=0.15)

        self.play(Write(key_text), ShowCreation(box))
        self.wait(2)
        self.clear_scene()

    def scene3_single_thread_instruction(self):
        title = Text("Scene 3: Single Thread Instruction Breakdown", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        code_text = Text("sdata[0] += sdata[1];", font_size=32, color=YELLOW)
        code_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(code_text))
        self.wait(0.5)

        arrow_down = Arrow(UP, DOWN, buff=0).scale(0.5)
        arrow_down.next_to(code_text, DOWN, buff=0.3)
        self.play(ShowCreation(arrow_down))

        split_text = Text("Splits into two memory instructions:", font_size=24)
        split_text.next_to(arrow_down, DOWN, buff=0.3)
        self.play(Write(split_text))

        instr1 = VGroup(
            Text("1)", font_size=24, color=BLUE),
            Text("LOAD sdata[1]", font_size=28, color=BLUE)
        ).arrange(RIGHT, buff=0.2)

        instr2 = VGroup(
            Text("2)", font_size=24, color=GREEN),
            Text("STORE sdata[0]", font_size=28, color=GREEN)
        ).arrange(RIGHT, buff=0.2)

        instructions = VGroup(instr1, instr2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        instructions.next_to(split_text, DOWN, buff=0.4)

        self.play(Write(instr1))
        self.wait(0.3)
        self.play(Write(instr2))
        self.wait(0.5)

        banks = VGroup()
        bank_labels_group = VGroup()
        for i in range(4):
            bank = Rectangle(width=1.2, height=1.5)
            bank.set_stroke(WHITE, width=2)
            bank.set_fill(GREY_D, opacity=0.3)
            bank.shift(RIGHT * (i - 1.5) * 1.5 + DOWN * 2)
            banks.add(bank)

            label = Text(f"Bank {i}", font_size=18)
            label.next_to(bank, DOWN, buff=0.1)
            bank_labels_group.add(label)

        self.play(FadeIn(banks), Write(bank_labels_group))

        load_arrow = Arrow(instr1.get_bottom(), banks[1].get_top(), color=BLUE, buff=0.1)
        self.play(ShowCreation(load_arrow))
        self.play(banks[1].animate.set_fill(BLUE, opacity=0.6))

        load_label = Text("LOAD → Bank 1", font_size=20, color=BLUE)
        load_label.next_to(banks[1], RIGHT, buff=0.5)
        self.play(Write(load_label))
        self.wait(0.5)

        store_arrow = Arrow(instr2.get_bottom(), banks[0].get_top(), color=GREEN, buff=0.1)
        self.play(ShowCreation(store_arrow))
        self.play(banks[0].animate.set_fill(GREEN, opacity=0.6))

        store_label = Text("STORE → Bank 0", font_size=20, color=GREEN)
        store_label.next_to(banks[0], LEFT, buff=0.5)
        self.play(Write(store_label))

        key_point = Text("A single thread never causes a bank conflict even if they are accessing the same bank!",
                        font_size=26, color=YELLOW)
        key_point.to_edge(DOWN, buff=0.3)
        box = SurroundingRectangle(key_point, color=YELLOW, buff=0.1)
        self.play(Write(key_point), ShowCreation(box))
        self.wait(2)
        self.clear_scene()

    def scene4_warp_level_conflict(self):
        title = Text("Scene 4: Warp-Level Bank Conflict", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        thread0_box = Square(side_length=0.8)
        thread0_box.set_stroke(WHITE, width=2)
        thread0_box.set_fill(GREEN_E, opacity=0.5)
        thread0_label = Text("T0", font_size=24)
        thread0 = VGroup(thread0_box, thread0_label)
        thread0.move_to(LEFT * 4 + UP * 2)

        thread16_box = Square(side_length=0.8)
        thread16_box.set_stroke(WHITE, width=2)
        thread16_box.set_fill(GREEN_E, opacity=0.5)
        thread16_label = Text("T16", font_size=24)
        thread16 = VGroup(thread16_box, thread16_label)
        thread16.move_to(RIGHT * 4 + UP * 2)

        self.play(FadeIn(thread0), FadeIn(thread16))

        code0 = Text("sdata[0] += sdata[1]", font_size=22, color=BLUE)
        code0.next_to(thread0, DOWN, buff=0.3)

        code16 = Text("sdata[32] += sdata[33]", font_size=22, color=BLUE)
        code16.next_to(thread16, DOWN, buff=0.3)

        self.play(Write(code0), Write(code16))
        self.wait(0.5)

        focus_text = Text("Focus on LOAD instruction:", font_size=26, color=YELLOW)
        focus_text.shift(UP * 0.3)
        self.play(Write(focus_text))

        load0 = Text("loads sdata[1]", font_size=20)
        load0.next_to(code0, DOWN, buff=0.2)

        load16 = Text("loads sdata[33]", font_size=20)
        load16.next_to(code16, DOWN, buff=0.2)

        self.play(Write(load0), Write(load16))

        banks = VGroup()
        for i in range(4):
            bank = Rectangle(width=1.8, height=1.2)
            bank.set_stroke(WHITE, width=2)
            bank.set_fill(GREY_D, opacity=0.3)
            bank.shift(RIGHT * (i - 1.5) * 2.2 + DOWN * 2.5)
            banks.add(bank)

            label = Text(f"Bank {i}", font_size=20)
            label.move_to(bank.get_center())
            banks.add(label)

        self.play(FadeIn(banks))

        calc0 = Text("1 % 32 = 1 → Bank 1", font_size=18, color=TEAL)
        calc0.next_to(load0, DOWN, buff=0.15)

        calc16 = Text("33 % 32 = 1 → Bank 1", font_size=18, color=TEAL)
        calc16.next_to(load16, DOWN, buff=0.15)

        self.play(Write(calc0), Write(calc16))

        arrow0 = Arrow(calc0.get_bottom(), banks[2].get_top() + LEFT * 0.3, color=RED, buff=0.1)
        arrow16 = Arrow(calc16.get_bottom(), banks[2].get_top() + RIGHT * 0.3, color=RED, buff=0.1)

        self.play(ShowCreation(arrow0), ShowCreation(arrow16))

        bank1_rect = banks[2]
        self.play(bank1_rect.animate.set_fill(RED, opacity=0.8), rate_func=there_and_back, run_time=0.5)
        self.play(bank1_rect.animate.set_fill(RED, opacity=0.8), rate_func=there_and_back, run_time=0.5)
        bank1_rect.set_fill(RED, opacity=0.6)

        conflict_label = Text("BANK CONFLICT!", font_size=32, color=RED)
        conflict_label.next_to(banks, DOWN, buff=0.3)
        self.play(Write(conflict_label))

        explanation = Text(
            "Different elements (sdata[1] vs sdata[33]) but SAME bank!",
            font_size=22, color=YELLOW
        )
        explanation.to_edge(DOWN, buff=0.2)
        self.play(Write(explanation))
        self.wait(2)
        self.clear_scene()

    def scene5_two_accesses_not_problem(self):
        title = Text("Scene 5: Why Two Accesses Per Thread Is NOT the Problem", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        timeline_label = Text("Time →", font_size=24)
        timeline_label.to_edge(LEFT).shift(UP * 1.5 + RIGHT * 0.5)

        timeline = Arrow(LEFT * 5, RIGHT * 5, color=WHITE, buff=0)
        timeline.shift(UP * 1)

        self.play(Write(timeline_label), ShowCreation(timeline))

        instr1_box = Rectangle(width=3, height=1)
        instr1_box.set_fill(BLUE, opacity=0.5)
        instr1_box.set_stroke(BLUE, width=2)
        instr1_box.move_to(LEFT * 2.5 + UP * 1)

        instr1_label = Text("LOAD sdata[1]", font_size=20)
        instr1_label.move_to(instr1_box.get_center())

        instr2_box = Rectangle(width=3, height=1)
        instr2_box.set_fill(GREEN, opacity=0.5)
        instr2_box.set_stroke(GREEN, width=2)
        instr2_box.move_to(RIGHT * 2.5 + UP * 1)

        instr2_label = Text("STORE sdata[0]", font_size=20)
        instr2_label.move_to(instr2_box.get_center())

        self.play(FadeIn(instr1_box), Write(instr1_label))
        self.wait(0.3)
        self.play(FadeIn(instr2_box), Write(instr2_label))

        bank1_access = Text("Bank 1", font_size=18, color=BLUE)
        bank1_access.next_to(instr1_box, DOWN, buff=0.2)

        bank0_access = Text("Bank 0", font_size=18, color=GREEN)
        bank0_access.next_to(instr2_box, DOWN, buff=0.2)

        self.play(Write(bank1_access), Write(bank0_access))

        point1 = Text("Each thread touches two banks...", font_size=26)
        point1.shift(DOWN * 0.8)
        self.play(Write(point1))

        point2 = Text("...but in DIFFERENT instructions!", font_size=26, color=YELLOW)
        point2.next_to(point1, DOWN, buff=0.3)
        self.play(Write(point2))

        separator = Line(LEFT * 6, RIGHT * 6, color=GREY)
        separator.shift(DOWN * 1.8)
        self.play(ShowCreation(separator))

        emphasis = VGroup(
            Text("Conflicts only occur when", font_size=22),
            Text("MULTIPLE THREADS", font_size=26, color=RED),
            Text("access the same bank in the", font_size=22),
            Text("SAME INSTRUCTION", font_size=26, color=RED),
        ).arrange(DOWN, buff=0.1)
        emphasis.to_edge(DOWN, buff=0.4)

        self.play(Write(emphasis), run_time=2)
        self.wait(2)
        self.clear_scene()

    def scene6_sequential_addressing(self):
        title = Text("Scene 6: Sequential Addressing Pattern", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        code = Text("sdata[tid] += sdata[tid + blockDim.x / 2];", font_size=28, color=YELLOW)
        code.next_to(title, DOWN, buff=0.4)
        self.play(Write(code))

        explain = Text("For a warp of 32 threads (tid = 0 to 31):", font_size=22)
        explain.next_to(code, DOWN, buff=0.3)
        self.play(Write(explain))

        math_text = VGroup(
            Text("tid + blockDim.x/2 maps to:", font_size=18),
            Text("Thread 0  → sdata[128] → Bank 0", font_size=16),
            Text("Thread 1  → sdata[129] → Bank 1", font_size=16),
            Text("...", font_size=16),
            Text("Thread 31 → sdata[159] → Bank 31", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        math_text.next_to(explain, DOWN, buff=0.2)
        math_text.to_edge(LEFT, buff=0.3)

        self.play(Write(math_text), run_time=1.5)
        self.wait(0.5)

        visual_label = Text("Perfect 1-to-1 mapping:", font_size=22, color=GREEN)
        visual_label.next_to(math_text, DOWN, buff=0.3).shift(RIGHT * 5)
        self.play(Write(visual_label))

        threads_row = VGroup()
        banks_row = VGroup()
        arrows = VGroup()

        for i in range(8):
            t_box = Square(side_length=0.45)
            t_box.set_fill(GREEN_E, opacity=0.5)
            t_box.set_stroke(WHITE, width=1)
            t_label = Text(f"T{i}", font_size=11)
            thread = VGroup(t_box, t_label)
            thread.move_to(RIGHT * (i - 3.5) * 0.6 + DOWN * 1.8)
            threads_row.add(thread)

            b_box = Square(side_length=0.45)
            b_box.set_fill(BLUE_E, opacity=0.5)
            b_box.set_stroke(WHITE, width=1)
            b_label = Text(f"B{i}", font_size=11)
            bank = VGroup(b_box, b_label)
            bank.move_to(RIGHT * (i - 3.5) * 0.6 + DOWN * 2.8)
            banks_row.add(bank)

            arrow = Arrow(thread.get_bottom(), bank.get_top(), color=GREEN, buff=0.05, stroke_width=2)
            arrows.add(arrow)

        dots1 = Text("...", font_size=18)
        dots1.next_to(threads_row, RIGHT, buff=0.15)
        dots2 = Text("...", font_size=18)
        dots2.next_to(banks_row, RIGHT, buff=0.15)

        self.play(FadeIn(threads_row), FadeIn(banks_row))
        self.play(LaggedStartMap(ShowCreation, arrows, lag_ratio=0.1))
        self.play(Write(dots1), Write(dots2))

        result = Text("NO BANK CONFLICTS - Each bank accessed exactly once!",
                     font_size=22, color=GREEN)
        result.to_edge(DOWN, buff=0.2)
        box = SurroundingRectangle(result, color=GREEN, buff=0.1)
        self.play(Write(result), ShowCreation(box))
        self.wait(2)
        self.clear_scene()

    def scene7_final_comparison(self):
        title = Text("Scene 7: Interleaved vs Sequential Addressing", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        divider = Line(UP * 2.5, DOWN * 3, color=GREY)
        self.play(ShowCreation(divider))

        # LEFT SIDE
        left_title = Text("Interleaved Addressing", font_size=26, color=RED)
        left_title.move_to(LEFT * 3.5 + UP * 2)
        self.play(Write(left_title))

        left_code = Text("sdata[tid*2] += sdata[tid*2+1]", font_size=16, color=YELLOW)
        left_code.next_to(left_title, DOWN, buff=0.2)
        self.play(Write(left_code))

        left_threads = VGroup()
        left_banks = VGroup()

        for idx in range(4):
            t_box = Square(side_length=0.4)
            t_box.set_fill(GREEN_E, opacity=0.5)
            t_label = Text(f"T{idx}", font_size=10)
            thread = VGroup(t_box, t_label)
            thread.move_to(LEFT * (5 - idx * 0.6) + UP * 0.8)
            left_threads.add(thread)

        for i in range(8):
            b_box = Rectangle(width=0.35, height=0.8)
            b_box.set_fill(BLUE_E, opacity=0.3)
            b_box.set_stroke(WHITE, width=1)
            b_label = Text(f"B{i}", font_size=8)
            b_label.next_to(b_box, DOWN, buff=0.05)
            bank = VGroup(b_box, b_label)
            bank.move_to(LEFT * (5.5 - i * 0.5) + DOWN * 0.8)
            left_banks.add(bank)

        self.play(FadeIn(left_threads), FadeIn(left_banks))

        conflict_arrow1 = Arrow(
            left_threads[0].get_bottom(), left_banks[1].get_top(),
            color=RED, buff=0.05, stroke_width=2
        )
        conflict_arrow2 = Arrow(
            left_threads[1].get_bottom() + LEFT * 0.1, left_banks[1].get_top() + RIGHT * 0.1,
            color=RED, buff=0.05, stroke_width=2
        )

        self.play(ShowCreation(conflict_arrow1), ShowCreation(conflict_arrow2))
        self.play(left_banks[1][0].animate.set_fill(RED, opacity=0.7))

        conflict_label = Text("CONFLICT!", font_size=16, color=RED)
        conflict_label.next_to(left_banks[1], DOWN, buff=0.4)
        self.play(Write(conflict_label))

        # RIGHT SIDE
        right_title = Text("Sequential Addressing", font_size=26, color=GREEN)
        right_title.move_to(RIGHT * 3.5 + UP * 2)
        self.play(Write(right_title))

        right_code = Text("sdata[tid] += sdata[tid+n/2]", font_size=16, color=YELLOW)
        right_code.next_to(right_title, DOWN, buff=0.2)
        self.play(Write(right_code))

        right_threads = VGroup()
        right_banks = VGroup()
        right_arrows = VGroup()

        for i in range(8):
            t_box = Square(side_length=0.4)
            t_box.set_fill(GREEN_E, opacity=0.5)
            t_label = Text(f"T{i}", font_size=10)
            thread = VGroup(t_box, t_label)
            thread.move_to(RIGHT * (2 + i * 0.55) + UP * 0.8)
            right_threads.add(thread)

            b_box = Rectangle(width=0.35, height=0.8)
            b_box.set_fill(GREEN_E, opacity=0.3)
            b_box.set_stroke(WHITE, width=1)
            b_label = Text(f"B{i}", font_size=8)
            b_label.next_to(b_box, DOWN, buff=0.05)
            bank = VGroup(b_box, b_label)
            bank.move_to(RIGHT * (2 + i * 0.55) + DOWN * 0.8)
            right_banks.add(bank)

            arrow = Arrow(thread.get_bottom(), bank.get_top(), color=GREEN, buff=0.05, stroke_width=2)
            right_arrows.add(arrow)

        self.play(FadeIn(right_threads), FadeIn(right_banks))
        self.play(LaggedStartMap(ShowCreation, right_arrows, lag_ratio=0.05))

        clean_label = Text("NO CONFLICTS", font_size=16, color=GREEN)
        clean_label.next_to(right_banks, DOWN, buff=0.4)
        self.play(Write(clean_label))

        caption = Text(
            "Sequential addressing avoids modulo wraparound inside a warp,\n"
            "eliminating shared memory bank conflicts.",
            font_size=22, color=YELLOW
        )
        caption.to_edge(DOWN, buff=0.3)
        box = SurroundingRectangle(caption, color=YELLOW, buff=0.15)

        self.play(Write(caption), ShowCreation(box), run_time=2)
        self.wait(2)
