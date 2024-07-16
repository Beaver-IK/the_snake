import pygame
from gameparts import *


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if game_object.direction != COMMANDS[event.key][1]:
                game_object.next_direction = COMMANDS[event.key][0]


def main():
    pygame.init()
    apple_rudolf = Apple()
    snake_oleg = Snake()

    while True:
        clock.tick(SPEED)  # Установка скорости. В планах опциональное увеличение.
        handle_keys(snake_oleg)  # Считываем команду с клавиатуры
        snake_oleg.update_direction()  # Устанавливаем считанное направление
        snake_oleg.move()  # Двигаем змея
        snake_oleg.check_abroad()  # Контролируем выход за границу поля
        snake_oleg.collision_check()  # Контролируем столкновение с хвостом
        # Позже сделаю камни и буду передават в статичный метод объект ...
        # ... камней и проверять на столкновение с ними.
        if snake_oleg.eat_an_apple(snake_oleg, apple_rudolf):  # Контроль поедания яблок
            apple_rudolf.randomize_position()  # Если съедаем - генерируем новое
        snake_oleg.draw()  # Рисуем Олега
        apple_rudolf.draw()  # Рисуем Рудольфа
        pygame.display.update()  # Обновляем экран


if __name__ == '__main__':
    main()
