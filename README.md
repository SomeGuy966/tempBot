# tempBot

If you want to deploy an updated version of the code to production, you need to do `firebase deploy --only functions`.
A successful merge to the github repo will _NOT_ trigger a prod update.

To test your functions locally:

1. Setup local instance by going to your tempbot directory and running this command: `firebase emulators:start --only functions`
2. Check it's up and running (you should see a line like "All emulators ready! It is now safe to connect your app.")
3. Run this command `curl -X GET http://localhost:5001/tempbot-15da0/us-central1/on_request_example`
