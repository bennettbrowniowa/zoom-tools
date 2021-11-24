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
                    if line[0]!='\t' or len(all_chat)==0:
                        all_chat.append([folder.name,line,""])
                    else:
                        all_chat[-1][2]+=line
            except:
                print(folder.name, " has no meeting_saved_chat.")
    print("all_chat contains ",len(all_chat)," entries")
    return all_chat

def parse_chat(chat):
    chat_date=chat[0].split(" ")[0]
    class_period=" ".join(chat[0].split(" ")[2:-1])
    chat_time=chat[1].split(" ")[0]
    try:
        chat_sender=chat[1].split("From ")[1].split(" To ")[0]
    except:
        print("parse_chat exception: ",chat)
        chat_sender=chat[2]
    chat_private="Everyone:" not in chat[1]
    chat_content=chat[2]
    return {"date":chat_date,
            "class":class_period,
            "student":chat_sender,
            "private":chat_private,
            "text":chat_content}

def filter_chat(chats, classname=None, start_date=None, end_date=None):
    # Accepts a list of chats in dictionary form
    # Returns a list of chats in attribute-value dictionary pairs
    # classname!=None : filters, prints a list of classes filtered out
    # dates!None: independent filters, inclusive
    filtered_chats = []
    excluded_classes = set()
    for chat in chats:
        if classname:
            if chat["class"]==classname:
                filtered_chats.append(chat)
            else:
                excluded_classes.add(chat["class"])
    if classname:
        print("Excluded classes: ", excluded_classes)
    return filtered_chats

all_chat=get_all_chat() #list of (dateclass,timefromto,content)
chat_list_of_dict = list(map(parse_chat, all_chat))
preal = filter_chat(chat_list_of_dict,'Pre-Algebra')
#'Algebra II Pd 5 with B Brown', 'Algebra II Pd4 with B Brown', 'Junior High Algebra with B Brown (Pd 1)','HS Algebra (Pd 9 with B Brown)'
