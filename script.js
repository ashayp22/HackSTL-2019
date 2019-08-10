console.log("hello world");
console.log("working");

var Twit = require("twit");

// Pulling all my twitter account info from another file
var config = require("./config");

// Making a Twit object for connection to the API
var T = new Twit(config);

// File system
var fs = require('fs');
// Request for downloading files
var request = require('request');

// Require child_process for triggering script for python
var exec = require('child_process').exec;

var twitter_handler = "SmileAI10";


var Sentencer = require("sentencer");

Sentencer.configure({
  // the list of nouns to use
  nounList: ["flower", "orchid", "puppy", "pickle", "flute", "student"],

  // the list of adjectives to use
  adjectiveList: ["happy", "ecstatic", "overjoyed", "beaming", "gleeful", "cheery", "delighted", "joyful"]

});

var jokeMaker = require("one-liner-joke");

// T.post('statuses/update', { status: 'hello world!' }, function(err, data, response) {
//   console.log(data)
// })


//every 2 minutes, sees if someone retweetwed your tweet

setInterval(checkHashtag, 1000*60*0.8*1);

function checkHashtag() {
  var params = {
    q: "#hackstlgrinai since:2019-8-1",
    count: 1
  }

  T.get('search/tweets', params, gotData);  //gets the top recent tweets

  function gotData(err, data, response) {

    var all_tweets = data.statuses;

    console.log("here starting")

    console.log(all_tweets)

    if(all_tweets == undefined) {
      console.log("no tweets, undefined");
      return;
    }

    for(var i = 0; i < all_tweets.length; i++) {

      console.log(all_tweets[i].text);

      //someone has tweeted

      //get the data of the tweet
      var media = all_tweets[i].entities.media;
      var reply_to = all_tweets[i].in_reply_to_screen_name;
      var name = all_tweets[i].user.screen_name;
      var id = all_tweets[i].id_str;
      //get the location of the tweet
      var loc = all_tweets[i].location;


      //gets the previous tweet data

      var content = getAllContent()

      if(content.data.id != id) { //make sure it isn't the same tweet from last time
        if(reply_to == twitter_handler) { //make sure it is a reply
          //update name and id
          updateNameId(name, id);
          //now upload media

          if(media == undefined) { //no image provided
            var reply = '@' + name + ' I need an image!';
            T.post('statuses/update', {
                status: reply,
                in_reply_to_status_id: id
              }, tweeted);
          } else {
            var img = media[0].media_url;
            downloadFile(img, 'media'); //download the image
          }
        }
      } else {
        console.log("sorry, already did");
      }

    }

  }
}

checkHashtag();

// Deal with downloading
function downloadFile(url, filename) {

    console.log('Attemping to download url: ' + url + ' to ' + filename);
    // Make the request
    request.head(url, downloaded);


    // Here's the callback for when it is done
    function downloaded(err, res, body) {

      // Look at what it is
      var type = res.headers['content-type'];

      // Figure out what file extension it should have
      var i = type.indexOf('/');
      var ext = type.substring(i + 1, type.length);
      filename = filename + '.' + ext;

      updateExtension(ext);

      // Now save it to disk with that filename
      // Put it in the folder
      request(url).pipe(fs.createWriteStream(filename)).on('close', alter);

      //now we alter the image

      function alter() { //call the  python script, then change the callback to post
        console.log("altering right now");
        var cmd = "py -3.6 script.py";
        exec(cmd, post);
      }

      //now we tweet the image

      function post(err, stdout, stderr) {
        var b64content = fs.readFileSync(filename, {
            encoding: 'base64'
        })

        // Upload the media
        T.post('media/upload', {
            media_data: b64content
          }, uploaded);

        function uploaded(err, data, response) {
          // Now we can reference the media and post a tweet
          // with the media attached
          var mediaIdStr = data.media_id_string;
          var content = getAllContent();
          var faceInfo = getFaceInfo();
/*          var params = {
              status: 'here is the image with glasses @' + content.data.name,
              in_reply_to_status_id: content.data.id,
              media_ids: [mediaIdStr]
            }
*/
          var params;

          //Tweets whether they are smiling or not
          if (faceInfo.isSmiling == "0") {
            console.log("not grinning")


            var j = jokeMaker.getRandomJoke({'exclude_tags': ['dirty', 'racist', 'marriage']});

            params = {
              status: "You are not grinning @" + content.data.name + ". Here's a joke: " + j.body + "",
              in_reply_to_status_id: content.data.id,
              media_ids: [mediaIdStr]
            }

          }
          else {
            console.log("is grinning")
            var adj = Sentencer.make("{{ an_adjective }}");
            var noun = Sentencer.make("{{ noun }}");

            params = {
              status: "You are grinning @" + content.data.name + ". You look like " + adj + " " + noun + ".",
              in_reply_to_status_id: content.data.id,
              media_ids: [mediaIdStr]
            }
          }

          //Post tweet
          T.post('statuses/update', params, tweeted);

          remove(); //remove the image stored
        };
      }

      function remove() { //Now we remove it
        fs.unlinkSync(filename);
      };
    }

}


function getFaceInfo(){
  //get data from json file about the face/mouth
  var contents = fs.readFileSync("smiling.json");
  return JSON.parse(contents);
}

function tweeted(err, success) { //callback for posting
  if (err !== undefined) {
    console.log(err);
  } else {
    console.log('Tweeted: ' + success.text);
  }
}

function getAllContent() { //gets data from the json file about the previous tweet
  var contents = fs.readFileSync("info.json");
  // Define to JSON type
  return JSON.parse(contents);
}

function updateNameId(name, id) { //updates the json file
  var obj = {
   data: {}
 };

 obj.data = {name: name, id: id, extension: 'png'};

 var json = JSON.stringify(obj);
 fs.writeFile('info.json', json, 'utf8', writeCallback);

}

function updateExtension(ext) { //updates the json file
  var obj = {
    data: {}
  };

  var content = getAllContent()

  obj.data = {name: content.data.name, id: content.data.id, extension: ext};
  var json = JSON.stringify(obj);
  fs.writeFile('info.json', json, 'utf8', writeCallback);
}

function writeCallback(err) { //callback for the function above
  console.log("updated node file");
}
