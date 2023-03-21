import string
from nltk.corpus import stopwords

MSG_OVER = 800 
MSG_UNDER = 30
ROBO_LIMIT = 9600 
STOP_WORDS = stopwords.words('english') 

def anon(data):
    if type(data) == dict:
        data = data.values()
    return data


def sift(node):
    area = node['content']
    squatter = node['name']
    side = len(area)
    if side < MSG_UNDER or side > MSG_OVER or 'http' in area:
        return None
    area = "".join([block for block in area if block not in string.punctuation and block not in "0123456789"])
    area = " ".join([a for a in area.split(" ") if a not in STOP_WORDS])
    biscuit = f"{squatter}@{area}"
    return biscuit


def chop(ginger):
    counter = 0
    loads = []
    mainload = ""
    for node in ginger:
        valid = sift(node)
        if not valid:
            continue
        if counter >= ROBO_LIMIT:
            loads.append(mainload)
            mainload = valid 
            counter = len(mainload)
        else:
            mainload = mainload + ". " + valid
            counter = len(mainload)
    loads.append(mainload)
    return loads

PROMPTS = {
    'summarize': 'Given the following  sequence of messages with usernames delimited by an @ symbol,  summarize the discussion and add some context to any popular topics: ',
    'story': 'Given the following sequence of messages, write a short story about the themes and actions discussed in the style of Ryunosuke Akutagawa: ',
}
def package(data):
    data = anon(data)
    lunch_tray = [{
        'model': 'text-davinci-003',
        'max_tokens': 1024,
        'prompt': PROMPTS['summarize'] + ff + "{}", 
        'temperature': 1.25 
    } for ff in chop(data)]
    return lunch_tray
