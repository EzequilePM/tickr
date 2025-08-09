from datetime import datetime
from tickr.config import config
from tickr.utils import *

# from tickr.utils import get_annex_data, get_title

class Annex:
  """
    Annex is a `.md` document with more information of event
  """

  def __init__(self, doc_hash: str, text="") -> None:

    self.doc = text
    self.hash = doc_hash

  def save_in(self, dir_path: str) -> str:
    """
      save the instance in `md` file and return the file's path
    """
    file_path = f"{dir_path}/{self.hash}.md"
    save_in_md(file_path, self.doc)

    return file_path

class Event:
  """
  Represents a single calendar event.

  An Event consists of the following components:

  - tag (str):
    Used to categorize or group events.

  - title and description (str):
    The title contains the main information about the event.
    If a description is provided, it is stored in a separate annex file.

  - date (datetime):
    Stores the date and time of the event.
  ---
  # Annex
  The annex file is used to store additional information related to the event.
  It is composed of two parts:
    - A header (internal metadata)
    - A body (the detailed description of the event)
  ---
  """
  def __init__(self):

    """
      Create default instance of Event
    """

    self.tag = ""
    self.title = ""
    self.date = None  # date event
    self.to_annex = "" # Annex file


  def set_event(self, tag: str,
                title: str,
                date: datetime,
                description: str = None
                ):

    """
      Set Event fills
    """

    self.tag = tag
    self.title = title
    self.date = date
    self.to_annex = description

    self.date_day = self.date.strftime(config['event']['format_date'])

  def __str__(self):
    return f"""
    [{self.__class__}]
    {self.tag}
    {self.title} - {self.date_day}
    {self.to_annex}"""

  def save_event(self):
    """
    Save data of this event
    """
    directory = config['event']['path']

    event_hash = make_hash(str(self), config['user']['hash_length'])

    event_path = f"{directory}/tickr-{self.title}_{self.date_day}_{event_hash}.json"

    data = {"title": self.title,
            "tag": self.tag,
            "hash": event_hash,
            "date": self.date.strftime(config['event']['format_date']),
            "annex": Annex(event_hash, f"# {self.title}\n{self.to_annex}").save_in(config['event']['path'])
            }

    save_in_json(event_path, data)

  def load_event(self, file_name: str) -> None:
    """
    Given the event's file_name, which corresponds to the name of the JSON file,
    `load_event` loads the event information into this instance.

    Args:
      file_name(str): The name of JSON file ontaining the event data.
    """
    json_event = get_json_data(file_name)

    self.tag = json_event['tag']
    self.title = json_event['title']
    self.date_day = json_event['date']
    self.date = datetime.strptime(json_event['date'],
                                  config['event']['format_date'])
    self.to_annex = json_event['annex']
