from json import load, dump
from os import listdir, remove, close, path
from pathlib import Path
import sys, subprocess, tempfile
import re
import hashlib

def get_json_data(path: Path) -> dict:
  """
		get all data from a json file
  """
  with open(path, "r", encoding="UTF-8") as file:
    return load(file)

def get_markdown_data(path: Path) -> str:
  """
		get text from a Markdown file
  """
  with open(path, "r", encoding="UTF-8") as file:
    return file.read()

def save_in_json(path: Path, data: dict) -> None:
  """
		save the data in path
  """
  with open(path, "w", encoding="UTF-8") as file:
    dump(data, file, indent=2)

def save_in_md(path: Path, text: str) -> None:
  """
		save the text in md file in path
  """
  with open(path, "x", encoding="UTF-8") as file:
    file.write(text)

def make_hash(text: str, n= 6) -> str:
  return hashlib.sha1(text.encode()).hexdigest()[:n]

def list_files(path: Path):
  """
  Lists files and folders within a given path.

  Args:
      path (Path): The path of the folder to list.

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

def search_files(directory: Path, substring: str) -> list[str]:
  """
  Finds files whose names partially or fully match the provided substring,
  only within the directory.

  - Does not perfrom deep searches.
  - Is case-sensitive.

  Args:
    directory (Path): Directory to search within.
    substring (str): Part of the name to search for.

  Returns:
    list(Path): Basenames of files containing `substring` in `directory`.
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

def call_text_editor(editor_name: str, header: str) -> str:

  """
  Open a text editor and wait until the user saves the file.

  Args:
    editor_name (str): Name of the text editor to open.
    header (str): Initial text of document

  Returns:
    document_text (str): Content of the saved file.
  """
  text = ""
  try:
    fd, tmp_path = tempfile.mkstemp(suffix=".md")
    close(fd)

    with open(tmp_path, "w", encoding="utf-8") as f:
      f.write(header)

    subprocess.run([editor_name, tmp_path])
    with open(tmp_path, "r", encoding="utf-8") as f:
      text = f.read()
    
  except FileNotFoundError as e:
    print(f"No file or command found: {e}")

  except PermissionError as e:
    print(f"Permissions problem: {e}")

  except subprocess.CalledProcessError as e:
    print(f"The editor returned an error: {e}")

  except Exception as e:
    print(f"Unexpected error: {e}")

  finally:
    if path.exists(tmp_path):
        remove(tmp_path)

  return text
