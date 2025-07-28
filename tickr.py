from tickr import core
from tickr.config import config
import datetime, argparse

def main():
  parser = argparse.ArgumentParser(description="Tickr - Agenda de consola")
  # add
  parser.add_argument('--add', action='store_true', help="Agrega un nuevo evento")
  
  parser.add_argument('-t', '--tag', default="EVENT",
                      type=str, help="etiqueta del evento")
  
  parser.add_argument('-T', '--title',
                      type=str, help="titulo del evento")

  parser.add_argument('-l', '--long_description',
                      help="descripción del evento")

  parser.add_argument('-d', '--date',
                      type=str, help="Dia del evento")

  args = parser.parse_args()

  if args.add:

    event = core.Event()
    event.set_event(args.tag, args.title,
                    datetime.datetime.strptime(args.date,
                                               config['event']['format_date']))
  
  if args.long_description:

    description = input("descripción:\n")

    event.set_event(args.tag, args.title,
                    datetime.datetime.strptime(args.date,
                                               config['event']['format_date']),
                                               description)


    event.save_event()
    print(str(event))

    
main()
