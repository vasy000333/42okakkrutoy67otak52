import turtle
import random
import math

# Настройки экрана
screen = turtle.Screen()
screen.tracer(0)
screen.bgcolor("black")
screen.setup(width=1600, height=900)
screen.title("Атомная симуляция с соединениями")
f = 0
# Параметры атомов
ATOM_TYPES = {
    'H': {'color': 'white', 'valence': 1, 'mass': 1, 'el': 2, 'z': 0, 'en': 1000, 't': "a","t2": 0},
    'O': {'color': 'green', 'valence': 2, 'mass': 4, 'el': 1, 'z': 0, 'en': 1000, 't': "a","t2": 0},
    'C': {'color': 'blue', 'valence': 4, 'mass': 3, 'el': 3, 'z': 0, 'en': 1000, 't': "a","t2": 0},
    'N': {'color': 'red', 'valence': 3, 'mass': 3, 'el': 4, 'z': 0, 'en': 1000, 't': "a","t2": 0},
}
LJ_EPS = 50.0             # глубина потенциальной ямы ( Lennard-Jones )
LJ_SIGMA = 20.0           # характерное расстояние LJ
LJ_CUTOFF = 120.0 
G = 0.0  # обычную гравитацию отключаем, соединение будет по валентности
JOIN_DISTANCE = 30  # расстояние для образования связи
SPRING_FORCE = 0.1  # сила связи



