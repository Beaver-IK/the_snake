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
COMMANDS = {
    pygame.K_UP: (UP, DOWN),
    pygame.K_DOWN: (DOWN, UP),
    pygame.K_LEFT: (LEFT, RIGHT),
    pygame.K_RIGHT: (RIGHT, LEFT),
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 20
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс, предназначенный для создания
    игровых объектов.
    """

    position = None
    body_color = None

    def __init__(self):
        pass

    def draw(self):
        """Метод отрисовки. Будет переопределен в наследных классах."""
        pass


class Apple(GameObject):
    """Наследованный класс от GameObject.
    Объект яблока.
    """

    def __init__(self):
        """Инициализатор Яблока
        При создании, задает параметр цвета яблока и
        случайное положение на поле.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (
            randrange(0, 620, GRID_SIZE),
            randrange(0, 460, GRID_SIZE)
        )

    def draw(self):
        """Функция отрисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Функция, задает случайные координаты нового яблока"""
        self.position = (
            randrange(0, 620, GRID_SIZE),
            randrange(0, 460, GRID_SIZE)
        )


class Snake(GameObject):
    """Наследованный класс от GameObject.
    Объект Змейки.
    """

    def __init__(self):
        """Инициализация начального состояния змейки.
        При создании задаются параметры:
        Цвет змейки(наследованный параметр), позиция в центре экрана
        (наследованный параметр), длина змейки, равная 1, список координат
        секций змейки, действующее направление, указанное
        направление, координаты последней секции змейки
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def reset(self):
        """Сбрасывает состояние змейки до стартового.
        Пересоздает игровое поле, оставляя действующие координаты
        яблока.
        Записывает достигнутый результат в файй, если он является
        лучшим.
        """
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
        """Обновляет направление движения змейки.
        Перенося указынное направление в действующее.
        """
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
        новую голову и удаляя последний элемент.
        """
        head_pos = self.get_head_position()
        head_pos = (
            head_pos[0] + self.direction[0],
            head_pos[1] + self.direction[1]
        )
        self.positions.insert(0, head_pos)
        self.last = self.positions.pop(-1)

    @staticmethod
    def eat_an_apple(self, apple_object: Apple) -> bool:
        """Функция класса. Принимает объекты змейки и яблока.
        Если яблоко съедено, увеличивает змейку на одну секцию
        и возвращает значение bool.
        """
        if self.positions[0] == apple_object.position:
            self.positions.append(self.last)
            self.lenght += 1
            return True
        return False

    def collision_check(self):
        """Функция проверки столкновения змейки с хвостом."""
        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def check_abroad(self):
        """Функция проверки выхода за границы игрового поля."""
        head_x, head_y = self.get_head_position()
        if head_x < 0 and self.direction == LEFT:
            self.positions[0] = (620, head_y)
        if head_x == SCREEN_WIDTH and self.direction == RIGHT:
            self.positions[0] = (0, head_y)
        if head_y < 0 and self.direction == UP:
            self.positions[0] = (head_x, 460)
        if head_y == SCREEN_HEIGHT and self.direction == DOWN:
            self.positions[0] = (head_x, 0)


def handle_keys(game_object):
    """Функция считывания комманд для змейки с клавиатуры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if game_object.direction != COMMANDS[event.key][1]:
                game_object.next_direction = COMMANDS[event.key][0]


def main():
    """Игра Змейка
    Задача игры:
    Управляя змейкой, направлять ее на яблоки, красного цвета. С каждым
    съеденным яблоком, змейка увеличивается на одну секцию.
    Логика:
    Инициализирутся игровое поле с заданными параметрами
    Инициализируются два объекта - змейка Олег и яблоко Рудольф
    Далее запускается цикл, обрабатывающий все события игры и обновляющий
    игровое поле.
    События:
    Задается заранее установленная скорость игры
    Считывается команда для змейки
    При необходимости обновляется направление следования змейки
    Движение змейки
    Контроль выхода змейки за границы игрового поля
    Контроль столкновения змейки с хвостом
    Контроль поедания яблок и увеличение змейки на одну секцию
    В случае поедания яблока, генерация нового яблока на игровом поле
    Отрисовка обновленных координат яблока и змейки
    Обновление игрового поля
    Скрытые события:
    При столкновении с хвостом, игра перезапускается, значение длины змейки
    обнуляется, а результат игры, в случае если он является лучшим,
    сохраняется в отдельном файле best_result.txt
    ПРИЯТНОЙ ИГРЫ!
    """
    pygame.init()
    apple_rudolf = Apple()
    snake_oleg = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake_oleg)
        snake_oleg.update_direction()
        snake_oleg.move()
        snake_oleg.check_abroad()
        snake_oleg.collision_check()
        if snake_oleg.eat_an_apple(snake_oleg, apple_rudolf):
            apple_rudolf.randomize_position()
        snake_oleg.draw()
        apple_rudolf.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
