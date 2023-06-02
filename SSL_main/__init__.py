import random

from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'Main'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_DRAWS = 4
    ADD_INFO_DRAWS = 1
    BONUS = 100
    MAJ_NUM = 60

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    #random variables generated for player
    jarFacing = models.IntegerField() #whether participant faces orange majority jar (0) or purple majority (1)
    costToChange = models.IntegerField() #(hidden) cost to using second answer
    firstDraws = models.StringField() #string encoding 0/1 sequence of orange and purple marbles drawn
    addDraw = models.StringField() #0/1 string encoding whether orange or purple marble drawn

    #choices made by participant
    firstGuess = models.IntegerField(
        choices=[
            [0,'ORANGE'],
            [1,'PURPLE'],
        ],
        widget=widgets.RadioSelect
    )
    wtp = models.IntegerField(min=0, max=C.BONUS)
    secondGuess = models.IntegerField(
        choices=[
            [0,'ORANGE'],
            [1,'PURPLE'],
        ],
        widget=widgets.RadioSelect
    )
    confidence = models.IntegerField(min=0,max=100)

# FUNCTIONS

## if we wanted to initialize some random values, could do here, though probably easier to wait until they're needed
def creating_session(subsession: Subsession):
    import itertools

    #establish the following random variables for participant:
    # 1. which jar
    # 2. cost to having second answer be used as final guess
    # 3. first 4 draws (including in which order!)
    # 4. additional draw
    for p in subsession.get_players():
        p.jarFacing = random.choice([0,1]) #will use convention that 0 = orange and 1 = purple
        p.costToChange = random.randint(1,C.BONUS)
        if p.jarFacing == 0:
            p.firstDraws = ''.join(random.choices(['0','1'],weights=[C.MAJ_NUM,100-C.MAJ_NUM],k = C.NUM_DRAWS))
            p.addDraw = str(random.choice(list(itertools.chain(itertools.repeat(0,C.MAJ_NUM),itertools.repeat(1,100-C.MAJ_NUM)))))
        elif p.jarFacing == 1:
            p.firstDraws = ''.join(random.choices(['0', '1'], weights=[C.MAJ_NUM, 100 - C.MAJ_NUM], k=C.NUM_DRAWS))
            p.addDraw = str(random.choice(
                list(itertools.chain(itertools.repeat(0, 100 - C.MAJ_NUM), itertools.repeat(1, C.MAJ_NUM)))))

# PAGES
class Draws(Page):
    #take in the result of the draws, display the appropriate gif of the four draws
    timeout_seconds = 6

class FirstGuess(Page):
    #repeat the result in text form, solicit first guess about which jar
    form_model = 'player'
    form_fields = ['firstGuess']

    @staticmethod
    def vars_for_template(player: Player):
        drawsAsInt = int(player.firstDraws[0])+int(player.firstDraws[1])+int(player.firstDraws[2])+int(player.firstDraws[3])
        return dict(numOrangeDraws=C.NUM_DRAWS - drawsAsInt, numPurpleDraws=drawsAsInt)

class WTPElicit(Page):
    #elicit wtp to be use second guess
    form_model = 'player'
    form_fields = ['wtp']

class AddInfo(Page):
    #show gif of additional draw
    timeout_seconds = 6

class SecondGuess(Page):
    #repeat the result of all 5 draws, solicit second guess about which jar
    form_model = 'player'
    form_fields = ['secondGuess','confidence']

    @staticmethod
    def vars_for_template(player: Player):
        drawsAsInt = int(player.firstDraws[0])+int(player.firstDraws[1])+int(player.firstDraws[2])+int(player.firstDraws[3])+int(player.addDraw[0])
        return dict(numOrangeDraws=C.NUM_DRAWS + C.ADD_INFO_DRAWS - drawsAsInt, numPurpleDraws=drawsAsInt)

class Outcome(Page):
    #provide results on which guess was used, which jar was faced, whether ``effective'' guess was correct, and total payment

    #maybe not the most proper place to do calculations, but compute the total bonus payment as part of telling html what the outcome is
    @staticmethod
    def vars_for_template(player: Player):
        pay = 0
        right = False
        secondGuessUsed = False
        if player.wtp >= player.costToChange:
            secondGuessUsed = True
            pay = pay - player.costToChange
            if player.secondGuess == player.jarFacing:
                pay = pay + C.BONUS
                right = True
        elif player.wtp < player.costToChange and player.firstGuess == player.jarFacing:
            pay = pay + C.BONUS
            right = True
        player.payoff = pay
        return dict(payout=pay, right=right, secondGuessUsed=secondGuessUsed)

page_sequence = [Draws, FirstGuess, WTPElicit, AddInfo, SecondGuess, Outcome]
