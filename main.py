from typing import Optional
import arcade
import math
import arcade.gui

# Игровые константы:

GRAVITATION = 1.5

#
RIGHT_FACING = 0
LEFT_FACING = 1

#
PLAYER_SPEED_ON_GROUND = 5
PLAYER_JUMP_IMPULSE = 30

# Окно
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "GAME"

# Размерность
PLAYER_SPRITE_SCALE = 3
ENEMIES_SPRITE_SCALE = 2.5
TILES_SPRITE_SCALE = 2

# Названия слоев тайлов
WALL_LIST_TILED_NAME = "Collision"
BACKGROUND_1_TILED_NAME = "Background_layer_1"
BACKGROUND_2_TILED_NAME = "Background_layer_2"
BACKGROUND_3_TILED_NAME = "Background_layer_3"

# Пули
BULLET_DAMAGE = 25
SHOOT_SPEED = 10
BULLET_SPEED = 12


# Игрок
class Player(arcade.Sprite) :
    def __init__(self, folder_name, file_name) :  # Инициализация переменных
        super().__init__()

        self.scale = PLAYER_SPRITE_SCALE
        self.upd = 0

        main_src = f"tiles/Sprites/{folder_name}"

        # Текстуры когда перс стоит, прыгает и падает
        self.idle_player_textures = []
        for i in range(5) :
            texture = arcade.load_texture_pair(f"{main_src}/{file_name}_idle_{i}.png")
            self.idle_player_textures.append(texture)

        self.walk_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"{main_src}/{file_name}_walk_{i}.png")
            self.walk_textures.append(texture)

        self.jump_player_textures = arcade.load_texture_pair(f"{main_src}/jump.png")
        self.fall_player_textures = arcade.load_texture_pair(f"{main_src}/fall.png")

        self.texture = self.idle_player_textures[0][0]
        self.hit_box = self.texture.hit_box_points
        self.char_face_direction = RIGHT_FACING  # Направление взгляда персонажа
        self.current_texture = 0

    def update_animation(self, delta_time: float = 1 / 60) :

        # Куда будет смотреть персонаж при движении
        if self.change_x < 0 and self.char_face_direction == RIGHT_FACING :
            self.char_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.char_face_direction == LEFT_FACING :
            self.char_face_direction = RIGHT_FACING

        #
        if self.change_y > 0 :
            self.texture = self.jump_player_textures[self.char_face_direction]
            return
        elif self.change_y < 0 :
            self.texture = self.fall_player_textures[self.char_face_direction]
            return

        #
        if self.change_x == 0 :
            if self.upd == 3 :
                self.current_texture += 1
                if self.current_texture > 5 :
                    self.current_texture = 0
                self.texture = self.idle_player_textures[self.current_texture][self.char_face_direction]
                self.upd = 0
                return
            self.upd += 1

        #
        if self.upd == 3 :
            self.current_texture += 1
            if self.current_texture > 5 :
                self.current_texture = 0
            self.texture = self.walk_textures[self.current_texture][self.char_face_direction]
            self.upd = 0
            return
        self.upd += 1


# Враги
class CyclopsEnemy(arcade.Sprite) :
    def __init__(self) :
        super().__init__()

        self.scale = ENEMIES_SPRITE_SCALE
        self.hp = 125

        self.upd_walk = 0

        main_src = f"tiles/Sprites/Enemies/cyclops"

        self.idle_textures = []
        for i in range(5) :
            texture = arcade.load_texture_pair(f"{main_src}/cyclops_idle_{i}.png")
            self.idle_textures.append(texture)

        self.hit_textures = []
        texture = arcade.load_texture_pair(f"{main_src}/cyclops_hit_0.png")
        self.hit_textures.append(texture)
        texture = arcade.load_texture_pair(f"{main_src}/cyclops_hit_1.png")
        self.hit_textures.append(texture)

        self.walk_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"{main_src}/cyclops_walk_{i}.png")
            self.walk_textures.append(texture)

        self.death_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"tiles/Sprites/death_{i}.png")
            self.death_textures.append(texture)

        self.texture = self.idle_textures[0][0]
        self.hit_box = self.texture.hit_box_points
        self.char_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

    def update_animation(self, delta_time: float = 1 / 60) :

        if self.change_x < 0 and self.char_face_direction == LEFT_FACING :
            self.char_face_direction = RIGHT_FACING
        elif self.change_x > 0 and self.char_face_direction == RIGHT_FACING :
            self.char_face_direction = LEFT_FACING

        if self.change_x == 0 :
            if self.upd_walk == 3 :
                self.current_texture += 1
                if self.current_texture > 4 :
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture][self.char_face_direction]
                self.upd_walk = 0
                return
            self.upd_walk += 1

        if self.upd_walk == 3 :
            self.current_texture += 1
            if self.current_texture > 5 :
                self.current_texture = 0
            self.texture = self.walk_textures[self.current_texture][self.char_face_direction]
            self.upd_walk = 0
            return
        self.upd_walk += 1


