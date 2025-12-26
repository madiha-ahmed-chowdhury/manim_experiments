# Scene name: CUDAMatrixMulVisualization
# Run with: manimgl matrix.py CUDAMatrixMulVisualization

from manimlib import *

class CUDAMatrixMulVisualization(Scene):
    def construct(self):
        # Constants
        self.M, self.K, self.N = 4, 3, 5
        self.cell_size = 0.5
        self.block_cell_size = 0.25

        # Phase 1: Matrix layout
        self.show_matrix_layout()

        # Phase 2: CUDA launch configuration
        self.show_cuda_config()

        # Phase 3: Thread mapping visualization
        self.show_thread_block()

        # Phase 4: Mapping formula display
        self.show_mapping_formulas()

        # Phase 5: Focus on one output element C[1,2]
        self.focus_on_element(1, 2)

        # Phase 6: Second example C[0,4]
        self.second_example(0, 4)

        # Phase 7: Final summary
        self.final_summary()

    # =========================================================================
    # Helper Functions
    # =========================================================================

    def create_matrix(self, rows, cols, cell_size, color=WHITE, label=None, show_indices=True):
        """Create a matrix as a grid of squares with optional labels and indices."""
        cells = VGroup()

        for r in range(rows):
            for c in range(cols):
                cell = Square(side_length=cell_size)
                cell.set_stroke(color, width=2)
                cell.move_to([c * cell_size, -r * cell_size, 0])
                cells.add(cell)

        # Center the grid
        cells.move_to(ORIGIN)

        result = VGroup(cells)

        # Add row indices on the left
        if show_indices:
            row_indices = VGroup()
            for r in range(rows):
                idx = Text(str(r), font_size=16)
                idx.next_to(cells[r * cols], LEFT, buff=0.15)
                row_indices.add(idx)
            result.add(row_indices)

            # Add column indices on top
            col_indices = VGroup()
            for c in range(cols):
                idx = Text(str(c), font_size=16)
                idx.next_to(cells[c], UP, buff=0.15)
                col_indices.add(idx)
            result.add(col_indices)

        # Add label above
        if label:
            label_text = Text(label, font_size=24)
            label_text.next_to(result, UP, buff=0.3)
            result.add(label_text)

        return result, cells

    def create_block(self, block_size=16, cell_size=0.25, active_rows=4, active_cols=5):
        """Create a CUDA block visualization with active/idle thread distinction."""
        cells = VGroup()
        active_cells = VGroup()
        idle_cells = VGroup()

        for r in range(block_size):
            for c in range(block_size):
                cell = Square(side_length=cell_size)
                cell.move_to([c * cell_size, -r * cell_size, 0])

                if r < active_rows and c < active_cols:
                    cell.set_stroke(GREEN, width=1)
                    cell.set_fill(GREEN, opacity=0.3)
                    active_cells.add(cell)
                else:
                    cell.set_stroke(GREY, width=0.5)
                    cell.set_fill(GREY, opacity=0.1)
                    idle_cells.add(cell)

                cells.add(cell)

        cells.move_to(ORIGIN)
        return cells, active_cells, idle_cells

    def highlight_thread(self, block_cells, thread_y, thread_x, block_size=16, color=YELLOW):
        """Highlight a specific thread in the block."""
        idx = thread_y * block_size + thread_x
        highlight = SurroundingRectangle(block_cells[idx], color=color, buff=0.02)
        return highlight

    def get_cell(self, cells, row, col, cols):
        """Get a specific cell from a grid."""
        return cells[row * cols + col]

    def highlight_row(self, cells, row, cols, color=YELLOW):
        """Create highlight rectangles for an entire row."""
        row_cells = VGroup(*[cells[row * cols + c] for c in range(cols)])
        return SurroundingRectangle(row_cells, color=color, buff=0.05)

    def highlight_col(self, cells, col, rows, cols, color=BLUE):
        """Create highlight rectangles for an entire column."""
        col_cells = VGroup(*[cells[r * cols + col] for r in range(rows)])
        return SurroundingRectangle(col_cells, color=color, buff=0.05)

    # =========================================================================
    # Phase 1: Matrix Layout
    # =========================================================================

    def show_matrix_layout(self):
        title = Text("CUDA Matrix Multiplication", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Layout: A on far left, B above C in center-left area
        # Create Matrix A (4x3) - positioned on the far left
        self.A_group, self.A_cells = self.create_matrix(
            self.M, self.K, self.cell_size, color=BLUE_C, label="A (4×3)"
        )
        self.A_group.shift(LEFT * 5 + DOWN * 0.5)

        # Create Matrix B (3x5) - positioned above C, slightly left of center
        self.B_group, self.B_cells = self.create_matrix(
            self.K, self.N, self.cell_size, color=RED_C, label="B (3×5)"
        )
        self.B_group.shift(LEFT * 1.5 + UP * 1.5)

        # Create Matrix C (4x5) - positioned below B, aligned with B
        self.C_group, self.C_cells = self.create_matrix(
            self.M, self.N, self.cell_size, color=GREEN_C, label="C (4×5)"
        )
        self.C_group.shift(LEFT * 1.5 + DOWN * 1.8)

        # Animate matrices appearing
        self.play(FadeIn(self.A_group), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(self.B_group), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(self.C_group), run_time=1.5)

        self.title = title
        self.wait(1.5)

    # =========================================================================
    # Phase 2: CUDA Launch Configuration
    # =========================================================================

    def show_cuda_config(self):
        config_text = VGroup(
            Text("blockDim = (16, 16)", font_size=16, color=YELLOW),
            Text("gridDim  = (1, 1)", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # Position in top-right corner
        config_text.to_corner(UR, buff=0.3)

        config_box = SurroundingRectangle(config_text, color=WHITE, buff=0.1)
        self.config_group = VGroup(config_box, config_text)

        self.play(FadeIn(self.config_group), run_time=1.5)
        self.wait(2)

    # =========================================================================
    # Phase 3: Thread Block Visualization
    # =========================================================================

    def show_thread_block(self):
        # Fade out matrices temporarily
        self.play(
            self.A_group.animate.set_opacity(0.3),
            self.B_group.animate.set_opacity(0.3),
            self.C_group.animate.set_opacity(0.3),
            run_time=1.5
        )

        # Create thread block - position on the right side of screen
        self.block_cells, self.active_cells, self.idle_cells = self.create_block(
            block_size=16, cell_size=self.block_cell_size,
            active_rows=self.M, active_cols=self.N
        )
        self.block_cells.shift(RIGHT * 3.5)

        # Block label
        block_label = Text("Thread Block (16×16)", font_size=24)
        block_label.next_to(self.block_cells, UP, buff=0.3)

        block_idx_label = Text("blockIdx = (0, 0)", font_size=20, color=YELLOW)
        block_idx_label.next_to(block_label, DOWN, buff=0.1)

        # Legend - smaller and more compact
        legend = VGroup(
            VGroup(
                Square(side_length=0.2).set_fill(GREEN, opacity=0.3).set_stroke(GREEN),
                Text("Active (row<4, col<5)", font_size=14)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Square(side_length=0.2).set_fill(GREY, opacity=0.1).set_stroke(GREY),
                Text("Idle threads", font_size=14)
            ).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.next_to(self.block_cells, RIGHT, buff=0.3)

        self.block_group = VGroup(self.block_cells, block_label, block_idx_label)

        self.play(FadeIn(self.block_group), FadeIn(legend), run_time=2)
        self.wait(2)

        # Highlight boundary
        boundary_rect = Rectangle(
            width=self.N * self.block_cell_size,
            height=self.M * self.block_cell_size,
            color=GREEN,
            stroke_width=3
        )
        # Position at top-left of active region
        boundary_rect.move_to(self.block_cells[0].get_center())
        boundary_rect.shift(
            RIGHT * (self.N - 1) * self.block_cell_size / 2 +
            DOWN * (self.M - 1) * self.block_cell_size / 2
        )

        self.play(ShowCreation(boundary_rect), run_time=1.5)
        self.wait(1.5)

        self.play(FadeOut(boundary_rect), FadeOut(legend), run_time=1)
        self.legend = legend

    # =========================================================================
    # Phase 4: Mapping Formula Display
    # =========================================================================

    def show_mapping_formulas(self):
        formulas = VGroup(
            Text("row = blockIdx.y × blockDim.y + threadIdx.y", font_size=18),
            Text("col = blockIdx.x × blockDim.x + threadIdx.x", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        formulas.to_edge(DOWN, buff=0.3)

        formula_box = SurroundingRectangle(formulas, color=BLUE_C, buff=0.1)
        self.formula_group = VGroup(formula_box, formulas)

        self.play(FadeIn(self.formula_group), run_time=1.5)
        self.wait(2)

    # =========================================================================
    # Phase 5: Focus on One Output Element
    # =========================================================================

    def focus_on_element(self, row, col):
        # Bring matrices back
        self.play(
            self.A_group.animate.set_opacity(1),
            self.B_group.animate.set_opacity(1),
            self.C_group.animate.set_opacity(1),
            run_time=1.5
        )

        # Rearrange scene for focus - scale down block slightly
        self.play(
            self.block_group.animate.scale(0.8),
            self.config_group.animate.shift(UP * 0.3),
            self.formula_group.animate.shift(DOWN * 0.2),
            run_time=1.5
        )

        # Highlight the target thread in the block
        thread_highlight = self.highlight_thread(
            self.block_cells, row, col, color=YELLOW
        )
        thread_highlight.scale(0.8)

        # Also highlight the actual thread cell with a fill to make it stand out
        thread_idx = row * 16 + col
        thread_cell_highlight = self.block_cells[thread_idx].copy()
        thread_cell_highlight.set_fill(YELLOW, opacity=0.8)
        thread_cell_highlight.set_stroke(YELLOW, width=2)

        # Position thread label below the block
        thread_label = Text(f"Thread ({col}, {row})", font_size=14, color=YELLOW)
        thread_label.next_to(self.block_group, DOWN, buff=0.15)

        self.play(
            ShowCreation(thread_highlight),
            FadeIn(thread_cell_highlight),
            FadeIn(thread_label),
            run_time=1.5
        )
        self.wait(1)

        # Highlight row of A
        row_highlight = self.highlight_row(self.A_cells, row, self.K, color=YELLOW)

        # Highlight column of B
        col_highlight = self.highlight_col(self.B_cells, col, self.K, self.N, color=BLUE)

        # Highlight target cell in C
        target_cell = self.get_cell(self.C_cells, row, col, self.N)
        cell_highlight = SurroundingRectangle(target_cell, color=GREEN, buff=0.05)

        self.play(ShowCreation(row_highlight), run_time=1)
        self.play(ShowCreation(col_highlight), run_time=1)
        self.play(ShowCreation(cell_highlight), run_time=1)
        self.wait(1)

        # Focus text
        focus_text = Text(f"Computing C[{row}, {col}]", font_size=24, color=GREEN)
        focus_text.next_to(self.title, DOWN, buff=0.15)
        self.play(FadeIn(focus_text), run_time=1)

        # Zoom in using camera - focus on the matrices area
        self.play(
            self.camera.frame.animate.scale(0.75).move_to(
                (self.A_group.get_center() + self.C_group.get_center()) / 2
            ),
            run_time=2
        )
        self.wait(1)

        # Show dot product components - position below the C matrix to stay on screen
        dot_product_text = VGroup(
            Text(f"A[{row},0] × B[0,{col}]", font_size=14),
            Text(f"A[{row},1] × B[1,{col}]", font_size=14),
            Text(f"A[{row},2] × B[2,{col}]", font_size=14),
        ).arrange(RIGHT, buff=0.3)
        dot_product_text.next_to(self.C_group, DOWN, buff=0.3)

        self.play(FadeIn(dot_product_text), run_time=1.5)
        self.wait(1)

        # Draw arrows from A row elements to target C cell
        # Each arrow starts from its A cell and points to the left side of C cell
        arrows_a = VGroup()
        for k in range(self.K):
            a_cell = self.get_cell(self.A_cells, row, k, self.K)
            # Offset the end point slightly for each k to avoid overlap
            offset = (k - 1) * 0.08 * UP
            arrow_a = Arrow(
                a_cell.get_right(),
                target_cell.get_left() + offset,
                color=YELLOW,
                buff=0.05,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows_a.add(arrow_a)

        # Draw arrows from B column elements to target C cell
        # Each arrow starts from its specific B cell's bottom and points to C cell's top
        arrows_b = VGroup()
        for k in range(self.K):
            b_cell = self.get_cell(self.B_cells, k, col, self.N)
            # Offset the end point slightly for each k to avoid overlap
            offset = (k - 1) * 0.08 * RIGHT
            arrow_b = Arrow(
                b_cell.get_bottom(),
                target_cell.get_top() + offset,
                color=BLUE,
                buff=0.05,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows_b.add(arrow_b)

        # Animate arrows one by one with corresponding dot product text highlight
        for k in range(self.K):
            # Highlight current dot product term
            dot_product_text[k].set_color(YELLOW)
            self.play(
                ShowCreation(arrows_a[k]),
                ShowCreation(arrows_b[k]),
                run_time=1.5
            )
            self.wait(0.5)
            dot_product_text[k].set_color(WHITE)

        self.wait(2)

        # Store for cleanup
        self.focus_elements = VGroup(
            thread_highlight, thread_cell_highlight, thread_label, row_highlight, col_highlight,
            cell_highlight, focus_text, dot_product_text, arrows_a, arrows_b
        )

    # =========================================================================
    # Phase 6: Second Example
    # =========================================================================

    def second_example(self, row, col):
        # Zoom out
        self.play(
            self.camera.frame.animate.scale(1.2).move_to(ORIGIN),
            FadeOut(self.focus_elements),
            run_time=2
        )
        self.wait(1)

        # Highlight new thread
        thread_highlight2 = self.highlight_thread(
            self.block_cells, row, col, color=ORANGE
        )
        thread_highlight2.scale(0.8)

        # Also highlight the actual thread cell with a fill
        thread_idx2 = row * 16 + col
        thread_cell_highlight2 = self.block_cells[thread_idx2].copy()
        thread_cell_highlight2.set_fill(ORANGE, opacity=0.8)
        thread_cell_highlight2.set_stroke(ORANGE, width=2)

        # Position thread label below the block
        thread_label2 = Text(f"Thread ({col}, {row})", font_size=14, color=ORANGE)
        thread_label2.next_to(self.block_group, DOWN, buff=0.15)

        # Highlight row of A (row 0)
        row_highlight2 = self.highlight_row(self.A_cells, row, self.K, color=ORANGE)

        # Highlight column of B (col 4)
        col_highlight2 = self.highlight_col(self.B_cells, col, self.K, self.N, color=TEAL)

        # Highlight target cell in C
        target_cell2 = self.get_cell(self.C_cells, row, col, self.N)
        cell_highlight2 = SurroundingRectangle(target_cell2, color=GREEN, buff=0.05)

        # Focus text
        focus_text2 = Text(f"Computing C[{row}, {col}]", font_size=24, color=ORANGE)
        focus_text2.next_to(self.title, DOWN, buff=0.15)

        self.play(
            ShowCreation(thread_highlight2),
            FadeIn(thread_cell_highlight2),
            FadeIn(thread_label2),
            ShowCreation(row_highlight2),
            ShowCreation(col_highlight2),
            ShowCreation(cell_highlight2),
            FadeIn(focus_text2),
            run_time=2
        )
        self.wait(1.5)

        # Emphasis text
        same_pattern = Text("Same kernel, different thread, same pattern", font_size=20, color=WHITE)
        same_pattern.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(same_pattern), run_time=1.5)
        self.wait(3)

        self.second_example_elements = VGroup(
            thread_highlight2, thread_cell_highlight2, thread_label2, row_highlight2, col_highlight2,
            cell_highlight2, focus_text2, same_pattern
        )

    # =========================================================================
    # Phase 7: Final Summary
    # =========================================================================

    def final_summary(self):
        # Zoom out to show everything
        self.play(
            self.camera.frame.animate.scale(1.3).move_to(ORIGIN),
            FadeOut(self.second_example_elements),
            run_time=2
        )
        self.wait(1)

        # Final summary text
        summary = VGroup(
            Text("One thread → one output element", font_size=20),
            Text("Dot product along K dimension", font_size=20),
            Text("Idle threads exit via bounds check", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        summary_box = SurroundingRectangle(summary, color=GREEN, buff=0.15)
        summary_group = VGroup(summary_box, summary)
        summary_group.to_edge(DOWN, buff=0.2)

        self.play(
            FadeOut(self.formula_group),
            FadeIn(summary_group),
            run_time=2
        )
        self.wait(4)

        # Final fade
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)
