import random
import json

class Pokemon:
    def __init__(self, species, moveset):
        self.level = 50
        self.name = species["name"]
        self.stats = species["stats"]
        self.type1 = species["type1"]
        self.type2 = species["type2"]
        self.moveset = moveset
        self.alive = True
        self.stats["hp"] = int((2 * self.stats["hp"] / 100) + self.level +10)
    
    def receive(self, move, atk_pokemon):
        print(atk_pokemon.name + " used " + move["name"])
        if move["type"] == atk_pokemon.type1 or move["type"] == atk_pokemon.type2:
            stab = 1.5
        else:
            stab = 1
        crit = 1
        damage = ((atk_pokemon.level*2/5 + 2) * move["damage"] + 2) * crit * stab * random.randint(85,101)
        if move["type"] in effectiveness[self.type1]["weakness"]:
            damage = move["damage"] * 2
            print("It is super effective")
        if move["type"] in effectiveness[self.type1]["resistance"]:
            damage = move["damage"] / 2
            print("it wasn't effective")
        try: 
            if move["type"] in effectiveness[self.type1]["immunity"]:
                damage = 0
                print("it doesn't affect " + self.name + "...")
        except:
            pass

        if self.type2 != None:
            if move["type"] in effectiveness[self.type2]["weakness"]:
                damage = move["damage"] * 2  
                print("It is super effective")
            if move["type"] in effectiveness[self.type2]["resistance"]:
                damage = move["damage"] / 2
                print("it wasn't effective")
            try :
                if move["type"] in effectiveness[self.type2]["immunity"]:
                    damage = 0
                    print("it doesn't affect " + self.name + "...")
            except :
                pass

        self.stats["hp"] -= int(damage)
        if self.stats["hp"] <= 0:
            print("Your " + self.name + " has fainted")
            self.alive = False
        else:
            print(self.name + " hp : " , self.stats["hp"])

class Player:
    def __init__(self, name, pokemon):
        self.name = name
        self.alive = pokemon
        self.active = pokemon[0]

    def change_pokemon(self,new_active):
        self.active = self.alive[new_active]


def choose_move(pokemon):
    num = 0
    for x in pokemon.moveset:
        print(num, " : " + x["name"])
        num += 1
    return int(input("Choose a move(number): "))

def check_alive(first, second, first_move, second_move):
    second.active.receive(first.active.moveset[first_move], first.active)
    if second.active.alive:
        first.active.receive(second.active.moveset[second_move], second.active)
    #Pokemon died
    else:
        second.alive.remove(second.active)
        if second.alive == []:
            print(second.name + " loses")
            return False
        else: 
            num = 0
            for x in second.alive:
                print(num, " : " + x.name)
                new_pokemon = int(input("Choose a new pokemon(num): "))
                second.change_pokemon(new_pokemon)
            return True

if __name__ == "__main__" :
    with open("effectiveness.json", "r") as e, open("pokedex.json", "r") as p, open("moves.json", "r") as m:
        pokedex = json.load(p)
        moves = json.load(m)
        effectiveness = json.load(e)
        print("-----Pokemon Battle-----\n\n\n")
        game = True
        pikachu = Pokemon(pokedex["Pikachu"], [moves["quickattack"],moves["thunderbolt"]])
        charmander = Pokemon(pokedex["Charmander"],[moves["flamethrower"],moves["ember"]])
        bulbasaur = Pokemon(pokedex["Bulbasaur"],[moves["razorleaf"]])
        player1 = Player("Player 1", [pikachu])
        player2 = Player("Player 2", [charmander,bulbasaur])
        while game == True:
            print(player1.active.name + "   HP : " , player1.active.stats["hp"] , "\n\nvs\n\n" + player2.active.name + "   HP : " , player2.active.stats["hp"] , "\n")
            
            #Player 1 chooses Move
            play1 = choose_move(player1.active)
            #Player 2 Chooses Move
            play2 = choose_move(player2.active)
            #Faster Pokemon does Move
            if player1.active.stats["spd"] > player2.active.stats["spd"]:
                game = check_alive(player1, player2, play1, play2)
            else :
                game = check_alive(player2,player1,play2,play1)
            # IF pokemon fainted change Pokemon
            #Other Pokemon does move 
        



