import curses
from curses import wrapper
import time
import random
#stdscr = standard screen


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("WELCOME TO THE TYPING SPEED TEST!!") #for placing lines and chars/ 1st is for lines and 2nd is for chars
    stdscr.addstr("\nPress any key to Begin !")
    stdscr.refresh()
    stdscr.getkey()

def dsply_txt(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")

    for i, char in enumerate (current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)
    

def load_text():
    with open("WPM_text.txt","r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() #get rid of all leading and trailing space chars so that it displays the exact line in the sentence.
    
def get_wpm_message(wpm):
    if wpm < 20:
        return random.choice([
            "Are you typing with a stick? 🪵",
            "Even a snail would finish a novel at this speed. 🐌",
            "Your keyboard is falling asleep, just like me. 💤",
            "Did you forget the alphabet halfway? 🤔",
            "Speed this slow should come with a warning sign! 🛑"
        ])
    elif wpm < 50:
        return random.choice([
            "Not bad, but let's not call Guinness just yet. 📖",
            "Faster than a sloth, slower than a rabbit. 🐇",
            "At least you're trying... right? 😏",
            "Your typing speed is average... just like your life decisions. 🤷",
            "You’re moving along, but don’t quit your day job. 💼"
        ])
    elif wpm < 70:
        return random.choice([
            "Impressive! Have you been practicing on typewriters? ⌨️",
            "Finally, some speed! Keep it up, champ. 🏆",
            "You're almost fast enough to text during a Marvel movie. 🎥",
            "You could type a novel... eventually. 📚",
            "Not bad! Just don’t let it go to your head. 🧢"
        ])
    else:
        return random.choice([
            "Wow! Are you sure you're not a robot? 🤖",
            "Speed demon alert! You’re making the keyboard smoke. 🔥",
            "Calm down, Flash! You're scaring the keyboard. ⚡",
            "This isn’t a race... but you’re winning anyway. 🏎️",
            "Are your fingers on fire? Because this is insane! 🔥"
        ])



def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed/60))/5)

        stdscr.clear()
        dsply_txt(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            message = get_wpm_message(wpm)
            stdscr.addstr(2, 0, message)
            stdscr.refresh()
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
            

    
def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) #the first color stands for foregroound and secondd one stands for background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start_screen(stdscr)

    while (True):
        wpm_test(stdscr)
        stdscr.addstr(4,0,"You Completed the test! press any key to continue the test!")
        stdscr.addstr(5,0,"If u want to exit, simply press ESC")

        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)