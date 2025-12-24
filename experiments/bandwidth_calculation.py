from manimlib import *


class GPUMemoryBandwidthExplained(Scene):
    """
    Comprehensive GPU Memory Bandwidth Tutorial
    Explains RTX 4500 Ada specifications and bandwidth calculations
    """

    def construct(self):
        # Colors
        NVIDIA_GREEN = "#76B900"
        MEMORY_BLUE = "#4A90D9"
        CALC_ORANGE = "#E67E22"
        HIGHLIGHT_YELLOW = "#F1C40F"
        COMPARE_PURPLE = "#9B59B6"
        TIP_CYAN = "#1ABC9C"

        # ============================================================
        # SECTION 1: Title and Introduction
        # ============================================================
        title = Text("GPU Memory Bandwidth", font_size=48, color=NVIDIA_GREEN)
        subtitle = Text("Understanding Performance Calculations", font_size=28, color=WHITE)
        gpu_name = Text("NVIDIA RTX 4500 Ada", font_size=32, color=HIGHLIGHT_YELLOW)

        title_group = VGroup(title, subtitle, gpu_name).arrange(DOWN, buff=0.4)
        title_group.to_edge(UP, buff=0.8)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(gpu_name, shift=UP * 0.3), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(title_group))
        self.wait(0.3)

        # ============================================================
        # SECTION 2: GPU Specifications Table
        # ============================================================
        section_title = Text("RTX 4500 Ada - Memory Specifications", font_size=36, color=NVIDIA_GREEN)
        section_title.to_edge(UP, buff=0.5)
        self.play(Write(section_title))

        # Create specification table
        # Memory clock: 9001 MHz effective (as reported by CUDA)
        # Effective data rate = 9001 MHz × 2 (DDR) = 18.002 Gbps ≈ 18 Gbps
        specs_data = [
            ("Specification", "Value", "Description"),
            ("Memory Type", "GDDR6", "Graphics DDR6 - High bandwidth memory"),
            ("Total Memory", "24 GB", "Video RAM for textures, buffers, models"),
            ("Bus Width", "192-bit", "Data path width to memory chips"),
            ("Memory Clock", "9001 MHz", "Effective memory clock (from CUDA query)"),
            ("Effective Rate", "18 Gbps", "9001 MHz × 2 (DDR) ≈ 18 Gbps per pin"),
            ("Memory Channels", "6", "Parallel 32-bit channels (6 × 32 = 192)"),
        ]

        # Table dimensions
        col_widths = [2.8, 2.0, 5.5]
        row_height = 0.55
        table_start_y = 2.0

        table_elements = VGroup()

        for row_idx, row_data in enumerate(specs_data):
            y_pos = table_start_y - row_idx * row_height
            x_offset = -5.0

            for col_idx, cell_text in enumerate(row_data):
                x_pos = x_offset + sum(col_widths[:col_idx]) + col_widths[col_idx] / 2

                # Header row styling
                if row_idx == 0:
                    cell = Text(cell_text, font_size=18, color=NVIDIA_GREEN)
                    cell.set_stroke(width=0.5)
                else:
                    if col_idx == 0:
                        cell = Text(cell_text, font_size=16, color=MEMORY_BLUE)
                    elif col_idx == 1:
                        cell = Text(cell_text, font_size=16, color=HIGHLIGHT_YELLOW)
                    else:
                        cell = Text(cell_text, font_size=14, color=GREY_B)

                cell.move_to([x_pos, y_pos, 0])
                table_elements.add(cell)

        # Add horizontal lines
        line_y_top = table_start_y + 0.3
        line_y_header = table_start_y - 0.3
        line_y_bottom = table_start_y - len(specs_data) * row_height + 0.25

        h_line1 = Line([-5.2, line_y_top, 0], [5.2, line_y_top, 0], color=GREY, stroke_width=1)
        h_line2 = Line([-5.2, line_y_header, 0], [5.2, line_y_header, 0], color=NVIDIA_GREEN, stroke_width=2)
        h_line3 = Line([-5.2, line_y_bottom, 0], [5.2, line_y_bottom, 0], color=GREY, stroke_width=1)

        table_elements.add(h_line1, h_line2, h_line3)

        self.play(LaggedStart(*[FadeIn(elem) for elem in table_elements], lag_ratio=0.05), run_time=2)
        self.wait(2)

        # ============================================================
        # SECTION 3: Memory Bus Visualization
        # ============================================================
        self.play(FadeOut(table_elements), FadeOut(section_title))

        bus_title = Text("Understanding the 192-bit Memory Bus", font_size=36, color=NVIDIA_GREEN)
        bus_title.to_edge(UP, buff=0.5)
        self.play(Write(bus_title))

        # Draw 6 memory channels
        channels = VGroup()
        channel_labels = VGroup()

        for i in range(6):
            x_pos = -4.5 + i * 1.5

            # Channel box
            channel = Rectangle(
                width=1.2, height=2.5,
                fill_color=MEMORY_BLUE, fill_opacity=0.3,
                stroke_color=MEMORY_BLUE, stroke_width=2
            )
            channel.move_to([x_pos, 0.5, 0])

            # 32-bit label inside
            bit_label = Text("32-bit", font_size=14, color=WHITE)
            bit_label.move_to([x_pos, 0.5, 0])

            # Channel number
            ch_num = Text(f"CH{i}", font_size=12, color=GREY_B)
            ch_num.next_to(channel, UP, buff=0.1)

            channels.add(VGroup(channel, bit_label))
            channel_labels.add(ch_num)

        # Brace showing total bus width
        total_brace = Brace(channels, DOWN, buff=0.2)
        total_label = Text("6 × 32 = 192 bits total bus width", font_size=18, color=HIGHLIGHT_YELLOW)
        total_label.next_to(total_brace, DOWN, buff=0.15)

        # GPU chip representation
        gpu_chip = Rectangle(
            width=3.0, height=1.2,
            fill_color=NVIDIA_GREEN, fill_opacity=0.3,
            stroke_color=NVIDIA_GREEN, stroke_width=3
        )
        gpu_chip.move_to([0, -2.5, 0])
        gpu_label = Text("GPU Core", font_size=20, color=NVIDIA_GREEN)
        gpu_label.move_to(gpu_chip.get_center())

        # Arrows from channels to GPU
        arrows = VGroup()
        for i in range(6):
            x_pos = -4.5 + i * 1.5
            arrow = Arrow(
                [x_pos, -0.8, 0], [x_pos * 0.3, -1.9, 0],
                stroke_width=2, color=MEMORY_BLUE,
                buff=0
            )
            arrows.add(arrow)

        self.play(
            LaggedStart(*[FadeIn(ch, shift=DOWN * 0.3) for ch in channels], lag_ratio=0.1),
            LaggedStart(*[FadeIn(lbl, shift=DOWN * 0.2) for lbl in channel_labels], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(
            GrowFromCenter(total_brace),
            Write(total_label),
            run_time=0.8
        )
        self.play(
            FadeIn(gpu_chip),
            Write(gpu_label),
            LaggedStart(*[GrowArrow(arr) for arr in arrows], lag_ratio=0.05),
            run_time=1.2
        )
        self.wait(1.5)

        # ============================================================
        # SECTION 4: Bandwidth Calculation Step-by-Step
        # ============================================================
        bus_elements = VGroup(channels, channel_labels, total_brace, total_label,
                              gpu_chip, gpu_label, arrows, bus_title)
        self.play(FadeOut(bus_elements))

        calc_title = Text("Calculating Theoretical Bandwidth", font_size=36, color=NVIDIA_GREEN)
        calc_title.to_edge(UP, buff=0.5)
        self.play(Write(calc_title))

        # First explain DDR (Double Data Rate)
        ddr_title = Text("First: Understanding DDR (Double Data Rate)", font_size=24, color=CALC_ORANGE)
        ddr_title.move_to([0, 2.2, 0])
        self.play(Write(ddr_title))

        ddr_explain1 = Text("Memory Clock from CUDA: 9001 MHz", font_size=22, color=WHITE)
        ddr_explain1.move_to([0, 1.5, 0])

        ddr_explain2 = Text("DDR transfers data on BOTH rising and falling clock edges", font_size=20, color=GREY_B)
        ddr_explain2.move_to([0, 1.0, 0])

        ddr_calc = Text("Effective Rate = 9001 MHz × 2 = 18002 MHz ≈ 18 Gbps", font_size=24, color=HIGHLIGHT_YELLOW)
        ddr_calc.move_to([0, 0.4, 0])

        # Visual showing clock edges
        clock_label = Text("Clock Signal:", font_size=16, color=GREY_B)
        clock_label.move_to([-4.5, -0.4, 0])

        # Simple square wave representation
        clock_wave = VGroup()
        wave_points = [
            [-3.5, -0.6, 0], [-3.5, -0.2, 0], [-2.5, -0.2, 0], [-2.5, -0.6, 0],
            [-1.5, -0.6, 0], [-1.5, -0.2, 0], [-0.5, -0.2, 0], [-0.5, -0.6, 0],
            [0.5, -0.6, 0], [0.5, -0.2, 0], [1.5, -0.2, 0], [1.5, -0.6, 0],
            [2.5, -0.6, 0], [2.5, -0.2, 0], [3.5, -0.2, 0], [3.5, -0.6, 0],
        ]
        for i in range(len(wave_points) - 1):
            line = Line(wave_points[i], wave_points[i + 1], color=MEMORY_BLUE, stroke_width=3)
            clock_wave.add(line)

        # Arrows showing data transfer points
        transfer_arrows = VGroup()
        transfer_positions = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]  # Both edges
        for i, x in enumerate(transfer_positions):
            arrow = Arrow([x, -0.8, 0], [x, -1.2, 0], stroke_width=2, color=NVIDIA_GREEN, buff=0)
            transfer_arrows.add(arrow)

        transfer_label = Text("Data transfers (both edges = 2× throughput)", font_size=16, color=NVIDIA_GREEN)
        transfer_label.move_to([0, -1.5, 0])

        self.play(Write(ddr_explain1), run_time=0.8)
        self.play(Write(ddr_explain2), run_time=0.8)
        self.play(Write(ddr_calc), run_time=1.0)
        self.wait(0.5)

        self.play(Write(clock_label), run_time=0.3)
        self.play(ShowCreation(clock_wave), run_time=1.0)
        self.play(
            LaggedStart(*[GrowArrow(arr) for arr in transfer_arrows], lag_ratio=0.1),
            run_time=1.0
        )
        self.play(Write(transfer_label), run_time=0.5)
        self.wait(1.5)

        # Clear DDR explanation
        ddr_elements = VGroup(ddr_title, ddr_explain1, ddr_explain2, ddr_calc,
                              clock_label, clock_wave, transfer_arrows, transfer_label)
        self.play(FadeOut(ddr_elements))

        # Now show the bandwidth formula
        formula_title = Text("Now: Calculate Bandwidth", font_size=24, color=CALC_ORANGE)
        formula_title.move_to([0, 2.5, 0])

        formula_line1 = Text("Bandwidth = (Bus Width × Effective Clock) / 8", font_size=26, color=WHITE)
        formula_line1.move_to([0, 1.9, 0])
        self.play(Write(formula_title), run_time=0.5)
        self.play(Write(formula_line1), run_time=0.8)
        self.wait(0.5)

        # Step-by-step calculation using Text objects
        step1_label = Text("Step 1: Multiply bus width by effective clock", font_size=20, color=CALC_ORANGE)
        step1_calc = Text("192 bits × 18 Gbps = 3456 Gb/s", font_size=26, color=WHITE)
        step1 = VGroup(step1_label, step1_calc).arrange(DOWN, buff=0.2)
        step1.move_to([0, 0.9, 0])

        step2_label = Text("Step 2: Divide by 8 to convert bits to bytes", font_size=20, color=CALC_ORANGE)
        step2_calc = Text("3456 Gb/s ÷ 8 = 432 GB/s", font_size=26, color=WHITE)
        step2 = VGroup(step2_label, step2_calc).arrange(DOWN, buff=0.2)
        step2.move_to([0, -0.3, 0])

        # Final result box
        result_box = Rectangle(
            width=7.5, height=1.0,
            fill_color=NVIDIA_GREEN, fill_opacity=0.2,
            stroke_color=NVIDIA_GREEN, stroke_width=3
        )
        result_text = Text("Theoretical Peak Bandwidth: 432 GB/s", font_size=28, color=NVIDIA_GREEN)
        result = VGroup(result_box, result_text)
        result_text.move_to(result_box.get_center())
        result.move_to([0, -1.8, 0])

        # Summary of values used
        summary = Text("192 bits × 18 Gbps / 8 = 432 GB/s", font_size=22, color=HIGHLIGHT_YELLOW)
        summary.move_to([0, -2.8, 0])

        self.play(Write(step1_label), run_time=0.5)
        self.play(Write(step1_calc), run_time=0.8)
        self.wait(0.5)

        self.play(Write(step2_label), run_time=0.5)
        self.play(Write(step2_calc), run_time=0.8)
        self.wait(0.5)

        self.play(
            FadeIn(result_box, scale=1.1),
            Write(result_text),
            run_time=1.0
        )
        self.play(Write(summary), run_time=0.5)
        self.wait(2)

        # Update variable for fadeout
        formula_line1 = VGroup(formula_title, formula_line1)

        # ============================================================
        # SECTION 5: Comparison with G80 (GeForce 8800 GTX)
        # ============================================================
        calc_elements = VGroup(calc_title, formula_line1, step1, step2, result, summary)
        self.play(FadeOut(calc_elements))

        compare_title = Text("Generational Comparison: G80 vs RTX 4500 Ada", font_size=32, color=NVIDIA_GREEN)
        compare_title.to_edge(UP, buff=0.5)
        self.play(Write(compare_title))

        # G80 specs (GeForce 8800 GTX - 2006)
        g80_header = Text("G80 (8800 GTX) - 2006", font_size=22, color=COMPARE_PURPLE)
        g80_specs = VGroup(
            Text("• Bus Width: 384-bit", font_size=16),
            Text("• Memory: GDDR3", font_size=16),
            Text("• Clock: 900 MHz effective", font_size=16),
            Text("• Bandwidth: 86.4 GB/s", font_size=16, color=COMPARE_PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g80_group = VGroup(g80_header, g80_specs).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        g80_group.move_to([-3.5, 0.8, 0])

        # RTX 4500 Ada specs
        rtx_header = Text("RTX 4500 Ada - 2024", font_size=22, color=NVIDIA_GREEN)
        rtx_specs = VGroup(
            Text("• Bus Width: 192-bit", font_size=16),
            Text("• Memory: GDDR6", font_size=16),
            Text("• Clock: 18 Gbps effective", font_size=16),
            Text("• Bandwidth: 432 GB/s", font_size=16, color=NVIDIA_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rtx_group = VGroup(rtx_header, rtx_specs).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rtx_group.move_to([5.0, 0.8, 0])

        # Comparison arrow
        vs_text = Text("VS", font_size=28, color=HIGHLIGHT_YELLOW)
        vs_text.move_to([0, 1.0, 0])

        # Improvement calculation
        improvement = Text("5× bandwidth improvement with half the bus width!",
                          font_size=20, color=HIGHLIGHT_YELLOW)
        improvement.move_to([0, -1, 0])

        insight = Text("Key insight: Higher data rate per pin compensates for narrower bus",
                      font_size=16, color=GREY_B)
        insight.move_to([0, -1.5, 0])

        # Bar chart comparison
        bar_g80 = Rectangle(width=1.0, height=0.86, fill_color=COMPARE_PURPLE, fill_opacity=0.7)
        bar_rtx = Rectangle(width=1.0, height=4.32, fill_color=NVIDIA_GREEN, fill_opacity=0.7)

        bar_g80.move_to([-1.5, -3.0 + 0.43, 0])
        bar_rtx.move_to([1.5, -3.0 + 2.16, 0])

        bar_g80_label = Text("86 GB/s", font_size=14, color=WHITE)
        bar_rtx_label = Text("432 GB/s", font_size=14, color=WHITE)
        bar_g80_label.next_to(bar_g80, UP, buff=0.1)
        bar_rtx_label.next_to(bar_rtx, UP, buff=0.1)

        bar_g80_name = Text("G80", font_size=12, color=GREY_B)
        bar_rtx_name = Text("RTX 4500", font_size=12, color=GREY_B)
        bar_g80_name.next_to(bar_g80, DOWN, buff=0.1)
        bar_rtx_name.next_to(bar_rtx, DOWN, buff=0.1)

        self.play(
            Write(g80_header),
            Write(rtx_header),
            FadeIn(vs_text, scale=1.2),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[FadeIn(spec, shift=RIGHT * 0.2) for spec in g80_specs], lag_ratio=0.1),
            LaggedStart(*[FadeIn(spec, shift=LEFT * 0.2) for spec in rtx_specs], lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            GrowFromEdge(bar_g80, DOWN),
            GrowFromEdge(bar_rtx, DOWN),
            FadeIn(bar_g80_label), FadeIn(bar_rtx_label),
            FadeIn(bar_g80_name), FadeIn(bar_rtx_name),
            run_time=1.2
        )
        self.play(Write(improvement), run_time=0.8)
        self.play(FadeIn(insight), run_time=0.5)
        self.wait(2)

        # ============================================================
        # SECTION 6: Data Flow Visualization
        # ============================================================
        compare_elements = VGroup(
            compare_title, g80_group, rtx_group, vs_text, improvement, insight,
            bar_g80, bar_rtx, bar_g80_label, bar_rtx_label, bar_g80_name, bar_rtx_name
        )
        self.play(FadeOut(compare_elements))

        flow_title = Text("How Threads Access Memory", font_size=36, color=NVIDIA_GREEN)
        flow_title.to_edge(UP, buff=0.5)
        self.play(Write(flow_title))

        # Memory hierarchy diagram
        # Global Memory (top)
        global_mem = Rectangle(width=10, height=1.2, fill_color=MEMORY_BLUE, fill_opacity=0.3,
                              stroke_color=MEMORY_BLUE, stroke_width=2)
        global_mem.move_to([0, 2.2, 0])
        global_label = Text("Global Memory (VRAM - 24GB)", font_size=18, color=MEMORY_BLUE)
        global_label.move_to(global_mem.get_center())

        # L2 Cache
        l2_cache = Rectangle(width=8, height=0.8, fill_color="#8E44AD", fill_opacity=0.3,
                            stroke_color="#8E44AD", stroke_width=2)
        l2_cache.move_to([0, 1.0, 0])
        l2_label = Text("L2 Cache (48 MB)", font_size=16, color="#8E44AD")
        l2_label.move_to(l2_cache.get_center())

        # 192-bit bus representation
        bus_lines = VGroup()
        for i in range(12):
            x = -4.5 + i * 0.82
            line = Line([x, 1.5, 0], [x, 0.5, 0], stroke_width=2, color=HIGHLIGHT_YELLOW)
            bus_lines.add(line)
        bus_note = Text("192-bit bus", font_size=12, color=HIGHLIGHT_YELLOW)
        bus_note.move_to([5.5, 1.0, 0])

        # Shared Memory / L1 (per SM)
        sm_group = VGroup()
        for i in range(4):
            x = -4.5 + i * 3.0
            sm = Rectangle(width=2.5, height=0.8, fill_color=CALC_ORANGE, fill_opacity=0.3,
                          stroke_color=CALC_ORANGE, stroke_width=2)
            sm.move_to([x, -0.3, 0])
            sm_label = Text(f"SM {i} Shared Mem", font_size=12, color=CALC_ORANGE)
            sm_label.move_to(sm.get_center())
            sm_group.add(VGroup(sm, sm_label))

        # Thread blocks
        thread_blocks = VGroup()
        for i in range(4):
            x = -4.5 + i * 3.0
            block = VGroup()
            for j in range(4):
                for k in range(4):
                    thread = Square(side_length=0.15, fill_color=TIP_CYAN, fill_opacity=0.8,
                                   stroke_width=0)
                    thread.move_to([x - 0.35 + k * 0.23, -1.3 - j * 0.23, 0])
                    block.add(thread)
            block_label = Text(f"Block {i}", font_size=10, color=TIP_CYAN)
            block_label.move_to([x, -2.3, 0])
            thread_blocks.add(VGroup(block, block_label))

        # Registers (per thread)
        reg_label = Text("Registers (per thread, fastest)", font_size=14, color="#27AE60")
        reg_label.move_to([0, -2.8, 0])

        # Speed annotations
        speed_global = Text("~400 cycles latency", font_size=11, color=GREY_B)
        speed_l2 = Text("~100 cycles", font_size=11, color=GREY_B)
        speed_shared = Text("~20 cycles", font_size=11, color=GREY_B)
        speed_reg = Text("~1 cycle", font_size=11, color=GREY_B)

        speed_global.next_to(global_mem, RIGHT, buff=0.2)
        speed_l2.next_to(l2_cache, RIGHT, buff=0.2)
        speed_shared.next_to(sm_group[3], RIGHT, buff=0.3)
        speed_reg.next_to(reg_label, RIGHT, buff=0.3)

        self.play(
            FadeIn(global_mem), Write(global_label),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[GrowFromPoint(line, line.get_start()) for line in bus_lines], lag_ratio=0.05),
            FadeIn(bus_note),
            run_time=0.8
        )
        self.play(
            FadeIn(l2_cache), Write(l2_label),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[FadeIn(sm, shift=DOWN * 0.2) for sm in sm_group], lag_ratio=0.1),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[FadeIn(tb, scale=0.8) for tb in thread_blocks], lag_ratio=0.1),
            run_time=0.8
        )
        self.play(Write(reg_label), run_time=0.5)
        self.play(
            FadeIn(speed_global), FadeIn(speed_l2),
            FadeIn(speed_shared), FadeIn(speed_reg),
            run_time=0.8
        )
        self.wait(2)

        # ============================================================
        # SECTION 7: Coalescing and Bank Conflicts
        # ============================================================
        flow_elements = VGroup(
            flow_title, global_mem, global_label, l2_cache, l2_label,
            bus_lines, bus_note, sm_group, thread_blocks, reg_label,
            speed_global, speed_l2, speed_shared, speed_reg
        )
        self.play(FadeOut(flow_elements))

        perf_title = Text("Why Real Bandwidth < Theoretical Peak", font_size=32, color=NVIDIA_GREEN)
        perf_title.to_edge(UP, buff=0.5)
        self.play(Write(perf_title))

        # Coalesced vs Non-coalesced
        coal_title = Text("Memory Coalescing", font_size=24, color=CALC_ORANGE)
        coal_title.move_to([-4.0, 2.0, 0])

        # Good coalescing diagram
        good_label = Text("✓ Coalesced Access", font_size=16, color="#27AE60")
        good_label.move_to([-4.0, 1.5, 0])

        good_threads = VGroup()
        good_mem = VGroup()
        for i in range(8):
            t = Square(side_length=0.35, fill_color=TIP_CYAN, fill_opacity=0.8, stroke_width=1)
            t.move_to([-6.0 + i * 0.5, 1.0, 0])
            good_threads.add(t)

            m = Square(side_length=0.35, fill_color=MEMORY_BLUE, fill_opacity=0.5, stroke_width=1)
            m.move_to([-6.0 + i * 0.5, 0.2, 0])
            good_mem.add(m)

        good_arrows = VGroup()
        for i in range(8):
            arr = Arrow([-6.0 + i * 0.5, 0.8, 0], [-6.0 + i * 0.5, 0.4, 0],
                       stroke_width=2, color="#27AE60", buff=0)
            good_arrows.add(arr)

        good_note = Text("1 transaction, 100% efficiency", font_size=12, color="#27AE60")
        good_note.move_to([-4.0, -0.3, 0])

        # Bad coalescing diagram
        bad_label = Text("✗ Strided Access", font_size=16, color="#E74C3C")
        bad_label.move_to([-4.0, -0.8, 0])

        bad_threads = VGroup()
        bad_mem = VGroup()
        for i in range(8):
            t = Square(side_length=0.35, fill_color=TIP_CYAN, fill_opacity=0.8, stroke_width=1)
            t.move_to([-6.0 + i * 0.5, -1.3, 0])
            bad_threads.add(t)

        for i in range(16):
            m = Square(side_length=0.35, fill_color=MEMORY_BLUE, fill_opacity=0.3, stroke_width=1)
            m.move_to([-6.5 + i * 0.4, -2.1, 0])
            if i % 2 == 0:
                m.set_fill(MEMORY_BLUE, opacity=0.8)
            bad_mem.add(m)

        bad_arrows = VGroup()
        for i in range(8):
            arr = Arrow([-6.0 + i * 0.5, -1.5, 0], [-6.5 + i * 2 * 0.4, -1.9, 0],
                       stroke_width=2, color="#E74C3C", buff=0)
            bad_arrows.add(arr)

        bad_note = Text("Multiple transactions, wasted bandwidth", font_size=12, color="#E74C3C")
        bad_note.move_to([-4.0, -2.6, 0])

        # Bank conflicts section
        bank_title = Text("Shared Memory Bank Conflicts", font_size=24, color=CALC_ORANGE)
        bank_title.move_to([3.5, 2.0, 0])

        # Banks visualization
        banks = VGroup()
        for i in range(8):
            bank = Rectangle(width=0.5, height=1.5, fill_color=CALC_ORANGE, fill_opacity=0.3,
                           stroke_color=CALC_ORANGE, stroke_width=1)
            bank.move_to([1.5 + i * 0.6, 0.8, 0])
            bank_num = Text(str(i), font_size=10, color=WHITE)
            bank_num.move_to(bank.get_top() + DOWN * 0.2)
            banks.add(VGroup(bank, bank_num))

        banks_label = Text("32 banks (showing 8)", font_size=12, color=GREY_B)
        banks_label.move_to([3.5, -0.2, 0])

        conflict_note = Text("Conflict: Multiple threads access same bank", font_size=14, color="#E74C3C")
        conflict_note.move_to([3.5, -0.7, 0])

        no_conflict = Text("No conflict: Each thread → different bank", font_size=14, color="#27AE60")
        no_conflict.move_to([3.5, -1.1, 0])

        # Efficiency loss factors
        factors_title = Text("Bandwidth Efficiency Factors:", font_size=18, color=HIGHLIGHT_YELLOW)
        factors_title.move_to([3.5, -1.8, 0])

        factors = VGroup(
            Text("• Memory coalescing: 50-100%", font_size=14),
            Text("• Cache hit rate: varies", font_size=14),
            Text("• Bank conflicts: 0-32× penalty", font_size=14),
            Text("• Occupancy: thread utilization", font_size=14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        factors.move_to([3.5, -2.6, 0])

        self.play(Write(coal_title), run_time=0.5)
        self.play(
            Write(good_label),
            LaggedStart(*[FadeIn(t, scale=0.5) for t in good_threads], lag_ratio=0.05),
            LaggedStart(*[FadeIn(m, scale=0.5) for m in good_mem], lag_ratio=0.05),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in good_arrows], lag_ratio=0.05),
            run_time=0.5
        )
        self.play(Write(good_note), run_time=0.4)

        self.play(
            Write(bad_label),
            LaggedStart(*[FadeIn(t, scale=0.5) for t in bad_threads], lag_ratio=0.05),
            LaggedStart(*[FadeIn(m, scale=0.5) for m in bad_mem], lag_ratio=0.03),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in bad_arrows], lag_ratio=0.05),
            run_time=0.5
        )
        self.play(Write(bad_note), run_time=0.4)

        self.play(Write(bank_title), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in banks], lag_ratio=0.05),
            run_time=0.8
        )
        self.play(Write(banks_label), run_time=0.4)
        self.play(Write(conflict_note), Write(no_conflict), run_time=0.8)

        self.play(Write(factors_title), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in factors], lag_ratio=0.1),
            run_time=0.8
        )
        self.wait(2)

        # ============================================================
        # SECTION 8: Summary and Best Practices
        # ============================================================
        perf_elements = VGroup(
            perf_title, coal_title, good_label, good_threads, good_mem, good_arrows, good_note,
            bad_label, bad_threads, bad_mem, bad_arrows, bad_note,
            bank_title, banks, banks_label, conflict_note, no_conflict,
            factors_title, factors
        )
        self.play(FadeOut(perf_elements))

        summary_title = Text("Summary: RTX 4500 Ada Memory System", font_size=32, color=NVIDIA_GREEN)
        summary_title.to_edge(UP, buff=0.5)
        self.play(Write(summary_title))

        # Summary table
        summary_box = Rectangle(width=10, height=2.5, fill_color=MEMORY_BLUE, fill_opacity=0.1,
                               stroke_color=MEMORY_BLUE, stroke_width=2)
        summary_box.move_to([0, 1.5, 0])

        summary_content = VGroup(
            Text("Memory: 24 GB GDDR6  |  Bus: 192-bit (6 channels × 32-bit)", font_size=18),
            Text("Memory Clock: 2250 MHz base → 18 Gbps effective (DDR)", font_size=18),
            Text("Theoretical Peak Bandwidth: 432 GB/s", font_size=20, color=NVIDIA_GREEN),
            Text("Practical Bandwidth: ~300-380 GB/s (depends on access patterns)", font_size=16, color=GREY_B),
        ).arrange(DOWN, buff=0.25)
        summary_content.move_to(summary_box.get_center())

        # Best practices
        tips_title = Text("Tips to Maximize Memory Throughput", font_size=24, color=TIP_CYAN)
        tips_title.move_to([0, -0.5, 0])

        tips = VGroup(
            Text("1. Coalesce memory accesses - consecutive threads access consecutive addresses", font_size=16),
            Text("2. Use shared memory for data reuse - 20× lower latency than global memory", font_size=16),
            Text("3. Avoid bank conflicts - pad arrays or use different access patterns", font_size=16),
            Text("4. Maximize occupancy - balance registers, shared memory, and threads per block", font_size=16),
            Text("5. Prefer structure of arrays (SoA) over array of structures (AoS)", font_size=16),
            Text("6. Use read-only cache (__ldg) for data that won't be modified", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tips.move_to([0, -2.0, 0])

        self.play(FadeIn(summary_box), run_time=0.5)
        self.play(
            LaggedStart(*[Write(line) for line in summary_content], lag_ratio=0.2),
            run_time=2
        )
        self.wait(0.5)

        self.play(Write(tips_title), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(tip, shift=RIGHT * 0.3) for tip in tips], lag_ratio=0.15),
            run_time=2
        )
        self.wait(2)

        # Final message
        final_box = Rectangle(width=8, height=0.8, fill_color=NVIDIA_GREEN, fill_opacity=0.2,
                             stroke_color=NVIDIA_GREEN, stroke_width=3)
        final_text = Text("Bandwidth is the lifeblood of GPU computing!", font_size=22, color=NVIDIA_GREEN)
        final_group = VGroup(final_box, final_text)
        final_text.move_to(final_box.get_center())
        final_group.move_to([0, -3.5, 0])

        self.play(
            FadeIn(final_box, scale=1.1),
            Write(final_text),
            run_time=1
        )
        self.wait(2)


