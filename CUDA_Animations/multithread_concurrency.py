from manim import *

class BlockDistributionAcrossSMs(Scene):
    def construct(self):
        # Title
        title = Text("Block Distribution Across SMs", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create SM grid (simplified - showing 8 SMs for clarity)
        num_sms = 8
        sm_width = 1.2
        sm_height = 0.8
        sm_spacing = 0.15

        # ============ PART 1: Small Kernels (Concurrent) ============
        part1_title = Text("Small Kernels: 2 blocks each", font_size=28, color=GREEN)
        part1_title.next_to(title, DOWN, buff=0.3)
        self.play(Write(part1_title))

        # Create SMs
        sms = VGroup()
        sm_labels = VGroup()
        for i in range(num_sms):
            sm = Rectangle(width=sm_width, height=sm_height, color=WHITE)
            sm.shift(RIGHT * (i - num_sms/2 + 0.5) * (sm_width + sm_spacing))
            sm.shift(DOWN * 0.5)
            sms.add(sm)

            label = Text(f"SM{i}", font_size=14, color=GRAY)
            label.next_to(sm, DOWN, buff=0.1)
            sm_labels.add(label)

        sms_group = VGroup(sms, sm_labels)
        sms_group.shift(DOWN * 0.5)
        self.play(Create(sms), Write(sm_labels))
        self.wait(0.3)

        # Stream colors
        stream_colors = [RED, BLUE, YELLOW, PURPLE]
        stream_names = ["K0", "K1", "K2", "K3"]

        # Legend
        legend = VGroup()
        for i, (color, name) in enumerate(zip(stream_colors, stream_names)):
            box = Square(side_length=0.3, color=color, fill_opacity=0.8)
            label = Text(f"Stream {i} ({name})", font_size=16, color=color)
            label.next_to(box, RIGHT, buff=0.1)
            item = VGroup(box, label)
            item.shift(DOWN * 3.2 + RIGHT * (i - 1.5) * 2.5)
            legend.add(item)

        self.play(Create(legend))
        self.wait(0.3)

        # Small kernels: 2 blocks each, 4 kernels = 8 blocks total
        # All fit simultaneously across 8 SMs
        small_blocks = VGroup()
        block_assignments = [
            (0, 0), (1, 0),  # K0: SM0, SM1
            (2, 1), (3, 1),  # K1: SM2, SM3
            (4, 2), (5, 2),  # K2: SM4, SM5
            (6, 3), (7, 3),  # K3: SM6, SM7
        ]

        for sm_idx, kernel_idx in block_assignments:
            block = Rectangle(
                width=sm_width * 0.8,
                height=sm_height * 0.6,
                color=stream_colors[kernel_idx],
                fill_opacity=0.8
            )
            block.move_to(sms[sm_idx].get_center())

            label = Text(stream_names[kernel_idx], font_size=12, color=WHITE)
            label.move_to(block.get_center())

            small_blocks.add(VGroup(block, label))

        # Animate blocks appearing simultaneously (showing concurrency)
        self.play(
            LaggedStart(*[FadeIn(b, scale=0.5) for b in small_blocks], lag_ratio=0.05),
            run_time=1.5
        )

        # Add concurrent execution indicator
        concurrent_text = Text("All kernels run CONCURRENTLY!", font_size=24, color=GREEN)
        concurrent_text.shift(DOWN * 2.3)
        self.play(Write(concurrent_text))
        self.wait(1.5)

        # Clear for part 2
        self.play(
            FadeOut(small_blocks),
            FadeOut(concurrent_text),
            FadeOut(part1_title)
        )

        # ============ PART 2: Large Kernels (Sequential) ============
        part2_title = Text("Large Kernels: 8 blocks each", font_size=28, color=RED)
        part2_title.next_to(title, DOWN, buff=0.3)
        self.play(Write(part2_title))

        # Show K0 filling ALL SMs
        k0_blocks = VGroup()
        for i in range(num_sms):
            block = Rectangle(
                width=sm_width * 0.8,
                height=sm_height * 0.6,
                color=stream_colors[0],
                fill_opacity=0.8
            )
            block.move_to(sms[i].get_center())

            label = Text("K0", font_size=12, color=WHITE)
            label.move_to(block.get_center())

            k0_blocks.add(VGroup(block, label))

        saturated_text = Text("K0 saturates ALL SMs!", font_size=24, color=RED)
        saturated_text.shift(DOWN * 2.3)

        self.play(
            LaggedStart(*[FadeIn(b, scale=0.5) for b in k0_blocks], lag_ratio=0.05),
            run_time=1
        )
        self.play(Write(saturated_text))
        self.wait(1)

        # Show waiting queue
        queue_title = Text("Waiting Queue:", font_size=20, color=GRAY)
        queue_title.shift(DOWN * 2.8 + LEFT * 4)

        waiting_kernels = VGroup()
        for i in range(1, 4):
            box = Rectangle(
                width=0.8, height=0.5,
                color=stream_colors[i],
                fill_opacity=0.6
            )
            label = Text(stream_names[i], font_size=14, color=WHITE)
            label.move_to(box.get_center())
            kernel = VGroup(box, label)
            kernel.shift(DOWN * 2.8 + LEFT * (2 - i * 1.2))
            waiting_kernels.add(kernel)

        self.play(Write(queue_title), Create(waiting_kernels))
        self.wait(1)

        # Animate K0 finishing and K1 taking over
        self.play(FadeOut(saturated_text))

        k0_finish = Text("K0 finishes...", font_size=20, color=GRAY)
        k0_finish.shift(DOWN * 2.3)
        self.play(Write(k0_finish))
        self.wait(0.5)

        # K1 replaces K0
        k1_blocks = VGroup()
        for i in range(num_sms):
            block = Rectangle(
                width=sm_width * 0.8,
                height=sm_height * 0.6,
                color=stream_colors[1],
                fill_opacity=0.8
            )
            block.move_to(sms[i].get_center())

            label = Text("K1", font_size=12, color=WHITE)
            label.move_to(block.get_center())

            k1_blocks.add(VGroup(block, label))

        # Update queue
        new_waiting = VGroup()
        for i in range(2, 4):
            box = Rectangle(
                width=0.8, height=0.5,
                color=stream_colors[i],
                fill_opacity=0.6
            )
            label = Text(stream_names[i], font_size=14, color=WHITE)
            label.move_to(box.get_center())
            kernel = VGroup(box, label)
            kernel.shift(DOWN * 2.8 + LEFT * (2.5 - (i-1) * 1.2))
            new_waiting.add(kernel)

        self.play(
            ReplacementTransform(k0_blocks, k1_blocks),
            FadeOut(waiting_kernels[0]),
            waiting_kernels[1:].animate.shift(RIGHT * 1.2),
            FadeOut(k0_finish)
        )

        k1_runs = Text("K1 now saturates ALL SMs!", font_size=20, color=BLUE)
        k1_runs.shift(DOWN * 2.3)
        self.play(Write(k1_runs))
        self.wait(1)

        # ============ PART 3: Side by side comparison ============
        self.play(
            FadeOut(k1_blocks),
            FadeOut(part2_title),
            FadeOut(waiting_kernels),
            FadeOut(queue_title),
            FadeOut(k1_runs),
            FadeOut(sms_group),
            FadeOut(legend)
        )

        comparison_title = Text("Comparison: Small vs Large Kernels", font_size=32)
        comparison_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(comparison_title))

        # Left side: Small kernels
        left_label = Text("Small Kernels\n(2 blocks each)", font_size=20, color=GREEN)
        left_label.shift(LEFT * 4 + UP * 0.5)

        # Timeline for small kernels
        small_timeline = VGroup()
        for i in range(4):
            bar = Rectangle(
                width=2, height=0.4,
                color=stream_colors[i],
                fill_opacity=0.8
            )
            bar.shift(LEFT * 4 + DOWN * (0.3 + i * 0.5))
            label = Text(f"K{i}", font_size=12, color=WHITE)
            label.move_to(bar.get_center())
            small_timeline.add(VGroup(bar, label))

        # Right side: Large kernels
        right_label = Text("Large Kernels\n(8 blocks each)", font_size=20, color=RED)
        right_label.shift(RIGHT * 3 + UP * 0.5)

        # Timeline for large kernels (sequential)
        large_timeline = VGroup()
        for i in range(4):
            bar = Rectangle(
                width=1.5, height=0.4,
                color=stream_colors[i],
                fill_opacity=0.8
            )
            bar.shift(RIGHT * (1 + i * 1.6) + DOWN * 1)
            label = Text(f"K{i}", font_size=12, color=WHITE)
            label.move_to(bar.get_center())
            large_timeline.add(VGroup(bar, label))

        # Time arrows
        left_arrow = Arrow(LEFT * 5.5, LEFT * 2.5, color=WHITE, buff=0)
        left_arrow.shift(DOWN * 2.8)
        left_time = Text("Time →", font_size=14)
        left_time.next_to(left_arrow, DOWN, buff=0.1)

        right_arrow = Arrow(RIGHT * 0.2, RIGHT * 6, color=WHITE, buff=0)
        right_arrow.shift(DOWN * 2.8)
        right_time = Text("Time →", font_size=14)
        right_time.next_to(right_arrow, DOWN, buff=0.1)

        # Total time indicators
        left_total = Text("Total: T", font_size=18, color=GREEN)
        left_total.shift(LEFT * 4 + DOWN * 3.3)

        right_total = Text("Total: 4T", font_size=18, color=RED)
        right_total.shift(RIGHT * 3 + DOWN * 3.3)

        self.play(
            Write(left_label),
            Write(right_label)
        )
        self.play(
            LaggedStart(*[FadeIn(b) for b in small_timeline], lag_ratio=0.1),
            LaggedStart(*[FadeIn(b) for b in large_timeline], lag_ratio=0.2),
        )
        self.play(
            Create(left_arrow), Write(left_time),
            Create(right_arrow), Write(right_time)
        )
        self.play(Write(left_total), Write(right_total))

        # Final insight
        insight = Text(
            "Streams enable concurrency, but SM capacity determines actual overlap!",
            font_size=22,
            color=YELLOW
        )
        insight.to_edge(DOWN, buff=0.3)
        self.play(Write(insight))
        self.wait(2)


