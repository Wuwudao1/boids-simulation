import pygame
import random
import math

# ……开始了。别眨眼。
pygame.init()
WIDTH, HEIGHT = 800, 600  # 画布大小，别太小，鸟儿飞不开
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 配置参数，太多就乱，太少就寂寞
NUM_BOIDS = 30           # 鸟的数量，别太贪心
MAX_SPEED = 4            # 飞行速度上线，不能太疯
NEIGHBOR_DIST = 50       # 感知范围，太远就冷漠，太近就窒息

class Boid:
    def __init__(self):
        # 随机出生在世界的某个角落
        self.position = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        # 随机朝向，像刚睡醒的鸟
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def update(self, boids):
        # 看看周围，做出反应
        self.flock(boids)
        # 移动自己
        self.position += self.velocity
        # 世界是圆的，飞出去就从另一边回来
        self.borders()

    def flock(self, boids):
        alignment = pygame.Vector2()   # 跟大家朝同一个方向走
        cohesion = pygame.Vector2()    # 往大家中间靠
        separation = pygame.Vector2()  # 离别人远一点，别贴太近

        total = 0
        for other in boids:
            if other is self:
                continue  # 不看自己，当然

            distance = self.position.distance_to(other.position)
            if distance < NEIGHBOR_DIST:
                alignment += other.velocity     # 对齐：看大家怎么飞
                cohesion += other.position      # 凝聚：靠拢
                diff = self.position - other.position
                if distance > 0:
                    separation += diff / distance  # 分离：远离别人
                total += 1

        if total > 0:
            # 方向一致性：和大家速度方向靠拢
            alignment = (alignment / total).normalize() * MAX_SPEED - self.velocity
            # 凝聚力：靠近中心点
            cohesion = ((cohesion / total) - self.position).normalize() * MAX_SPEED - self.velocity
            # 分离：远离人群中心
            separation = (separation / total).normalize() * MAX_SPEED - self.velocity

            # 混合三种力，比例可以调，像调情绪一样
            self.velocity += alignment * 0.05 + cohesion * 0.01 + separation * 0.1

        # 保持速度上线，别太躁
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * MAX_SPEED

    def borders(self):
        # 环世界逻辑，出界就从另一边回来
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = HEIGHT
        if self.position.y > HEIGHT: self.position.y = 0

    def draw(self):
        # 别太花里胡哨，白点就够了
        pygame.draw.circle(screen, (255, 255, 255), self.position, 3)

# 生成一群孤独又同步的个体
boids = [Boid() for _ in range(NUM_BOIDS)]

# 主循环，像心跳一样，一次都不能少
running = True
while running:
    screen.fill((0, 0, 0))  # 黑夜，是最好的背景
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 你说结束，我就停

    for boid in boids:
        boid.update(boids)
        boid.draw()

    pygame.display.flip()  # 更新画面
    clock.tick(60)         # 一秒60帧，刚刚好

pygame.quit()  # 就这样，别回头
