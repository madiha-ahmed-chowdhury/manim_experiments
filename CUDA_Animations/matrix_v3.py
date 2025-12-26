from manimlib import *

class TiledMatMulFlowDiagram(Scene):
    def construct(self):
        # Colors for memory spaces
        GLOBAL_COLOR = "#4A90D9"  # Blue
        SHARED_COLOR = "#E67E22"  # Orange
        REGISTER_COLOR = "#27AE60"  # Green
        SYNC_COLOR = "#E74C3C"  # Red
        CONTROL_COLOR = "#7F8C8D"  # GREY

        # Dimensions
        BOX_WIDTH = 3.2
        BOX_HEIGHT = 0.55
        SYNC_WIDTH = 5.5
        SYNC_HEIGHT = 0.35
        VERTICAL_SPACING = 0.95

        # Helper function to create a standard box
        def create_box(text, color, width=BOX_WIDTH, height=BOX_HEIGHT):
            rect = Rectangle(
                width=width, height=height,
                fill_color=color, fill_opacity=0.3,
                stroke_color=color, stroke_width=2
            )
            label = Text(text, font_size=20, color=WHITE)
            return VGroup(rect, label)

        # Helper function to create sync barrier
        def create_sync_barrier():
            rect = Rectangle(
                width=SYNC_WIDTH, height=SYNC_HEIGHT,
                fill_color=SYNC_COLOR, fill_opacity=0.5,
                stroke_color=SYNC_COLOR, stroke_width=3
            )
            label = Text("__syncthreads()", font_size=18, color=WHITE)
            return VGroup(rect, label)

        # Helper function to create perfectly straight vertical arrow
        def create_vertical_arrow(y_start, y_end, x=0, color=WHITE):
            line = Line(
                np.array([x, y_start - 0.08, 0]),
                np.array([x, y_end + 0.12, 0]),
                stroke_width=2, color=color
            )
            tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
            tip.scale(0.08)
            tip.move_to([x, y_end + 0.05, 0])
            tip.rotate(PI)  # Point down
            return VGroup(line, tip)

        # Helper function to create perfectly straight horizontal arrow
        def create_horizontal_arrow(x_start, x_end, y, color=WHITE):
            line = Line(
                np.array([x_start + 0.05, y, 0]),
                np.array([x_end - 0.12, y, 0]),
                stroke_width=2, color=color
            )
            tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
            tip.scale(0.08)
            tip.move_to([x_end - 0.05, y, 0])
            tip.rotate(-PI/2)  # Point right
            return VGroup(line, tip)

        # Title
        title = Text("Tiled Matrix Multiplication - Kernel Execution Flow", font_size=28, color=WHITE)
        title.to_edge(UP, buff=0.3)

        # Column headers
        header_y = 3.0
        global_header = Text("Global Memory", font_size=18, color=GLOBAL_COLOR)
        shared_header = Text("Shared Memory", font_size=18, color=SHARED_COLOR)
        register_header = Text("Registers", font_size=18, color=REGISTER_COLOR)

        global_header.move_to([-4.2, header_y, 0])
        shared_header.move_to([0, header_y, 0])
        register_header.move_to([4.2, header_y, 0])

        # Vertical lane dividers
        lane_line1 = DashedLine([-2.1, header_y - 0.3, 0], [-2.1, -5.0, 0], color=GREY)
        lane_line2 = DashedLine([2.1, header_y - 0.3, 0], [2.1, -5.0, 0], color=GREY)

        # Store Y positions explicitly for perfect alignment
        y_positions = {}

        # Starting Y position for flow elements
        current_y = 2.4
        CENTER_X = 0  # All main flow elements centered here

        # 1. Kernel Entry
        y_positions['kernel_entry'] = current_y
        kernel_entry = create_box("Kernel Entry", CONTROL_COLOR, width=2.5, height=0.45)
        kernel_entry.move_to([CENTER_X, current_y, 0])
        current_y -= VERTICAL_SPACING

        # 2. Compute numTiles
        y_positions['compute_tiles'] = current_y
        compute_tiles = create_box("numTiles = K / TILE_SIZE", REGISTER_COLOR)
        compute_tiles.move_to([CENTER_X, current_y, 0])
        current_y -= VERTICAL_SPACING * 0.8

        # 3. Loop start (diamond shape)
        y_positions['loop_start'] = current_y
        loop_diamond = Polygon(
            [0, 0.4, 0], [1.2, 0, 0], [0, -0.4, 0], [-1.2, 0, 0],
            fill_color=CONTROL_COLOR, fill_opacity=0.3,
            stroke_color=CONTROL_COLOR, stroke_width=2
        )
        loop_label = Text("t = 0 to numTiles-1", font_size=16, color=WHITE)
        loop_start = VGroup(loop_diamond, loop_label)
        loop_start.move_to([CENTER_X, current_y, 0])
        current_y -= VERTICAL_SPACING

        # Loop body background
        loop_bg = Rectangle(
            width=6.0, height=4.2,
            fill_color=GREY, fill_opacity=0.08,
            stroke_color=GREY, stroke_width=1, stroke_opacity=0.5
        )
        loop_bg.move_to([CENTER_X, current_y - 1.5, 0])
        loop_label_bg = Text("K-tile loop", font_size=14, color=GREY)
        loop_label_bg.next_to(loop_bg, UP, buff=0.05).align_to(loop_bg, LEFT).shift(RIGHT * 0.2)

        # 4. Load A tile
        y_positions['load_a'] = current_y
        load_a_box = create_box("Load A[tile] → sA", SHARED_COLOR)
        load_a_box.move_to([CENTER_X + 0.2, current_y, 0])  # Slight offset for data arrow
        load_a_global = Square(side_length=0.35, fill_color=GLOBAL_COLOR, fill_opacity=0.5, stroke_color=GLOBAL_COLOR)
        load_a_global.move_to([CENTER_X - 2.0, current_y, 0])
        load_a_arrow = create_horizontal_arrow(CENTER_X - 1.8, CENTER_X - 1.4, current_y, color=GLOBAL_COLOR)
        current_y -= VERTICAL_SPACING * 0.7

        # 5. Load B tile
        y_positions['load_b'] = current_y
        load_b_box = create_box("Load B[tile] → sB", SHARED_COLOR)
        load_b_box.move_to([CENTER_X + 0.2, current_y, 0])
        load_b_global = Square(side_length=0.35, fill_color=GLOBAL_COLOR, fill_opacity=0.5, stroke_color=GLOBAL_COLOR)
        load_b_global.move_to([CENTER_X - 2.0, current_y, 0])
        load_b_arrow = create_horizontal_arrow(CENTER_X - 1.8, CENTER_X - 1.4, current_y, color=GLOBAL_COLOR)
        current_y -= VERTICAL_SPACING * 0.8

        # 6. First sync barrier
        y_positions['sync1'] = current_y
        sync1 = create_sync_barrier()
        sync1.move_to([CENTER_X, current_y, 0])
        current_y -= VERTICAL_SPACING * 0.8

        # 7. Partial dot product
        y_positions['dot_product'] = current_y
        dot_product = create_box("sum += sA × sB", REGISTER_COLOR)
        dot_product.move_to([CENTER_X + 0.2, current_y, 0])
        dot_shared = Square(side_length=0.35, fill_color=SHARED_COLOR, fill_opacity=0.5, stroke_color=SHARED_COLOR)
        dot_shared.move_to([CENTER_X - 2.0, current_y, 0])
        dot_arrow = create_horizontal_arrow(CENTER_X - 1.8, CENTER_X - 1.4, current_y, color=SHARED_COLOR)
        current_y -= VERTICAL_SPACING * 0.8

        # 8. Second sync barrier
        y_positions['sync2'] = current_y
        sync2 = create_sync_barrier()
        sync2.move_to([CENTER_X, current_y, 0])
        current_y -= VERTICAL_SPACING

        # 9. Loop back arrow - using clean orthogonal lines
        loop_back_x = 3.5  # Fixed x position for loop back
        seg1 = Line([2.75, y_positions['sync2'], 0], [loop_back_x, y_positions['sync2'], 0], stroke_width=2, color=CONTROL_COLOR)
        seg2 = Line([loop_back_x, y_positions['sync2'], 0], [loop_back_x, y_positions['loop_start'], 0], stroke_width=2, color=CONTROL_COLOR)
        seg3 = Line([loop_back_x, y_positions['loop_start'], 0], [1.3, y_positions['loop_start'], 0], stroke_width=2, color=CONTROL_COLOR)

        # Add arrowhead pointing left
        arrow_tip = Triangle(fill_color=CONTROL_COLOR, fill_opacity=1, stroke_width=0)
        arrow_tip.scale(0.08)
        arrow_tip.move_to([1.25, y_positions['loop_start'], 0])
        arrow_tip.rotate(PI/2)  # Point left
        loop_back = VGroup(seg1, seg2, seg3, arrow_tip)

        loop_back_label = Text("next tile", font_size=14, color=CONTROL_COLOR)
        loop_back_label.move_to([loop_back_x + 0.5, (y_positions['sync2'] + y_positions['loop_start']) / 2, 0])

        # 10. Write C
        y_positions['write_c'] = current_y
        write_c_box = create_box("C[row,col] = sum", GLOBAL_COLOR)
        write_c_box.move_to([CENTER_X + 0.2, current_y, 0])
        write_c_reg = Square(side_length=0.35, fill_color=REGISTER_COLOR, fill_opacity=0.5, stroke_color=REGISTER_COLOR)
        write_c_reg.move_to([CENTER_X - 2.0, current_y, 0])
        write_c_arrow = create_horizontal_arrow(CENTER_X - 1.8, CENTER_X - 1.4, current_y, color=REGISTER_COLOR)
        current_y -= VERTICAL_SPACING

        # 11. Kernel Exit
        y_positions['kernel_exit'] = current_y
        kernel_exit = create_box("Kernel Exit", CONTROL_COLOR, width=2.5, height=0.45)
        kernel_exit.move_to([CENTER_X, current_y, 0])

        # Control flow arrows (vertical) - all at x=0 for perfect alignment
        arrows = VGroup()
        arrows.add(create_vertical_arrow(y_positions['kernel_entry'] - 0.225, y_positions['compute_tiles'] + BOX_HEIGHT/2, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['compute_tiles'] - BOX_HEIGHT/2, y_positions['loop_start'] + 0.4, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['loop_start'] - 0.4, y_positions['load_a'] + BOX_HEIGHT/2, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['load_a'] - BOX_HEIGHT/2, y_positions['load_b'] + BOX_HEIGHT/2, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['load_b'] - BOX_HEIGHT/2, y_positions['sync1'] + SYNC_HEIGHT/2, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['sync1'] - SYNC_HEIGHT/2, y_positions['dot_product'] + BOX_HEIGHT/2, CENTER_X))
        arrows.add(create_vertical_arrow(y_positions['dot_product'] - BOX_HEIGHT/2, y_positions['sync2'] + SYNC_HEIGHT/2, CENTER_X))

        # Exit arrow from loop
        exit_arrow = create_vertical_arrow(y_positions['sync2'] - SYNC_HEIGHT/2, y_positions['write_c'] + BOX_HEIGHT/2, CENTER_X)
        exit_label = Text("done", font_size=14, color=CONTROL_COLOR)
        exit_label.move_to([CENTER_X - 0.4, (y_positions['sync2'] + y_positions['write_c']) / 2, 0])

        arrows.add(create_vertical_arrow(y_positions['write_c'] - BOX_HEIGHT/2, y_positions['kernel_exit'] + 0.225, CENTER_X))

        # Legend
        legend_title = Text("Legend:", font_size=16, color=WHITE)
        legend_items = VGroup(
            VGroup(Square(side_length=0.25, fill_color=GLOBAL_COLOR, fill_opacity=0.5, stroke_color=GLOBAL_COLOR),
                   Text("Global Memory", font_size=14, color=GLOBAL_COLOR)).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.25, fill_color=SHARED_COLOR, fill_opacity=0.5, stroke_color=SHARED_COLOR),
                   Text("Shared Memory", font_size=14, color=SHARED_COLOR)).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.25, fill_color=REGISTER_COLOR, fill_opacity=0.5, stroke_color=REGISTER_COLOR),
                   Text("Registers", font_size=14, color=REGISTER_COLOR)).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.25, fill_color=SYNC_COLOR, fill_opacity=0.5, stroke_color=SYNC_COLOR),
                   Text("Sync Barrier", font_size=14, color=SYNC_COLOR)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        legend = VGroup(legend_title, legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(DL, buff=0.4)

        # Add all elements to scene (no animation, just add)
        self.add(title)
        self.add(global_header, shared_header, register_header)
        self.add(lane_line1, lane_line2)
        self.add(loop_bg, loop_label_bg)
        self.add(kernel_entry)
        self.add(compute_tiles)
        self.add(loop_start)
        self.add(load_a_global, load_a_box, load_a_arrow)
        self.add(load_b_global, load_b_box, load_b_arrow)
        self.add(sync1)
        self.add(dot_shared, dot_product, dot_arrow)
        self.add(sync2)
        self.add(loop_back, loop_back_label)
        self.add(write_c_reg, write_c_box, write_c_arrow)
        self.add(exit_arrow, exit_label)
        self.add(kernel_exit)
        self.add(arrows)
        self.add(legend)

        # Adjust camera to fill screen - zoom in and center on content
        self.camera.frame.set_height(9)  # Smaller = more zoomed in
        self.camera.frame.move_to([0, -0.8, 0])  # Center on the diagram


# To save as PNG image, run interactively and press 's':
# manimgl matrix_v3.py TiledMatMulFlowDiagram
# Then press 's' to save screenshot to images/ folder
#
# Or use this Python script to save directly:
if __name__ == "__main__":
    from manimlib import config
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 1

    scene = TiledMatMulFlowDiagram()
    scene.run()
    # Press 's' in the window to save, then 'q' to quit
