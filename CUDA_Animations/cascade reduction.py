from manimlib import *


class GridStrideReduction(Scene):
    def construct(self):
        # =====================================================================
        # SCENE 1: Show the code first
        # =====================================================================
        title = Text("Grid-Stride Reduction in CUDA", font_size=36)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.5)

        # Show the kernel code
        code_title = Text("Kernel Code:", font_size=24, color=YELLOW)
        code_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(code_title), run_time=0.8)

        code_lines = VGroup(
            Text("unsigned int tid = threadIdx.x;", font_size=16, font="Consolas"),
            Text("unsigned int i = blockIdx.x*(blockSize*2) + threadIdx.x;", font_size=16, font="Consolas"),
            Text("unsigned int gridSize = blockSize*2*gridDim.x;", font_size=16, font="Consolas"),
            Text("sdata[tid] = 0;", font_size=16, font="Consolas"),
            Text("while (i < n) {", font_size=16, font="Consolas"),
            Text("    sdata[tid] += g_idata[i] + g_idata[i+blockSize];", font_size=16, font="Consolas", color=GREEN),
            Text("    i += gridSize;", font_size=16, font="Consolas"),
            Text("}", font_size=16, font="Consolas"),
        )
        code_lines.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        code_lines.next_to(code_title, DOWN, buff=0.3)

        code_box = SurroundingRectangle(code_lines, color=WHITE, buff=0.2)

        self.play(
            ShowCreation(code_box),
            LaggedStartMap(Write, code_lines, lag_ratio=0.15),
            run_time=3
        )
        self.wait(2)

        # =====================================================================
        # SCENE 2: Show configuration and thread info
        # =====================================================================
        self.play(
            FadeOut(code_lines),
            FadeOut(code_box),
            FadeOut(code_title),
            run_time=0.8
        )

        config_title = Text("Configuration:", font_size=24, color=YELLOW)
        config_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(config_title), run_time=0.6)

        # Configuration with calculations
        config_items = VGroup(
            Text("n = 128 elements", font_size=20),
            Text("blockSize = 4 threads per block", font_size=20),
            Text("gridDim.x = 4 blocks", font_size=20),
            Text("gridSize = blockSize × 2 × gridDim.x = 4 × 2 × 4 = 32", font_size=20, color=YELLOW),
        )
        config_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        config_items.next_to(config_title, DOWN, buff=0.4)

        self.play(
            LaggedStartMap(Write, config_items, lag_ratio=0.3),
            run_time=2.5
        )
        self.wait(1.5)

        # Thread calculation
        thread_calc_title = Text("Each thread sums:", font_size=22, color=GREEN)
        thread_calc_title.next_to(config_items, DOWN, buff=0.5)

        thread_calc = VGroup(
            Text("128 elements ÷ (4 blocks × 4 threads) = 8 elements per thread", font_size=18),
            Text("But each iteration loads 2 elements (i and i+blockSize)", font_size=18),
            Text("So each thread does 4 iterations of the while loop", font_size=18, color=YELLOW),
        )
        thread_calc.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        thread_calc.next_to(thread_calc_title, DOWN, buff=0.2)

        self.play(Write(thread_calc_title), run_time=0.6)
        self.play(
            LaggedStartMap(Write, thread_calc, lag_ratio=0.3),
            run_time=2
        )
        self.wait(2)

        # Clear for array visualization
        self.play(
            FadeOut(config_title),
            FadeOut(config_items),
            FadeOut(thread_calc_title),
            FadeOut(thread_calc),
            run_time=0.8
        )

        # =====================================================================
        # SCENE 3: Show the full array (128 elements)
        # =====================================================================
        global_label = Text("Global Memory: g_idata[0] ... g_idata[127]", font_size=22, color=BLUE)
        global_label.next_to(title, DOWN, buff=0.3)
        self.play(Write(global_label), run_time=1)

        # Create 128 boxes (split into 2 rows for visibility)
        box_width = 0.17
        box_height = 0.35

        # Row 1: array[0-63]
        row1_boxes = VGroup()
        start_x = -5.5
        row1_y = 0.5

        for i in range(64):
            box = Rectangle(width=box_width, height=box_height)
            box.set_stroke(WHITE, width=0.5)
            box.set_fill(BLUE_E, opacity=0.3)
            box.move_to([start_x + i * (box_width + 0.01), row1_y, 0])
            row1_boxes.add(box)

        # Row 2: array[64-127]
        row2_boxes = VGroup()
        row2_y = -0.2

        for i in range(64):
            box = Rectangle(width=box_width, height=box_height)
            box.set_stroke(WHITE, width=0.5)
            box.set_fill(BLUE_E, opacity=0.3)
            box.move_to([start_x + i * (box_width + 0.01), row2_y, 0])
            row2_boxes.add(box)

        all_boxes = VGroup(row1_boxes, row2_boxes)

        # Labels for key indices
        idx_labels = VGroup()
        for idx in [0, 32, 63]:
            label = Text(f"[{idx}]", font_size=10)
            label.next_to(row1_boxes[idx], DOWN, buff=0.03)
            idx_labels.add(label)
        for idx in [0, 32, 63]:
            label = Text(f"[{idx + 64}]", font_size=10)
            label.next_to(row2_boxes[idx], DOWN, buff=0.03)
            idx_labels.add(label)

        self.play(
            LaggedStartMap(FadeIn, row1_boxes, lag_ratio=0.01),
            LaggedStartMap(FadeIn, row2_boxes, lag_ratio=0.01),
            run_time=2
        )
        self.play(Write(idx_labels), run_time=1)
        self.wait(1)

        # =====================================================================
        # SCENE 4: Block 0, Thread 0 detailed with calculations
        # =====================================================================
        block0_title = Text("Block 0, Thread 0 - Step by Step", font_size=22, color=GREEN)
        block0_title.next_to(global_label, DOWN, buff=0.1)
        self.play(
            FadeOut(global_label),
            Write(block0_title),
            run_time=1
        )

        def get_box(idx):
            if idx < 64:
                return row1_boxes[idx]
            else:
                return row2_boxes[idx - 64]

        # Show calculations for Thread 0 of Block 0
        # tid = 0, blockIdx.x = 0
        # i = 0*(4*2) + 0 = 0
        # gridSize = 4*2*4 = 32

        # Initial calculation
        init_calc = VGroup(
            Text("tid = threadIdx.x = 0", font_size=14, font="Consolas"),
            Text("blockIdx.x = 0", font_size=14, font="Consolas"),
            Text("i = 0*(4*2) + 0 = 0", font_size=14, font="Consolas", color=YELLOW),
            Text("gridSize = 32", font_size=14, font="Consolas"),
        )
        init_calc.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        init_calc.to_edge(RIGHT, buff=0.3).shift(UP * 2)

        init_box = SurroundingRectangle(init_calc, color=GREEN, buff=0.1)

        self.play(
            ShowCreation(init_box),
            Write(init_calc),
            run_time=1.5
        )
        self.wait(1)

        # Iteration 1: i=0, access g_idata[0] + g_idata[4]
        iter_label = Text("Iteration 1: i = 0", font_size=16, color=YELLOW)
        iter_label.to_edge(DOWN, buff=0.6)

        op_text = Text("sdata[0] += g_idata[0] + g_idata[4]", font_size=16, font="Consolas", color=GREEN)
        op_text.next_to(iter_label, DOWN, buff=0.15)

        self.play(Write(iter_label), Write(op_text), run_time=0.8)

        box1, box2 = get_box(0), get_box(4)
        self.play(
            box1.animate.set_fill(RED, opacity=0.8),
            box2.animate.set_fill(ORANGE, opacity=0.8),
            run_time=0.6
        )
        self.wait(0.8)
        self.play(
            box1.animate.set_fill(BLUE_E, opacity=0.3),
            box2.animate.set_fill(BLUE_E, opacity=0.3),
            run_time=0.4
        )

        # Update i
        update_text = Text("i += gridSize → i = 0 + 32 = 32", font_size=14, color=WHITE)
        update_text.next_to(op_text, DOWN, buff=0.1)
        self.play(Write(update_text), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(iter_label), FadeOut(op_text), FadeOut(update_text), run_time=0.4)

        # Iteration 2: i=32, access g_idata[32] + g_idata[36]
        iter_label = Text("Iteration 2: i = 32", font_size=16, color=YELLOW)
        iter_label.to_edge(DOWN, buff=0.6)

        op_text = Text("sdata[0] += g_idata[32] + g_idata[36]", font_size=16, font="Consolas", color=GREEN)
        op_text.next_to(iter_label, DOWN, buff=0.15)

        self.play(Write(iter_label), Write(op_text), run_time=0.8)

        box1, box2 = get_box(32), get_box(36)
        self.play(
            box1.animate.set_fill(RED, opacity=0.8),
            box2.animate.set_fill(ORANGE, opacity=0.8),
            run_time=0.6
        )
        self.wait(0.8)
        self.play(
            box1.animate.set_fill(BLUE_E, opacity=0.3),
            box2.animate.set_fill(BLUE_E, opacity=0.3),
            run_time=0.4
        )

        update_text = Text("i += gridSize → i = 32 + 32 = 64", font_size=14, color=WHITE)
        update_text.next_to(op_text, DOWN, buff=0.1)
        self.play(Write(update_text), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(iter_label), FadeOut(op_text), FadeOut(update_text), run_time=0.4)

        # Iteration 3: i=64, access g_idata[64] + g_idata[68]
        iter_label = Text("Iteration 3: i = 64", font_size=16, color=YELLOW)
        iter_label.to_edge(DOWN, buff=0.6)

        op_text = Text("sdata[0] += g_idata[64] + g_idata[68]", font_size=16, font="Consolas", color=GREEN)
        op_text.next_to(iter_label, DOWN, buff=0.15)

        self.play(Write(iter_label), Write(op_text), run_time=0.8)

        box1, box2 = get_box(64), get_box(68)
        self.play(
            box1.animate.set_fill(RED, opacity=0.8),
            box2.animate.set_fill(ORANGE, opacity=0.8),
            run_time=0.6
        )
        self.wait(0.8)
        self.play(
            box1.animate.set_fill(BLUE_E, opacity=0.3),
            box2.animate.set_fill(BLUE_E, opacity=0.3),
            run_time=0.4
        )

        update_text = Text("i += gridSize → i = 64 + 32 = 96", font_size=14, color=WHITE)
        update_text.next_to(op_text, DOWN, buff=0.1)
        self.play(Write(update_text), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(iter_label), FadeOut(op_text), FadeOut(update_text), run_time=0.4)

        # Iteration 4: i=96, access g_idata[96] + g_idata[100]
        iter_label = Text("Iteration 4: i = 96", font_size=16, color=YELLOW)
        iter_label.to_edge(DOWN, buff=0.6)

        op_text = Text("sdata[0] += g_idata[96] + g_idata[100]", font_size=16, font="Consolas", color=GREEN)
        op_text.next_to(iter_label, DOWN, buff=0.15)

        self.play(Write(iter_label), Write(op_text), run_time=0.8)

        box1, box2 = get_box(96), get_box(100)
        self.play(
            box1.animate.set_fill(RED, opacity=0.8),
            box2.animate.set_fill(ORANGE, opacity=0.8),
            run_time=0.6
        )
        self.wait(0.8)
        self.play(
            box1.animate.set_fill(BLUE_E, opacity=0.3),
            box2.animate.set_fill(BLUE_E, opacity=0.3),
            run_time=0.4
        )

        update_text = Text("i += gridSize → i = 96 + 32 = 128 ≥ n, STOP", font_size=14, color=RED)
        update_text.next_to(op_text, DOWN, buff=0.1)
        self.play(Write(update_text), run_time=0.6)
        self.wait(1)

        # Summary for Thread 0
        thread0_summary = Text("Thread 0 summed 8 elements: [0,4,32,36,64,68,96,100]", font_size=16, color=GREEN)
        thread0_summary.next_to(update_text, DOWN, buff=0.2)
        self.play(Write(thread0_summary), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(iter_label), FadeOut(op_text), FadeOut(update_text),
            FadeOut(thread0_summary), FadeOut(init_calc), FadeOut(init_box),
            run_time=0.6
        )

        # =====================================================================
        # SCENE 5: Show all threads of Block 0
        # =====================================================================
        self.play(FadeOut(block0_title), run_time=0.4)

        all_threads_title = Text("All 4 Threads of Block 0 (in parallel)", font_size=22, color=GREEN)
        all_threads_title.next_to(title, DOWN, buff=0.25)
        self.play(Write(all_threads_title), run_time=0.8)

        # Show all threads info
        thread_info = VGroup(
            Text("Thread 0: [0,4], [32,36], [64,68], [96,100]", font_size=14, color=RED),
            Text("Thread 1: [1,5], [33,37], [65,69], [97,101]", font_size=14, color=ORANGE),
            Text("Thread 2: [2,6], [34,38], [66,70], [98,102]", font_size=14, color=TEAL),
            Text("Thread 3: [3,7], [35,39], [67,71], [99,103]", font_size=14, color=PURPLE),
        )
        thread_info.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        thread_info.to_edge(RIGHT, buff=0.2).shift(UP * 1.5)

        self.play(
            LaggedStartMap(Write, thread_info, lag_ratio=0.2),
            run_time=2
        )

        # Highlight all Block 0 accesses
        block0_indices = [0, 4, 32, 36, 64, 68, 96, 100,
                         1, 5, 33, 37, 65, 69, 97, 101,
                         2, 6, 34, 38, 66, 70, 98, 102,
                         3, 7, 35, 39, 67, 71, 99, 103]

        anims = []
        for idx in block0_indices:
            box = get_box(idx)
            anims.append(box.animate.set_fill(RED, opacity=0.6))
        self.play(*anims, run_time=1.5)

        parallel_note = Text("All 4 threads execute their while loops in parallel!", font_size=18, color=GREEN)
        parallel_note.to_edge(DOWN, buff=0.4)
        self.play(Write(parallel_note), run_time=1)
        self.wait(2)

        # Reset
        reset_anims = []
        for idx in block0_indices:
            box = get_box(idx)
            reset_anims.append(box.animate.set_fill(BLUE_E, opacity=0.3))
        self.play(*reset_anims, FadeOut(parallel_note), run_time=0.8)

        # =====================================================================
        # SCENE 6: Show Block 1 with calculation
        # =====================================================================
        self.play(FadeOut(all_threads_title), FadeOut(thread_info), run_time=0.5)

        block1_title = Text("Block 1, Thread 0 - Different Starting Point", font_size=22, color=ORANGE)
        block1_title.next_to(title, DOWN, buff=0.25)
        self.play(Write(block1_title), run_time=0.8)

        # Block 1 calculation
        block1_calc = VGroup(
            Text("tid = threadIdx.x = 0", font_size=14, font="Consolas"),
            Text("blockIdx.x = 1", font_size=14, font="Consolas"),
            Text("i = 1*(4*2) + 0 = 8", font_size=14, font="Consolas", color=YELLOW),
            Text("gridSize = 32", font_size=14, font="Consolas"),
        )
        block1_calc.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        block1_calc.to_edge(RIGHT, buff=0.3).shift(UP * 2)

        block1_box = SurroundingRectangle(block1_calc, color=ORANGE, buff=0.1)

        self.play(
            ShowCreation(block1_box),
            Write(block1_calc),
            run_time=1.5
        )

        # Show Block 1 Thread 0 iterations
        block1_ops = [(8, 12), (40, 44), (72, 76), (104, 108)]
        i_values = [8, 40, 72, 104]

        for iter_num, ((idx1, idx2), i_val) in enumerate(zip(block1_ops, i_values)):
            iter_label = Text(f"Iteration {iter_num + 1}: i = {i_val}", font_size=16, color=YELLOW)
            iter_label.to_edge(DOWN, buff=0.6)

            op_text = Text(f"sdata[0] += g_idata[{idx1}] + g_idata[{idx2}]", font_size=16, font="Consolas", color=ORANGE)
            op_text.next_to(iter_label, DOWN, buff=0.15)

            self.play(Write(iter_label), Write(op_text), run_time=0.6)

            box1, box2 = get_box(idx1), get_box(idx2)
            self.play(
                box1.animate.set_fill(ORANGE, opacity=0.8),
                box2.animate.set_fill(YELLOW, opacity=0.8),
                run_time=0.5
            )
            self.wait(0.5)
            self.play(
                box1.animate.set_fill(BLUE_E, opacity=0.3),
                box2.animate.set_fill(BLUE_E, opacity=0.3),
                FadeOut(iter_label), FadeOut(op_text),
                run_time=0.4
            )

        self.play(FadeOut(block1_calc), FadeOut(block1_box), run_time=0.5)

        # =====================================================================
        # SCENE 7: All blocks overview
        # =====================================================================
        self.play(FadeOut(block1_title), run_time=0.4)

        overview_title = Text("All 4 Blocks Working in Parallel", font_size=24, color=YELLOW)
        overview_title.next_to(title, DOWN, buff=0.25)
        self.play(Write(overview_title), run_time=0.8)

        # Highlight all blocks with different colors
        block_colors = [RED, ORANGE, GREEN, PURPLE]
        block_all_indices = [
            # Block 0: all threads
            [0, 4, 1, 5, 2, 6, 3, 7, 32, 36, 33, 37, 34, 38, 35, 39,
             64, 68, 65, 69, 66, 70, 67, 71, 96, 100, 97, 101, 98, 102, 99, 103],
            # Block 1: all threads
            [8, 12, 9, 13, 10, 14, 11, 15, 40, 44, 41, 45, 42, 46, 43, 47,
             72, 76, 73, 77, 74, 78, 75, 79, 104, 108, 105, 109, 106, 110, 107, 111],
            # Block 2: all threads
            [16, 20, 17, 21, 18, 22, 19, 23, 48, 52, 49, 53, 50, 54, 51, 55,
             80, 84, 81, 85, 82, 86, 83, 87, 112, 116, 113, 117, 114, 118, 115, 119],
            # Block 3: all threads
            [24, 28, 25, 29, 26, 30, 27, 31, 56, 60, 57, 61, 58, 62, 59, 63,
             88, 92, 89, 93, 90, 94, 91, 95, 120, 124, 121, 125, 122, 126, 123, 127],
        ]

        anims = []
        for block_num, indices in enumerate(block_all_indices):
            color = block_colors[block_num]
            for idx in indices:
                box = get_box(idx)
                anims.append(box.animate.set_fill(color, opacity=0.7))
        self.play(*anims, run_time=2)

        block_legend = VGroup(
            Text("Block 0", font_size=16, color=RED),
            Text("Block 1", font_size=16, color=ORANGE),
            Text("Block 2", font_size=16, color=GREEN),
            Text("Block 3", font_size=16, color=PURPLE),
        )
        block_legend.arrange(RIGHT, buff=0.5)
        block_legend.to_edge(DOWN, buff=0.3)
        self.play(Write(block_legend), run_time=1)

        coverage_note = Text("All 128 elements covered by 4 blocks × 4 threads!", font_size=18, color=WHITE)
        coverage_note.next_to(block_legend, UP, buff=0.2)
        self.play(Write(coverage_note), run_time=1)
        self.wait(2)

        # =====================================================================
        # SCENE 8: Summary
        # =====================================================================
        self.play(
            FadeOut(overview_title),
            FadeOut(block_legend),
            FadeOut(coverage_note),
            FadeOut(all_boxes),
            FadeOut(idx_labels),
            run_time=1
        )

        summary_title = Text("Summary", font_size=36, color=GREEN)
        summary_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(summary_title), run_time=1)

        summary_points = VGroup(
            Text("• Each thread accumulates multiple partial sums", font_size=20),
            Text("• Grid-stride loop (i += gridSize) allows processing large arrays", font_size=20),
            Text("• Each iteration loads 2 elements: g_idata[i] + g_idata[i+blockSize]", font_size=20),
            Text("• All blocks and threads execute in parallel", font_size=20, color=YELLOW),
            Text("• Final reduction happens in shared memory (sdata)", font_size=20),
        )
        summary_points.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        summary_points.move_to(ORIGIN)

        self.play(
            LaggedStartMap(Write, summary_points, lag_ratio=0.4),
            run_time=4
        )
        self.wait(3)

        # Final fade out
        self.play(
            FadeOut(title),
            FadeOut(summary_title),
            FadeOut(summary_points),
            run_time=1.5
        )
        self.wait(1)
