
//get API keys

console.log("Signature: ", class1.signature);
userName = "Minion";
classToJoin = class1; //{name:,password:,meetingNumber:}

// Import SDK
// Following developer docs at
// https://marketplace.zoom.us/docs/sdk/native-sdks/web/component-view/import-sdk

const client = ZoomMtgEmbedded.createClient();
let meetingSDKElement = document.getElementById('meetingSDKElement');
client.init({
  debug: true,
  zoomAppRoot: meetingSDKElement,
  language: 'en-US',
  customize: {
    meetingInfo: ['topic', 'host', 'mn', 'pwd', 'telPwd', 'invite', 'participant', 'dc', 'enctype'],
    toolbar: {
      buttons: [
        {
          text: 'Custom Button',
          className: 'CustomButton',
          onClick: () => {
            console.log('custom button');
          }
        }
      ]
    }
  }
});

// Join meeting
// Following dev docs at
// https://marketplace.zoom.us/docs/sdk/native-sdks/web/component-view/meetings


client.join({
	apiKey: apiKey,
	signature: classToJoin.signature,
	meetingNumber: classToJoin.meetingNumber,
	password: classToJoin.password,
	userName: userName
})
/*
//https://marketplace.zoom.us/docs/sdk/video/web/essential/chat
//get chat interface object
const chat = client.getChatClient();
chat.sendToAll('hello everyone');

// send message to everyone
chat.send('hello', userId)

// send message to someone
client.on('chat-on-message', (payload) => {
  const {
    message,
    sender: {
      name: senderName,
      userIdSender,
    },
    receiver: {
      name: receiverName,
      userIdReceiver,
    },
    timestamp
  } = payload;
  console.log(`Message: ${message}, from ${senderName} to ${receiverName}`)
})

//send a chat to a user

var UserIdStudent = userIdReceiver
chat.send('hello', userIdStudent).then(payload => {
  const {
    message,
    receiver: {
      name,
      userIdSender,
    }
  } = payload;
  console.log(`Message: ${message}, from me to ${name}`)
})

//send chat to everyone
chat.sendToAll('hello everyone');

//receive messages
client.on('chat-on-message', (payload) => {
  const {
    message,
    sender: {
      name: senderName,
      userId,
    },
    receiver: {
      name: receiverName,
      userId,
    },
    timestamp
  } = payload;
  console.log(`Message: ${message}, from ${senderName} to ${receiverName}`)
})

*/