class HornedMonsterEnemy(arcade.Sprite) :
    def __init__(self) :
        super().__init__()

        self.enemy_type = "horned_monster"
        self.hp = 75
        self.scale = ENEMIES_SPRITE_SCALE
        main_src = f"tiles/Sprites/Enemies/horned_monster"

        self.upd_walk = 0

        self.idle_textures = []
        for i in range(5) :
            texture = arcade.load_texture_pair(f"{main_src}/horned_monster_idle_{i}.png")
            self.idle_textures.append(texture)

        self.hit_textures = []
        texture = arcade.load_texture_pair(f"{main_src}/horned_monster_hit_0.png")
        self.hit_textures.append(texture)
        texture = arcade.load_texture_pair(f"{main_src}/horned_monster_hit_1.png")
        self.hit_textures.append(texture)

        self.walk_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"{main_src}/horned_monster_walk_{i}.png")
            self.walk_textures.append(texture)

        self.death_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"tiles/Sprites/death_{i}.png")
            self.death_textures.append(texture)

        self.texture = self.idle_textures[0][0]
        self.hit_box = self.texture.hit_box_points
        self.char_face_direction = RIGHT_FACING
        self.current_texture = 0

    def update_animation(self, delta_time: float = 1 / 60) :

        if self.change_x < 0 and self.char_face_direction == LEFT_FACING :
            self.char_face_direction = RIGHT_FACING
        elif self.change_x > 0 and self.char_face_direction == RIGHT_FACING :
            self.char_face_direction = LEFT_FACING

        if self.change_x == 0 :
            if self.upd_walk == 3 :
                self.current_texture += 1
                if self.current_texture > 4 :
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture][self.char_face_direction]
                self.upd_walk = 0
                return
            self.upd_walk += 1

        if self.upd_walk == 3 :
            self.current_texture += 1
            if self.current_texture > 5 :
                self.current_texture = 0
            self.texture = self.walk_textures[self.current_texture][self.char_face_direction]
            self.upd_walk = 0
            return
        self.upd_walk += 1


class BeeEnemy(arcade.Sprite) :
    def __init__(self) :
        super().__init__()

        self.enemy_type = "bee"
        self.hp = 50
        self.scale = ENEMIES_SPRITE_SCALE
        main_src = f"tiles/Sprites/Enemies/bee"

        self.upd_walk = 0

        self.idle_textures = []
        for i in range(4) :
            texture = arcade.load_texture_pair(f"{main_src}/bee_idle_{i}.png")
            self.idle_textures.append(texture)

        self.hit_textures = []
        texture = arcade.load_texture_pair(f"{main_src}/bee_hit_0.png")
        self.hit_textures.append(texture)
        texture = arcade.load_texture_pair(f"{main_src}/bee_hit_1.png")
        self.hit_textures.append(texture)

        self.walk_textures = []
        for i in range(4) :
            texture = arcade.load_texture_pair(f"{main_src}/bee_walk_{i}.png")
            self.walk_textures.append(texture)

        self.death_textures = []
        for i in range(6) :
            texture = arcade.load_texture_pair(f"tiles/Sprites/death_{i}.png")
            self.death_textures.append(texture)

        self.texture = self.idle_textures[0][0]
        self.hit_box = self.texture.hit_box_points
        self.char_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

    def update_animation(self, delta_time: float = 1 / 60) :

        if self.change_x < 0 and self.char_face_direction == LEFT_FACING :
            self.char_face_direction = RIGHT_FACING
        elif self.change_x > 0 and self.char_face_direction == RIGHT_FACING :
            self.char_face_direction = LEFT_FACING

        if self.change_x == 0 :
            if self.upd_walk == 3 :
                self.current_texture += 1
                if self.current_texture > 3 :
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture][self.char_face_direction]
                self.upd_walk = 0
                return
            self.upd_walk += 1

        if self.upd_walk == 3 :
            self.current_texture += 1
            if self.current_texture > 3 :
                self.current_texture = 0
            self.texture = self.walk_textures[self.current_texture][self.char_face_direction]
            self.upd_walk = 0
            return
        self.upd_walk += 1


