
#import expyriment
import random
from expyriment import design, control, stimuli, misc

#generate random numbers for dec_uni block

numbers = list(range(100,999))
#exclude cue number and 500s
exclude_set1 = range(500,599)
exp_numbers = list(num for num in numbers if num not in exclude_set1)
exp_numbers_fnl = random.sample(exp_numbers,10)

#generate random numbers for cen_dec_uni block
#repeat above process
hundred_numbers = list(range(500,599))
exclude_set2 = {555}
exp_hund_numbers= list(num for num in hundred_numbers if num not in exclude_set2)
exp_hund_numbers_fnl = random.sample(exp_hund_numbers, 10)

TARGETS1 = exp_numbers_fnl 
TARGETS2 = exp_hund_numbers_fnl
#set max response delay
MAX_RESPONSE_DELAY = 2000
#define keyboard input for "larger" and "smaller" responses
LRG_RESPONSE_KEY = misc.constants.K_f
SML_RESPONSE_KEY = misc.constants.K_j

#start experiment design
exp = design.Experiment(name="3 Digit Comparison task", text_size=40)
control.initialize(exp)
#create cue using red colour 
cue = stimuli.TextLine("555", text_colour=[255,0,0])
blankscreen = stimuli.BlankScreen()

#create first block
block1 = design.Block("cen_dec_uni")
for number in TARGETS1:
    t = design.Trial()
    t.set_factor('number', number)
#set factors for correct responses
    t.set_factor('is_larger', number > 555)
    t.set_factor('is_smaller', number < 555)
#create stimulus using green colour
    t.add_stimulus(stimuli.TextLine(str(number), text_colour=[0,255,0]))
    block1.add_trial(t)

#repeat above for second block with new set of targets
block2 =design.Block("cen_uni")
for number in TARGETS2:
    t = design.Trial()
    t.set_factor('number', number)
    t.set_factor('is_larger', number > 555)
    t.set_factor('is_smaller', number < 555)
    t.add_stimulus(stimuli.TextLine(str(number), text_colour=[0,255,0]))
    block2.add_trial(t)
#set instructions 
instructions = stimuli.TextScreen("Instructions",
    f"""
    You will see the number 555, after 2 seconds a new green number will appear. Your task is to decide, as quickly as possible, whether the new number is larger or smaller than 555.
    if it is larger, press '{chr(LRG_RESPONSE_KEY)}'
    if it is smaller, press '{chr(SML_RESPONSE_KEY)}'
    There will be {len(TARGETS1+TARGETS2)} trials in total. 
    Press the space bar to start.""")
#set variable names for data to be recorded after experiment
exp.add_data_variable_names(['number', 'is_larger', 'is_smaller','respkey', 'RT', 'is_correct','block'])
control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()
#start first block
for trial in block1.trials:
    blankscreen.present()
    exp.clock.wait(2000)
    cue.present()
    exp.clock.wait(3000)
    trial.stimuli[0].present()
    key, rt = exp.keyboard.wait([LRG_RESPONSE_KEY, SML_RESPONSE_KEY], duration=MAX_RESPONSE_DELAY)
#set conditions for correct answer
    is_correct_answer = (trial.get_factor('is_larger') and key == LRG_RESPONSE_KEY) or \
                        (not trial.get_factor('is_larger') and key ==  SML_RESPONSE_KEY)
#add data to be recorded 
    exp.data.add([trial.get_factor('number'), trial.get_factor('is_larger'), trial.get_factor('is_smaller'), chr(key), rt, is_correct_answer, block1.name])
#start second block
#repeat above processes
for trial in block2.trials:
    blankscreen.present()
    exp.clock.wait(2000)
    cue.present()
    exp.clock.wait(3000)
    trial.stimuli[0].present()
    key, rt = exp.keyboard.wait([LRG_RESPONSE_KEY, SML_RESPONSE_KEY], duration=MAX_RESPONSE_DELAY)
    is_correct_answer = (trial.get_factor('is_larger') and key == LRG_RESPONSE_KEY) or \
                        (not trial.get_factor('is_larger') and key ==  SML_RESPONSE_KEY)
    exp.data.add([trial.get_factor('number'), trial.get_factor('is_larger'), trial.get_factor('is_smaller'), chr(key), rt, is_correct_answer, block2.name])
#end experiment
control.end()