class BandwidthCalculationDiagram(Scene):
    """
    Static diagram showing bandwidth calculation formula and values
    """

    def construct(self):
        NVIDIA_GREEN = "#76B900"
        MEMORY_BLUE = "#4A90D9"
        HIGHLIGHT_YELLOW = "#F1C40F"

        # Title
        title = Text("GPU Memory Bandwidth Calculation", font_size=36, color=NVIDIA_GREEN)
        title.to_edge(UP, buff=0.4)

        # Main formula - correct: (Bus Width × Effective Clock) / 8
        formula = Tex(
            r"\text{Bandwidth} = \frac{\text{Bus Width (bits)} \times \text{Effective Clock (Gbps)}}{8}",
            font_size=42
        )
        formula.move_to([0, 2.2, 0])

        # RTX 4500 Ada calculation
        rtx_title = Text("RTX 4500 Ada", font_size=28, color=NVIDIA_GREEN)
        rtx_title.move_to([-3.5, 1.2, 0])

        rtx_calc = VGroup(
            Tex(r"= \frac{192 \text{ bits} \times 18 \text{ Gbps}}{8}", font_size=36),
            Tex(r"= \frac{3456 \text{ Gb/s}}{8}", font_size=36),
            Tex(r"= 432 \text{ GB/s}", font_size=42, color=NVIDIA_GREEN),
        ).arrange(DOWN, buff=0.3)
        rtx_calc.move_to([-3.5, -0.3, 0])

        # G80 calculation
        g80_title = Text("G80 (8800 GTX)", font_size=28, color="#9B59B6")
        g80_title.move_to([3.5, 1.2, 0])

        g80_calc = VGroup(
            Tex(r"= \frac{384 \text{ bits} \times 1.8 \text{ Gbps}}{8}", font_size=36),
            Tex(r"= \frac{691.2 \text{ Gb/s}}{8}", font_size=36),
            Tex(r"= 86.4 \text{ GB/s}", font_size=42, color="#9B59B6"),
        ).arrange(DOWN, buff=0.3)
        g80_calc.move_to([3.5, -0.3, 0])

        # Divider
        divider = DashedLine([0, 1.5, 0], [0, -1.8, 0], color=GREY)

        # Comparison note
        improvement = Text("5× faster with half the bus width!", font_size=20, color=HIGHLIGHT_YELLOW)
        improvement.move_to([0, -2.3, 0])

        insight = Text("Higher data rate per pin is the key advancement", font_size=16, color=GREY_B)
        insight.move_to([0, -2.8, 0])

        # ASCII-style data rate explanation
        ddr_box = Rectangle(width=10, height=1.2, fill_color=MEMORY_BLUE, fill_opacity=0.1,
                           stroke_color=MEMORY_BLUE, stroke_width=1)
        ddr_box.move_to([0, -3.6, 0])

        ddr_text = VGroup(
            Text("GDDR6: 9001 MHz effective × 2 (DDR) = 18 Gbps per pin", font_size=14),
            Text("GDDR3:  900 MHz × 2 (DDR) = 1.8 Gbps per pin", font_size=14),
        ).arrange(DOWN, buff=0.15)
        ddr_text.move_to(ddr_box.get_center())

        # Add everything
        self.add(title, formula)
        self.add(rtx_title, rtx_calc)
        self.add(g80_title, g80_calc)
        self.add(divider)
        self.add(improvement, insight)
        self.add(ddr_box, ddr_text)

        # Adjust camera
        self.camera.frame.set_height(9)
        self.camera.frame.move_to([0, -0.5, 0])


