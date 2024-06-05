import random
import sys
from time import sleep
import nltk
from nltk.corpus import brown
print_flag = False

def load_words():
    words = []
    with open("words.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                words.append(word)
    return words

def past_words():
    words = []
    with open("pastwords.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                words.append(word)
    return words


def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]


def check(words, input, solution):  # green>yellow>grey
    output = [];
    for i in range(5):
        if input[i] == solution[i]:
            output.append('g')
            words = update_words_green(words, input[i], i)
        elif input[i] in solution:
            output.append('y')
            words = update_words_yellow(words, input[i], i)

        else:
            output.append('-')
            words = update_words_grey(words, input[i])

    return words, output


def update_words_green(words, letter, index):
    return [x for x in words if x[index] == letter]


def update_words_yellow(words, letter, index):
    return [x for x in words if (x[index] != letter) and letter in x]


def update_words_grey(words, letter):
    return [x for x in words if letter not in x]

def word_random(words):
    i = random.randint(0, len(words) - 1)  # randint includes both endpoints
    return words[i];



def count_vowels(word):
    vowels = 'aeiou'
    return sum(1 for char in word if char in vowels)

def word_least_vowels(words):
    words_subset = []
    min_vowels = float('inf')
    for word in words:
        num_vowels = count_vowels(word)
        if num_vowels < min_vowels:
            min_vowels = num_vowels
    for word in words:
        if count_vowels(word) == min_vowels:
            words_subset.append(word)
    return word_random(words_subset)

def word_most_vowels(words):
    words_subset = []
    max_vowels = 0
    for word in words:
        num_vowels = count_vowels(word)
        if num_vowels > max_vowels:
            max_vowels = num_vowels

    for word in words:
        if count_vowels(word) == max_vowels:
            words_subset.append(word)
    return word_random(words_subset)

def starts_with_blend_or_digraph(word):
    blends_and_digraphs = ['bl', 'br', 'ch', 'ck', 'cl', 'cr', 'dr', 'fl', 'fr', 'gh', 'gl', 'gr', 'ng', 'ph', 'pl', 'pr', 'qu', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr']
    for word in blends_and_digraphs:
        if word.startswith(word):
            return True
    return False

def blends_digraphs(words):
    temp = [word for word in words if starts_with_blend_or_digraph(word)]
    if len(temp) == 0:
        return word_least_vowels()
    elif len(temp) ==1:
        return temp[0]
    else:
        return word_least_vowels(temp)

def optimization1(words): #remove past words
    return list(words - set(past_words()))


def setup(start, sol, words):
    if (len(start) == len(sol) != 5):
        print("Invalid input")
        exit(0)

    if start not in words:
        print("'"+start+"'", "is not a valid word")
        exit()

    if sol not in words:
        print("'"+sol+"'", "is not a valid word")
        exit()

    if start == sol:
        return 'ggggg'
    return '-----'


#AGENTS
def general(start="hello", sol="there"):
    words = set(load_words())

    if start=="" and sol=="":
        start, sol = input("Enter start word and solution (space separated)").split()
    if start=="":
        start = word_random(words)


    output = setup(start, sol, words)

    i = 1

    while output != 'ggggg':
        # print("remaining words", words)
        words, output = check(words, start, sol)
        output = ''.join(output)
        if print_flag:
            print("#", i, "\tguess:", start, "\toutput", output, "\t words left", len(words))
        i += 1
        start = word_random(words)

    if print_flag:
        print("Solution found in", i, "guesses.")

    return i

def player1(start="hello", sol="chair"):
    words = set(load_words())
    if start == "" and sol == "":
        start, sol = input("Enter start word and solution (space separated)").split()
    if start == "":
        start = word_random(words)
    setup(start, sol, words)
    output = '-----'
    i = 1
    while output != 'ggggg':
        # print("remaining words", words)
        words, output = check(words, start, sol)
        output = ''.join(output)
        if print_flag:
            print("#", i, "\tguess:", start, "\toutput", output, "\t words left", len(words))
        i += 1
        if output[2] == 'g' and start[2] in 'aeiou':
            start = blends_digraphs(words)
        else:
            start = word_least_vowels(words)

    if print_flag:
        print("Solution found in", i, "guesses.")

    return i


def player2(sol="chair"):
    if sol=="":
        start, sol = input("Enter solution (space separated)").split()
    start = "train"
    words = set(load_words())
    setup(start, sol, words)
    output = '-----'
    i = 1
    while output != 'ggggg':
        # print("remaining words", words)
        words, output = check(words, start, sol)
        output = ''.join(output)
        if print_flag:
            print("#", i, "\tguess:", start, "\toutput", output, "\t words left", len(words))
        i += 1
        if i == 2:
            start = "close"
        else:
            start = word_random(words)

    if print_flag:
        print("Solution found in", i, "guesses.")
    return i

def player3(sol="chair"):
    if sol=="":
        start, sol = input("Enter solution (space separated)").split()
    start = "stare"
    words = set(load_words())
    setup(start, sol, words)
    output = '-----'
    i = 1
    while output != 'ggggg':
        # print("remaining words", words)
        words, output = check(words, start, sol)
        output = ''.join(output)
        if print_flag:
            print("#", i, "\tguess:", start, "\toutput", output, "\t words left", len(words))
        i += 1
        start = word_most_vowels(words)

    if print_flag:
        print("Solution found in", i, "guesses.")
    return i


def main(SOL):
    gen = []
    p1 = []
    p2 = []
    p3 = []

    past = ["ABACK","ABASE","ABATE","ABBEY","ABIDE"]
     # past = ["ABACK","ABASE","ABATE","ABBEY","ABIDE","ABOUT","ABOVE","ABYSS","ACRID","ACTOR","ACUTE","ADAPT","ADMIT","ADOBE","ADOPT","ADORE","ADULT","AFTER","AGAIN","AGAPE","AGATE","AGENT","AGILE","AGING","AGLOW","AGONY","AGREE","AHEAD","ALBUM","ALIEN","ALIKE","ALIVE","ALLOW","ALOFT","ALONE","ALOOF","ALOUD","ALPHA","ALTAR","ALTER","AMASS","AMBER","AMISS","AMPLE","ANGEL","ANGER","ANGRY","ANODE","ANTIC","AORTA","APART","APHID","APPLE","APPLY","APRON","APTLY","ARBOR","ARDOR","ARGUE","AROMA","ASCOT","ASIDE","ASKEW","ASSET","ATOLL","ATONE","AUDIO","AUDIT","AVAIL","AVERT","AWAIT","AWAKE","AWFUL","AXIOM","AZURE","BACON","BADGE","BADLY","BAGEL","BAKER","BALSA","BANAL","BARGE","BASIC","BASIN","BATHE","BATON","BATTY","BAYOU","BEACH","BEADY","BEAST","BEEFY","BEGET","BEGIN","BEING","BELCH","BELIE","BELLY","BELOW","BENCH","BERET","BERTH","BESET","BEVEL","BINGE","BIOME","BIRCH","BIRTH","BLACK","BLAME","BLAND","BLEAK","BLEED","BLEEP","BLIMP","BLOCK","BLOKE","BLOND","BLOWN","BLUFF","BLURB","BLURT","BLUSH","BOOBY","BOOST","BOOZE","BOOZY","BORAX","BOUGH","BRAID","BRAKE","BRASH","BRAVE","BRAVO","BREAD","BREAK","BREED","BRIAR","BRIBE","BRIDE","BRIEF","BRINE","BRING","BRINK","BRINY","BRISK","BROKE","BROOK","BROOM","BROTH","BRUSH","BUGGY","BUILD","BUILT","BULKY","BULLY","BUNCH","BURLY","CABLE","CACAO","CACHE","CANDY","CANNY","CANOE","CAPER","CARAT","CARGO","CAROL","CARRY","CATCH","CATER","CAULK","CAUSE","CEDAR","CHAFE","CHAIN","CHAMP","CHANT","CHAOS","CHARD","CHARM","CHART","CHEAT","CHEEK","CHEER","CHEST","CHIEF","CHILD","CHILL","CHIME","CHOIR","CHOKE","CHORD","CHUNK","CHUTE","CIDER","CIGAR","CINCH","CIRCA","CIVIC","CLASS","CLEAN","CLEAR","CLEFT","CLERK","CLICK","CLIMB","CLING","CLOCK","CLONE","CLOSE","CLOTH","CLOWN","CLUCK","COACH","COAST","COCOA","COLON","COMET","COMMA","CONDO","CONIC","CORNY","COULD","COUNT","COURT","COVET","COWER","COYLY","CRAFT","CRAMP","CRANE","CRANK","CRASS","CRATE","CRAVE","CRAZE","CRAZY","CREAK","CREDO","CREPT","CRIME","CRIMP","CROAK","CRONE","CROSS","CRUMB","CRUST","CUMIN","CURLY","CYNIC","DADDY","DAISY","DANCE","DANDY","DEATH","DEBUG","DECAY","DECAL","DELTA","DELVE","DENIM","DEPOT","DEPTH","DEVIL","DIARY","DIGIT","DINER","DINGO","DISCO","DITTO","DODGE","DOING","DONOR","DONUT","DOUBT","DOWRY","DOZEN","DRAIN","DREAM","DRINK","DRIVE","DROLL","DROOP","DUCHY","DUTCH","DUVET","DWARF","DWELL","DWELT","EARLY","EARTH","EBONY","EGRET","EJECT","ELDER","ELOPE","ELUDE","EMAIL","EMBER","EMPTY","ENEMA","ENJOY","ENNUI","ENTER","EPOCH","EPOXY","EQUAL","EQUIP","ERODE","ERROR","ERUPT","ESSAY","ETHIC","ETHOS","EVADE","EVERY","EVOKE","EXACT","EXALT","EXCEL","EXERT","EXIST","EXPEL","EXTRA","EXULT","FACET","FARCE","FAULT","FAVOR","FEAST","FEIGN","FERRY","FEWER","FIELD","FIEND","FIFTY","FINAL","FINCH","FINER","FIRST","FISHY","FIXER","FJORD","FLAIL","FLAIR","FLAME","FLANK","FLARE","FLASK","FLESH","FLICK","FLING","FLIRT","FLOAT","FLOCK","FLOOD","FLOOR","FLORA","FLOSS","FLOUT","FLUFF","FLUME","FLYER","FOCAL","FOCUS","FOGGY","FOLLY","FORAY","FORCE","FORGE","FORGO","FORTH","FORTY","FOUND","FOYER","FRAME","FRANK","FRESH","FRIED","FROCK","FROND","FRONT","FROST","FROTH","FROZE","FUNGI","FUNNY","GAMER","GAMMA","GAUDY","GAUZE","GAWKY","GECKO","GENRE","GHOUL","GIANT","GIDDY","GIRTH","GIVEN","GLASS","GLAZE","GLEAM","GLEAN","GLIDE","GLOAT","GLOBE","GLOOM","GLORY","GLOVE","GLYPH","GNASH","GOLEM","GONER","GOOSE","GORGE","GOUGE","GRACE","GRADE","GRAIL","GRAND","GRAPH","GRASP","GRATE","GREAT","GREEN","GREET","GRIEF","GRIME","GRIMY","GRIPE","GROIN","GROUP","GROUT","GROVE","GROWL","GRUEL","GUANO","GUARD","GUEST","GUIDE","GUILD","GULLY","GUMMY","GUPPY","HAIRY","HAPPY","HATCH","HATER","HAVOC","HEADY","HEARD","HEART","HEATH","HEAVE","HEAVY","HEIST","HELIX","HELLO","HERON","HINGE","HITCH","HOARD","HOBBY","HOMER","HORDE","HORSE","HOTEL","HOUND","HOUSE","HOWDY","HUMAN","HUMID","HUMOR","HUMPH","HUNCH","HUNKY","HURRY","HUTCH","HYPER","IGLOO","IMAGE","IMPEL","INANE","INDEX","INEPT","INERT","INFER","INPUT","INTER","INTRO","IONIC","IRATE","IRONY","ISLET","ITCHY","IVORY","JAUNT","JAZZY","JERKY","JOKER","JOLLY","JOUST","JUDGE","KARMA","KAYAK","KAZOO","KEBAB","KHAKI","KIOSK","KNEEL","KNELT","KNOCK","KNOLL","KOALA","LABEL","LABOR","LAPEL","LAPSE","LARGE","LARVA","LASER","LATTE","LAYER","LEAFY","LEAKY","LEAPT","LEARN","LEASH","LEAVE","LEDGE","LEERY","LEGGY","LEMON","LIBEL","LIGHT","LILAC","LIMIT","LINEN","LINER","LINGO","LIVER","LOCAL","LOCUS","LOFTY","LOGIC","LOOPY","LOSER","LOUSE","LOVER","LOWLY","LOYAL","LUCID","LUCKY","LUNAR","LUNCH","LUNGE","LUSTY","LYING","MADAM","MAGIC","MAGMA","MAIZE","MAJOR","MANIA","MANLY","MANOR","MAPLE","MARCH","MARRY","MARSH","MASON","MASSE","MATCH","MATEY","MAXIM","MAYBE","MAYOR","MEALY","MEANT","MEDAL","MEDIA","MERCY","MERGE","MERIT","MERRY","METAL","METRO","MICRO","MIDGE","MIDST","MIMIC","MINCE","MINUS","MODEL","MOIST","MOLAR","MONEY","MONTH","MOOSE","MOSSY","MOTOR","MOTTO","MOULT","MOUNT","MOURN","MOUSE","MOVIE","MUCKY","MUMMY","MURAL","MUSIC","MUSTY","NAIVE","NANNY","NASTY","NATAL","NAVAL","NEEDY","NEVER","NICER","NIGHT","NINJA","NINTH","NOBLE","NOISE","NORTH","NYMPH","OCCUR","OCEAN","OFFAL","OFTEN","OLDER","OLIVE","ONION","ONSET","OPERA","OTHER","OUGHT","OUTDO","OUTER","OVERT","OXIDE","PANEL","PANIC","PAPAL","PAPER","PARER","PARRY","PARTY","PASTA","PATTY","PAUSE","PEACE","PEACH","PERCH","PERKY","PESKY","PHASE","PHONE","PHONY","PHOTO","PIANO","PICKY","PIETY","PILOT","PINCH","PINEY","PINKY","PINTO","PIOUS","PIPER","PIQUE","PITHY","PIXEL","PIXIE","PLACE","PLAIT","PLANK","PLANT","PLATE","PLAZA","PLEAT","PLUCK","PLUNK","POINT","POISE","POKER","POLKA","POLYP","POUND","POWER","PRICE","PRICK","PRIDE","PRIME","PRIMO","PRINT","PRIZE","PROBE","PROVE","PROWL","PROXY","PRUNE","PSALM","PULPY","PURGE","QUALM","QUART","QUEEN","QUERY","QUEST","QUEUE","QUICK","QUIET","QUIRK","QUOTE","RADIO","RAINY","RAISE","RAMEN","RANCH","RANGE","RATIO","RAYON","REACT","REALM","REBUS","REBUT","RECAP","REGAL","RELIC","RENEW","REPAY","REPEL","RESIN","RETCH","RETRO","RETRY","REVEL","RHINO","RHYME","RIDGE","RIGHT","RIPER","RISEN","RIVAL","ROBIN","ROBOT","ROCKY","RODEO","ROGUE","ROOMY","ROUGE","ROUND","ROUSE","ROUTE","ROVER","ROYAL","RUDDY","RUDER","RUPEE","RUSTY","SAINT","SALAD","SALLY","SALSA","SALTY","SASSY","SAUTE","SCALD","SCANT","SCARE","SCARF","SCOLD","SCOPE","SCORN","SCOUR","SCOUT","SCRAM","SCRAP","SCRUB","SEDAN","SEEDY","SENSE","SERUM","SERVE","SEVER","SHADE","SHAKE","SHALL","SHAME","SHANK","SHARD","SHARP","SHAWL","SHAVE","SHIFT","SHINE","SHIRE","SHIRK","SHORN","SHOWN","SHOWY","SHRUB","SHRUG","SHYLY","SIEGE","SIGHT","SINCE","SISSY","SKIER","SKILL","SKIMP","SKIRT","SKUNK","SLATE","SLEEK","SLEEP","SLICE","SLOPE","SLOSH","SLOTH","SLUMP","SLUNG","SMALL","SMART","SMASH","SMEAR","SMELT","SMILE","SMIRK","SMITE","SMITH","SNACK","SNAFU","SNAIL","SNAKE","SNAKY","SNARE","SNARL","SNEAK","SNORT","SNOUT","SOGGY","SOLAR","SOLID","SOLVE","SONIC","SOUND","SOWER","SPACE","SPADE","SPEAK","SPELL","SPELT","SPEND","SPENT","SPICE","SPICY","SPIEL","SPIKE","SPILL","SPIRE","SPLAT","SPOKE","SPRAY","SPURT","SQUAD","SQUAT","STAFF","STAGE","STAID","STAIR","STALE","STALL","STAND","STARK","START","STASH","STATE","STEAD","STEED","STEEL","STEIN","STICK","STIFF","STILL","STING","STINK","STOCK","STOLE","STOMP","STONE","STONY","STOOL","STORE","STORY","STOUT","STOVE","STRAP","STRAW","STUDY","STUNG","STYLE","SUGAR","SULKY","SURER","SURLY","SUSHI","SWEAT","SWEEP","SWEET","SWILL","SWINE","SWIRL","SWISH","SYRUP","TABLE","TABOO","TACIT","TAKEN","TALON","TANGY","TAPER","TAPIR","TARDY","TASTE","TASTY","TAUNT","TAWNY","TEARY","TEASE","TEMPO","TENTH","TEPID","THEIR","THEME","THERE","THESE","THIEF","THING","THINK","THIRD","THORN","THOSE","THREE","THREW","THROW","THUMB","THUMP","THYME","TIARA","TIBIA","TIDAL","TIGER","TILDE","TIPSY","TITAN","TITHE","TODAY","TONIC","TOPAZ","TOPIC","TORSO","TOTEM","TOUCH","TOUGH","TOWEL","TOXIC","TOXIN","TRACE","TRACT","TRADE","TRAIN","TRAIT","TRASH","TRAWL","TREAT","TREND","TRIAD","TRICE","TRITE","TROLL","TROPE","TROVE","TRUSS","TRUST","TRUTH","TRYST","TUTOR","TWANG","TWEAK","TWEED","TWICE","TWINE","TWIRL","ULCER","ULTRA","UNCLE","UNDER","UNDUE","UNFED","UNFIT","UNIFY","UNITE","UNLIT","UNMET","UNTIE","UNTIL","UNZIP","UPSET","URBAN","USAGE","USHER","USING","USUAL","USURP","UTTER","VAGUE","VALET","VALUE","VALID","VAPID","VENOM","VERGE","VERVE","VIGOR","VIOLA","VIRAL","VITAL","VIVID","VODKA","VOICE","VOILA","VOTER","VOUCH","WACKY","WALTZ","WASTE","WATCH","WEARY","WEDGE","WHACK","WHALE","WHEEL","WHELP","WHERE","WHICH","WHIFF","WHILE","WHINE","WHINY","WHIRL","WHISK","WHOOP","WINCE","WINDY","WOKEN","WOMAN","WOOER","WORDY","WORLD","WORRY","WORSE","WORST","WOULD","WOVEN","WRATH","WRIST","WRITE","WRONG","WROTE","WRUNG","YACHT","YEARN","YIELD","YOUNG","YOUTH","ZESTY"]
    for j in past:
        SOL = j.lower()
        for i in range(20):
            gen.append(general(sol=SOL))
            p1.append(player1(sol=SOL))
            p2.append(player2(SOL))
            p3.append(player3(SOL))

    print("Averages for", SOL)
    print("General", sum(gen)/len(gen))
    print("P1", sum(p1)/len(p1))
    print("P2", sum(p2)/len(p2))
    print("P3", sum(p3)/len(p3))

    gen = [gen.count(i)/len(gen) for i in range(1, 11)]
    p1 = [p1.count(i)/len(p1) for i in range(1, 11)]
    p2 = [p2.count(i)/len(p2) for i in range(1, 11)]
    p3 = [p3.count(i)/len(p3) for i in range(1, 11)]



    with open("output.txt", "w") as file:
        file.write('\t'.join(map(str, gen))+'\n')
        file.write('\t'.join(map(str, p1))+'\n')
        file.write('\t'.join(map(str, p2))+'\n')
        file.write('\t'.join(map(str, p3))+'\n')



# main("stark");


#################### DEMO ######################################################
def demo(start, sol):
    global print_flag
    print_flag = True

    # General Agent (Random)
    print("General Agent (Random)")
    general(start, sol)

    # Player1 (consonants, blends - th, cr, st, etc)
    print("\nPlayer1 (consonants, blends - th, cr, st, etc)")
    player1(start, sol)

    # Player2 (1st: CLOSE 2nd: TRAIN, then random)
    print("\nPlayer2 (1st: CLOSE 2nd: TRAIN, then random)")
    player2(sol)

    # Player3 (1st: STARE, lots of vowels)
    print("\nPlayer3 (1st: STARE, lots of vowels)")
    player2(sol)





start, sol = input("Enter start word and solution separated by space (START SOLUTION)").split()
demo(start, sol)