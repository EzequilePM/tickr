"""
Tickr - CLI-based personal agenda.

This script allows the user to manage scheduled events and tags
using command-line arguments.

Available commands:
  add     Add a new event or tag
  (upcoming: list, edit, delete)

Usage example:
  python tickr.py add -f event -g work -t "Meeting" -d 2025-08-03
"""
from tickr import core
from tickr.config import config

from datetime import datetime
import argparse

congif_date_format = config['event']['format_date']

def make_event(arg_dict: dict) -> object:
  """
  Create an instance of the Event calss.
  
  Args:
    arg_dict (dict): Dictionary with keys 'tag', 'title' and 'date'.

  Returns:
    Event: Configured instance of Event class.
  """

  event = core.Event()
  event.set_event(tag=arg_dict["tag"],
                  title=arg_dict["title"],
                  date=datetime.strptime(arg_dict["date"], congif_date_format),
                  description=arg_dict["message"]
                  )
  return event

def main():
  # Ticker inputs
  parser = argparse.ArgumentParser(description="Tickr - agenda CLI")
  input_command = parser.add_subparsers(dest="command", required=True)
  
  ## Command add
  #- tiker.py add
  command_add = input_command.add_parser("add", help="add event/tag to Tickr")

  command_add.add_argument('-f', '--flag', default='event',
                           type=str, help="event, tag")
  
  command_add.add_argument('-g', '--tag', default='defoult',
                      type=str, help="event tag")
  
  command_add.add_argument('-t', '--title',
                      type=str, help="event title")

  command_add.add_argument('-m', '--message', type=str, default="",
                      help="event description")

  command_add.add_argument('-d', '--date',
                      type=str, help="Date to schedule the event")

  # TODO Implement command to list events.

  # TODO Implement command to edit events.

  # TODO Implement command to delete events.
  args = parser.parse_args()

  if args.command == "add":

    if args.message == "":
      pass

    if args.flag == 'event':
      event = make_event(vars(args))

    elif args.flag == 'tag':
      # TODO: Implement tag's utilitis
      pass
    else:
      print("flag input error")
    
  event.save_event()
  print(str(event))
  print("\033[1;32m\nEvent made correctly\033[0m")

main()
