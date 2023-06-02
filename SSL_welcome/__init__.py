import random

from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'GuessJar'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ADD_DRAWS = 1
    NUM_DRAWS = 4
    ENDOWMENT = 100
    BONUS = 100
    MAJ = 60
    MIN = 40
    SHOWUP = 1000

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    IntroCheck1 = models.IntegerField()
    IntroCheck2 = models.IntegerField()
    IntroCheck3 = models.IntegerField()
    IntroCheck4 = models.IntegerField()

    MajExample = models.IntegerField(
        choices=[
            [1,'ORANGE'],
            [2,'PURPLE'],
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    #MajCheck1 = models.IntegerField()
    #MajCheck2 = models.IntegerField()
    MajCheck3 = models.IntegerField(
        choices=[
            [1,'ORANGE'],
            [2,'PURPLE'],
        ],
        widget=widgets.RadioSelect
    )

    WTPExample = models.IntegerField(min=0, max=C.BONUS, blank=True)

    WTPCheck1 = models.IntegerField()
    WTPCheck2 = models.IntegerField()
    WTPCheck3 = models.BooleanField(
        choices=[
            [False,'No'],
            [True,'Yes']
        ]
    )
    WTPCheck4 = models.IntegerField()
 #   WTPCheck5 = models.IntegerField()

    AddInfoCheck1 = models.IntegerField()
    AddInfoCheck2 = models.BooleanField(blank=True)
    AddInfoCheck3 = models.BooleanField(blank=True)
    AddInfoCheck4 = models.BooleanField(blank=True)
    AddInfoCheck5 = models.BooleanField(blank=True)
    AddInfoCheck6 = models.BooleanField(blank=True)
    AddInfoCheck7 = models.BooleanField(blank=True)

    # random variables generated for player
    jarFacing = models.IntegerField()  # whether participant faces orange majority jar (0) or purple majority (1)
    costToChange = models.IntegerField()  # (hidden) cost to using second answer
    firstDraws = models.StringField()  # string encoding 0/1 sequence of orange and purple marbles drawn
    addDraw = models.StringField()  # 0/1 string encoding whether orange or purple marble drawn

    # choices made by participant
    firstGuess = models.IntegerField(
        choices=[
            [0, 'ORANGE'],
            [1, 'PURPLE'],
        ],
        widget=widgets.RadioSelect
    )
    wtp = models.IntegerField(min=0, max=C.BONUS)
    secondGuess = models.IntegerField(
        choices=[
            [0, 'ORANGE'],
            [1, 'PURPLE'],
        ],
        widget=widgets.RadioSelect
    )
    confidence1 = models.IntegerField(min=0, max=10)
    confidence2 = models.IntegerField(min=0, max=10)

    gender = models.IntegerField(
        choices=[
            [0, 'Woman'],
            [1, 'Man'],
            [2, 'Non-binary'],
            [3, 'Not listed'],
            [4, 'Prefer not to reply'],
        ],
        widget=widgets.RadioSelect
    )

    risks = models.IntegerField(min=0, max=10)
    goodcauses = models.IntegerField(min=0, max=10)
    math = models.IntegerField(min=0, max=10)
    windfall = models.IntegerField(min=0, max=1600)

def IntroCheck1_error_message(player, value):
    if value != C.MIN:
        return 'Please try question 1 again. The PURPLE jar has 60 purple marbles and 40 orange marbles. The ORANGE jar has 60 orange marbles and 40 purple marbles.'

def IntroCheck2_error_message(player, value):
    if value != 100:
        return 'Please try question 2 again. Both the ORANGE jar and the PURPLE jar have 100 marbles in total.'

def IntroCheck3_error_message(player, value):
    if value != 50:
        return 'Please try question 3 again, entering a number between 0 and 100. Each jar was equally likely to have been chosen.'

def IntroCheck4_error_message(player, value):
    if value != 100:
        return 'Please try question 4 again, remembering that marbles are placed back in the bag after each draw.'

#def MajCheck2_choices(player):
#    import random
#    choices = [
#        [1,'The answer that is used as my final guess at the end of the study'],
#        [2,'The answer that I give after seeing {} marbles drawn from the bag'.format(C.NUM_DRAWS)],
#        [3,'The answer that I give after seeing all information about the bag']
#    ]
#    random.shuffle(choices)
#    return choices

#def MajCheck1_error_message(player, value):
#    if value != 2:
#        return 'Please try question 1 again, remembering you will be asked after seeing the initial {} draws and again after receiving the additional piece of information'.format(C.NUM_DRAWS)

#def MajCheck2_error_message(player, value):
#    if value != 1:
#        return 'Please try question 2 again'

def MajCheck3_error_message(player, value):
    if value != 1:
        return 'Please try question 3 again, remembering that you are more likely to see orange marbles drawn from the ORANGE jar and purple marbles drawn from the PURPLE jar.'

def WTPCheck1_choices(player):
    import random
    choices = [
        [1,'The guess I just made after seeing {} marble draws'.format(C.NUM_DRAWS)],
        [2,'The  second guess I will make after seeing the additional piece of information about the jar']
    ]
    random.shuffle(choices)
    return choices

#def WTPCheck5_choices(player):
#    import random
#    choices = [
#        [1,'My first answer after seeing {} marble draws'.format(C.NUM_DRAWS)],
#        [2,'My second answer after seeing the additional piece of information about the bag'],
#        [3,'Either my first or my second answer depending on whether I decide to make use of my right to change my final guess']
#    ]
#    random.shuffle(choices)
#    return choices

def WTPCheck1_error_message(player, value):
    if value != 1:
        return 'Please try question 1 again. Your second guess is only used if the computer picks a price no greater than the number you report.'

def WTPCheck2_error_message(player, value):
    if value != 72:
        return 'Please try question 2 again. You should report exactly how valuable you think the additional information will be.'

def WTPCheck3_error_message(player, value):
    if value:
        return 'Please try question 3 again. The guess you will make after seeing the additional information is only used if the computer picks a price no greater than the number you report.'

def WTPCheck4_error_message(player, value):
    if value != 42:
        return 'Please try question 4 again. You pay the price the computer picks if you reported that you are willing to pay that much or more.'

#def WTPCheck5_error_message(player, value):
#    if value != 3:
#        return 'Please try question 5 again'

def AddInfoCheck1_choices(player):
    import random
    choices = [
        [1,'{} draws'.format(C.NUM_DRAWS)],
        [2,'{0} or {1} draws'.format(C.NUM_DRAWS,C.NUM_DRAWS+C.ADD_DRAWS)],
        [3,'{} draws'.format(C.NUM_DRAWS+C.ADD_DRAWS)]
    ]
    random.shuffle(choices)
    return choices

def AddInfoCheck1_error_message(player, value):
    if value != 2:
        return 'Please try question 1 again'

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
            p.firstDraws = ''.join(random.choices(['0','1'],weights=[C.MAJ,100-C.MAJ],k = C.NUM_DRAWS))
            p.addDraw = str(random.choice(list(itertools.chain(itertools.repeat(0,C.MAJ),itertools.repeat(1,100-C.MAJ)))))
        elif p.jarFacing == 1:
            p.firstDraws = ''.join(random.choices(['0', '1'], weights=[C.MAJ, 100 - C.MAJ], k=C.NUM_DRAWS))
            p.addDraw = str(random.choice(
                list(itertools.chain(itertools.repeat(0, 100 - C.MAJ), itertools.repeat(1, C.MAJ)))))

# PAGES
class Introduction(Page):
    #@staticmethod
    #def vars_for_template(player: Player):
    #    return dict(numMajMarbles = int(100*C.MAJRATIO), numMinMarbles = int(100 - 100*C.MAJRATIO))

    #@staticmethod
    #def app_after_this_page(player, upcoming_apps):
    #    if player.participant.STRATEGY_ELICIT:
    #        return "SSLsingle1a_intro"
    pass

class IntroCheck(Page):
    form_model = 'player'
    form_fields = ['IntroCheck1','IntroCheck2','IntroCheck3','IntroCheck4']

class Majority(Page):
    form_model = 'player'
    form_fields = ['MajExample']

class MajCheck(Page):
    form_model = 'player'
    form_fields = ['MajCheck3']

class JarSelect(Page):
    timeout_seconds = 10

class DrawPrep(Page):
    pass

class Draws(Page):
    #take in the result of the draws, display the appropriate gif of the four draws
    timeout_seconds = 27.5

class FirstGuess(Page):
    #repeat the result in text form, solicit first guess about which jar
    form_model = 'player'
    form_fields = ['firstGuess','confidence1']

    @staticmethod
    def vars_for_template(player: Player):
        drawsAsInt = int(player.firstDraws[0])+int(player.firstDraws[1])+int(player.firstDraws[2])+int(player.firstDraws[3])
        return dict(numOrangeDraws=C.NUM_DRAWS - drawsAsInt, numPurpleDraws=drawsAsInt)

class WTP(Page):
    form_model = 'player'
    form_fields = ['WTPExample']

class WTPCheck(Page):
    form_model = 'player'
    form_fields = ['WTPCheck1','WTPCheck2','WTPCheck3','WTPCheck4']

class AddInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(totDraws=C.NUM_DRAWS+C.ADD_DRAWS)

class AddInfoCheck(Page):
    form_model = 'player'
    form_fields = ['AddInfoCheck1','AddInfoCheck2','AddInfoCheck3','AddInfoCheck4','AddInfoCheck5','AddInfoCheck6','AddInfoCheck7']

    @staticmethod
    def error_message(player, values):
        print('hi')
        if values['AddInfoCheck2'] != True or values['AddInfoCheck3'] != True or values['AddInfoCheck4'] != True or values[
            'AddInfoCheck5'] == True or values['AddInfoCheck6'] == True or values['AddInfoCheck7'] == True:
            return 'Please try question 2 again. Remember, you purchase the right to change your final guess whenever the computer chooses a number no bigger than what you reported'

class WTPElicit(Page):
    #elicit wtp to be use second guess
    form_model = 'player'
    form_fields = ['wtp']

class AddInfoShow(Page):
    #show gif of additional draw
    timeout_seconds = 5.5

class SecondGuess(Page):
    #repeat the result of all 5 draws, solicit second guess about which jar
    form_model = 'player'
    form_fields = ['secondGuess','confidence2']

    @staticmethod
    def vars_for_template(player: Player):
        drawsAsInt = int(player.firstDraws[0])+int(player.firstDraws[1])+int(player.firstDraws[2])+int(player.firstDraws[3])+int(player.addDraw[0])
        return dict(numOrangeDraws=C.NUM_DRAWS + C.ADD_DRAWS - drawsAsInt, numPurpleDraws=drawsAsInt)

class Survey(Page):
    form_model = 'player'
    form_fields = ['gender','risks','goodcauses','math','windfall']

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

page_sequence = [Introduction,IntroCheck,Majority,MajCheck,JarSelect,DrawPrep,Draws,FirstGuess,WTP,WTPCheck,AddInfo,AddInfoCheck,WTPElicit,AddInfoShow,SecondGuess,Survey, Outcome]
