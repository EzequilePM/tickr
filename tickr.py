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
from tickr.utils import search_files, call_text_editor
from datetime import datetime
from typing import Any
import argparse
from sys import stdin
from os import remove, path, environ

hash_length: int = config['user']['hash_length']
text_editor: str = config['user']['text_editor']
config_date_format = config['event']['format_date']
dir_path = config['event']['path']

def match_in_files(dir_path: str, subString: str) -> list[str]:
  """
  filter events by word match

  Args:
    subString (str): Internal string in file name.
    dir_path (str): Path of directory event.
  
  Returns:
    list(str): List of event path that content `subString`
  """
  rule_event = "^tickr-.+{}.+\.json$"
  events_json_names = search_files(dir_path, rule_event.format(subString))
  return list(map(lambda json: f"{dir_path}/{json}", events_json_names))

def header_annex(to_event:dict) -> str:
  ancho = max(len(to_event['title']), len(to_event['tag']))
  return f"""- {to_event['tag']}
- {to_event['date']}
{'-' * ancho}"""

def get_dict_event(event_path: str) -> dict[str, Any]:
  """
  Load and return the event data from file paths.

  Args:
    event_path (str): path of json event.

  Returns:
    dict(str, Any): dict with the info of event.
  """
  event = core.Event()
  event.load_event(event_path)
  return event.__dict__

def get_dicts_of_events(event_paths: list[str]) -> list[dict[str, Any]]:
  """
  Load and return the event data from a list of file paths.


  Args:
    event_paths (list(str)): List of events paths.
  Returns:
    list[dict(str, Any)]: A list of dictionaries containing event data.
  """

  return list(map(get_dict_event, event_paths))

def set_format_preferences(data_of_event: dict[str, str]) -> dict[str, str]:
  """
  Applies a format to the values(str) with the specific keys in the provided dictionary.
  """
  # TODO: Add customization configs
  if len(data_of_event['title'])>25:
    title = data_of_event['title']
    data_of_event['title'] = title[:22] + "..."

  return data_of_event

def list_of_events(event_paths: list[str]) -> None:
  """
  Print a summary of all saved events to the console.
  Args:
      event_paths (list(str)): List of events  paths
    Returns:
      str: Printed output with a list display of events
  """

  event_dicts = get_dicts_of_events(event_paths)
  for data_of_event in  map(set_format_preferences, event_dicts):

    print(f"{data_of_event['title']:<25}{data_of_event['tag']:<20}{data_of_event['date']}   |{data_of_event['to_annex']}")


def list_full_events(event_paths: list[str]) -> None:
    """
    Print a detailed list of all events (excluding annex content).

    Args:
      event_paths (list[str]): List of paths to event files.

    Returns:
      str: Printed output with a separator line and event data.
    """
    event = core.Event()

    for event_path in event_paths:
      event.load_event(event_path)
      print(f"{'-' * 50}\n{str(event)}")

def make_event(arg_dict: dict) -> core.Event:
  """
  Create an instance of the Event class.

  Args:
    arg_dict (dict): Dictionary with keys 'tag', 'title' and 'date'.

  Returns:
    Event: Configured instance of Event class.
  """

  event = core.Event()
  event.set_event(tag=arg_dict["tag"],
                  title=arg_dict["title"],
                  date=datetime.strptime(arg_dict["date"], config_date_format),
                  description=arg_dict["message"]
                  )
  return event