class SMCapacityVisualization(Scene):
    """Bonus: Visualize thread capacity and saturation"""
    def construct(self):
        title = Text("GPU Thread Capacity: RTX 4500 Ada", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # GPU stats
        stats = VGroup(
            Text("60 SMs × 1536 threads = 92,160 max concurrent threads", font_size=24),
        )
        stats.next_to(title, DOWN, buff=0.4)
        self.play(Write(stats))

        # Create capacity bar
        capacity_bar = Rectangle(width=10, height=1, color=WHITE)
        capacity_bar.shift(DOWN * 0.5)
        capacity_label = Text("92,160 threads (100%)", font_size=18)
        capacity_label.next_to(capacity_bar, UP, buff=0.1)

        self.play(Create(capacity_bar), Write(capacity_label))

        # Show different kernel sizes
        examples = [
            ("4 blocks × 256 = 1,024 threads", 1024/92160, GREEN, "1.1%"),
            ("60 blocks × 256 = 15,360 threads", 15360/92160, BLUE, "16.7%"),
            ("90 blocks × 1024 = 92,160 threads", 1.0, YELLOW, "100%"),
            ("256 blocks × 1024 = 262,144 threads", 1.0, RED, "284% (queued!)"),
        ]

        for i, (desc, fill_ratio, color, pct) in enumerate(examples):
            # Clear previous fill
            fill_width = min(fill_ratio, 1.0) * 10
            fill = Rectangle(
                width=fill_width, height=0.9,
                color=color, fill_opacity=0.7
            )
            fill.align_to(capacity_bar, LEFT)
            fill.shift(RIGHT * 0.05)

            desc_text = Text(desc, font_size=20, color=color)
            desc_text.shift(DOWN * 2)

            pct_text = Text(pct, font_size=24, color=color)
            pct_text.shift(DOWN * 2.7)

            if i == 0:
                self.play(Create(fill), Write(desc_text), Write(pct_text))
            else:
                self.play(
                    Transform(fill, fill),
                    Transform(desc_text, desc_text),
                    Transform(pct_text, pct_text)
                )

            self.wait(1.5)

            if i < len(examples) - 1:
                self.play(FadeOut(fill), FadeOut(desc_text), FadeOut(pct_text))

        # Overflow visualization for last example
        overflow = Rectangle(
            width=10 * (262144/92160 - 1), height=0.9,
            color=RED, fill_opacity=0.3
        )
        overflow.next_to(capacity_bar, RIGHT, buff=0.1)
        overflow_label = Text("Queued blocks", font_size=16, color=RED)
        overflow_label.next_to(overflow, UP, buff=0.1)

        self.play(Create(overflow), Write(overflow_label))
        self.wait(2)
