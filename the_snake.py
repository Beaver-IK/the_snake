from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -20)
DOWN = (0, 20)
LEFT = (-20, 0)
RIGHT = (20, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:

    position = None
    body_color = None

    def __init__(self):

        self.position = None
        self.body_color = None

    def draw(self):
        pass

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        pass


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
        self.next_direction = RIGHT
        self.body_color = SNAKE_COLOR
        self.last = None

    def reset(self):
        """Cбрасывает змейку в начальное состояние."""
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        global clock
        clock = pygame.time.Clock()
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

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
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

    def __str__(self) -> str:
        pass


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.check_abroad()
        if snake.eat_an_apple(snake, apple):
            apple.randomize_position()
        # проверка столконовения змейки с собой (можно попробовать написать статик-метод, внутри класса змейки), если да, то метод reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