class MemoryHierarchyASCII(Scene):
    """
    ASCII-style visualization of GPU memory hierarchy
    """

    def construct(self):
        NVIDIA_GREEN = "#76B900"

        title = Text("GPU Memory Hierarchy", font_size=36, color=NVIDIA_GREEN)
        title.to_edge(UP, buff=0.4)

        # Create ASCII-style boxes
        hierarchy = """
┌─────────────────────────────────────────────────────────────┐
│                    GLOBAL MEMORY (VRAM)                      │
│                 24 GB GDDR6 @ 432 GB/s peak                  │
│              Latency: ~400-600 cycles                        │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │    192-bit Bus    │
                    │  (6×32-bit lanes) │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      L2 CACHE (48 MB)                        │
│                   Shared across all SMs                      │
│                  Latency: ~100-200 cycles                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  SM 0 L1/SMEM │   │  SM 1 L1/SMEM │   │  SM N L1/SMEM │
│   128 KB each │   │   128 KB each │   │   128 KB each │
│ ~20-30 cycles │   │ ~20-30 cycles │   │ ~20-30 cycles │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
  ┌─────┴─────┐       ┌─────┴─────┐       ┌─────┴─────┐
  │ REGISTERS │       │ REGISTERS │       │ REGISTERS │
  │ 256KB/SM  │       │ 256KB/SM  │       │ 256KB/SM  │
  │ ~1 cycle  │       │ ~1 cycle  │       │ ~1 cycle  │
  └───────────┘       └───────────┘       └───────────┘
        """

        hierarchy_text = Text(hierarchy, font_size=11, font="Consolas")
        hierarchy_text.move_to([0, -0.3, 0])

        self.add(title, hierarchy_text)

        self.camera.frame.set_height(9)
        self.camera.frame.move_to([0, -0.3, 0])