class Menu(arcade.View) :
    def __init__(self) :
        super().__init__()

        self.button_active: bool = True

        self.manager = arcade.gui.UIManager()

        self.manager.enable()

        self.gui_box = arcade.gui.UIBoxLayout()

    def on_show(self) :
        arcade.set_background_color(arcade.color.WHITE)

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=180)

        self.gui_box.add(start_button.with_space_around(bottom=20))
        self.gui_box.add(quit_button)

        start_button.on_click = self.on_click_start
        quit_button.on_click = self.on_click_quit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.gui_box)
        )

    def on_click_start(self, event) :
        if self.button_active :
            game = Game()
            self.window.show_view(game)
            self.button_active = False
            print("start: ", event)
        else :
            pass

    def on_click_quit(self, event) :
        if self.button_active :
            arcade.close_window()
        else :
            pass

    def on_draw(self) :
        self.clear()
        self.manager.draw()


class Game(arcade.View) :

    def __init__(self) :
        super().__init__()

        self.camera = None

        self.player: Optional[Player] = None

        self.wall_list: Optional[arcade.SpriteList] = None
        self.background_layer_1: Optional[arcade.SpriteList] = None
        self.background_layer_2: Optional[arcade.SpriteList] = None
        self.background_layer_3: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None

        self.scene = None

        self.tile_map = None

        self.A_press: bool = False
        self.D_press: bool = False
        self.shoot_press: bool = False
        self.ability_shooting: bool = False
        self.shooting_timer = 0
        self.W_press: bool = False
        self.jump_reset: bool = False

        self.physics_engine: Optional[arcade.PhysicsEnginePlatformer] = None

    # Загрузка карты, и прочих спрайтов
    def setup(self) :

        self.camera = arcade.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)

        map_src = "tiled_map/Forest_MAP.tmj"

        layer_settings = {
            WALL_LIST_TILED_NAME : {"use_spatial_hash" : True}
        }

        self.tile_map = arcade.load_tilemap(map_src, TILES_SPRITE_SCALE, layer_settings)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.wall_list = self.tile_map.sprite_lists[WALL_LIST_TILED_NAME]
        self.background_layer_1 = self.tile_map.sprite_lists[BACKGROUND_1_TILED_NAME]
        self.background_layer_2 = self.tile_map.sprite_lists[BACKGROUND_2_TILED_NAME]
        self.background_layer_3 = self.tile_map.sprite_lists[BACKGROUND_3_TILED_NAME]

        self.bullet_list = arcade.SpriteList()

        self.ability_shooting = True
        self.shooting_timer = 0

        self.player = Player("Player", "player")
        self.player.center_x = 100
        self.player.center_y = 110
        self.scene.add_sprite("Player", self.player)

        enemies_list = self.tile_map.object_lists["Enemies"]

        for obj in enemies_list :
            cartesian_product = self.tile_map.get_cartesian(
                obj.shape[0], obj.shape[1]
            )

            enemy_type = obj.properties["enemy_type"]
            if enemy_type == "cyclops" :
                enemy = CyclopsEnemy()
            elif enemy_type == "horned_monster" :
                enemy = HornedMonsterEnemy()
            elif enemy_type == "bee" :
                enemy = BeeEnemy()

            enemy.center_x = math.floor(
                cartesian_product[0] * TILES_SPRITE_SCALE * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian_product[1] + 1) * (self.tile_map.tile_height * TILES_SPRITE_SCALE) + 9
            )

            if "left_border" in obj.properties :
                enemy.left_border = obj.properties["left_border"]
            if "right_border" in obj.properties :
                enemy.right_border = obj.properties["right_border"]
            if "change_x" in obj.properties :
                enemy.change_x = obj.properties["change_x"]

            if enemy_type == "horned_monster" :
                enemy.center_y -= 2

            if enemy_type == "bee" :
                enemy.center_y += 7

            self.scene.add_sprite("Enemies", enemy)

        self.scene.add_sprite_list("Bullets")

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITATION,
            walls=self.scene[WALL_LIST_TILED_NAME]
        )

        # Отрисовка слоев

    def on_draw(self) :
        arcade.start_render()

        self.background_layer_3.draw()
        self.background_layer_2.draw()
        self.background_layer_1.draw()
        self.wall_list.draw()
        self.scene.draw()
        self.camera.use()

    def keychange(self) :
        if self.W_press :
            if (
                    self.physics_engine.can_jump(y_distance=8)
                    and not self.jump_reset
            ) :
                self.player.change_y = PLAYER_JUMP_IMPULSE
                self.jump_reset = True

        if self.D_press and not self.A_press :
            self.player.change_x = PLAYER_SPEED_ON_GROUND
        elif self.A_press and not self.D_press :
            self.player.change_x = -PLAYER_SPEED_ON_GROUND
        else :
            self.player.change_x = 0

    def on_key_press(self, key, modifiers) :
        if key == arcade.key.W :
            self.W_press = True
        elif key == arcade.key.A :
            self.A_press = True
        elif key == arcade.key.D :
            self.D_press = True
        elif key == arcade.key.L :
            self.shoot_press = True

        self.keychange()

    def on_key_release(self, key, modifiers) :
        if key == arcade.key.W :
            self.W_press = False
            self.jump_reset = False
        elif key == arcade.key.A :
            self.A_press = False
        elif key == arcade.key.D :
            self.D_press = False
        elif key == arcade.key.L :
            self.shoot_press = False

        self.keychange()

    def camera_player(self) :
        camera_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        camera_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if camera_center_x < 0 :
            camera_center_x = 0
        if camera_center_y < 0 :
            camera_center_y = 0

        tracking_object = camera_center_x, camera_center_y
        self.camera.move_to(tracking_object)

    def on_update(self, delta_time) :

        self.physics_engine.update()

        if self.physics_engine.can_jump() :
            self.player.can_jump = False
        else :
            self.player.can_jump = True

        bullet_right_face_image = "tiles/Sprites/Player/fireball.png"
        bullet_left_face_image = "tiles/Sprites/Player/fireball_1.png"

        if self.ability_shooting :
            if self.shoot_press :
                bullet = arcade.Sprite(bullet_right_face_image, 0.2)

                if self.player.char_face_direction == RIGHT_FACING :
                    bullet.change_x = BULLET_SPEED
                if self.player.char_face_direction == LEFT_FACING :
                    bullet = arcade.Sprite(bullet_left_face_image, 0.2)
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.player.center_x
                bullet.center_y = self.player.center_y

                self.scene.add_sprite("Bullets", bullet)
                self.ability_shooting = False
        else :
            self.shooting_timer += 1
            if self.shooting_timer == SHOOT_SPEED :
                self.ability_shooting = True
                self.shooting_timer = 0

        self.scene.update_animation(delta_time, ["Enemies", "Player"])
        self.scene.update(["Enemies", "Bullets"])

        for enemy in self.scene["Enemies"] :
            if (
                    enemy.right_border
                    and enemy.right > enemy.right_border
                    and enemy.change_x > 0
            ) :
                enemy.change_x *= -1

            if (
                    enemy.left_border
                    and enemy.left < enemy.left_border
                    and enemy.change_x < 0
            ) :
                enemy.change_x *= -1

        for bullet in self.scene["Bullets"] :
            bullet_collision_list = arcade.check_for_collision_with_lists(bullet, [self.scene["Enemies"],
                                                                                   self.scene["Collision"]])
            if bullet_collision_list :
                bullet.remove_from_sprite_lists()

                for collision in bullet_collision_list :
                    if (
                            self.scene["Enemies"]
                            in collision.sprite_lists
                    ) :
                        collision.hp -= BULLET_DAMAGE
                        if collision.hp <= 0 :
                            collision.remove_from_sprite_lists()
                return
            if (bullet.right < 0) or (
                    bullet.left
                    > (self.tile_map.width * self.tile_map.tile_width) * TILES_SPRITE_SCALE
            ) :
                bullet.remove_from_sprite_lists()

        collision_with_enemies = arcade.check_for_collision_with_list(self.player, self.scene["Enemies"])

        for collision in collision_with_enemies :
            if self.scene["Enemies"] in collision.sprite_lists :
                self.setup()
                return

        self.camera_player()


# Запуск
def main() :
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu = Menu()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__" :
    main()
