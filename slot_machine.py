import pandas as pd
import pygame
import time
import random

class SlotMachineInternal:
    def __init__(self, cycle=0):
        self.cycle = cycle
        self.slot1 = "000"
        self.slot2 = "000"
        self.slot3 = "000"
        self.seed = pd.read_csv("random_number_generator/lfsr_output.csv", dtype={'Value': str})["Value"]

    def spin_batch(self, num_frames):
        """Simulate multiple spins and return slot triplets for animation."""
        frames = []
        for _ in range(num_frames):
            value = self.seed[self.cycle % len(self.seed)]
            slot1, slot2, slot3 = value[:3], value[3:6], value[6:9]
            frames.append((slot1, slot2, slot3))
            self.cycle += 1
        return frames

class SlotMachine:
    def __init__(self):
        self.internal = SlotMachineInternal()
        self.visual = {
            "000": "images/sun.png",
            "001": "images/cherry.png",
            "010": "images/orange.png",
            "011": "images/melon.png",
            "100": "images/lemon.png",
            "101": "images/grape.png",
            "110": "images/star.png",
            "111": "images/diamond.png"
        }

        self.images = {
            key: pygame.transform.scale(pygame.image.load(path), (150, 150))
            for key, path in self.visual.items()
        }

        pygame.mixer.init()
        self.spin_sound = pygame.mixer.Sound("audio/spin.mp3")
        self.win_sound = pygame.mixer.Sound("audio/win.mp3")

        self.font = pygame.font.Font(None, 50)
        self.slot_bg_color = (50, 50, 50)
        self.result = "Press SPACE to Spin"

        self.anim_frames = []   # List of slot triplets (20 frames)
        self.anim_index = 0
        self.anim_start_time = None
        self.anim_frame_duration = 0.1  # seconds per frame
        self.anim_total_time = 4.0
        self.display_codes = ["000", "000", "000"]
        self.spinning = False

    def spin_start(self):
        self.anim_frames = self.internal.spin_batch(20)
        self.anim_index = 0
        self.anim_start_time = time.time()
        self.spinning = True
        self.result = ""
        self.spin_sound.play()


    def update_spin(self):
        if not self.spinning:
            return

        now = time.time()
        elapsed = now - self.anim_start_time

        next_index = int(elapsed // self.anim_frame_duration)
        if next_index < len(self.anim_frames):
            self.display_codes = list(self.anim_frames[next_index])
        else:
            self.display_codes = list(self.anim_frames[-1])
            self.spinning = False
            self.result = self.get_result()

            if "JACKPOT" in self.result or "Two of a kind" in self.result:
                self.win_sound.play()


    def get_result(self):
        s1, s2, s3 = self.display_codes
        if s1 == s2 == s3:
            return "🎉 JACKPOT!"
        elif s1 == s2 or s2 == s3 or s1 == s3:
            return "✨ Two of a kind!"
        else:
            return "Try again!"

    def draw(self, screen):
        self.update_spin()
        screen.fill((15, 15, 15))  # Dark background

        # === Slot Machine Frame ===
        pygame.draw.rect(screen, (0, 0, 0), (90, 140, 620, 310), border_radius=30)     # Shadow
        pygame.draw.rect(screen, (200, 0, 0), (100, 150, 600, 290), border_radius=25)  # Main frame
        pygame.draw.rect(screen, (240, 30, 30), (110, 160, 580, 270), border_radius=20)  # Inner frame

        # === Top Light Bar ===
        pygame.draw.ellipse(screen, (255, 255, 100), (250, 120, 300, 40))

        # === Lever (dynamic) ===
        lever_color = (220, 220, 220)
        knob_color = (255, 40, 40)

        if self.spinning:
            pygame.draw.line(screen, lever_color, (720, 220), (750, 350), 10)   # tilted handle
            pygame.draw.circle(screen, knob_color, (750, 350), 18)
        else:
            pygame.draw.line(screen, lever_color, (730, 180), (730, 300), 10)   # vertical handle
            pygame.draw.circle(screen, knob_color, (730, 180), 18)

        # === Slot Area Background ===
        pygame.draw.rect(screen, (30, 30, 30), (140, 200, 520, 180), border_radius=18)

        # === Slots ===
        for i, code in enumerate(self.display_codes):
            x = 160 + i * 180
            y = 220

            # Outer shadow frame
            pygame.draw.rect(screen, (80, 80, 80), (x-6, y-6, 160, 160), border_radius=12)

            # Light inner slot box
            pygame.draw.rect(screen, (235, 235, 235), (x, y, 150, 150), border_radius=10)

            # Symbol
            screen.blit(self.images[code], (x, y))

        # === Result Text ===
        if self.result:
            text_surface = self.font.render(self.result, True, (255, 255, 0))
            screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 480))
