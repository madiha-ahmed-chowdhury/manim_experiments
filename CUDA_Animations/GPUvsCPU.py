from manimlib import *

class K8sGPUAnimation(Scene):

    def create_node(self, label):
        box = Rectangle(width=5, height=3)
        text = Text(label, font_size=28).next_to(box, UP)
        return VGroup(box, text)

    def create_pod(self, label, color=BLUE):
        pod = RoundedRectangle(width=1.6, height=0.8, corner_radius=0.2, color=color)
        text = Text(label, font_size=20).move_to(pod.get_center())
        return VGroup(pod, text)

    def create_cpu(self, label):
        cpu = Square(side_length=0.8, color=GREEN)
        text = Text(label, font_size=18).move_to(cpu.get_center())
        return VGroup(cpu, text)

    def create_gpu(self):
        gpu = Rectangle(width=3.5, height=1.5, color=ORANGE)
        text = Text("GPU", font_size=28).move_to(gpu.get_center())
        return VGroup(gpu, text)

    # --------------------------------------------------
    # Scene 1: CPU Fractional Sharing
    # --------------------------------------------------
    def scene_cpu_sharing(self):

        title = Text("CPU Resource Sharing in Kubernetes", font_size=36).to_edge(UP)
        self.play(Write(title))

        node = self.create_node("Kubernetes Node")
        node.shift(LEFT * 3)

        cpus = VGroup(*[
            self.create_cpu(f"C{i}") for i in range(1, 5)
        ]).arrange(RIGHT, buff=0.3).move_to(node[0].get_center())

        self.play(ShowCreation(node), FadeIn(cpus))

        podA = self.create_pod("Pod A\n0.5 CPU")
        podB = self.create_pod("Pod B\n0.25 CPU")
        podC = self.create_pod("Pod C\n0.25 CPU")

        pods = VGroup(podA, podB, podC).arrange(DOWN, buff=0.5).shift(RIGHT * 3)

        self.play(FadeIn(pods))

        arrows = VGroup(
            Arrow(podA.get_left(), cpus[0].get_right()),
            Arrow(podB.get_left(), cpus[1].get_right()),
            Arrow(podC.get_left(), cpus[2].get_right()),
        )

        self.play(ShowCreation(arrows))

        explanation = Text(
            "CPU can be time-sliced using OS scheduler and cgroups",
            font_size=24
        ).to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 2: GPU Architecture
    # --------------------------------------------------
    def scene_gpu_architecture(self):

        title = Text("CPU vs GPU Architecture", font_size=36).to_edge(UP)
        self.play(Write(title))

        # --- CPU side: few large cores ---
        cpu_chip = Rectangle(width=3, height=3, color=GREEN)
        cpu_cores = VGroup(*[
            Square(side_length=0.9, color=GREEN, fill_opacity=0.3)
            for _ in range(4)
        ]).arrange_in_grid(n_rows=2, n_cols=2, buff=0.2).move_to(cpu_chip.get_center())
        cpu_label = Text("CPU", font_size=28).next_to(cpu_chip, UP)
        cpu_desc = Text("4 powerful cores", font_size=20).next_to(cpu_chip, DOWN)
        cpu_purpose = Text("Meant for multitasking", font_size=18, color=GREEN).next_to(cpu_desc, DOWN)
        cpu_group = VGroup(cpu_chip, cpu_cores, cpu_label, cpu_desc, cpu_purpose).shift(LEFT * 3.5)

        # --- GPU side: many small cores ---
        gpu_chip = Rectangle(width=3.5, height=3, color=ORANGE)
        gpu_cores = VGroup(*[
            Square(side_length=0.22, color=ORANGE, fill_opacity=0.3)
            for _ in range(80)
        ]).arrange_in_grid(n_rows=8, n_cols=10, buff=0.08).move_to(gpu_chip.get_center())
        gpu_label = Text("GPU", font_size=28).next_to(gpu_chip, UP)
        gpu_desc = Text("1000s of small cores", font_size=20).next_to(gpu_chip, DOWN)
        gpu_purpose = Text("Used for massively parallel tasks", font_size=18, color=ORANGE).next_to(gpu_desc, DOWN)
        gpu_group = VGroup(gpu_chip, gpu_cores, gpu_label, gpu_desc, gpu_purpose).shift(RIGHT * 3.5)

        self.play(FadeIn(cpu_group), FadeIn(gpu_group))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 3: GPU Exclusive Allocation
    # --------------------------------------------------
    def scene_gpu_exclusive(self):

        title = Text("GPU Allocation is Exclusive", font_size=34).to_edge(UP)
        self.play(Write(title))

        node = self.create_node("GPU Node")
        node.shift(LEFT * 3)

        gpu = self.create_gpu().move_to(node[0].get_center())

        self.play(ShowCreation(node), FadeIn(gpu))

        pod1 = self.create_pod("Training Pod\nrequests GPU", RED).shift(RIGHT * 3)
        pod2 = self.create_pod("Waiting Pod", BLUE).next_to(pod1, DOWN)

        self.play(FadeIn(pod1), FadeIn(pod2))

        arrow = Arrow(pod1.get_left(), gpu.get_right())
        self.play(ShowCreation(arrow))

        usage = Rectangle(width=0.35, height=1.5, fill_opacity=0.8, color=RED).align_to(gpu[0], LEFT).align_to(gpu[0], DOWN)

        usage_label = Text("10% GPU Used", font_size=20).next_to(gpu, DOWN)

        self.play(ShowCreation(usage), Write(usage_label))

        lock = Text("Exclusive Lock", font_size=22, color=YELLOW).next_to(gpu, UP)
        self.play(Write(lock))

        wait_text = Text(
            "Remaining GPU cannot be allocated to other pods",
            font_size=24
        ).to_edge(DOWN)

        self.play(Write(wait_text))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 4: NVIDIA Device Plugin
    # --------------------------------------------------
    def scene_device_plugin(self):

        title = Text("Step 1: NVIDIA Device Plugin", font_size=36).to_edge(UP)
        self.play(Write(title))

        node = self.create_node("GPU Node")
        plugin = self.create_pod("Device Plugin", PURPLE).move_to(node[0].get_center())

        self.play(ShowCreation(node), FadeIn(plugin))

        discover = Text("Discovers GPUs", font_size=24).next_to(plugin, DOWN)
        register = Text("Registers nvidia.com/gpu", font_size=24).next_to(discover, DOWN)

        self.play(Write(discover))
        self.play(Write(register))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 5: Pod YAML GPU Request
    # --------------------------------------------------
    def scene_yaml_request(self):

        title = Text("Step 2: Request GPU in Pod Spec", font_size=36).to_edge(UP)
        self.play(Write(title))

        yaml_text = Code(
            code="""resources:
  limits:
    nvidia.com/gpu: 1""",
            language="yaml",
            font_size=24
        )

        self.play(ShowCreation(yaml_text))

        scheduler = Text("Scheduler Finds Free GPU Node", font_size=28).to_edge(DOWN)
        self.play(Write(scheduler))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 6: Assignment and Isolation
    # --------------------------------------------------
    def scene_assignment(self):

        title = Text("Step 3: GPU Attached to Container Runtime", font_size=34).to_edge(UP)
        self.play(Write(title))

        gpu = self.create_gpu().shift(LEFT * 2)
        pod = self.create_pod("Running Pod", RED).shift(RIGHT * 2)

        arrow = Arrow(gpu.get_right(), pod.get_left())

        self.play(ShowCreation(gpu), FadeIn(pod))
        self.play(ShowCreation(arrow))

        iso = Text("GPU Isolated From Other Pods", font_size=28).to_edge(DOWN)
        self.play(Write(iso))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Scene 7: Advanced Sharing MIG + Time Slice
    # --------------------------------------------------
    def scene_advanced(self):

        title = Text("Advanced GPU Sharing", font_size=36).to_edge(UP)
        self.play(Write(title))

        gpu = self.create_gpu().shift(LEFT * 3)
        self.play(ShowCreation(gpu))

        # MIG partitions
        parts = VGroup(*[
            Rectangle(width=1.1, height=1.2) for _ in range(3)
        ]).arrange(RIGHT, buff=0.1).move_to(gpu[0].get_center())

        self.play(Create(parts))

        mig_text = Text("MIG Partitions", font_size=24).next_to(gpu, DOWN)
        self.play(Write(mig_text))

        # Time slicing visualization
        pods = VGroup(*[
            self.create_pod(f"Pod {i}") for i in range(1, 4)
        ]).arrange(DOWN).shift(RIGHT * 3)

        self.play(FadeIn(pods))

        time_text = Text("Time-Slicing Sharing", font_size=24).to_edge(DOWN)
        self.play(Write(time_text))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # --------------------------------------------------
    # Master Animation Flow
    # --------------------------------------------------
    def construct(self):

        self.scene_cpu_sharing()
        self.scene_gpu_architecture()
        self.scene_gpu_exclusive()
        self.scene_device_plugin()
        self.scene_yaml_request()
        self.scene_assignment()
        # self.scene_advanced()