class Atom:
    def __init__(self, atom_type):
        self.atom_type = atom_type
        self.radius = 10
        self.t2 = ATOM_TYPES[atom_type]['t2']
        self.en = ATOM_TYPES[atom_type]['en']
        self.t = ATOM_TYPES[atom_type]['t']
        self.mass = ATOM_TYPES[atom_type]['mass']
        self.valence = ATOM_TYPES[atom_type]['valence']
        self.el = ATOM_TYPES[atom_type]['el']
        self.z = ATOM_TYPES[atom_type]['z']
        self.remaining_valence = self.valence
        self.color = ATOM_TYPES[atom_type]['color']
        self.x = random.randint(-750, 750)
        self.y = random.randint(-400, 400)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.connections = []
        self.con2 = []

        # Визуальное отображение
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(self.color)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.shapesize(0.8)
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.penup()
        self.label.color("white")
        self.update_label()

    def update_label(self):
        self.label.clear()
        if self.z == -1: c = f"- {self.atom_type}";
        elif self.z == 1: c = f"+{self.atom_type}";
        else: c = f"0{self.atom_type}"
        self.label.goto(self.x + 5, self.y + 5)
        self.label.write(c, align="left", font=("Arial", 8, "normal"))

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
    def ggg(self, other):
        if self == other:
            return
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0 or dist > 1000:
            return

        nx = dx / dist
        ny = dy / dist

        # --- Жёсткое отталкивание только если слишком близко ---
        MIN_DIST = self.radius + other.radius
        if dist < MIN_DIST:
            overlap = MIN_DIST - dist
            self.x -= nx * overlap * 0.5
            self.y -= ny * overlap * 0.5
            other.x += nx * overlap * 0.5
            other.y += ny * overlap * 0.5
            # небольшое гашение скоростей
            self.vx *= 0.7
            self.vy *= 0.7
            other.vx *= 0.7
            other.vy *= 0.7
            return # не добавляем больше сил, чтобы не дергались

        # --- Кулон ---
        K = 2000.0
        qprod = self.z * other.z
        force_mag = K * qprod / (dist ** 2 + 1e-6)
        self.vx += nx * force_mag / self.mass
        self.vy += ny * force_mag / self.mass
        other.vx -= nx * force_mag / other.mass
        other.vy -= ny * force_mag / other.mass

        # --- Lennard-Jones (примитивно) ---
        if dist < LJ_CUTOFF:
            # LJ: F = 24*eps*(2*(sigma^12)/r^13 - (sigma^6)/r^7)
            s = LJ_SIGMA
            e = LJ_EPS
            r = max(dist, 1e-6)
            r2 = r * r
            r6 = r2 * r2 * r2
            s6 = s ** 6
            s12 = s6 * s6
            force_lj = 24 * e * (2 * s12 / (r6 * r6 * r) - s6 / (r6 * r))
            fx_lj = nx * force_lj
            fy_lj = ny * force_lj
            self.vx += fx_lj / self.mass
            self.vy += fy_lj / self.mass
            other.vx -= fx_lj / other.mass
            other.vy -= fy_lj / other.mass


    def try_join(self, other):
        if self.remaining_valence > 0 and other.remaining_valence > 0 and other not in self.connections and self.en > 0:
            dist = self.distance_to(other)
            if dist < JOIN_DISTANCE:
                self.connections.append(other)
                other.connections.append(self)
                self.remaining_valence -= 1
                other.remaining_valence -= 1
                self.en -= 50
                other.en -= 50
                if other.el > self.el:
                    other.z = 1
                    self.z = -1
                elif other.el < self.el:
                    other.z = -1
                    self.z =   1
                elif other.el == self.el:
                    other.z = 0
                    self.z = 0
    def try_join2(self, other):
        if self.remaining_valence >= 2 and other.remaining_valence >= 2 and other not in self.connections and self.en > 500:
            dist = self.distance_to(other)
            if dist < JOIN_DISTANCE:
                self.connections.append(other)
                other.connections.append(self)
                self.remaining_valence -= 2
                other.remaining_valence -= 2
                self.en -= 100
                other.en -= 100
                if other.el > self.el:
                    other.z = 1
                    self.z = -1
                elif other.el < self.el:
                    other.z = -1
                    self.z =   1
                elif other.el == self.el:
                    other.z = 0
                    self.z = 0


    def apply_spring_force(self):
        for other in self.connections:
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.hypot(dx, dy)
            if distance == 0:
                continue
            force = (distance - JOIN_DISTANCE) * SPRING_FORCE
            angle = math.atan2(dy, dx)
            fx = math.cos(angle) * force
            fy = math.sin(angle) * force
            self.vx += fx / self.mass
            self.vy += fy / self.mass
    def a(self):
        for other in self.con2:
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.hypot(dx, dy)
            if distance == 0:
                continue
            force = (distance - JOIN_DISTANCE) * SPRING_FORCE
            angle = math.atan2(dy, dx)
            fx = math.cos(angle) * force
            fy = math.sin(angle) * force
            self.vx += fx / self.mass
            self.vy += fy / self.mass

    def move(self):
        if self.en > 0 and self.t == 'a' and self.t2 == 0:
            self.en -= 1
            MAX_SPEED = 10  # или любое разумное значение
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > MAX_SPEED:
                scale = MAX_SPEED / speed
                self.vx *= scale
                self.vy *= scale
            self.x += self.vx
            self.y += self.vy

                # Столкновение с краями
            if self.x < -790 or self.x > 790:
                self.vx *= -1
            if self.y < -440 or self.y > 440:
                self.vy *= -1

            self.turtle.goto(self.x, self.y)
            self.update_label()
    def ph(self):
        if self.t2 == 1:
            f = self.mass * 10
            self.vy += f
            self.turtle.goto(self.x, self.y)
            self.update_label()

# Создаём атомы
atoms = [Atom(random.choice(list(ATOM_TYPES.keys()))) for _ in range(200)]
def bbb(self, other):
        global f
        for connected in other.connections[:]: 
            print("nnnnnnnn")
            other.connections.remove(connected)
            connected.connections.remove(other)
            other.remaining_valence += 1
            connected.remaining_valence += 1
            other.z = 0
            connected.z = 0
# Рисуем линии связей
bond_drawer = turtle.Turtle()
bond_drawer.hideturtle()
bond_drawer.color("gray")
bond_drawer.penup()

