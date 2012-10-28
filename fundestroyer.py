#! /usr/bin/python
# written by amandle
# fundestroyer.py makes letterpress fun for no one.

# usage:
# you can simply execute the script:
# fundestroyer.py
# For convenience the first argument to the script can be the letters on the board.

from copy import copy
import sys

GRID_WIDTH = 5
GRID_HEIGHT = 5

def load_dictionary():
  with open('/usr/share/dict/words') as f:
    dictionary = f.readlines()
  return dictionary


def find_words(board, dictionary, important_letters):
  found_words = []
  for word in dictionary:
    word = word.strip().lower()
    scratch_board = copy(board)
    word_found = True
    for character in word:
      if character in scratch_board:
        scratch_board = scratch_board.replace(character, '', 1)
      else:
        if DEBUG:
          print 'character %s not found in %s' % (character, scratch_board)
        word_found = False
        break
    if word_found:
      scratch_word = copy(word)
      importance = 0
      for letter in important_letters:
        if letter in scratch_word:
          importance += 1
          scratch_word = scratch_word.replace(letter, '', 1)
      found_words.append({
        'word': word,
        'importance': importance,
      })
  return found_words


def get_grid():
  board = ''
  while len(board) != GRID_WIDTH * GRID_HEIGHT:
    print 'please enter the grid characters %s' % len(board)
    board = sys.stdin.readline().strip()
  print 'the board is:'
  for y in range(GRID_HEIGHT):
    line = board[y * GRID_WIDTH: y * GRID_WIDTH + GRID_WIDTH]
    print line
  return board

if __name__ == '__main__':
  args = sys.argv[1:]
  dictionary = load_dictionary()
  board = args[0]
  if len(board) != GRID_WIDTH * GRID_HEIGHT:
    board = get_grid()
  print 'what letters are important?'
  important_letters = sys.stdin.readline().strip()
  found = find_words(board, dictionary, important_letters)
  found_importance = sorted(found, cmp=lambda x, y: cmp(x.get('importance'), y.get('importance')))
  found_length = sorted(found, cmp=lambda x, y: cmp(len(x.get('word')), len(y.get('word'))))
  print 'found words, sorted by importance:'
  for word_struct in found_importance:
    print '%s: %d' % (word_struct.get('word'), word_struct.get('importance'))
  print 'longest word: %s' % found_length[-1].get('word')
