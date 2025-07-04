import asyncio
import pygame
from slot_machine import SlotMachine

async def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🎰 Slot Machine")

    machine = SlotMachine()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                machine.spin_start()

        machine.draw(screen)
        pygame.display.flip()
        await asyncio.sleep(0.01)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
