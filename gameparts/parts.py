from random import randrange
import pygame
from .const import *


class GameObject:

    position = None
    body_color = None

    def __init__(self):

        self.position = None
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    """Объект Яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (randrange(0, 620, GRID_SIZE), randrange(0, 460, GRID_SIZE))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        self.position = (randrange(0, 620, GRID_SIZE), randrange(0, 460, GRID_SIZE))


class Snake(GameObject):
    """Объект змейки"""

    def __init__(self):
        """Инициализация начального состояния змейки."""

        super().__init__()
        self.body_color = SNAKE_COLOR
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def reset(self):
        """Cбрасывает змейку в начальное состояние."""
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        global clock
        clock = pygame.time.Clock()
        with open('best_result.txt', 'r', encoding='utf-8') as file:
            result = int(file.read())
        if result < self.lenght:
            with open('best_result.txt', 'w', encoding='utf-8') as file:
                file.write(f'{self.lenght}')
        self.__init__()
        pygame.init()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """

        head_pos = self.get_head_position()
        head_pos = (head_pos[0] + self.direction[0], head_pos[1] + self.direction[1])
        self.positions.insert(0, head_pos)
        self.last = self.positions.pop(-1)

    @staticmethod
    def eat_an_apple(self, apple_object: Apple) -> bool:
        if self.positions[0] == apple_object.position:
            self.positions.append(self.last)
            self.lenght += 1
            return True
        return False

    def collision_check(self):
        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def check_abroad(self):
        head_x, head_y = self.get_head_position()
        if head_x < 0 and self.direction == LEFT:
            self.positions[0] = (620, head_y)
        if head_x == SCREEN_WIDTH and self.direction == RIGHT:
            self.positions[0] = (0, head_y)
        if head_y < 0 and self.direction == UP:
            self.positions[0] = (head_x, 460)
        if head_y == SCREEN_HEIGHT and self.direction == DOWN:
            self.positions[0] = (head_x, 0)
