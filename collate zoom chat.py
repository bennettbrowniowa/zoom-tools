import os
# zoom_folder = "C:\\Users\\benne\\Documents\\Zoom"
zoom_folder = "G:\\My Drive\\All IC G drive (BBrown)\\automation\\2021-22 tri 2 zoom chat automate"


def get_all_chat():
    os.chdir(zoom_folder)
    folders = os.scandir()
    all_chat=[]
    for folder in folders:
        if folder.is_dir():
            chatFileName = os.path.join(folder.path,"meeting_saved_chat.txt")
            try:
                with open(chatFileName,"r") as chatfilehandle:
                    chat = chatfilehandle.readlines()
                for line in chat:
                    try:
                        if line[0]!='\t':
                            all_chat.append([folder.name,line,""])
                        else:
                            if len(all_chat)==0:
                                pass#print("get all chat: nonerror voice 1: ",all_chat[-1])

                            else:
                                #print("get all chat: nonerror voice 2: ",all_chat[-1])
                                all_chat[-1][2]+=line
                    except:
                        print("get_all_chat: unable to parse line: ",line) # errors from this unicode encoded somehow in chat: ☹️
            except:
                print("get_all_chat: file missing - ",folder.name, " has no meeting_saved_chat.")
                print("line: ",line, len(chat), chat[0])
    print("all_chat contains ",len(all_chat)," entries")
    return all_chat

def parse_chat(chat):
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
            "time":chat_time ,"minute":(int(chat_time.split(":")[1])-int(start_time.split(".")[1]))%60,
            "class":class_period,
            "student":chat_sender,"first name":first_name,"last name":last_name,
            "private":chat_private,
            "text":chat_content}

def filter_chat(chats, classname=None, start_date=None, end_date=None):
    # Accepts a list of chats in dictionary form
    # Returns a list of chats in attribute-value dictionary pairs
    # classname!=None : filters, prints a list of classes filtered out
    # dates!None: independent filters, inclusive
    if classname:
        chat_subset = filter_chat_by_class(chats, classname)
    else:
        chat_subset = chats
    if start_date or end_date:
        chat_subset = filter_chat_by_date(chat_subset, start_date)
    return chat_subset

def filter_chat_by_class(chats, classname):
    # Accepts a list of chats in dictionary form
    # Returns a list of chats in attribute-value dictionary pairs
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
    # chats is a list of attribute-value dicts
    #returns a dict of "lastname, firstname":{"count": int, "text":[[date,minute,text],[d,m,t],...]}
    results = {}
    for chat in chats:
        name = chat['last name']+', '+chat['first name']
        if name not in results:
            results[name]={"count":0,"text":[]}
        results[name]["count"]+=1
        results[name]["text"].append([chat["date"],chat["minute"],chat["text"]])
    return results

# load and parse
all_chat=get_all_chat() #list of (dateclass,timefromto,content)
chat_list_of_dict = list(map(parse_chat, all_chat))
classes = ['Pre-Algebra','Algebra II Pd 5 with B Brown', 'Algebra II Pd4 with B Brown', 'Junior High Algebra with B Brown (Pd 1)','HS Algebra (Pd 9 with B Brown)']
class_chat={}
#report number of chats by class
for a_class in classes:
    class_chat[a_class] = filter_chat(chat_list_of_dict,a_class, start_date=None,end_date=None)
    print(a_class, " had ",len(class_chat[a_class]), " chats.")


def gradebook_chat_counts(class_chat):
    #classes is a list of classname strings
#   #class_chat is a dictionary with each key a str=a classname
#   #
    classes = class_chat.keys()
    for a_class in classes:
        print()
        print(a_class)
        counts = count_by_student(class_chat[a_class])
        counts_sorted = sorted(counts.keys(), key=str.casefold)
        #counts_sorted = [counts[key] for key in sorted(counts.keys)]
        for name in counts_sorted:
            print(name,": ",counts[name]["count"])
            #print("\t",counts[name]["text"])

gradebook_chat_counts(class_chat)
classes = class_chat.keys()