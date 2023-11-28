import game.location as location
import game.config as config
from game.display import announce
from game.events import *
from game.items import items
import random
#import nympy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class LizIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "My_Island"
        self.symbol = "I"
        self.visitable = True #Sets to true so the pirates can visit the island and enables sublocations
        self.starting_location = BeachWithShip(self)
        self.locations = {}
        self.locations["SouthBeach"] = self.starting_location
        self.locations["WestBeach"] = WestBeach(self)
        self.locations["HillWithSign"] = Signpost(self)
        self.locations["ForestEdge"] = ForestEdge(self)
        self.locations["EastBeach"] = EastBeach(self)
        self.locations["Cliff"] = Cliff(self)
        self.locations["RuinedCastle"] = RuinedCastle(self)
        self.locations["ForestMaze"] = ForestMaze(self)
        self.locations["Mountain"] = Mountain(self)
        self.locations["Cave"] = Cave(self)
    
    def enter(self, ship):
        announce("You arrive at an island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class BeachWithShip(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "SouthBeach"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["HillWithSign"]
            config.the_player.go = True
        if (verb == "south"):
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["WestBeach"]
            config.the_player.go = True
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["EastBeach"]
            config.the_player.go = True
    
    def enter(self):
        announce("You head ashore. There is a hill with a signpost to the north.")
        announce("There are two other beaches to the East and West that you can see.")

class Signpost(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "HillWithSign"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["northeast"] = self
        self.verbs["northwest"] = self
        self.verbs["investigate"] = self

        self.signUsed = False
        self.RIDDLE_AMOUNT = 3

    def enter(self):
        announce("You walk to the top of the hill. A crude and weathered signpost sits before you. You can investigate the sign further")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["ForestEdge"]
            config.the_player.go = True
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["SouthBeach"]
            config.the_player.go = True
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["WestBeach"]
            config.the_player.go = True
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["EastBeach"]
            config.the_player.go = True
        if (verb == "northeast"):
            config.the_player.next_loc = self.main_location.locations["Cliff"]
            config.the_player.go = True
        if (verb == "northwest"):
            config.the_player.next_loc = self.main_location.locations["RuinedCastle"]
            config.the_player.go = True
        if (verb == "investigate"):
            self.HandleSignpost()
        
    def HandleSignpost(self):
        if(not self.signUsed):
            announce("You investigate the signpost and see some faded text, pointing in different directions.")
            choice = input("Do you wish to solve the riddles to decipher the faded text?")
            if ("yes" in choice.lower()):
                self.HandleRiddles()
            else:
                announce("You turn away from the Signpost.")
        else:
            announce("There is treasure beyond the forest in the mountain caves to the North, an old castle to the northwest, a cliff to the northeast, and fishing spots are at the East and West Beaches.")

    def HandleRiddles(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = self.RIDDLE_AMOUNT

        while(guesses > 0):
            print(riddle[0])
            plural = ""
            if(guesses != 1):
                plural = "s"
            
            print(f"You have {guesses} left")
            choice = input("What is your guess?")

            if (riddle[1] in choice.lower()):
                self.RiddleReward()
                announce("You have guessed correctly! The sign tells you there is a mountain cave to the north of the forest with treasure, an old castle to the northwest, and a cliff to the northeast, and fishing spots on the East and West Beaches.")
                guesses = 0
            else:
                guesses -= 1
                announce("You have guessed incorrectly")
        if (guesses <= 0):
            self.signUsed = True

    def RiddleReward(self):
        for i in config.the_player.get_pirates():
            announce(f"{i} is inspired!")
            i.health = i.max_health
        self.shrineUsed = True

    def GetRiddleAndAnswer(self):
        riddleList = [("Under a full moon, I throw a yellow hat into the sea. What happens to the yellow hat?", "wet"),
                      ("They come out at night without being called, and are lost in the day without being stolen. What are they?", "stars"),
                      ("I welcome the day with a show of light, I stealthily came here in the night. I bathe the earthly world at dawn, but by noon, alas I'm gone. What am I?", "morning dew"),
                      ("It has keys, but no locks. It has space, but no room. You can enter, but can't go inside. What is it?", "keyboard"),
                      ("Where is the only place where today comes before yesterday?", "dictionary")]
        return random.choice(riddleList)
    
class WestBeach(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "WestBeach"
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["north"] = self
        self.verbs["fish"] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())
    
    def enter(self):
        announce("You have reached the Western Beach. There is a fishing spot here.")
        announce("You can also see the ruins of a castle to the north and a hill with a signpost to the east")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'fish'):
            self.HandleFish()
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["SouthBeach"]
            config.the_player.go = True
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations["HillWithSign"]
            config.the_player.go = True
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations["RuinedCastle"]
            config.the_player.go = True

    def HandleFish(self):
        announce("You've decided to fish! You take out your fishing rod and start fishing.")
        pass
        
        """
        1/10 large fish (15-30 food)
        1/10 shark (random pirate gets hurt)
        8/10 normal fish (1-5 food)
        """


class EastBeach(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "EastBeach"
        self.verbs = ["south"]
        self.verbs = ["west"]
        self.verbs = ["north"]
        self.verbs = ["fish"]

        self.rope_ladder = False

        self.event_chance = 25
        self.events.append(seagull.Seagull())
    
    def enter(self):
        announce("You have reached the Eastern Beach. There is a fishing spot here.")
        announce("You can see an unpassable cliff face to the north. There is a glittering object at the top of the cliff.")
        announce("You can also see a hill with a signpos to the west")

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["SouthBeach"]
            config.the_player.go = True
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Signpost"]
            config.the_player.go = True
        if (verb == "north"):
            #check if rope_ladder is true
            if (self.rope_ladder == True):
                config.the_player.next_loc = self.main_location.locations["Cliff"]
                config.the_player.go = True
            else:
                announce("You cannot climb the cliff yet.")
        if (verb == "fish"):
            self.HandleFish()

    def HandleFish(self): #REPEAT CODE! USE AS A MODULE IMPORT
        announce("You've decided to fish! You take out your fishing rod and start fishing.")
        pass
        
        """
        1/10 large fish (15-30 food)
        1/10 shark (random pirate gets hurt)
        8/10 normal fish (1-5 food)
        """


class ForestEdge(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "ForestEdge"
        self.verbs = ["south"]
        self.verbs = ["east"]
        self.verbs = ["west"]
        self.verbs = ["north"]
        self.verbs = ["investigate"]
    
    def enter(self):
        announce("You see a forest surrounded by a thick hedge in front of you.")
        announce("There is a sign next to an open gate in the hedge. Do you wish to investigate it?")

class ForestMaze(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "ForestMaze"
        self.verbs = ["forward"]
        self.verbs = ["south"]
        self.verbs = ["left"]
        self.verbs = ["right"]
    
    def enter(self):
        announce("You have entered the maze. You may continue forward or return south to exit the maze.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["ForestEdge"]
            config.the_player.go = True
        if (verb == "forward"):
            self.HandleMaze()

    def HandleMaze(self):
        announce("You see 3 paths ahead of you. One to the left, one forward, and one to the right.")
        announce("If you head south, you leave the maze.")
        choice = input("Where do you want to go? ")
        if ("left" in choice.lower()):
            self.HandleMazeChance()
        if ("right" in choice.lower()):
            self.HandleMazeChance()
        if ("forward" in choice.lower()):
            self.HandleMazeChance()
        if ("south" in choice.lower()):
            config.the_player.next_loc = self.main_location.locations["ForestEdge"]
            config.the_player.go = True

    def HandleMazeChance(self):
        chance = random.randint(1, 11)
        if (chance == 1):
            self.event_chance = 100
            self.events.append(GiantLizardEvent())
        elif (chance == 10):
            self.event_chance = 50
            self.events.append(sickness.Sickness())
        else:
            self.event_chance = 10
            self.events.append(seagull.Seagull())

class GiantLizardEvent(event.Event):
    def __init__(self):
        self.name = "Giant Lizard's Attack"
    
    def process(self, world):
        result = {}
        lizard = GiantLizard()
        announce("A Giant Lizard hops down from the hedge and attacks your crew!")
        combat.Combat([lizard]).combat()
        announce("The lizard lets out a death rattle, then falls limp.")
        result["newevents"] = []
        result["message"] = ""

        treasure = random.randint(1,6)
        treasures = ['sabre', 'pistol', 'food', 'club', 'coins']
        for treasure in treasures:
            item = treasure
        
        announce("The Lizard was protecting an item. It looks like it would make a great weapon")
        if (item == 'sabre'):
            config.the_player.add_to_inventory([Sabre()])
        if (item == 'pistol'):
            config.the_player.add_to_inventory([Pistol()])
        if (item == 'food'):
            self.food = 25
        if (item == 'club'):
            config.the_player.add_to_inventory([LizardTail()])
        if (item == 'coins'):
            config.the_player.add_to_inventory([CoinPile()])


class GiantLizard(Monster):
    def __init__(self):
        # Giant Lizard has 7-20 hp, with 3 attacks and 100-125 speed

        attacks = {}
        attacks["bite"] = ["bites", random.randrange(50, 80), (5, 15)]
        attacks["swipe"] = ["swipes", random.randrange(60, 90), (5, 15)]
        attacks["poison"] = ["poison", random.randrange(10, 15), (5, 15)]    
        super().__init__("Giant Lizard", random.range(7, 21), attacks, 100 + random.randint(0, 26))

class Sabre(items):
    def __init__(self):
        super().__init__("sabre", 15)
        self.damage(15, 80)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class LizardTail(items):
    def __init__(self):
        super().__init__("Lizard Club", 550)
        self.damage(20, 50)
        self.skill = "melee"
        self.verb = "bash"
        self.verb2 = "bashes"

class Pistol(items):
    def __init__(self):
        super().__init__("pistol", 500)
        self.damage(20, 150)
        self.firearm = True
        self.charges = 6
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"

class CoinPile(items):
    def __init__(self):
        super().__init__("coins", 6000)

class Cliff(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Cliff"
        self.verbs = ["west"]
        self.verbs = ["southwest"]
        self.verbs = ["investigate"]
        self.verbs = ["rope"]
        self.ladder = False
        self.verbs = ["descend"]
        #self.verbs = ["grab"]

    def enter(self):
        announce("You see a cliff's edge in front of you. There is a beach to the south that you could use a rope to descend to." +
                 "You also see the edge of a forest to the west and a hill with a signpost to the southwest" + 
                 "There is a slight reflection of something in the debris by the edge.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations("ForestEdge")
            config.the_player.go = True
        if (verb == "southwest"):
            config.the_player.next_loc = self.main_location.locations("Signpost")
            config.the_player.go = True
        if (verb == "rope"):
            self.RopeEvent()
        if (verb == "investigate"):
            self.HandleCliff()
        if (verb == "descend"):
            config.the_player.next_loc = self.main_location.locations("EastBeach")
            config.the_player.go = True

    def RopeEvent(self):
        if (not self.ladder):
            print("You have decided to use a rope to climb down to the Eastern Beach. This rope may be used as a shortcut to the top of the cliff in the future.")
            choice = input("Do you wish to continue?")
            if ("yes" in choice.lower()):
                self.HandleRope()
            else:
                print("You turn away from the cliff's edge.")

        else:
            print("You see a rope tied off in front of you. You can descend the cliff from here.")

    def HandleRope(self):
        choice = input("Do you wish to make a rope ladder.")
        if ("yes" in choice.lower()):
            self.event_chance = 25
            self.events.append(seagull.Seagull())
            announce("You have made a rope ladder, and you can now safely climb the cliff.")
            return self.rope_ladder == True
        
        else:
            self.event_chance = 100
            self.events.append(seagull.Seagull())
            announce("Once the seagulls are dealt with, you look up and see more seagulls flying around your group. They seem to be watching you.")
            splat = random.randint(1, 100)
            if (splat % 2 == 0):
                announce("You decide to descend too quickly, causing one of your pirates to slip and fall to their death.")
                c = random.choice(config.the_player.get_pirates())
                #check for health of pirate
                if (c.inflict_damage (self, "Slipped on the rope")):
                    self.result["message"] = ".. " + c.get_name() + " fell to their death!"

                #add in code for a pirate's death
            else:
                announce("Your crew has made it safely down, but the rope is too slippery to return the way you came safely.")

    def HandleCliff(self):
        announce("You decide to investigate the debris.\nUpon closer inspection, the debris looks to be old nesting material for the seagulls, as well as a few shiny baubles" +
                 "There also seems to be fresh food among the debris.")
        self.event_chance = 10
        self.events.append(seagull.Seagull())
        choice = input("Do you wish to investigate further?")
        if ("yes" in choice.lower()):
            announce("You decide to look closer at the debris.")
            self.event_chance = 60
            self.events.append(seagull.Seagull())
            announce("Upon closer inspection, you see an overflowing pouch of gold coins, a statuette of a dragon, and some food.")
            choice2 = input("What to you wish to grab?")
            if ("coins" in choice2.lower()):
                self.events_chance = 100
                self.events.append(seagull.Seagull())
                config.the_player.add_to_inventory([CoinPile()])
            if ("statuette" in choice2.lower()):
                self.events_chance = 90
                self.events.append(GiantLizardEvent())
                config.the_player.add_to_inventory([Statuette()])
            if ("food" in choice2.lower()):
                self.food = 100
                config.the_player.add_to_inventory([Pizza()])
            
class RopeLadder(items):
    def __init__(self):
        super().__init__("rope ladder", 5)

class Statuette(items):
    def __init__(self):
        super().__init__("Dragon Statuette", 15000)

class Pizza(items):
    def __init__(self):
        super().__init__("pizza", 0)

class Taco(items):
    def __init__(self):
        super().__init__("taco", 0)

class RuinedCastle(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "RuinedCastle"
        self.verbs["investigate"] = self
        self.verbs["south"] = self
        self.verbs["southeast"] = self
        self.verbs["east"] = self
        self.verbs["enter"] = self

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "investigate"):
            self.HandleCastleDoor()
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["WestBeach"]
            config.the_player.go = True
        if (verb == "southeast"):
            config.the_player.next_loc = self.main_location.locations["HillWithSign"]
            config.the_player.go = True
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["ForestEdge"]
            config.the_player.go = True
        if (verb == "enter"):
            announce("Castle Puzzle Here")
            #self.HandleCastlePuzzle()
    
    def enter(self):
        announce("You arrive at the ruins of a castle. There is a hill with a signpost to the southeast and the edge of a forest to the east.")
        announce("The doors of the ruined castle are flung open. You can enter the room beyond the door or investigate the door.")

    def HandleCastleDoor(self):
        announce("The large oaken doors look as if they had been ripped off their hinges. There is also scorch marks and large gouges on the door")
        choice = input("Do you wish to take a closer look?")
        if ("yes" in choice.lower()):
            announce("The gouges look like claw marks, and there are scales scattered around the doorway. There is also a note on the ground.")
            choice2 = input("Do you wish to read the note?")
            if ("yes" in choice2.lower()):
                print("Want to appease the God of the Island? I'll be waiting on the Mountain. -- Simon")
            else:
                announce("You turn away from the note.")
        else:
            announce("You turn away from the door.")

    def HandleCastlePuzzle(self):
        #Tower of Hanoi Puzzle, prize is a cake
        pass

class Mountain(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Mountain"
        self.verbs["speak"] = self
        self.verbs["south"] = self
        self.verbs["north"] = self

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "speak"):
            self.HandleSimon()
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["ForestEdge"]
            config.the_player.go = True
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Cave"]
            config.the_player.go = True
    
    def enter(self):
        announce("You arrive at the mountain. There is a path winding up the mountain to a cave in the north. You can return to the Forest Edge to the south")
        announce("You also see a tent with brightly colored flags waving in the breeze. There is a man next to the tent, "+ 
                 "dressed in bright colors, as if to stand out among the rocks along the path. He calls out to you, requesting to speak with you.")
    
    def HandleSimon(self):
        pass

class Cave(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Cave"
        self.verbs["investigate"] = self
        self.verbs["south"] = self

        self.event_chance = 25
        self.events.append(GiantLizardEvent())

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "investigate"):
            self.HandleCavePuzzle()
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Mountain"]
            config.the_player.go = True
    
    def enter(self):
        announce("You finally arrive at the Cave. You see it is blocked off by a shrine. There is a sign next to the shrine that you can investigate."+
                 "\nYou may go back down the mountain path to the south.")
        
    def HandleCavePuzzle(self):
        pass