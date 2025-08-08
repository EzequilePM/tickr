from json import load, dump
from os import listdir
import re
import hashlib

def get_json_data(path: str) -> dict:
  """
		get all data from a json file
  """
  with open(path, "r", encoding="UTF-8") as file:
    return load(file)

def get_markdown_data(path: str) -> str:
  """
		get text from a Markdown file
  """
  with open(path, "r", encoding="UTF-8") as file:
    return file.read()

def save_in_json(path: str, data: dict) -> None:
  """
		save the data in path
  """
  with open(path, "w", encoding="UTF-8") as file:
    dump(data, file, indent=2)

def save_in_md(path: str, text: str) -> None:
  """
		save the text in md file in path
  """
  with open(path, "x", encoding="UTF-8") as file:
    file.write(text)
  
def make_hash(text: str, n= 6) -> str:
  return hashlib.sha1(text.encode()).hexdigest()[:n]

def list_files(path):
  """
  Lists files and folders within a given path.

  Args:
      path (str): The path of the folder to list.

  Returns:
      list: A list of file and folder names in the path.
  """
  try:
      contents = listdir(path)
      return contents
  except FileNotFoundError:
      return "The specified path does not exist."
  except Exception as e:
      return f"An error occurred: {e}"

def search_files(directory, substring) -> list[str]:
  """
  Finds files whose names partially or fully match the provided substring,
  only within the directory.

  - Does not perfrom deep searches.
  - Is case-sensitive.

  Args:
    directory (str): Directory to search within.
    substring (str): Part of the name to search for.

  Returns:
    list(str): Basenames of files containing `substring` in `directory`.
  """

  return list(filter(lambda element: search_in_string(element, substring),
                      list_files(directory))
                      )

def search_in_string(text, substring) -> bool:
  """
  Search at least one existence of subString in a text

  Args:
    text (str): search space
    subString (str) 
  """
  return bool(re.search(substring, text))