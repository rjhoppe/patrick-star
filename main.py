import random
# import selenium
from data import * 

class Idiot:
  def __init__(self):
    self.first_name = None
    self.last_name = None
    self.full_name = None
    self.intro = None
    self.random_include_name = random.randint(1, 2)
    self.random_include_greeting = random.randint(1, 4)
    if self.random_include_name == 1:
      self.include_name = True
    else:
      self.include_name = False
    if self.random_include_greeting == 1:
      self.include_greeting = True
    else:
      self.include_greeting = False

  def gen_name(self):
    if self.include_name == True:
      self.first_name = random.choice(first_names)
      self.last_name  = random.choice(last_names)
      self.full_name = self.first_name + ' ' + self.last_name

  def gen_intro(self):
    random_intro = random.randint(1, 10)
    if self.full_name is not None:
      match random_intro:
        case 1:
          self.intro = f'Hello my name is {self.full_name}. '
        case 2:
          self.intro = f"The name's {self.full_name} and "
        case 3:
          self.intro = f"Hi {self.full_name} here "
        case 4:
          self.intro = f'Hi this is ol {self.first_name} '
        case 5:
          self.intro = f'Yo, this is {self.first_name} '
        case 6:
          self.intro = f'Yo this is big {self.first_name} '
        case 7:
          self.intro = f'Good evening. You are speaking to {self.full_name}. '
        case 8:
          self.intro = f'My name is {self.full_name}. I am sure you have heard of me. The {self.last_name}s are quite established in this region. '
        case 9:
          self.intro = f'Hello my name is {self.full_name}. '
        case 10:
          self.intro = f'Hello my name is {self.full_name}. '
    else:
      match random_intro:
        case 1:
          self.intro = 'Hello hope you are doing well. I was hoping I could ask you a question? '
        case 2:
          time_measurement = random.choice(time_measurements)
          self.intro = f'Hey hope you remember me, we met several {time_measurement} ago, haha. '
        case 3:
          self.intro = 'Hi, first of all I love your shoes! '
        case 4:
          self.intro = 'yoo lovin the kicks '
        case 5:
          self.intro = 'Hello! '
        case 6:
          self.intro = 'helllloooooooo! '
        case 7:
          self.intro = 'Hey fellas, '
        case 8:
          time_measurement = random.choice(time_measurements)
          self.intro = f'Hey we met several {time_measurement} ago. '
        case 9:
          self.intro = 'uwu -'
        case 10:
          self.intro = 'Hey, I really dig the shoes. '

  def gen_query(self):
    random_query = random.randint(1, 20)
    match random_query:
      case 1:
        random_shoe_link = random.choice(weird_shoes_urls)
        self.query = f'I am wondering if you have anything like this? {random_shoe_link}. lmk'
      case 2:
        random_shoe_part = random.choice(shoe_parts)
        self.query = f'What is your selection of shoes with {random_shoe_part} on them? thanks'
      case 3:
        random_color = random.choice(random_colors)
        random_shoe = random.choice(kind_of_shoes)
        self.query = f'Do you have any {random_shoe} in {random_color}? Much thanks'
      case 4:
        random_color = random.choice(random_colors)
        self.query = f'How is your selection for things in {random_color}?'
      case 5:
        self.query = "do you have any shoes in size 16? I can fit into a woman's size 19 if that helps"
      case 6:
        self.query = 'Do you do the shoe engraving thing?'
      case 7:
        random_shoe = random.choice(kind_of_shoes)
        self.query = f'do you guys have anything like {random_shoe}?'
      case 8:
        self.query = 'how do you get your foot in the shoe after you put in the shoe tree? I am a little confused as to how this works. thx'
      case 9:
        num = random.randint(1, 13)
        self.query = f"I signed up with {num} different accounts, but I can't use all my codes?"
      case 10:
        random_shoe = random.choice(kind_of_shoes)
        random_sports_team = random.choice(sports_teams)
        self.query = f'can you do {random_shoe} in {random_sports_team} colors?'
      case 11:
        random_choice_1 = random.choice(kind_of_shoes)
        random_choice_2 = random.choice(kind_of_shoes)
        random_choice_3 = random.choice(kind_of_shoes)
        self.query = f'can you do a {random_choice_1}, {random_choice_2}, {random_choice_3} mix?'
      case 12:
        random_shoe = random.choice(kind_of_shoes)
        self.query = f'help find - {random_shoe} :)'
      case 13:
        self.query = 'I am looking for shoes with much comfort in little pay and very stylish'
      case 14:
        self.query = 'how get foot out of shoe? am little stuck for while'
      case 15:
        random_animal = random.choice(random_animals)
        self.query = f'do you have any shoes made out of {random_animal}?'
      case 16:
        random_sports_team = random.choice(sports_teams)
        random_animal = random.choice(random_animals)
        self.query = f'do you have any shoes made out of {random_animal}? And can you do it in {random_sports_team} colors ???'
      case 17:
        self.query = 'Do these shoes come with bluetooth?'
      case 18:
        self.query = 'Are these shoes self cleaning? Do they come with a self cleaning option?'
      case 19:
        self.query = 'can you make shoes that change color based on my mood'
      case 20:
        self.query = 'do you sell shoes in 5s - I can fit in a womans 4 as well'
    return self.query

def submit_annyoing_msg():
  pass

def time_to_annoy():
  PatrickStar = Idiot()
  if PatrickStar.include_name == True:
    PatrickStar.gen_name()

  if PatrickStar.include_greeting == True:
    PatrickStar.gen_intro()

  query = PatrickStar.gen_query()
  if PatrickStar.intro is not None:
    query = PatrickStar.intro + PatrickStar.query

  print(query)

if __name__ == '__main__':
  time_to_annoy()