def main():
  global text_editor
  # Ticker inputs
  parser = argparse.ArgumentParser(description="Tickr - agenda CLI")
  input_command = parser.add_subparsers(dest="command", required=True)

  ## Command add
  #- tiker.py add
  command_add = input_command.add_parser("add", help="add event/tag to Tickr")

  command_add.add_argument('-f', '--flag', default='event',
                           type=str, help="event, tag")

  command_add.add_argument('-g', '--tag', default='default',
                      type=str, help="event tag")

  command_add.add_argument('-t', '--title',
                      type=str, help="event title")

  command_add.add_argument('-m', '--message', type=str, default="",
                      help="event description")

  command_add.add_argument('-d', '--date',
                      type=str, help="Date to schedule the event")



  command_ls = input_command.add_parser("ls", help="List all events")

  command_ls.add_argument('-f', '--flag', default='event',
                           type=str, help="event, tag")

  command_ls.add_argument('-l', '--list', action="store_true",
                           help="format of list as ls command")

  command_ls.add_argument('-m', '--match', default="",
                           type=str, help="Applay search by match")

  command_edit = input_command.add_parser("edit", help="Allows you to modify an event or tag")

  command_edit.add_argument('-f', '--flag', default='event',
                           type=str, help="event, tag")

  command_edit.add_argument('-o', '--old_event', default="",
                           type=str, help="Full path of the old event")

  command_edit.add_argument('-t', '--title', default="",
                           type=str, help="Remplase old title with new title")

  command_edit.add_argument('-a', '--annex_path', default="",
                           type=str, help="Remplase old annex with new annex file")

  command_edit.add_argument('-g', '--tag', default="",
                           type=str, help="Remplase old tag with new tag")

  command_edit.add_argument('-d', '--date', default="",
                           type=str, help="Remplase old date with new date")
  
  command_edit.add_argument('-m', '--match', default="",
                           type=str, help="Applay search by match")

  command_delete = input_command.add_parser("delete", help="Delete an event")

  command_delete.add_argument('-f', '--flag', default='event',
                           type=str, help="event, tag")

  command_delete.add_argument('-n', '--name', required=True,
                              type=str, help="Name of event file")
  
  command_delete.add_argument('-s', '--skip-verify',
                              action="store_true", help="Skips deletion confirmations")
  
  command_delete.add_argument('-a', '--remove-annex',
                               action="store_true", help="delete annex file and kept the event")
  
  command_delete.add_argument('-e', '--remove-event',
                               action="store_true", help="delete event file and kept the annex")
  
  command_delete.add_argument('-m', '--match', default="",
                               type=str, help="Applay search by match")

  args = parser.parse_args()
  type_element = args.flag

  if type_element == 'event':
    if args.command == "add":

      if stdin.isatty():
        # tty input
        editor_from_env = environ.get(text_editor)
        if editor_from_env:
          text_editor = editor_from_env

        args.message = call_text_editor(text_editor, header_annex(vars(args))) if not args.message else args.message
        
      if args.title is None:
        print("\033[1;31m[ERROR] Event title is required\033[0m")
        return

      try:
        event = make_event(vars(args))
        event.save_event()
        print(str(event))

      except TypeError:
        print("\033[1;31m[ERROR] Date of event not entered\033[0m")

      except ValueError:
        print(f"\033[1;31m[ERROR] The format of the date '{args.date}' of format is not valid")
        print(f"Expected format: {config_date_format}\033[0m")

    elif args.command == 'ls':
      event_paths = match_in_files(dir_path, args.match)      
      if args.list:
        list_of_events(event_paths)
      else:
        list_full_events(event_paths)

    elif args.command == 'edit':

      if args.old_event:
        path_to_edit_event = args.old_event
      elif args.match:
        candidates = match_in_files(dir_path, args.match)
        if len(candidates) == 1:
          path_to_edit_event = candidates[0]
        
        elif len(candidates) == 0:
          print("\033[1;33m[INFO]","No event matches\033[1;0m")
          
        else:
          print("\033[1;33m[INFO]","Multiple events coincide\033[1;0m")
          list_of_events(candidates)
          exit(1)

      # TODO: edit events.
      # Modify Event class to save hash.
      # TODO: Add: checks and error messages.


      to_edit_event = core.Event()
      to_edit_event.load_event(path_to_edit_event)
      print(to_edit_event)

      # Set vlaues
      to_edit_event.title = args.title if args.title != "" else to_edit_event.title
      to_edit_event.annex = args.annex_path if args.annex_path != "" else to_edit_event.to_annex
      to_edit_event.tag = args.tag if args.tag != "" else to_edit_event.tag

      if args.date != "":
        to_edit_event.date = datetime.strptime(args.date, config_date_format)

      to_edit_event.save_event()
      remove(path_to_edit_event)

    elif args.command == 'delete':

      event_to_delete = args.name
      event = core.Event()
      delete_path = path.join(dir_path, event_to_delete) 
      try:
        event.load_event(delete_path)
      except FileNotFoundError:
        print(f"\033[1;33m Event file '{delete_path}' not found.\033[1;0m")
        exit(1)

      annex_path = event.to_annex

      print("\033[1;33m[INFO]","The event does not have an annex file\033[1;0m" if annex_path is None else f"The event has an annex file: {annex_path}\033[1;0m")
      # manual verification:
      if not args.skip_verify:
        if args.remove_event:
          manual_delet_event = input(f"Are you sure to delete:  {event_to_delete}\n").strip().upper()
        
        if args.remove_annex:
          manual_delet_annex = input("Delete annex file?\n").strip().upper()

      if (args.skip_verify or manual_delet_event) and args.remove_event :

        try:
          remove(delete_path)
        except FileNotFoundError:
          print(f"\033[1;31m[ERROR] Event file not found\033[1;0m")
          exit(1)

        except PermissionError:
          print(f"\033[1;31m[ERROR] Permission denied when trying to access file {delete_path}\033[1;0m")
          exit(1)

        print(f"\033[1;33m[INFO] Deleted evnet file: {event_to_delete}\033[1;0m")

      if (args.skip_verify or manual_delet_annex) and args.remove_annex:
        try:
          if path.exists(annex_path):
            remove(annex_path)

          else:
            print(f"Annex files '{annex_path}' do not exist, nothing to delete.\033[1;0m")

        except FileNotFoundError:
          print(f"\033[1;31m[ERROR] Event file not found\033[1;0m")
          exit(1)

        except PermissionError:
          print(f"\033[1;31m[ERROR] You do not have permission to interact with the file {annex_path}\033[1;0m")
          exit(1)

        #Event does not have an annex file
        event.to_annex = None
        print(f"\033[1;33m[INFO] Deleted annex file: {annex_path}\033[1;0m")

    else:
      print(f"\033[1;31m[ERROR] Unknown command {args.command}.\033[0m")

  elif args.flag == 'tag':
    # TODO: Implement tag's utilitis
    pass

  else:
    print("\033[1;31m[ERROR] Unknown flag. Use 'event' or 'tag'.\033[0m")

if __name__ == '__main__':
  main()
