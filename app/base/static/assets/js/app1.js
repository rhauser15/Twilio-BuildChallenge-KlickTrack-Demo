const usernameInput = document.getElementById('username');
const button = document.getElementById('join_leave');
const areaInput = document.getElementById('area');
const serviceInput = document.getElementById('service_name');
const sendInput = document.getElementById('send');
const container = document.getElementById('container');
const count = document.getElementById('count');


function addLocalVideo() {
    fetch('/test')
      .then(function (response) {
          return response.json();
      }).then(function (text) {
          console.log('GET response:');
          console.log(text.greeting);
      });
};

//Provision User during signup.


function connectButtonHandler(event) {
  event.preventDefault();
  let username = usernameInput.value;
   if (!username) {

            alert('Enter your name before connecting');

            return;
        }
  fetch('/provision', {
      method: 'POST',
      body: JSON.stringify({'username': username})
  }).then(function (response) {
          return response.json();
      }).then(function (sid) {
          console.log('GET response2:');
          console.log(sid.sid);
          Status.innerHTML = '&nbsp Success';
      });
};

// 2. Provision phone numbers based on area code.
function areaCodeHandler(event) {
  event.preventDefault();
  let area = areaInput.value;
   if (!area) {

            alert('Enter your name before connecting');

            return;
        }
  fetch('/purchase', {
      method: 'POST',
      body: JSON.stringify({'area': area})
  }).then(function (response) {
          return response.json();
      }).then(function (number) {
          console.log('GET response3:');
          console.log(number.number);
          document.getElementById('purchased_numbers' ).innerHTML += '<li> '+ number.number + ' </li>';;
      });
};

//3. Provision Messaging service.

function messagingServiceHandler(event) {
  event.preventDefault();
  let service_name = serviceInput.value;
   if (!username) {

            alert('Enter your name before connecting');

            return;
        }
  fetch('/provision_m', {
      method: 'POST',
      body: JSON.stringify({'service_name': service_name})
  }).then(function (response) {
          return response.json();
      }).then(function (service) {
          console.log('GET response4:');
          console.log(service.service_name);
          document.getElementById('service_status' ).innerHTML += '<p> Messaging service provisioned: '+ service.service_name + ' </p>';;
      });
};

//4. Assign numbers to messaging service.

function assignNumbers(event) {
  event.preventDefault();
  let assign = 'yes';

  fetch('/assign', {
      method: 'POST',
      body: JSON.stringify({'service_name': service_name})
  }).then(function (response) {
          return response.json();
      }).then(function (service) {
          console.log('GET response5:');
          console.log(service.service_name);
          document.getElementById('assign_status' ).innerHTML += '<p> Numbers successfully assigned </p>';;
      });
};

//8. send message

function sendMessage(event) {
  event.preventDefault();
  let send = sendInput.value;

  fetch('/send', {
      method: 'POST',
      body: JSON.stringify({'send': send})
  }).then(function (response) {
          return response.json();
      }).then(function (service) {
          console.log('GET response5:');
          console.log(service.send);
          document.getElementById('send_status' ).innerHTML += '<p> Message sent </p>';;
      });
};


/*function connect(username) {
    let promise = new Promise((resolve, reject) => {
        // get a token from the back end
        fetch('/provision', {
            method: 'POST',
            body: JSON.stringify({'username': username})
  })
}};*/
/*function updateParticipantCount() {
    if (!connected)
        count.innerHTML = 'Disconnected.';
    else
        count.innerHTML = (room.participants.size + 1) + ' participants online.';
};

function participantConnected(participant) {
    let participantDiv = document.createElement('div');
    participantDiv.setAttribute('id', participant.sid);
    participantDiv.setAttribute('class', 'participant');

    let tracksDiv = document.createElement('div');
    participantDiv.appendChild(tracksDiv);

    let labelDiv = document.createElement('div');
    labelDiv.innerHTML = participant.identity;
    participantDiv.appendChild(labelDiv);

    container.appendChild(participantDiv);

    participant.tracks.forEach(publication => {
        if (publication.isSubscribed)
            trackSubscribed(tracksDiv, publication.track);
    });
    participant.on('trackSubscribed', track => trackSubscribed(tracksDiv, track));
    participant.on('trackUnsubscribed', trackUnsubscribed);

    updateParticipantCount();
};

function participantDisconnected(participant) {
    document.getElementById(participant.sid).remove();
    updateParticipantCount();
};

function trackSubscribed(div, track) {
    div.appendChild(track.attach());
};

function trackUnsubscribed(track) {
    track.detach().forEach(element => element.remove());
};

function disconnect() {
    room.disconnect();
    while (container.lastChild.id != 'local')
        container.removeChild(container.lastChild);
    button.innerHTML = 'Join call';
    connected = false;
    updateParticipantCount();
};

addLocalVideo(); */
document.getElementById("join_leave").addEventListener('click', connectButtonHandler);
document.getElementById("button_purchase").addEventListener('click', areaCodeHandler);
document.getElementById("button_service").addEventListener('click',  messagingServiceHandler);
document.getElementById("button_assign").addEventListener('click',  assignNumbers);
document.getElementById("button_send").addEventListener('click',  sendMessage);