from manimlib import *

class PagedAttention(Scene):
    def construct(self):
        # Configuration
        BLOCK_SIZE = 4  # tokens per block
        PROMPT = ["Alan", "Turing", "is", "a", "computer", "scientist"]
        COMPLETIONS = ["and", "mathematician", "renowned", "for"]

        HIGHLIGHT_COLOR = "#FF6B6B"  # Red for highlighting

        # Colors
        PROMPT_COLOR = "#FFE4B5"  # Light orange for prompt tokens
        COMPLETION_COLOR = "#90EE90"  # Light green for completion tokens
        EMPTY_COLOR = "#E8E8E8"  # Gray for empty slots
        BLOCK_BORDER = "#333333"

        # Title
        title = Text("PagedAttention: Dynamic KV-Cache Allocation", font_size=36)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Section 1: Show the prompt (longer now)
        prompt_label = Text("Prompt:", font_size=32, color=YELLOW)
        prompt_label.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)

        prompt_text = Text('"Alan Turing is a computer scientist"', font_size=28, color=WHITE)
        prompt_text.next_to(prompt_label, RIGHT, buff=0.3)

        self.play(Write(prompt_label), Write(prompt_text))
        self.wait(0.5)

        # Section 2: Physical Memory Blocks (on the right)
        physical_label = Text("Physical KV-Cache Blocks", font_size=24, color="#87CEEB")
        physical_label.to_edge(RIGHT, buff=1.5).shift(UP * 2)

        # Create physical memory blocks (6 blocks, 4 slots each)
        physical_blocks = VGroup()
        block_labels = VGroup()

        for i in range(6):
            block = VGroup()
            for j in range(BLOCK_SIZE):
                cell = Rectangle(
                    width=0.8, height=0.5,
                    fill_color=EMPTY_COLOR,
                    fill_opacity=0.3,
                    stroke_color=BLOCK_BORDER,
                    stroke_width=1
                )
                block.add(cell)
            block.arrange(RIGHT, buff=0)
            physical_blocks.add(block)

            label = Text(f"Block {i}", font_size=16)
            block_labels.add(label)

        physical_blocks.arrange(DOWN, buff=0.15)
        physical_blocks.next_to(physical_label, DOWN, buff=0.3)

        for i, (block, label) in enumerate(zip(physical_blocks, block_labels)):
            label.next_to(block, LEFT, buff=0.2)

        self.play(
            Write(physical_label),
            *[ShowCreation(block) for block in physical_blocks],
            *[Write(label) for label in block_labels]
        )
        self.wait(0.5)

        # Section 3: Logical View (Block Table) on the left
        logical_label = Text("Logical KV-Cache (Block Table)", font_size=24, color="#FFB347")
        logical_label.to_edge(LEFT, buff=0.5).shift(UP * 0.5)

        # Block table header
        table_header = VGroup(
            Rectangle(width=1.2, height=0.4, fill_color="#444444", fill_opacity=0.8, stroke_width=1),
            Rectangle(width=0.8, height=0.4, fill_color="#444444", fill_opacity=0.8, stroke_width=1),
            Rectangle(width=0.6, height=0.4, fill_color="#444444", fill_opacity=0.8, stroke_width=1),
        ).arrange(RIGHT, buff=0)

        header_texts = VGroup(
            Text("Logical", font_size=12),
            Text("Phys", font_size=12),
            Text("#", font_size=12),
        )
        for txt, rect in zip(header_texts, table_header):
            txt.move_to(rect)

        table_header_group = VGroup(table_header, header_texts)
        table_header_group.next_to(logical_label, DOWN, buff=0.3)

        self.play(Write(logical_label), ShowCreation(table_header), Write(header_texts))

        # Tracking variables
        logical_blocks = VGroup()
        token_texts_physical = []  # Store text objects in physical blocks

        # Function to create a logical block row
        def create_logical_row(logical_idx, physical_idx, filled):
            row = VGroup(
                Rectangle(width=1.2, height=0.4, fill_color="#2a2a2a", fill_opacity=0.8, stroke_width=1),
                Rectangle(width=0.8, height=0.4, fill_color="#2a2a2a", fill_opacity=0.8, stroke_width=1),
                Rectangle(width=0.6, height=0.4, fill_color="#2a2a2a", fill_opacity=0.8, stroke_width=1),
            ).arrange(RIGHT, buff=0)

            texts = VGroup(
                Text(f"Block {logical_idx}", font_size=11),
                Text(str(physical_idx), font_size=11),
                Text(str(filled), font_size=11),
            )
            for txt, rect in zip(texts, row):
                txt.move_to(rect)

            return VGroup(row, texts)

        # Function to add token to physical block
        def add_token_to_physical(block_idx, slot_idx, token, color):
            cell = physical_blocks[block_idx][slot_idx]
            cell.generate_target()
            cell.target.set_fill(color, opacity=0.7)

            token_text = Text(token, font_size=10)
            token_text.move_to(cell)
            token_texts_physical.append(token_text)

            return cell, token_text

        # Process prompt tokens
        self.play(FadeOut(prompt_text), FadeOut(prompt_label))

        step_text = Text("Step 1: Allocate Block 0 for first 4 prompt tokens", font_size=20, color=YELLOW)
        step_text.to_edge(DOWN, buff=1.5)
        self.play(Write(step_text))

        # First 4 tokens go to Block 0
        animations = []
        for i, token in enumerate(PROMPT[:4]):
            cell, token_text = add_token_to_physical(0, i, token, PROMPT_COLOR)
            animations.append(MoveToTarget(cell))
            animations.append(Write(token_text))

        # Create first logical block entry
        logical_row_0 = create_logical_row(0, 0, 4)
        logical_row_0.next_to(table_header_group, DOWN, buff=0.05)
        logical_blocks.add(logical_row_0)

        self.play(*animations, ShowCreation(logical_row_0[0]), Write(logical_row_0[1]))
        self.wait(1)

        # Next 2 tokens need a new block
        self.play(FadeOut(step_text))
        step_text = Text("Step 2: Block 0 full! Allocate Block 1 for remaining prompt", font_size=20, color=YELLOW)
        step_text.to_edge(DOWN, buff=1.5)
        self.play(Write(step_text))

        animations = []
        for i, token in enumerate(PROMPT[4:]):
            cell, token_text = add_token_to_physical(1, i, token, PROMPT_COLOR)
            animations.append(MoveToTarget(cell))
            animations.append(Write(token_text))

        # Create second logical block entry
        logical_row_1 = create_logical_row(1, 1, 2)
        logical_row_1.next_to(logical_row_0, DOWN, buff=0.05)
        logical_blocks.add(logical_row_1)

        self.play(*animations, ShowCreation(logical_row_1[0]), Write(logical_row_1[1]))
        self.wait(1)

        # Now show completion generation
        self.play(FadeOut(step_text))
        step_text = Text("Step 3: Generate completion tokens one by one", font_size=20, color=YELLOW)
        step_text.to_edge(DOWN, buff=1.5)
        self.play(Write(step_text))
        self.wait(0.5)

        # Current state: Block 1 has 2 tokens, can fit 2 more
        current_block_idx = 1
        current_slot_idx = 2
        current_logical_idx = 1

        for i, token in enumerate(COMPLETIONS):
            # Check if we need a new block
            if current_slot_idx >= BLOCK_SIZE:
                current_block_idx += 1
                current_slot_idx = 0
                current_logical_idx += 1

                # Create new logical block entry
                new_logical_row = create_logical_row(current_logical_idx, current_block_idx, 0)
                new_logical_row.next_to(logical_blocks[-1], DOWN, buff=0.05)
                logical_blocks.add(new_logical_row)

                self.play(ShowCreation(new_logical_row[0]), Write(new_logical_row[1]))

            # Show prediction
            pred_text = Text(f'Predicting: "{token}"', font_size=18, color=COMPLETION_COLOR)
            pred_text.next_to(step_text, UP, buff=0.3)
            self.play(Write(pred_text))

            # Add token to physical block
            cell, token_text = add_token_to_physical(current_block_idx, current_slot_idx, token, COMPLETION_COLOR)

            # Create highlights for cell and logical row
            cell_highlight = SurroundingRectangle(cell, color=HIGHLIGHT_COLOR, stroke_width=3, buff=0.02)
            logical_row_highlight = SurroundingRectangle(
                logical_blocks[-1],
                color=HIGHLIGHT_COLOR,
                stroke_width=3,
                buff=0.05
            )

            # Show highlights, then fill cell
            self.play(
                ShowCreation(cell_highlight),
                ShowCreation(logical_row_highlight),
                run_time=0.4
            )

            self.play(MoveToTarget(cell), Write(token_text), run_time=0.5)

            # Update the filled count in logical block table
            current_slot_idx += 1
            filled_count = current_slot_idx

            # Update the # Filled column
            old_count_text = logical_blocks[-1][1][2]
            new_count_text = Text(str(filled_count), font_size=11)
            new_count_text.move_to(logical_blocks[-1][0][2])

            self.play(
                Transform(old_count_text, new_count_text),
                FadeOut(pred_text),
                FadeOut(cell_highlight),
                FadeOut(logical_row_highlight),
                run_time=0.5
            )
            self.wait(0.2)

        # Final summary
        self.play(FadeOut(step_text))

        summary = VGroup(
            Text("PagedAttention Benefits:", font_size=24, color=YELLOW),
            Text("- Dynamic allocation - only use memory as needed", font_size=18),
            Text("- No internal fragmentation - blocks filled on demand", font_size=18),
            Text("- Non-contiguous storage - efficient memory utilization", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary.to_edge(DOWN, buff=0.3)

        self.play(Write(summary))
        self.wait(3)


class PagedAttentionDetailed(Scene):
    def construct(self):
        # More detailed version with memory fragmentation comparison

        # Title
        title = Text("Why PagedAttention?", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Part 1: Show the problem with naive allocation
        problem_title = Text("The Problem: Memory Fragmentation", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem_title))

        # Show naive allocation
        naive_label = Text("Naive: Reserve max_length per request", font_size=20)
        naive_label.next_to(problem_title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        # Create memory bar showing wasted space
        memory_bar = Rectangle(width=10, height=0.8, stroke_color=WHITE)
        memory_bar.next_to(naive_label, DOWN, buff=0.3)

        # Request 1: uses 30% of reserved
        req1_reserved = Rectangle(width=3, height=0.8, fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE)
        req1_used = Rectangle(width=1, height=0.8, fill_color=BLUE, fill_opacity=0.8, stroke_color=BLUE)
        req1_reserved.move_to(memory_bar.get_left() + RIGHT * 1.5)
        req1_used.align_to(req1_reserved, LEFT)

        # Request 2: uses 50% of reserved
        req2_reserved = Rectangle(width=3, height=0.8, fill_color=GREEN, fill_opacity=0.3, stroke_color=GREEN)
        req2_used = Rectangle(width=1.5, height=0.8, fill_color=GREEN, fill_opacity=0.8, stroke_color=GREEN)
        req2_reserved.next_to(req1_reserved, RIGHT, buff=0)
        req2_used.align_to(req2_reserved, LEFT)

        # Wasted label
        wasted_label = Text("Wasted!", font_size=14, color=RED)
        wasted_label.next_to(req1_reserved, UP, buff=0.1)

        self.play(
            Write(naive_label),
            ShowCreation(memory_bar)
        )
        self.play(
            ShowCreation(req1_reserved),
            ShowCreation(req1_used),
            ShowCreation(req2_reserved),
            ShowCreation(req2_used),
        )
        self.play(Write(wasted_label))
        self.wait(1)

        # Part 2: Show PagedAttention solution
        old_elements = VGroup(naive_label, memory_bar, req1_reserved, req1_used,
                             req2_reserved, req2_used, wasted_label)

        self.play(FadeOut(old_elements), FadeOut(problem_title))

        solution_title = Text("The Solution: PagedAttention", font_size=28, color=GREEN)
        solution_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(solution_title))

        # Explanation points
        points = VGroup(
            Text("1. Divide KV-cache into fixed-size blocks", font_size=22),
            Text("2. Allocate blocks on-demand as tokens are generated", font_size=22),
            Text("3. Use a block table to map logical -> physical blocks", font_size=22),
            Text("4. Blocks don't need to be contiguous!", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        points.next_to(solution_title, DOWN, buff=0.5)

        for point in points:
            self.play(Write(point))
            self.wait(0.5)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Transition to main demo
        demo_text = Text("Let's see it in action!", font_size=36)
        self.play(Write(demo_text))
        self.wait(1)
        self.play(FadeOut(demo_text))


if __name__ == "__main__":
    # Run with: manimgl Paged_attention.py PagedAttention
    pass