def draw_bonds():
    bond_drawer.clear()
    for atom in atoms:
        for other in atom.connections:
            if atom.x < other.x:  # рисуем связь только один раз
                bond_drawer.goto(atom.x, atom.y)
                bond_drawer.pendown()
                bond_drawer.goto(other.x, other.y)
                bond_drawer.penup()
b2 = turtle.Turtle()
b2.hideturtle()
b2.color("yellow")
b2.penup()

def d2():
    b2.clear()
    for atom in atoms:
        for other in atom.con2:
            if atom.x < other.x:  # рисуем связь только один раз
                b2.goto(atom.x, atom.y)
                b2.pendown()
                b2.goto(other.x, other.y)
                b2.penup()

def h(atoms):
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            a = atoms[i]
            b = atoms[j]
            dx = b.x - a.x
            dy = b.y - a.y
            distance = math.hypot(dx, dy)
            min_dist = a.radius + b.radius

            if distance < min_dist and distance != 0:
                # Сдвинем атомы, чтобы не пересекались
                b.en += 10
                a.en += 10
                # если противоположные заряды и энергии достаточно - разрыв
                if b.z == -1 and a.z == 1 and a.en > 500:
                    if a.el > b.el:
                        bbb(a,b)
                    elif a.el < b.el:
                        bbb(b,a)
                if b.z == 1 and a.z == -1 and b.en > 500:
                    if a.el > b.el:
                        bbb(a,b)
                    elif a.el < b.el:
                        bbb(b,a)
                if b.en > 0 and a.en > 0:
                    overlap = 0.5 * (min_dist - distance)
                    nx = dx / distance
                    ny = dy / distance

                    a.x -= nx * overlap
                    a.y -= ny * overlap
                    b.x += nx * overlap
                    b.y += ny * overlap

                    # Простое отражение скоростей
                    a.vx, b.vx = b.vx, a.vx
                    a.vy, b.vy = b.vy, a.vy
c2 = "H"
def set_atom_type_H():
    global c2
    c2 = 'H'

def set_atom_type_O():
    global c2
    c2 = 'O'

def set_atom_type_C():
    global c2
    c2 = 'C'
def set_atom_type_N():
    global c2
    c2 = 'N'

def dfh():
    for atom in atoms:
        atom.t = 'a'
def dfh2():
    for atom in atoms:
        atom.t = 'n'
def ener():
    for a in atoms:
        a.en = 400
def ener2():
    for a in atoms:
        a.en = 1000
def ddd3():
    for atom in atoms:
        atom.turtle.hideturtle()
        atom.label.clear()
    atoms.clear()
g = 0
def ddd4():
    global g
    g = 1
def ddd5():
    global g
    g = 0



# Привязка клавиш к смене типа
screen.onkey(set_atom_type_H, '1')
screen.onkey(set_atom_type_O, '2')
screen.onkey(set_atom_type_C, '3')
screen.onkey(set_atom_type_N, '4')
screen.onkey(dfh, "a")
screen.onkey(dfh2, "n")
screen.onkey(ener,"e")
screen.onkey(ener,"r")
screen.onkey(ddd3,"d")
screen.onkey(ddd4,"g")
screen.onkey(ddd5,"f")
screen.listen()

def create_atom_on_click(x, y):
        atom = Atom(c2)
        atom.x = x
        atom.y = y
        atom.turtle.goto(x, y)
        atom.update_label()
        atoms.append(atom)
        atom.t = "n"
        if g == 1:
            atom.t2 = 1

# Главный цикл
def update():
    # Попытки соединений
    for atom in atoms:
        for other in atoms:
            if atom != other:
                atom.ph()
                atom.ggg(other)
                atom.try_join2(other)
                atom.try_join(other)
    screen.onclick(create_atom_on_click)
    # Притяжение связей
    for atom in atoms:
        atom.a()
        atom.apply_spring_force()

    # Движение
    for atom in atoms:
        atom.move()
    h(atoms)
    # Рисуем связи
    draw_bonds()

    screen.ontimer(update, 40)
    screen.update()

update()
screen.mainloop()