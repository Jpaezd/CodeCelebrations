import pygame
import sys
import random
import math

pygame.init()

# --- CONFIGURACIÓN DE VENTANA ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bitcoin Pac-Man Navideño — by JPaezD")

clock = pygame.time.Clock()

# --- CARGA DE IMÁGENES ---
btc = pygame.image.load("assets/btc.png")
btc = pygame.transform.scale(btc, (60, 60))

coin_images = {
    "USD": pygame.transform.scale(pygame.image.load("assets/usd.png"), (40, 40)),
    "EUR": pygame.transform.scale(pygame.image.load("assets/eur.png"), (40, 40)),
    "JPY": pygame.transform.scale(pygame.image.load("assets/jpy.png"), (40, 40)),
    "GBP": pygame.transform.scale(pygame.image.load("assets/gbp.png"), (40, 40)),
    "CNY": pygame.transform.scale(pygame.image.load("assets/cny.png"), (40, 40)),
}

# --- POSICIÓN INICIAL DE BITCOIN ---
btc_x, btc_y = WIDTH // 2, HEIGHT // 2
btc_speed = 2.5

# --- GENERAR MONEDAS FIAT ESTÁTICAS ---
coins = []
for key in coin_images:
    x = random.randint(60, WIDTH - 60)
    y = random.randint(60, HEIGHT - 60)
    coins.append([key, x, y])

# --- GENERAR NIEVE ---
snowflakes = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 5)
    speed = random.uniform(1, 3)
    snowflakes.append([x, y, size, speed])

# --- GENERAR LUCES DEL ÁRBOL ---
lights = []
for i in range(15):
    x = WIDTH // 2 - 50 + random.randint(0, 100)
    y = HEIGHT - 150 + random.randint(0, 150)
    color = random.choice([(255,0,0), (255,255,0), (0,255,0), (0,255,255)])
    blink_speed = random.randint(20, 60)
    lights.append([x, y, color, blink_speed, 0])

# --- LOOP PRINCIPAL ---
running = True
while running:
    screen.fill((10, 10, 20))  # Fondo oscuro elegante

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- SI NO HAY MONEDAS, TERMINA ---
    if not coins:
        font = pygame.font.SysFont("Arial", 40)
        done_text = font.render("¡Todas las monedas fiat fueron comidas!", True, (255, 215, 0))
        screen.blit(done_text, (100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # --- DIBUJAR ÁRBOL DE NAVIDAD ---
    tree_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 150, 100, 150)
    pygame.draw.polygon(screen, (0, 150, 0), [
        (WIDTH//2, HEIGHT - 300),
        (WIDTH//2 - 100, HEIGHT - 50),
        (WIDTH//2 + 100, HEIGHT - 50)
    ])
    pygame.draw.rect(screen, (139,69,19), (WIDTH//2 - 15, HEIGHT - 50, 30, 50))

    # --- DIBUJAR LUCES ---
    for light in lights:
        light[4] += 1
        if (light[4] // light[3]) % 2 == 0:
            pygame.draw.circle(screen, light[2], (light[0], light[1]), 5)

    # --- NIEVE ---
    for flake in snowflakes:
        flake[1] += flake[3]
        flake[0] += math.sin(pygame.time.get_ticks()/500) * 0.5  # ligero movimiento horizontal
        pygame.draw.circle(screen, (255, 255, 255), (int(flake[0]), int(flake[1])), flake[2])
        if flake[1] > HEIGHT:
            flake[1] = -flake[2]
            flake[0] = random.randint(0, WIDTH)

    # --- SELECCIONAR LA MONEDA MÁS CERCANA ---
    target = min(
        coins,
        key=lambda c: math.dist((btc_x, btc_y), (c[1], c[2]))
    )

    # --- MOVIMIENTO AUTOMÁTICO DE BITCOIN HACIA LA MONEDA ---
    tx, ty = target[1], target[2]
    angle = math.atan2(ty - btc_y, tx - btc_x)
    btc_x += math.cos(angle) * btc_speed
    btc_y += math.sin(angle) * btc_speed

    # Dibujar Bitcoin
    screen.blit(btc, (btc_x, btc_y))

    # --- DETECCIÓN DE COLISIÓN ---
    btc_rect = pygame.Rect(btc_x, btc_y, 60, 60)
    coins = [
        c for c in coins
        if not btc_rect.colliderect(pygame.Rect(c[1], c[2], 40, 40))
    ]

    # --- DIBUJAR MONEDAS FIAT ---
    for c in coins:
        screen.blit(coin_images[c[0]], (c[1], c[2]))

    # --- TEXTO EN LA ESQUINA INFERIOR ---
    font = pygame.font.SysFont("Arial", 24)
    text = font.render("By JPaezD  |  linkedin.com/in/jpaezd", True, (255, 255, 255))
    screen.blit(text, (20, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)
