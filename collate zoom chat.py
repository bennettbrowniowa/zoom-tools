import os
import matplotlib.pyplot as plt
# zoom_folder = "C:\\Users\\benne\\Documents\\Zoom"
zoom_folder = "G:\\My Drive\\All IC G drive (BBrown)\\automation\\2021-22 tri 2 zoom chat automate"


def get_all_chat():
    ''' Read meeting_saved_chat.txt in each subfolder of zoom_folder
    ' Returns a list of lists [class/date, sender/recipient, textContent]
    '''
    os.chdir(zoom_folder)
    folders = os.scandir()
    all_chat=[]
    for folder in folders:
        if folder.is_dir():
            chatFileName = os.path.join(folder.path, "meeting_saved_chat.txt")
            try:
                with open(chatFileName, "r") as chatfilehandle:
                    chat = chatfilehandle.readlines()
                for line in chat:
                    try:
                        if line[0] != '\t':
                            all_chat.append([folder.name, line, ""])
                        else:
                            if len(all_chat)==0:
                                pass#print("get all chat: nonerror voice 1: ", all_chat[-1])

                            else:
                                #print("get all chat: nonerror voice 2: ",all_chat[-1])
                                all_chat[-1][2]+=line
                    except:
                        print("get_all_chat: unable to parse line: ", line) # errors from this unicode encoded somehow in chat: ☹️
            except:
                print("get_all_chat: file missing - ",folder.name, " has no meeting_saved_chat.")
                print("line: ", line, len(chat), chat[0])
    print("all_chat contains ", len(all_chat), " entries")
    return all_chat

def parse_chat(chat):
    ''' Accepts a list of [str1, str2, str3] representing one chat where
    ' str1 = filename of zoom folder with date and class period
    ' str2 = line from chat log with sender and recipient
    ' str3 = lines from chat log containing 1 message
    '
    ' Returns a dictionary for the one chat
    '''
    chat_date = chat[0].split(" ")[0]
    start_time = chat[0].split(" ")[1]
    class_period=" ".join(chat[0].split(" ")[2:-1])
    chat_time=chat[1].split(" ")[0]
    try:
        chat_sender=chat[1].split("From ")[1].split(" to ")[0].strip()
    except:
        print("parse_chat exception: ",chat)
    chat_private="Everyone:" not in chat[1]
    chat_content=chat[2].replace("\t","",1)#remove first tab
    first_name = chat_sender.split(" ")[0]
    last_name = " ".join(chat_sender.split(" ")[1:])
    return {"date":chat_date,
            "time":chat_time ,
            "minute":(int(chat_time.split(":")[1]) - int(start_time.split(".")[1])) % 60,
            "class":class_period,
            "student":chat_sender, "first name":first_name, "last name":last_name,
            "private":chat_private,
            "text":chat_content}

def filter_chat(chats, classname=None, start_date=None, end_date=None):
    ''' Accepts a list of chats in dictionary form
    ' Returns a list of chats in attribute-value dictionary pairs
    ' classname!=None : filters, prints a list of classes filtered out
    ' dates!None: independent filters, inclusive
    '''
    if classname:
        chat_subset = filter_chat_by_class(chats, classname)
    else:
        chat_subset = chats
    if start_date or end_date:
        chat_subset = filter_chat_by_date(chat_subset, start_date)
    return chat_subset

def filter_chat_by_class(chats, classname):
    ''' Accepts a list of chats in dictionary form
    ' Returns a list of chats in attribute-value dictionary pairs
    '''
    filtered_chats = []
    excluded_classes = set()
    for chat in chats:
        if chat["class"]==classname:
            filtered_chats.append(chat)
        else:
            excluded_classes.add(chat["class"])
    #print("Excluded classes: ", excluded_classes)
    return filtered_chats

def count_by_student(chats):
    ''' chats is a list of attribute-value dicts
    ' returns a dict of "lastname, firstname":{"count": int, "text":[[date,minute,text],[d,m,t],...]}
    '''
    results = {}
    for chat in chats:
        name = chat['last name'] + ', ' + chat['first name']
        if name not in results:
            results[name]={"count":0,"text":[]}
        results[name]["count"] += 1
        results[name]["text"].append([chat["date"], chat["minute"], chat["text"]])
    return results

# load and parse
all_chat=get_all_chat() #list of (dateclass,timefromto,content)
chat_list_of_dict = list(map(parse_chat, all_chat))
chats = chat_list_of_dict
# replace this line by building a set of keys
classes = ['Pre-Algebra','Algebra II Pd 5 with B Brown', 'Algebra II Pd4 with B Brown', 'Junior High Algebra with B Brown (Pd 1)','HS Algebra (Pd 9 with B Brown)']
class_chat={}
#report number of chats by class
for a_class in classes:
    class_chat[a_class] = filter_chat(chat_list_of_dict,a_class, start_date=None,end_date=None)
    print(a_class, " had ",len(class_chat[a_class]), " chats.")


def print_gradebook_chat_counts(class_chat, show_text=False):
    '''classes is a list of classname strings
    'class_chat is a dictionary with each key a str=a classname
    '''
    classes = class_chat.keys()
    for a_class in classes:
        print()
        print(a_class)
        counts = count_by_student(class_chat[a_class])
        counts_sorted = sorted(counts.keys(), key=str.casefold)
        for name in counts_sorted:
            print(name, ": ", counts[name]["count"])
            if show_text:
                print("\t",counts[name]["text"]) # each students aggregate text
print_gradebook_chat_counts(class_chat)

def histogram_of_session(chats):
    '''chats is a list of dict, each dict is a chat
    ' [{"minute":int}]
    '''
    minutes=[]
    for chat in chats:
        minutes.append(chat["minute"])
    fig, ax = plt.subplots(1,1)
    ax.hist(minutes)
    ax.set_title("# Text responses vs. time into class")
    ax.set_xlabel("Minutes into class")
    ax.set_ylabel("# Text Responses")
    #ax.fig.show()
    return fig, ax

classes = class_chat.keys()
for classname in classes:
    fig, ax = histogram_of_session(class_chat[classname])
    ax.text(0, 0, classname)

def frequency_by_responses(chats):
    '''chats is a list of dict, each dict is a chat
    ' creates a histogram
    '''
    # Get dict of "lastname, firstname":{"count": int, "text":[[date,minute,text],[d,m,t],...]}
    counts = count_by_student(chats)
    count_list = []
    for student in counts:
        count_list.append(counts[student]["count"])
    # Make figure
    fig, ax = plt.subplots(1, 1)
    ax.hist(count_list)
    ax.set_title("# Frequency by Engagement Level")
    ax.set_xlabel("Number of responses in Zoom chat")
    ax.set_ylabel("Frequency (Number of Students)")
    fig.show()
    return fig, ax

for classname in classes:
    fig, ax = frequency_by_responses(filter_chat_by_class(chats,classname))
    ax.text(0,0,classname)
    fig.show()