class CoalescingVisualization(Scene):
    """
    Animated visualization of memory coalescing
    """

    def construct(self):
        NVIDIA_GREEN = "#76B900"
        TIP_CYAN = "#1ABC9C"
        MEMORY_BLUE = "#4A90D9"

        title = Text("Memory Coalescing: Good vs Bad", font_size=32, color=NVIDIA_GREEN)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Warp of 32 threads (showing 8 for simplicity)
        warp_label = Text("Warp (32 threads, showing 8)", font_size=16, color=GREY_B)
        warp_label.move_to([0, 2.3, 0])

        threads = VGroup()
        for i in range(8):
            t = VGroup(
                Square(side_length=0.5, fill_color=TIP_CYAN, fill_opacity=0.8, stroke_width=1),
                Text(f"T{i}", font_size=10, color=WHITE)
            )
            t[1].move_to(t[0].get_center())
            t.move_to([-3.5 + i * 1.0, 1.8, 0])
            threads.add(t)

        self.play(FadeIn(warp_label))
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in threads], lag_ratio=0.05))

        # Memory row (128-byte cache line)
        mem_label = Text("Memory (128-byte cache line)", font_size=16, color=GREY_B)
        mem_label.move_to([0, 0.3, 0])

        mem_cells = VGroup()
        for i in range(8):
            m = VGroup(
                Square(side_length=0.5, fill_color=MEMORY_BLUE, fill_opacity=0.5, stroke_width=1),
                Text(f"M{i}", font_size=10, color=WHITE)
            )
            m[1].move_to(m[0].get_center())
            m.move_to([-3.5 + i * 1.0, -0.2, 0])
            mem_cells.add(m)

        self.play(FadeIn(mem_label))
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mem_cells], lag_ratio=0.05))

        # GOOD: Coalesced access
        good_title = Text("✓ Coalesced: T[i] reads M[i]", font_size=20, color="#27AE60")
        good_title.move_to([-4.0, -1.2, 0])

        self.play(Write(good_title))

        # Animate coalesced reads
        good_arrows = VGroup()
        for i in range(8):
            arr = Arrow(
                threads[i].get_bottom() + DOWN * 0.1,
                mem_cells[i].get_top() + UP * 0.1,
                stroke_width=3, color="#27AE60", buff=0.05
            )
            good_arrows.add(arr)

        self.play(LaggedStart(*[GrowArrow(a) for a in good_arrows], lag_ratio=0.05))

        result_good = Text("Result: 1 memory transaction (100% efficiency)", font_size=16, color="#27AE60")
        result_good.move_to([0, -1.7, 0])
        self.play(Write(result_good))
        self.wait(1)

        # Fade out good, show bad
        self.play(
            FadeOut(good_arrows),
            FadeOut(good_title),
            FadeOut(result_good)
        )

        # BAD: Strided access
        bad_title = Text("✗ Strided: T[i] reads M[i*2]", font_size=20, color="#E74C3C")
        bad_title.move_to([-4.0, -1.2, 0])

        self.play(Write(bad_title))

        bad_arrows = VGroup()
        for i in range(4):  # Only show first 4 for clarity
            arr = Arrow(
                threads[i].get_bottom() + DOWN * 0.1,
                mem_cells[i * 2].get_top() + UP * 0.1,
                stroke_width=3, color="#E74C3C", buff=0.05
            )
            bad_arrows.add(arr)

        self.play(LaggedStart(*[GrowArrow(a) for a in bad_arrows], lag_ratio=0.1))

        result_bad = Text("Result: 2+ transactions, 50% efficiency (gaps wasted)",
                         font_size=16, color="#E74C3C")
        result_bad.move_to([0, -1.7, 0])
        self.play(Write(result_bad))

        # Highlight wasted cells
        wasted = VGroup(mem_cells[1], mem_cells[3], mem_cells[5], mem_cells[7])
        self.play(
            wasted.animate.set_fill(RED, opacity=0.3),
            run_time=0.5
        )

        wasted_label = Text("(wasted bandwidth)", font_size=12, color=RED)
        wasted_label.next_to(wasted, DOWN, buff=0.3)
        self.play(FadeIn(wasted_label))

        self.wait(2)


# Run command:
# manimgl bandwidth_calculation.py GPUMemoryBandwidthExplained
# manimgl bandwidth_calculation.py BandwidthCalculationDiagram -s  (for static image)
# manimgl bandwidth_calculation.py MemoryHierarchyASCII -s
# manimgl bandwidth_calculation.py CoalescingVisualization
