# Scene name: TiledMatrixMulVisualization
# Run with: manimgl matrix_v2.py TiledMatrixMulVisualization

from manimlib import *

class TiledMatrixMulVisualization(Scene):
    def construct(self):
        # Constants
        self.M, self.K, self.N = 4, 4, 4  # Square matrices for simplicity
        self.TILE_SIZE = 2
        self.cell_size = 0.5
        self.block_cell_size = 0.3

        # Part 1: Introduction - Problem Statement
        self.show_introduction()

        # Part 2: Memory Hierarchy Explanation
        self.show_memory_hierarchy()

        # Part 3: Matrix Layout and Tiling Concept
        self.show_matrix_layout()

        # Part 4: Show Thread Block and Shared Memory
        self.show_thread_block_shared_memory()

        # Part 5: Tile 0 - First Iteration
        self.show_tile_iteration(tile_idx=0)

        # Part 6: Tile 1 - Second Iteration
        self.show_tile_iteration(tile_idx=1)

        # Part 7: Accumulation and Final Result
        self.show_accumulation()

        # Part 8: Summary
        self.final_summary()

    # =========================================================================
    # Helper Functions
    # =========================================================================

    def create_matrix(self, rows, cols, cell_size, color=WHITE, label=None, show_indices=True, prefix=""):
        """Create a matrix as a grid of squares with element labels like a00, b01, etc."""
        cells = VGroup()
        element_labels = VGroup()

        for r in range(rows):
            for c in range(cols):
                cell = Square(side_length=cell_size)
                cell.set_stroke(color, width=2)
                cell.move_to([c * cell_size, -r * cell_size, 0])
                cells.add(cell)

                # Add element label like a00, b01, etc.
                if prefix:
                    elem_label = Text(f"{prefix}{r}{c}", font_size=16)
                    elem_label.move_to(cell.get_center())
                    element_labels.add(elem_label)

        # Center the grid
        cells.move_to(ORIGIN)
        if prefix:
            element_labels.move_to(ORIGIN)

        result = VGroup(cells)

        if prefix:
            result.add(element_labels)

        # Add row indices on the left
        if show_indices:
            row_indices = VGroup()
            for r in range(rows):
                idx = Text(str(r), font_size=20)
                idx.next_to(cells[r * cols], LEFT, buff=0.1)
                row_indices.add(idx)
            result.add(row_indices)

            # Add column indices on top
            col_indices = VGroup()
            for c in range(cols):
                idx = Text(str(c), font_size=20)
                idx.next_to(cells[c], UP, buff=0.1)
                col_indices.add(idx)
            result.add(col_indices)

        # Add label above
        if label:
            label_text = Text(label, font_size=28)
            label_text.next_to(result, UP, buff=0.2)
            result.add(label_text)

        return result, cells, element_labels if prefix else None

    def create_shared_memory_block(self, size, cell_size, color=PURPLE, label=None):
        """Create a shared memory tile visualization."""
        cells = VGroup()
        for r in range(size):
            for c in range(size):
                cell = Square(side_length=cell_size)
                cell.set_stroke(color, width=2)
                cell.set_fill(color, opacity=0.2)
                cell.move_to([c * cell_size, -r * cell_size, 0])
                cells.add(cell)

        cells.move_to(ORIGIN)
        result = VGroup(cells)

        if label:
            label_text = Text(label, font_size=22, color=color)
            label_text.next_to(cells, UP, buff=0.15)
            result.add(label_text)

        return result, cells

    def create_thread_block(self, size, cell_size=0.3):
        """Create a thread block visualization."""
        cells = VGroup()
        for r in range(size):
            for c in range(size):
                cell = Square(side_length=cell_size)
                cell.set_stroke(GREEN, width=1)
                cell.set_fill(GREEN, opacity=0.3)
                cell.move_to([c * cell_size, -r * cell_size, 0])
                cells.add(cell)

        cells.move_to(ORIGIN)
        return cells

    def get_cell(self, cells, row, col, cols):
        """Get a specific cell from a grid."""
        return cells[row * cols + col]

    def highlight_tile(self, cells, tile_row, tile_col, tile_size, rows, cols, color=YELLOW):
        """Highlight a tile region in a matrix."""
        tile_cells = VGroup()
        for r in range(tile_size):
            for c in range(tile_size):
                actual_row = tile_row * tile_size + r
                actual_col = tile_col * tile_size + c
                if actual_row < rows and actual_col < cols:
                    tile_cells.add(cells[actual_row * cols + actual_col])
        return SurroundingRectangle(tile_cells, color=color, buff=0.02)

    # =========================================================================
    # Part 1: Introduction
    # =========================================================================

    def show_introduction(self):
        title = Text("CUDA Tiled Matrix Multiplication", font_size=40)
        title.to_edge(UP, buff=0.3)

        subtitle = Text("Leveraging Shared Memory for Performance", font_size=32, color=BLUE_C)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.wait(2)

        # Problem statement
        problem = VGroup(
            Text("Problem: Global memory is slow", font_size=28, color=RED_C),
            Text("Solution: Use shared memory (much faster)", font_size=28, color=GREEN_C),
            Text("Strategy: Load tiles into shared memory, compute locally", font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problem.next_to(subtitle, DOWN, buff=0.5)

        for line in problem:
            self.play(FadeIn(line), run_time=1.5)
            self.wait(0.5)

        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(problem),
            run_time=1.5
        )
        self.wait(0.5)

    # =========================================================================
    # Part 2: Memory Hierarchy
    # =========================================================================

    def show_memory_hierarchy(self):
        title = Text("GPU Memory Hierarchy", font_size=42)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.5)

        # Memory hierarchy boxes
        global_mem = VGroup(
            Rectangle(width=5, height=0.8, color=RED_C),
            Text("Global Memory (DRAM)", font_size=24),
        )
        global_mem[1].move_to(global_mem[0].get_center())

        shared_mem = VGroup(
            Rectangle(width=4, height=0.7, color=PURPLE),
            Text("Shared Memory (SRAM)", font_size=22),
        )
        shared_mem[1].move_to(shared_mem[0].get_center())

        registers = VGroup(
            Rectangle(width=3, height=0.6, color=GREEN),
            Text("Registers", font_size=20),
        )
        registers[1].move_to(registers[0].get_center())

        # Position hierarchy
        global_mem.shift(DOWN * 1.5)
        shared_mem.shift(DOWN * 0.3)
        registers.shift(UP * 0.8)

        hierarchy = VGroup(global_mem, shared_mem, registers)
        hierarchy.move_to(ORIGIN + DOWN * 0.5)

        # Arrows
        arrow1 = Arrow(global_mem[0].get_top(), shared_mem[0].get_bottom(), buff=0.1, color=YELLOW)
        arrow2 = Arrow(shared_mem[0].get_top(), registers[0].get_bottom(), buff=0.1, color=YELLOW)

        self.play(FadeIn(global_mem), run_time=1.5)
        self.wait(0.5)
        self.play(ShowCreation(arrow1), FadeIn(shared_mem), run_time=1.5)
        self.wait(0.5)
        self.play(ShowCreation(arrow2), FadeIn(registers), run_time=1.5)
        self.wait(1)

        # Key insight
        insight = Text("Key: Reuse data in shared memory to reduce global memory access",
                      font_size=26, color=YELLOW)
        insight.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(insight), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(hierarchy),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(insight),
            run_time=1.5
        )
        self.wait(0.5)

    # =========================================================================
    # Part 3: Matrix Layout and Tiling
    # =========================================================================

    def show_matrix_layout(self):
        title = Text("Tiled Matrix Multiplication", font_size=38)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.5)
        self.title = title

        # Create matrices A, B, C with element labels
        self.A_group, self.A_cells, self.A_labels = self.create_matrix(
            self.M, self.K, self.cell_size, color=BLUE_C, label="A (4x4)", prefix="a"
        )
        self.A_group.shift(LEFT * 4.5 + DOWN * 0.3)

        self.B_group, self.B_cells, self.B_labels = self.create_matrix(
            self.K, self.N, self.cell_size, color=RED_C, label="B (4x4)", prefix="b"
        )
        self.B_group.shift(UP * 1.5)

        self.C_group, self.C_cells, self.C_labels = self.create_matrix(
            self.M, self.N, self.cell_size, color=GREEN_C, label="C (4x4)", prefix="c"
        )
        self.C_group.shift(DOWN * 1.8)

        self.play(FadeIn(self.A_group), run_time=1)
        self.play(FadeIn(self.B_group), run_time=1)
        self.play(FadeIn(self.C_group), run_time=1)
        self.wait(1)

        # Show tiling concept
        tile_text = Text(f"Tile Size = {self.TILE_SIZE} x {self.TILE_SIZE}", font_size=28, color=YELLOW)
        tile_text.to_corner(UL, buff=0.5)
        self.play(FadeIn(tile_text), run_time=1)

        # Highlight tiles in A (row tiles)
        a_tile0 = self.highlight_tile(self.A_cells, 0, 0, self.TILE_SIZE, self.M, self.K, YELLOW)
        a_tile1 = self.highlight_tile(self.A_cells, 0, 1, self.TILE_SIZE, self.M, self.K, ORANGE)

        # Highlight tiles in B (column tiles)
        b_tile0 = self.highlight_tile(self.B_cells, 0, 0, self.TILE_SIZE, self.K, self.N, YELLOW)
        b_tile1 = self.highlight_tile(self.B_cells, 1, 0, self.TILE_SIZE, self.K, self.N, ORANGE)

        self.play(ShowCreation(a_tile0), ShowCreation(b_tile0), run_time=1.5)
        self.wait(0.5)

        tile0_label = Text("Tile 0", font_size=22, color=YELLOW)
        tile0_label.next_to(a_tile0, TOP, buff=0)
        self.play(FadeIn(tile0_label), run_time=0.5)
        self.wait(0.5)

        self.play(ShowCreation(a_tile1), ShowCreation(b_tile1), run_time=1.5)

        tile1_label = Text("Tile 1", font_size=22, color=ORANGE)
        tile1_label.next_to(a_tile1, TOP , buff=0.1)
        self.play(FadeIn(tile1_label), run_time=0.5)
        self.wait(1)
        

        # Explain iteration
        iter_text = Text("K / TILE_SIZE = 4 / 2 = 2 iterations", font_size=26, color=WHITE)
        iter_text.next_to(tile_text, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(iter_text), run_time=1)
        self.wait(2)

        # Clean up tile highlights
        self.play(
            FadeOut(a_tile0), FadeOut(a_tile1),
            FadeOut(b_tile0), FadeOut(b_tile1),
            FadeOut(tile0_label), FadeOut(tile1_label),
            FadeOut(tile_text), FadeOut(iter_text),
            run_time=1
        )

        self.tile_text = tile_text

    # =========================================================================
    # Part 4: Thread Block and Shared Memory
    # =========================================================================

    def show_thread_block_shared_memory(self):
        # Create thread block
        self.thread_block = self.create_thread_block(self.TILE_SIZE, cell_size=0.4)
        self.thread_block.shift(RIGHT * 4 + UP * 1)

        block_label = Text("Thread Block (2x2)", font_size=22)
        block_label.next_to(self.thread_block, UP, buff=0.2)

        self.block_group = VGroup(self.thread_block, block_label)

        # Create shared memory tiles
        self.sA_group, self.sA_cells = self.create_shared_memory_block(
            self.TILE_SIZE, 0.4, color=BLUE_C, label="sA (shared)"
        )
        self.sA_group.shift(RIGHT * 2.5 + DOWN * 0.8)

        self.sB_group, self.sB_cells = self.create_shared_memory_block(
            self.TILE_SIZE, 0.4, color=RED_C, label="sB (shared)"
        )
        self.sB_group.shift(RIGHT * 4.5 + DOWN * 0.8)

        self.play(FadeIn(self.block_group), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(self.sA_group), FadeIn(self.sB_group), run_time=1.5)
        self.wait(1)

        # Show each thread's responsibility
        thread_info = VGroup(
            Text("Each thread loads:", font_size=20),
            Text("  1 element from A -> sA", font_size=18, color=BLUE_C),
            Text("  1 element from B -> sB", font_size=18, color=RED_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        thread_info.next_to(self.sB_group, DOWN, buff=0.4)

        self.play(FadeIn(thread_info), run_time=1.5)
        self.wait(2)

        # Fade out thread info after showing
        self.play(FadeOut(thread_info), run_time=0.8)

        self.thread_info = thread_info

    # =========================================================================
    # Part 5 & 6: Tile Iterations
    # =========================================================================

    def show_tile_iteration(self, tile_idx):
        # Clear previous iteration elements if any
        if hasattr(self, 'iter_elements'):
            self.play(FadeOut(self.iter_elements), run_time=0.5)

        # Tile iteration title
        tile_title = Text(f"Tile {tile_idx}", font_size=32, color=YELLOW if tile_idx == 0 else ORANGE)
        tile_title.to_corner( TOP + LEFT, buff=0.15)
        self.play(FadeIn(tile_title), run_time=1)

        tile_color = YELLOW if tile_idx == 0 else ORANGE

        # Highlight current tile in A (row 0-1, tile column)
        a_tile_highlight = self.highlight_tile(
            self.A_cells, 0, tile_idx, self.TILE_SIZE, self.M, self.K, tile_color
        )

        # Highlight current tile in B (tile row, column 0-1)
        b_tile_highlight = self.highlight_tile(
            self.B_cells, tile_idx, 0, self.TILE_SIZE, self.K, self.N, tile_color
        )

        self.play(ShowCreation(a_tile_highlight), ShowCreation(b_tile_highlight), run_time=1.5)
        self.wait(1)

        # Show individual thread loads one by one
        load_text = Text("Loading from Global Memory:", font_size=22)
        load_text.to_edge(DOWN + RIGHT, buff=1.5)
        self.play(FadeIn(load_text), run_time=0.5)

        # Animate each thread loading its element
        thread_arrows_a = VGroup()
        thread_arrows_b = VGroup()
        sA_labels = VGroup()
        sB_labels = VGroup()

        for ty in range(self.TILE_SIZE):
            for tx in range(self.TILE_SIZE):
                thread_idx = ty * self.TILE_SIZE + tx

                # Highlight current thread
                thread_cell = self.thread_block[thread_idx]
                thread_highlight = thread_cell.copy()
                thread_highlight.set_fill(tile_color, opacity=0.8)
                thread_highlight.set_stroke(tile_color, width=3)

                # Thread label
                thread_label = Text(f"T({tx},{ty})", font_size=18, color=tile_color)
                thread_label.next_to(self.block_group, RIGHT, buff=0.1)

                self.play(FadeIn(thread_highlight), FadeIn(thread_label), run_time=0.3)

                # Source cell in A: row = ty, col = tile_idx * TILE_SIZE + tx
                a_row = ty
                a_col = tile_idx * self.TILE_SIZE + tx
                if a_col < self.K:
                    a_cell = self.get_cell(self.A_cells, a_row, a_col, self.K)
                    a_cell_highlight = a_cell.copy()
                    a_cell_highlight.set_fill(tile_color, opacity=0.6)

                    # Destination in sA
                    sA_cell = self.sA_cells[ty * self.TILE_SIZE + tx]

                    # Arrow from A to sA
                    arrow_a = Arrow(
                        a_cell.get_center(),
                        sA_cell.get_center(),
                        color=BLUE_C,
                        buff=0.1,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.2
                    )

                    self.play(
                        FadeIn(a_cell_highlight),
                        ShowCreation(arrow_a),
                        run_time=0.4
                    )

                    # Fill sA cell and add label with shared memory notation
                    sA_fill = sA_cell.copy()
                    sA_fill.set_fill(BLUE_C, opacity=0.5)
                    # Use local tile indices for shared memory: s_a[ty][tx]
                    sA_label = Text(f"s_a{ty}{tx}", font_size=12)
                    sA_label.move_to(sA_cell.get_center())
                    self.play(FadeIn(sA_fill), FadeIn(sA_label), run_time=0.2)

                    thread_arrows_a.add(arrow_a, a_cell_highlight, sA_fill)
                    sA_labels.add(sA_label)

                # Source cell in B: row = tile_idx * TILE_SIZE + ty, col = tx
                b_row = tile_idx * self.TILE_SIZE + ty
                b_col = tx
                if b_row < self.K:
                    b_cell = self.get_cell(self.B_cells, b_row, b_col, self.N)
                    b_cell_highlight = b_cell.copy()
                    b_cell_highlight.set_fill(tile_color, opacity=0.6)

                    # Destination in sB
                    sB_cell = self.sB_cells[ty * self.TILE_SIZE + tx]

                    # Arrow from B to sB
                    arrow_b = Arrow(
                        b_cell.get_center(),
                        sB_cell.get_center(),
                        color=RED_C,
                        buff=0.1,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.2
                    )

                    self.play(
                        FadeIn(b_cell_highlight),
                        ShowCreation(arrow_b),
                        run_time=0.4
                    )

                    # Fill sB cell and add label with shared memory notation
                    sB_fill = sB_cell.copy()
                    sB_fill.set_fill(RED_C, opacity=0.5)
                    # Use local tile indices for shared memory: s_b[ty][tx]
                    sB_label = Text(f"s_b{ty}{tx}", font_size=12)
                    sB_label.move_to(sB_cell.get_center())
                    self.play(FadeIn(sB_fill), FadeIn(sB_label), run_time=0.2)

                    thread_arrows_b.add(arrow_b, b_cell_highlight, sB_fill)
                    sB_labels.add(sB_label)

                self.play(FadeOut(thread_highlight), FadeOut(thread_label), run_time=0.2)

        self.wait(0.5)

        # Fade out load text after loading phase
        self.play(FadeOut(load_text), run_time=0.5)

        # Syncthreads
        sync_text = Text("__syncthreads()", font_size=26, color=PURPLE)
        sync_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(sync_text), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(sync_text), run_time=0.5)

        # Show computation phase
        compute_text = Text("Computing partial products:", font_size=22)
        compute_text.to_edge(TOP + LEFT, buff=1.5)
        self.play(FadeIn(compute_text), run_time=0.5)

        # Show multiplication expressions for each output element using global matrix notation
        c_highlights = VGroup()

        for row in range(self.TILE_SIZE):
            for col in range(self.TILE_SIZE):
                c_cell = self.get_cell(self.C_cells, row, col, self.N)
                c_highlight = c_cell.copy()
                c_highlight.set_fill(GREEN, opacity=0.3 + 0.2 * tile_idx)

                # Build multiplication expression using global indices (a00×b00 format)
                mult_parts = []
                for k in range(self.TILE_SIZE):
                    a_global_col = tile_idx * self.TILE_SIZE + k
                    b_global_row = tile_idx * self.TILE_SIZE + k
                    mult_parts.append(f"a{row}{a_global_col}×b{b_global_row}{col}")

                mult_expr = " + ".join(mult_parts)
                calc_text = Text(f"c{row}{col} = {mult_expr}", font_size=20, color=GREEN)
                calc_text.to_edge(DOWN, buff=0.3)

                # For c00, show arrows from shared memory elements to demonstrate the computation
                if row == 0 and col == 0:
                    self.play(FadeIn(c_highlight), FadeIn(calc_text), run_time=0.5)

                    # Show arrows for each multiplication in the dot product
                    for k in range(self.TILE_SIZE):
                        # Highlight s_a element (row 0, col k)
                        sA_cell = self.sA_cells[row * self.TILE_SIZE + k]
                        sA_highlight = sA_cell.copy()
                        sA_highlight.set_fill(YELLOW, opacity=0.8)
                        sA_highlight.set_stroke(YELLOW, width=3)

                        # Highlight s_b element (row k, col 0)
                        sB_cell = self.sB_cells[k * self.TILE_SIZE + col]
                        sB_highlight = sB_cell.copy()
                        sB_highlight.set_fill(YELLOW, opacity=0.8)
                        sB_highlight.set_stroke(YELLOW, width=3)

                        # Arrow from sA to C
                        arrow_sA = Arrow(
                            sA_cell.get_center(),
                            c_cell.get_left() + UP * 0.05 * (k - 0.5),
                            color=BLUE_C,
                            buff=0.08,
                            stroke_width=2,
                            max_tip_length_to_length_ratio=0.15
                        )

                        # Arrow from sB to C
                        arrow_sB = Arrow(
                            sB_cell.get_center(),
                            c_cell.get_top() + RIGHT * 0.05 * (k - 0.5),
                            color=RED_C,
                            buff=0.08,
                            stroke_width=2,
                            max_tip_length_to_length_ratio=0.15
                        )

                        # Show the individual multiplication with global indices for clarity
                        a_global_row = row
                        a_global_col = tile_idx * self.TILE_SIZE + k
                        b_global_row = tile_idx * self.TILE_SIZE + k
                        b_global_col = col
                        mult_single = Text(
                            f"a{a_global_row}{a_global_col} × b{b_global_row}{b_global_col}",
                            font_size=24, color=YELLOW
                        )
                        mult_single.next_to(calc_text, UP, buff=0.2)

                        self.play(
                            FadeIn(sA_highlight),
                            FadeIn(sB_highlight),
                            ShowCreation(arrow_sA),
                            ShowCreation(arrow_sB),
                            FadeIn(mult_single),
                            run_time=0.6
                        )
                        self.wait(0.4)
                        self.play(
                            FadeOut(sA_highlight),
                            FadeOut(sB_highlight),
                            FadeOut(arrow_sA),
                            FadeOut(arrow_sB),
                            FadeOut(mult_single),
                            run_time=0.3
                        )

                    self.wait(0.3)
                    self.play(FadeOut(calc_text), run_time=0.3)
                else:
                    # For other cells, just show the formula briefly
                    self.play(FadeIn(c_highlight), FadeIn(calc_text), run_time=0.4)
                    self.wait(0.3)
                    self.play(FadeOut(calc_text), run_time=0.2)

                c_highlights.add(c_highlight)

        # Fade out compute text after computation phase
        self.play(FadeOut(compute_text), run_time=0.5)

        self.wait(1)

        # Clear iteration elements
        self.iter_elements = VGroup(
            tile_title, a_tile_highlight, b_tile_highlight,
            thread_arrows_a, thread_arrows_b,
            sA_labels, sB_labels, c_highlights
        )

    # =========================================================================
    # Part 7: Accumulation
    # =========================================================================

    def show_accumulation(self):
        if hasattr(self, 'iter_elements'):
            self.play(FadeOut(self.iter_elements), run_time=0.5)

        # Show accumulation formula
        accum_title = Text("Result Accumulation", font_size=32, color=GREEN)
        accum_title.to_corner(TOP + LEFT, buff=0.2)
        self.play(FadeIn(accum_title), run_time=1)

        formula = VGroup(
            Text("C[row][col] = ", font_size=24),
            Text("sum over all tiles of:", font_size=24),
            Text("  sA[ty][k] × sB[k][tx]", font_size=24, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        formula.to_edge(DOWN +LEFT, buff=0.8)

        self.play(FadeIn(formula), run_time=1.5)
        self.wait(1)

        # Highlight final C matrix
        c_final_highlight = SurroundingRectangle(self.C_cells, color=GREEN, buff=0.1, stroke_width=3)
        self.play(ShowCreation(c_final_highlight), run_time=1.5)
        self.wait(2)

        # Fade out formula after showing
        self.play(FadeOut(formula), FadeOut(accum_title), run_time=0.8)

        self.accum_elements = VGroup(c_final_highlight)

    # =========================================================================
    # Part 8: Summary
    # =========================================================================

    def final_summary(self):
        # Fade out most elements
        self.play(
            FadeOut(self.A_group),
            FadeOut(self.B_group),
            FadeOut(self.C_group),
            FadeOut(self.block_group),
            FadeOut(self.sA_group),
            FadeOut(self.sB_group),
            FadeOut(self.accum_elements) if hasattr(self, 'accum_elements') else Wait(0.01),
            run_time=1.5
        )

        # Final summary
        summary_title = Text("Tiled GEMM Summary", font_size=42)
        summary_title.to_edge(UP, buff=0.5)

        summary = VGroup(
            Text("1. Divide matrices into tiles", font_size=28),
            Text("2. Each thread block computes one tile of C", font_size=28),
            Text("3. Load tiles from global to shared memory", font_size=28),
            Text("4. Compute using fast shared memory", font_size=28),
            Text("5. Accumulate partial results across tiles", font_size=28),
            Text("", font_size=10),
            Text("Benefits:", font_size=30, color=GREEN),
            Text("  - Reduced global memory access", font_size=26, color=GREEN_C),
            Text("  - Data reuse within thread block", font_size=26, color=GREEN_C),
            Text("  - ~10x speedup for large matrices", font_size=26, color=GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        summary.next_to(summary_title, DOWN, buff=0.4)

        self.play(Transform(self.title, summary_title), run_time=1)

        for line in summary:
            self.play(FadeIn(line), run_time=0.8)
            self.wait(0.3)

        self.wait(3)

        # Final fade
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)
