import pygame
import sys
import json
import random
import copy

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Colors
GRASS_GREEN = (34, 139, 34)
SAND_YELLOW = (238, 214, 175)
BLUE_PLAINS = (135, 206, 250)
CORN_FIELD = (255, 223, 0)
DARK_BROWN = (101, 67, 33)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
PURPLE = (147, 112, 219)
GREEN = (34, 139, 34)

# Card class
class Card:
    def __init__(self, name, landscape, ability, cost):
        self.name = name
        self.landscape = landscape
        self.ability = ability
        self.cost = cost

class Creature(Card):
    def __init__(self, name, landscape, cost, attack, defense, ability=None):
        super().__init__(name, landscape, ability, cost)     
        self.attack = attack
        self.defense = defense

class Spell(Card):
    def __init__(self, name, landscape, ability, cost):
        super().__init__(name, landscape, ability, cost)

class Building(Card):
    def __init__(self, name, landscape, ability, cost):
        super().__init__(name, landscape, ability, cost)

class Landscape:
    def __init__(self, name):
        self.name = name

class Hero(Card):
    def __init__(self, name, ability):
        super().__init__(name, None, ability, None)

# Visual Card class for rendering
class VisualCard:
    def __init__(self, card_data, x, y, width=70, height=100):
        self.card = card_data  # The actual card object (Creature, Spell, etc.)
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.sprite = None  # For future sprite loading
        
    def draw(self, screen, font, small_font):
        # Card background
        if isinstance(self.card, Creature):
            color = (200, 100, 100)
        elif isinstance(self.card, Spell):
            color = (100, 100, 200)
        elif isinstance(self.card, Building):
            color = (150, 150, 150)
        elif isinstance(self.card, Landscape):
            color = GREEN
        else:
            color = WHITE
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Card name (truncated if too long)
        name = self.card.name[:12] + "..." if len(self.card.name) > 15 else self.card.name
        name_text = small_font.render(name, True, BLACK)
        screen.blit(name_text, (self.rect.x + 5, self.rect.y + 5))
        
        # Card stats for creatures
        if isinstance(self.card, Creature):
            stats = small_font.render(f"ATK: {self.card.attack}", True, BLACK)
            screen.blit(stats, (self.rect.x + 5, self.rect.y + 25))
            stats = small_font.render(f"DEF: {self.card.defense}", True, BLACK)
            screen.blit(stats, (self.rect.x + 5, self.rect.y + 40))
            
        # Card cost
        if hasattr(self.card, 'cost') and self.card.cost is not None:
            cost_text = font.render(str(self.card.cost), True, WHITE)
            pygame.draw.circle(screen, BLUE, (self.rect.right - 15, self.rect.y + 15), 12)
            screen.blit(cost_text, (self.rect.right - 20, self.rect.y + 5))
    
    def draw_on_map(self, screen, map_rect):
        """Draw sprite representation on the visual map"""
        if isinstance(self.card, Creature):
            # Draw creature sprite (placeholder - replace with actual sprites)
            sprite_rect = pygame.Rect(0, 0, 80, 80)
            sprite_rect.center = map_rect.center
            pygame.draw.circle(screen, (255, 100, 100), sprite_rect.center, 35)
            pygame.draw.circle(screen, BLACK, sprite_rect.center, 35, 3)
            
            # Draw ATK/DEF on sprite
            font = pygame.font.Font(None, 24)
            atk_text = font.render(str(self.card.attack), True, WHITE)
            def_text = font.render(str(self.card.defense), True, WHITE)
            screen.blit(atk_text, (sprite_rect.centerx - 20, sprite_rect.centery - 8))
            screen.blit(def_text, (sprite_rect.centerx + 5, sprite_rect.centery - 8))
            
        elif isinstance(self.card, Building):
            # Draw building sprite as a rectangle
            sprite_rect = pygame.Rect(0, 0, 70, 55)
            sprite_rect.center = map_rect.center
            
            # Main building structure
            pygame.draw.rect(screen, (140, 100, 70), sprite_rect)
            pygame.draw.rect(screen, BLACK, sprite_rect, 3)
            
            # Roof
            roof_points = [
                (sprite_rect.centerx, sprite_rect.y - 15),
                (sprite_rect.left - 5, sprite_rect.y),
                (sprite_rect.right + 5, sprite_rect.y)
            ]
            pygame.draw.polygon(screen, (100, 70, 50), roof_points)
            pygame.draw.polygon(screen, BLACK, roof_points, 2)
            
            # Windows
            window_size = 12
            pygame.draw.rect(screen, (200, 200, 100), 
                           (sprite_rect.x + 10, sprite_rect.y + 10, window_size, window_size))
            pygame.draw.rect(screen, (200, 200, 100), 
                           (sprite_rect.right - 22, sprite_rect.y + 10, window_size, window_size))
            
            # Door
            pygame.draw.rect(screen, (80, 50, 30), 
                           (sprite_rect.centerx - 8, sprite_rect.bottom - 20, 16, 20))
        
        elif isinstance(self.card, Landscape):
            # Draw landscape as textured background (optional)
            sprite_rect = pygame.Rect(0, 0, 80, 50)
            sprite_rect.center = map_rect.center
            
            # Different colors based on landscape type
            if "Blue" in self.card.name or "Plains" in self.card.name:
                color = BLUE_PLAINS
            elif "Sand" in self.card.name:
                color = SAND_YELLOW
            elif "Corn" in self.card.name:
                color = CORN_FIELD
            elif "Ice" in self.card.name or "Frozen" in self.card.name:
                color = (200, 230, 255)
            else:
                color = GRASS_GREEN
            
            pygame.draw.rect(screen, color, sprite_rect)
            pygame.draw.rect(screen, BLACK, sprite_rect, 2)
    
    def handle_drag(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:  # Left mouse button
            if not self.dragging and self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self.offset_x = self.rect.x - mouse_pos[0]
                self.offset_y = self.rect.y - mouse_pos[1]
            
            if self.dragging:
                self.rect.x = mouse_pos[0] + self.offset_x
                self.rect.y = mouse_pos[1] + self.offset_y
        else:
            self.dragging = False

class Lane:
    def __init__(self, x, y, width, height, color, lane_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.lane_number = lane_number
        
        # Card slot dimensions - reduced size
        self.slot_height = (height - 50) // 3
        self.slot_margin = 5
        
        # Three rows: Landscape, Building, Creature
        self.landscape_slot = pygame.Rect(x + 5, y + 30, width - 10, self.slot_height)
        self.building_slot = pygame.Rect(x + 5, y + 30 + self.slot_height + self.slot_margin, 
                                         width - 10, self.slot_height)
        self.creature_slot = pygame.Rect(x + 5, y + 30 + 2 * (self.slot_height + self.slot_margin), 
                                        width - 10, self.slot_height)
        
        # Card holders - store VisualCard objects
        self.landscape_card = None
        self.building_card = None
        self.creature_card = None
        
    def draw(self, screen, font, small_font):
        # Draw lane background
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        
        # Draw lane number
        lane_text = small_font.render(f"Lane {self.lane_number}", True, BLACK)
        lane_rect = lane_text.get_rect(center=(self.rect.centerx, self.rect.y + 15))
        screen.blit(lane_text, lane_rect)
        
        # Draw landscape slot
        pygame.draw.rect(screen, LIGHT_GRAY, self.landscape_slot)
        pygame.draw.rect(screen, BLACK, self.landscape_slot, 2)
        if not self.landscape_card:
            land_label = pygame.font.Font(None, 14).render("Landscape", True, BLACK)
            screen.blit(land_label, (self.landscape_slot.x + 3, self.landscape_slot.y + 3))
        
        # Draw building slot
        pygame.draw.rect(screen, LIGHT_GRAY, self.building_slot)
        pygame.draw.rect(screen, BLACK, self.building_slot, 2)
        if not self.building_card:
            build_label = pygame.font.Font(None, 14).render("Building", True, BLACK)
            screen.blit(build_label, (self.building_slot.x + 3, self.building_slot.y + 3))
        
        # Draw creature slot
        pygame.draw.rect(screen, LIGHT_GRAY, self.creature_slot)
        pygame.draw.rect(screen, BLACK, self.creature_slot, 2)
        if not self.creature_card:
            creature_label = pygame.font.Font(None, 14).render("Creature", True, BLACK)
            screen.blit(creature_label, (self.creature_slot.x + 3, self.creature_slot.y + 3))
        
        # Draw cards in slots (smaller)
        if self.landscape_card:
            self.landscape_card.rect.center = self.landscape_slot.center
            self.landscape_card.rect.width = 60
            self.landscape_card.rect.height = self.slot_height - 10
            self.landscape_card.draw(screen, font, small_font)
        if self.building_card:
            self.building_card.rect.center = self.building_slot.center
            self.building_card.rect.width = 60
            self.building_card.rect.height = self.slot_height - 10
            self.building_card.draw(screen, font, small_font)
        if self.creature_card:
            self.creature_card.rect.center = self.creature_slot.center
            self.creature_card.rect.width = 60
            self.creature_card.rect.height = self.slot_height - 10
            self.creature_card.draw(screen, font, small_font)
    
    def draw_visual_map(self, screen, font, small_font):
        """Draw a simplified visual representation of cards as sprites"""
        # Draw building sprite if present
        if self.building_card:
            self.building_card.draw_on_map(screen, self.map_building_rect)
        
        # Draw creature sprite if present
        if self.creature_card:
            self.creature_card.draw_on_map(screen, self.map_creature_rect)
    
    def can_place_card(self, card):
        """Check if a card can be placed in this lane"""
        if isinstance(card, Landscape):
            return self.landscape_card is None
        elif isinstance(card, Building):
            return self.building_card is None
        elif isinstance(card, Creature):
            return self.creature_card is None
        return False
    
    def place_card(self, visual_card):
        """Place a card in the appropriate slot"""
        if isinstance(visual_card.card, Landscape) and self.landscape_card is None:
            self.landscape_card = visual_card
            visual_card.rect.center = self.landscape_slot.center
            return True
        elif isinstance(visual_card.card, Building) and self.building_card is None:
            self.building_card = visual_card
            visual_card.rect.center = self.building_slot.center
            return True
        elif isinstance(visual_card.card, Creature) and self.creature_card is None:
            self.creature_card = visual_card
            visual_card.rect.center = self.creature_slot.center
            return True
        return False

class Board:
    def __init__(self):
        # Smaller play area so it fits on screen
        screen_play_area = SCREEN_HEIGHT - 480  # reduced from -300

        # Adjusted proportions
        opponent_lane_height = int(screen_play_area * 0.20)
        visual_map_height = int(screen_play_area * 0.35)
        player_lane_height = int(screen_play_area * 0.20)

        # Board position and size
        board_width = SCREEN_WIDTH - 400
        board_x = 200
        board_y = 275

        lane_spacing = 20
        lane_width = (board_width - 15 * lane_spacing) // 6

        # Colors for lanes
        lane_colors = [GRASS_GREEN, SAND_YELLOW, BLUE_PLAINS, CORN_FIELD]

        self.opponent_lanes = []
        self.player_lanes = []

        # Create opponent lanes
        for i in range(4):
            x = board_x + lane_spacing + (lane_width + lane_spacing) * i + 250
            y = board_y - 50
            lane = Lane(x, y, lane_width, opponent_lane_height, lane_colors[i], i + 1)
            self.opponent_lanes.append(lane)

        # Visual map (battle zone)
        self.visual_map_rect = pygame.Rect(
            board_x + 150,
            board_y + opponent_lane_height + 15,
            board_width - 300,
            visual_map_height - 30
        )

        # Create player lanes (below battle zone)
        for i in range(4):
            x = board_x + lane_spacing + (lane_width + lane_spacing) * i + 250
            y = board_y + opponent_lane_height + visual_map_height + 10
            lane = Lane(x, y, lane_width, player_lane_height, lane_colors[i], i + 1)
            self.player_lanes.append(lane)

    def draw(self, screen, font, small_font):
        # Opponent label
        opponent_label = font.render("OPPONENT", True, WHITE)
        screen.blit(opponent_label, (120, self.opponent_lanes[0].rect.y - 25))

        # Draw opponent lanes
        for lane in self.opponent_lanes:
            lane.draw(screen, font, small_font)

        # Battle zone
        pygame.draw.rect(screen, (40, 40, 40), self.visual_map_rect)
        pygame.draw.rect(screen, (100, 100, 100), self.visual_map_rect, 4)
        map_label = font.render("BATTLE ZONE", True, WHITE)
        screen.blit(map_label, (self.visual_map_rect.centerx - 70, self.visual_map_rect.y + 5))

        # Draw map content
        self.draw_visual_map(screen, font, small_font)

        # Player label
        player_label = font.render("PLAYER", True, WHITE)
        screen.blit(player_label, (120, self.player_lanes[0].rect.y - 25))

        # Draw player lanes
        for lane in self.player_lanes:
            lane.draw(screen, font, small_font)

    def draw_visual_map(self, screen, font, small_font):
        lane_width = self.visual_map_rect.width // 4
        row_height = self.visual_map_rect.height // 6

        # Grid lines
        for i in range(1, 6):
            y = self.visual_map_rect.y + i * row_height
            pygame.draw.line(screen, (80, 80, 80),
                             (self.visual_map_rect.x, y),
                             (self.visual_map_rect.right, y), 1)

        for i in range(1, 4):
            x = self.visual_map_rect.x + i * lane_width
            pygame.draw.line(screen, (80, 80, 80),
                             (x, self.visual_map_rect.y),
                             (x, self.visual_map_rect.bottom), 1)

        # Opponent cards
        for i, lane in enumerate(self.opponent_lanes):
            lane_x = self.visual_map_rect.x + i * lane_width
            landscape_area = pygame.Rect(lane_x + 5, self.visual_map_rect.y + 5,
                                         lane_width - 10, row_height - 10)
            building_area = pygame.Rect(lane_x + lane_width // 2 - 30,
                                        self.visual_map_rect.y + row_height + 5, 60, 45)
            creature_area = pygame.Rect(lane_x + lane_width // 2 - 40,
                                        self.visual_map_rect.y + 2 * row_height + 10, 80, 70)

            if lane.landscape_card:
                lane.landscape_card.draw_on_map(screen, landscape_area)
            if lane.building_card:
                lane.building_card.draw_on_map(screen, building_area)
            if lane.creature_card:
                lane.creature_card.draw_on_map(screen, creature_area)

        # Divider line
        center_y = self.visual_map_rect.y + 3 * row_height
        pygame.draw.line(screen, WHITE,
                         (self.visual_map_rect.x, center_y),
                         (self.visual_map_rect.right, center_y), 3)

        # Player cards
        for i, lane in enumerate(self.player_lanes):
            lane_x = self.visual_map_rect.x + i * lane_width
            creature_area = pygame.Rect(lane_x + lane_width // 2 - 40,
                                        self.visual_map_rect.y + 3 * row_height + 10, 80, 70)
            building_area = pygame.Rect(lane_x + lane_width // 2 - 30,
                                        self.visual_map_rect.y + 4 * row_height + 5, 60, 45)
            landscape_area = pygame.Rect(lane_x + 5,
                                         self.visual_map_rect.y + 5 * row_height + 5,
                                         lane_width - 10, row_height - 10)

            if lane.creature_card:
                lane.creature_card.draw_on_map(screen, creature_area)
            if lane.building_card:
                lane.building_card.draw_on_map(screen, building_area)
            if lane.landscape_card:
                lane.landscape_card.draw_on_map(screen, landscape_area)

    def get_lane_at_position(self, pos, is_player):
        lanes = self.player_lanes if is_player else self.opponent_lanes
        for lane in lanes:
            if lane.rect.collidepoint(pos):
                return lane
        return None

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 25
        self.actions = 2
        self.hand = []  # List of VisualCard objects
        
    def draw_card(self, card_data, hand_area_rect):
        """Add a card to the player's hand"""
        # Calculate position in hand
        card_spacing = 110
        x = hand_area_rect.x + 10 + len(self.hand) * card_spacing
        y = hand_area_rect.y + 10
        
        visual_card = VisualCard(card_data, x, y)
        self.hand.append(visual_card)
        return visual_card

class CardWarsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Card Wars - Adventure Time")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 48)
        
        self.board = Board()
        
        # Players
        self.player = Player("Finn")
        self.opponent = Player("Jake")
        
        # Hand area - adjusted for smaller board
        self.hand_rect = pygame.Rect(400, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 500, 150)
        
        # Game state
        self.dragged_card = None
        self.dragged_from_hand = False
        
        # Initialize with test cards (you'll load from your data.json)
        self.init_test_cards()
        
    def init_test_cards(self):
        """Initialize with some test cards - replace with your data loading"""
        # Create some test creatures
        test_creature1 = Creature("Corn Dog", "Cornfield", 2, 3, 2, "Test ability")
        test_creature2 = Creature("Sand Angel", "SandyLands", 3, 4, 3, "Test ability")
        test_landscape = Landscape("Blue Plains")
        
        # Add to player hand
        self.player.draw_card(test_creature1, self.hand_rect)
        self.player.draw_card(test_creature2, self.hand_rect)
        self.player.draw_card(test_landscape, self.hand_rect)
    
    def draw_ui(self):
        # Title
        title = self.title_font.render("CARD WARS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Player health (bottom left)
        player_hp = self.font.render(f"{self.player.name} HP: {self.player.health}", True, BLUE)
        self.screen.blit(player_hp, (40, SCREEN_HEIGHT - 240))
        
        # Player actions
        player_actions = self.font.render(f"Actions: {self.player.actions}", True, BLUE)
        self.screen.blit(player_actions, (40, SCREEN_HEIGHT - 215))
        
        # Opponent health (top left)
        opponent_hp = self.font.render(f"{self.opponent.name} HP: {self.opponent.health}", True, RED)
        self.screen.blit(opponent_hp, (40, 55))
        
        # Hand area
        pygame.draw.rect(self.screen, GRAY, self.hand_rect, 3)
        hand_label = self.font.render("Your Hand", True, WHITE)
        self.screen.blit(hand_label, (self.hand_rect.centerx - 50, self.hand_rect.y - 30))
        
        # Draw cards in hand
        for card in self.player.hand:
            if card != self.dragged_card:
                card.draw(self.screen, self.font, self.small_font)
        
        # Draw dragged card last (on top)
        if self.dragged_card:
            self.dragged_card.draw(self.screen, self.font, self.small_font)
    
    def handle_card_drag(self, event):
        """Handle card dragging and placement"""
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicking on a card in hand
            for card in self.player.hand:
                if card.rect.collidepoint(mouse_pos):
                    self.dragged_card = card
                    self.dragged_from_hand = True
                    card.offset_x = card.rect.x - mouse_pos[0]
                    card.offset_y = card.rect.y - mouse_pos[1]
                    break
        
        elif event.type == pygame.MOUSEMOTION and self.dragged_card:
            # Update dragged card position
            self.dragged_card.rect.x = mouse_pos[0] + self.dragged_card.offset_x
            self.dragged_card.rect.y = mouse_pos[1] + self.dragged_card.offset_y
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragged_card:
            # Try to place card on board
            placed = False
            lane = self.board.get_lane_at_position(mouse_pos, True)
            
            if lane and lane.can_place_card(self.dragged_card.card):
                if lane.place_card(self.dragged_card):
                    self.player.hand.remove(self.dragged_card)
                    self.player.actions -= 1
                    placed = True
            
            # Return to hand if not placed
            if not placed and self.dragged_from_hand:
                # Reposition in hand
                card_index = 0
                card_spacing = 110
                for i, card in enumerate(self.player.hand):
                    card.rect.x = self.hand_rect.x + 10 + i * card_spacing
                    card.rect.y = self.hand_rect.y + 10
            
            self.dragged_card = None
            self.dragged_from_hand = False
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        # Reset actions for testing
                        self.player.actions = 2
                
                # Handle card dragging
                self.handle_card_drag(event)
            
            # Clear screen
            self.screen.fill((20, 20, 20))
            
            # Draw everything
            self.board.draw(self.screen, self.font, self.small_font)
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = CardWarsGame()
    game.run()