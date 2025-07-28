from json import load, dump
#from tickr.config import config
import hashlib

def get_json_data(path: str) -> dict:
  """
		get all data form a json fill
  """
  with open(path, "r", encoding="UTF-8") as file:
    return load(file)
  
def save_in_json(path: str, data: dict) -> None:
  """
		save the data in path
  """
  with open(path, "w", encoding="UTF-8") as file:
    dump(data, file, indent=2)

def save_in_md(path: str, text: str) -> None:
  """
		save the text in md fill in path
  """
  with open(path, "x", encoding="UTF-8") as file:
    file.write(text)
  
def make_hash(text: str, n= 6) -> str:
  return hashlib.sha1(text.encode()).hexdigest()[:n]

