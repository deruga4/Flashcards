import random as rand
import vocab as vocab
import sys
import status_messages as stat
import re
import traceback

# for tmp in vocab_groups:
#     print(tmp.tostr())

# new_group = ''
# while new_group != '!quit':
#     active_groups = []
#     

class State(object):
    def __init__():
        pass

class MenuState(State):
    def __init__(self, new_flashcards):
        self.flashcards = new_flashcards

    def dict_keys_to_list(self, dictionary):

        keys = []
        for k in dictionary.keys():
            keys.append(k)
        return keys

    def print_help(self):
        stat.print_input('Select groups to include. Enter >> to start game.\n')
        stat.print_input('Available groups:')
        stat.print_input(str(self.dict_keys_to_list(self.flashcards.vocab_name_group)) + '\n')
        stat.print_input('Active groups:')
        stat.print_input(str(self.dict_keys_to_list(self.flashcards.active_groups)) + '\n')
        stat.print_input('Available commands:')
        stat.print_input('addall - adds all groups to active groups')
        stat.print_input('removeall - removes all groups from active groups')
        stat.print_input('add [group] - add one groups from active groups')
        stat.print_input('remove [group] - remove one groups from active groups')
        stat.print_input('>> - start the game')
        stat.print_input('?? - display this message\n')

    def display(self):
        in_menu = True
        self.print_help()

        while in_menu:
            

            user_input = input('[>] ')
            parse_input = user_input.partition(' ')

            print()

            if parse_input[0] == 'addall':
                stat.print_success('Added all groups.')
                self.flashcards.active_groups = self.flashcards.vocab_name_group
            elif parse_input[0] == 'removeall':
                stat.print_success('Removed all groups.')
                self.flashcards.active_groups = {}
            elif parse_input[0] == 'add':
                new_group = parse_input[2]
                if new_group == '':
                    stat.print_input('Usage: add [group name]')
                elif not new_group in self.flashcards.vocab_name_group:
                    stat.print_fail('Group not found')
                else:
                    key = new_group
                    value = self.flashcards.vocab_name_group[new_group]
                    self.flashcards.to_active(key, value)
            elif parse_input[0] == 'remove':
                key = parse_input[2]
                try:
                    self.flashcards.vocab_name_group.pop()
                except KeyError:
                    stat.print_warn('Group not found.')
            elif parse_input[0] == '>>':
                self.flashcards.set_state(self.flashcards.game_state)
            elif parse_input[0] == '??':
                self.print_help()



            stat.print_input('Available groups:')
            stat.print_input(str(self.dict_keys_to_list(self.flashcards.vocab_name_group)) + '\n')
            stat.print_input('Active groups:')
            stat.print_input(str(self.dict_keys_to_list(self.flashcards.active_groups)) + '\n')


            # if len(user_input.split(' ')) == 1:
            #     if user_input == '>>':
            #         in_menu = False
            #         self.flashcards.set_state(self.flashcards.game_state)
            #     elif user_input == 'addall':
            #         stat.print_success('Added all groups.')
            #         self.flashcards.active_groups = self.flashcards.vocab_name_group
            #     elif user_input == 'removeall':
            #         stat.print_success('Removed all groups.')
            #         self.flashcards.active_groups = {}
            #     else:
            #         stat.print_fail('Invalid command.')

            # elif len(user_input.split(' ')) > 1:
            #     command, name = user_input.split(' ')
            #     if command == 'add':
            #         pass #TODO
            #     elif command == 'remove':
            #         pass #TODO
            #     else:
            #         stat.print_fail('Invalid command.')

class GameState(State):
    def __init__(self, new_flashcards):
        self.flashcards = new_flashcards

    def display(self):
        user_input = ''
        stat.print_input('Welcome! The vocab game will now start. You can quit any time by entering !! into the console.')
        stat.print_input('Go back by entering \'<<\'')
        stat.print_input('Quit by entering \'<<\'')
        while user_input != '!!':
            group = rand.choice(groups)
            word = rand.choice(list(group.get_vocab_list().keys()))
            user_input = input(word + ': ')
            if group.check(word, user_input):
                stat.print_success('Correct!')
            elif user_input == '!!':
                pass
            else:
                stat.print_fail('So close! The correct word was ' + group.get_answer(word))


class Flashcards:
    def __init__(self, args):
        self.game_state = GameState(self)
        self.menu_state = MenuState(self)
        self.state = self.menu_state

        self.verify_args(args)
        
        self.vocab = self.parse_files(args[1:])
        self.vocab_name_group = {vg.get_name():vg for vg in self.vocab}
        self.active_groups = {}

        self.state = self.menu_state
        self.state.display()

    def set_state(self, state):
        self.state = state
        self.state.display()

    def verify_args(self, args):
        try:
            if len(args) < 2:
                raise ValueError
            stat.print_success('Yep, everything looks good.')
        except ValueError:
            stat.print_warn('This script must be run with at least one vocabulary lists. Please view the documentation to learn how to create it.')
            stat.print_warn('Usage: python3 flashcard.py filename [filenames]')
            stat.print_warn('Example: python3 flashcard.py ~/vocab_list.txt ~/food.txt ~/fun.txt')
            sys.exit(0)

    def group_contains(self, vocab_groups):
        pass

    def parse_files(self, filenames):
        for filename in filenames:
            try:
                file = open(filename, 'r', encoding='utf-8')
                vocab_raw = file.read()
                stat.print_success('File ' + filename + ' found!')
                print('Building vocabulary list...')
                vocab_raw = vocab_raw.strip()
                groups = re.split(r'\n{2,}', vocab_raw)

                vocab_groups = [];

                for g in groups:
                    group_parse = g.split('\n')
                    group_name = group_parse[0]
                    group_list = {}

                    # print(group_name)

                    for p in group_parse[1:]:
                        # pair = re.split(r'(\b=\b|\s{1,}=\s{1,})', p)
                        pair = p.split('=')
                        # print(pair[0] + pair[1])
                        if pair[0].strip in vocab_groups:
                            stat.print_warn('Duplicate group name: ' + pair[0].strip() + '. Only the most recent entry will be entered.')

                        group_list[pair[0].strip()] = pair[1].strip()


                    vocab_groups.append(vocab.Vocab(group_name, group_list))


            except Exception as e:
                stat.print_fail('File location ' + filename + ' not found. Please double-check the file name and make sure it exists.')
                print(traceback.format_exc())

        return vocab_groups


    def to_active(self, key, value):
        self.active_groups[key] = value