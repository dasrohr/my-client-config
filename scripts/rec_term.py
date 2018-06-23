import os
import json
import glob
import re
import argparse
import PyZenity
import datetime
import string
import random
import subprocess

# global settings
path = os.environ['HOME'] + '/.rec_term/'
try:
  recording = os.environ['ASCIINEMA_REC']
except KeyError:
  recording = False

# meta data object definition
class meta_data(object):
  '''
  define the metadata object
    self.descr      = description                             str      (default None)
    self.date       = date-stamp the recording started        date-str (default now)
    self.wrms       = wrms nuber the recording is related to  int      (default None)
    self.file_meta  = name meta file      - no full path      str      (required)
    self.file_rec   = name recording file - no full path      str      (required)
  return the descriptor of the created object
  '''
  def __init__(self, file_meta, descr=None, wrms=None, date=str(datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S'))):
    self.descr     = descr
    self.date      = date
    self.wrms      = wrms
    self.file_rec  = file_meta[:-5]
    self.file_meta = file_meta

  def search(self, regex):
    '''
    search for regex string in all attributes and return object descriptor if match
    '''
    for attr, value in self.__dict__.iteritems():
      if ( value != None and re.match(regex, value)):
        return self

  def user_input(self):
    '''
    open dialogs to the user to input or edit attributes
    '''
    self.descr = PyZenity.GetText(text='Enter a Description:')
    self.wrms  = PyZenity.GetText(text='Enter a WRMS Number this is related to:')

  def write(self, root_path):
    '''
    write the object attributes to file
    '''
    # create touple to build json format
    data = { 
    'description' : self.descr,
    'date' : self.date,
    'wrms' : self.wrms,
    'meta' : self.file_meta
    }
    # write the data
    with open(root_path + self.file_meta, 'w') as file:
      json.dump(data, file)
      file.write('\n')

################################################################################################################

# Global Functions #
####################
def generate_filename(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
  '''
  generate a random string with a length og size= and return it together with the same sting and a '.meta' suffix
  '''
  name = ''.join(random.choice(chars) for _ in range(size))
  return name + '.meta'

def cinema(action, path, meta_object):
  '''
  build the command chain to execute asciinema
  '''
  cinema_cmd = ['asciinema', action]
  if ( action == 'rec' or action == 'play' ):
    cinema_cmd.append('-i 2')
  if action == 'rec':
    if append:
      cinema_cmd.append('--append')
    cinema_cmd.append('-q')
  if action == 'play':
    cinema_cmd.append('-s 2')
  cinema_cmd.append(path + meta_object.file_rec)
  subprocess.call(cinema_cmd)

def user_selection():
  # create objects from meta data of all records
  meta_objects = []
  meta_objects_filtered = []
  for file_meta in glob.glob(path + '/*.meta'):
    with open(file_meta, 'r') as json_file:
      data = json.load(json_file)
      meta_objects.append(meta_data(data['meta'],data['description'],data['wrms'],data['date']))
  # ask for a filter
  filter = PyZenity.GetText(text='Enter filter to filter recordings (empty for *)')
  # perform search on objects if we have a filter
  if filter:
    filter = re.compile('(?i).*%s.*'%filter)
    for meta_object in meta_objects:
      result = meta_object.search(filter)
      if result:
        meta_objects_filtered.append(result)
  else:
    meta_objects_filtered = meta_objects

  # build list for zenity dialog
  list = []
  cnt=0
  for meta_object in meta_objects_filtered:
      if meta_object.wrms is None:
        meta_object.wrms = ' '
      if meta_object.descr is None:
        meta_object.descr = ' '
      list.append([meta_object.date, meta_object.wrms, meta_object.descr, cnt])
      cnt = cnt + 1
  # show dialog with filtered data
  selection = PyZenity.List(["Date","WRMS","Description","hidden"], title="Select a Record", select_col=4, hide_col=4, midsearch=True, data=list)
  if not selection:
    # we choose nothing, exit
    exit()

  return meta_objects_filtered[int(selection[0])]

################################################################################################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='asciinema recording organizer')
  parser.add_argument("action", type=str, help='the action we are going to do (record|play|cat|rename)')
  parser.add_argument("-e", "--empty_meta", help='do not ask for metadata on start', action="store_true")
  parser.add_argument("-a", "--append", help='append to an existing record', action="store_true")
  args = parser.parse_args()

  if args.empty_meta:
    empty_meta = True
  else:
    empty_meta = False
  
  if args.append:
    append = True
  else:
    append = False

  if args.action in ('record', 'rec', 'r'):
    if append:
      meta_object = user_selection()
    else:
      # create filenames
      file_meta = generate_filename(size=12)
      # create the object
      meta_object = meta_data(file_meta)
      if not empty_meta:
        meta_object.user_input()
      meta_object.write(path)
    # set the metadata-file as bash-env-variable so that if we are going to edit the description while recording, 
    #  we can refer to the file we are currently recording
    os.environ["ASCIINEMA_META"] = meta_object.file_meta
    cinema('rec', path, meta_object)

  elif args.action in ('play', 'pl', 'p', 'replay', 'repl'):
    meta_object = user_selection()
    cinema('play', path, meta_object)

  elif args.action in ('cat', 'c'):
    meta_object = user_selection()
    cinema('cat', path, meta_object)

  elif args.action in ('rename', 'ren', 're'):
    if recording:
      file_meta = path + os.environ['ASCIINEMA_META']
      with open(file_meta, 'r') as json_file:
        data = json.load(json_file)
        meta_object = (meta_data(data['meta'],data['description'],data['wrms'],data['date']))
    else:
      meta_object = user_selection()
    try:
      meta_object.descr = PyZenity.GetText(text='Enter new Description:', entry_text=meta_object.descr)
      meta_object.wrms  = PyZenity.GetText(text='Enter new WRMS number:', entry_text=meta_object.wrms)
    except TypeError:
      print('nothing selected')
      exit()

    meta_object.write(path)

  elif args.action in ('delete', 'del', 'd'):
    meta_object = user_selection()
    if ( recording and os.environ['ASCIINEMA_META'] == meta_object.file_meta ):
      print('you selected the data from the current session to delete. do not do that :(')
      exit()
    try:
      os.remove(path + meta_object.file_meta)
      os.remove(path + meta_object.file_rec)
    except OSError:
      print('missing files')

  else:
    print('\
    start recording:                record, rec, r\n\
    replay recording:               replay, repl, play, p\n\
    cat out:                        cat, c\n\
    rename old or current record:   rename, ren, re\n\
    delete recording:               delete, del, d\n\
    ')
