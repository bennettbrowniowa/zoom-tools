import hashlib
import hmac
import base64
import time
host = 1 #change to 0 for non-host, 1 for host
def generateSignature(data):
    ts = int(round(time.time() * 1000)) - 30000;
    msg = data['apiKey'] + str(data['meetingNumber']) + str(ts) + str(data['role']);
    message = base64.b64encode(bytes(msg, 'utf-8'));
    # message = message.decode("utf-8");
    secret = bytes(data['apiSecret'], 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256);
    hash =  base64.b64encode(hash.digest());
    hash = hash.decode("utf-8");
    tmpString = "%s.%s.%s.%s.%s" % (data['apiKey'], str(data['meetingNumber']), str(ts), str(data['role']), hash);
    signature = base64.b64encode(bytes(tmpString, "utf-8"));
    signature = signature.decode("utf-8");
    return signature.rstrip("=");

def parse_meeting_link(meeting_link):
    meeting_number, password = meeting_link.split("?pwd=")
    meeting_number = int(meeting_number.split("/j/")[1])
    return meeting_number, password

def header_of_js(jsfile):
    jsfile.write('// This file created by Python.\n')
    jsfile.write('// Change content by changing the Python input file.\n')
    jsfile.write('\n')
    jsfile.write('var apiKey= "'+apiKey+'";\n')
    jsfile.write('\n')
    jsfile.write('var classes = [];\n')
    jsfile.write('\n')

def js_for_one_class(jsfile):
    jsfile.write('var class1 = Object();\n')
    jsfile.write('class1["name"] = "' + class_name + '";\n')
    jsfile.write('class1["password"] = "' + meeting_password + '";\n')
    jsfile.write('class1["meetingNumber"] = "' + str(meeting_number) + '";\n')
    jsfile.write('class1["signature"] = "' + signature + '";\n')
    jsfile.write('classes.push(class1);\n')
    jsfile.write('\n')

# The API key and API secret key are specific to your zoom user,
# and created by activating a free zoom dev account.
# To keep them private from piblic git commits, they are in a separate gitignored file
from zoom_links import apiKey, apiSecret, class_name_links
data={'apiKey': apiKey , 'apiSecret': apiSecret, 'role': host}

# Initialize outputs
jsfile = open("zoom_api_keys.js","w")
header_of_js(jsfile)
text_output=""

for class_name_link in class_name_links:
    class_name, class_link = class_name_link
    meeting_number, meeting_password = parse_meeting_link(class_link)
    data["meetingNumber"] = meeting_number
    signature = generateSignature(data)
    # Three kinds of output
    text_output += class_name + ": " + signature +"\n"
    js_for_one_class(jsfile)

print(text_output)
jsfile.close()