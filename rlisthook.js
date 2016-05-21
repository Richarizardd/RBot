module['exports'] = function rlist(hook) {

  // hook.io has a range of node modules available - see
  // https://hook.io/modules.
  // We use request (https://www.npmjs.com/package/request) for an easy way to
  // make the HTTP request.
  var request = require('request');

  // The parameters passed in via the slash command POST request.
  var params = hook.params;

  // Check that the hook has been triggered from our slash command by
  // matching the token against the one in our environment variables.
  if(1) {

    // Set up the options for the HTTP request.
    var options = {

      // Use the Webhook URL from the Slack Incoming Webhooks integration.
      uri: hook.env.rlist_url,

      method: 'POST',

      // Slack expects a JSON payload with a "text" property.
      json: {
        'text': 'Machine Learning Papers:\n1. Veta - https://goo.gl/Y6u7Ij\n2. Malon - https://goo.gl/o5SVWT\n3. Cruz-Roa - https://goo.gl/Lnk6ON\n4. Isaac - https://goo.gl/e1aG40',

        
        // Request that Slack parse URLs, usernames, emoji, etc. in the 
        // incoming text.
        'parse': 'full'
      }
    };

    // Make the POST request to the Slack incoming webhook.
    request(options, function (error, response, body) {
      
      // Pass error back to client if request endpoint can't be reached.
      if (error) {
        hook.res.end(error.message);
      }

      // Finally, send the response. This will be displayed to the user after
      // they submit the slash command.
      hook.res.end('We a real start up now.');
    });

  } else {
    // If the token didn't match, send a response anyway for debugging.
    hook.res.end('Incorrect token.');
  }
};
