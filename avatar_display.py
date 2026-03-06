#!/usr/bin/env python3
import pygame
import os
import sys

os.environ['WAYLAND_DISPLAY'] = 'wayland-0'
os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
os.environ['SDL_VIDEODRIVER'] = 'wayland'

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    W, H = screen.get_size()
    print(f"SDL screen size: {W}x{H}", flush=True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    woman_img = pygame.image.load(os.path.expanduser("~/ag-woman.png")).convert()
    man_img = pygame.image.load(os.path.expanduser("~/ag-man.png")).convert()

    orig_w = woman_img.get_width()
    orig_h = woman_img.get_height()
    print(f"Image size: {orig_w}x{orig_h}", flush=True)

    half_w = W // 2
    scale = min(half_w / orig_w, H / orig_h)
    scaled_w = int(orig_w * scale)
    scaled_h = int(orig_h * scale)
    print(f"Scaled to: {scaled_w}x{scaled_h}", flush=True)

    woman_scaled = pygame.transform.smoothscale(woman_img, (scaled_w, scaled_h))
    man_scaled = pygame.transform.smoothscale(man_img, (scaled_w, scaled_h))

    x_offset = (half_w - scaled_w) // 2
    y_offset = (H - scaled_h) // 2

    screen.fill((0, 0, 0))
    screen.blit(woman_scaled, (x_offset, y_offset))
    screen.blit(man_scaled, (half_w + x_offset, y_offset))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        clock.tick(30)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
