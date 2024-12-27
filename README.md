# tempBot

## Development cycle

- `git pull`: before you start coding, always make sure you have the latest version of the codebase. This doesn't matter if you're one developer on one machine, but the more machines and developers there are on a project, the more important this becomes.
- make code changes: Tony, you will be mainly changing main.py. Everything else you can consider one-time setup code.
- test changes locally
  - open a terminal and spin up a local emulator of your code using `firebase emulators:start --only functions`
  - wait to see "All emulators ready! It is now safe to connect your app."
  - while keeping the old terminal open and running a new one, enter this command `curl -X GET http://localhost:5001/tempbot-15da0/us-central1/on_request_example`
    - Note that the command changes depending on the endpoint. The actual template for this command is this: `curl -X GET http://localhost:<port you're serving the function emulator on>/<project id>/<region>/<name of endpoint>`. The project id can be found going to firebase --> settings. The region can be found via firebase --> functions --> looking for the row that corresponds to the function & seeing where it's served out of. The name of the endpoint is just the name of the python function (i.e. what's after `def` in main.py).
- if everything looks good, push the changes to github
  - `git add .`
  - `git commit -m"some message"`
  - `git push`
- now, manually push the updated function to production in firebase using `firebase deploy --only functions`
  - You need to do this because a successful merge to the github repo will _NOT_ trigger a prod update.
- now, to be safe, you can test the function in production using `curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://on-request-example-4owbjzhjma-uc.a.run.app`
  - note that the template for this command is `curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" <endpoint address>`

# Explaining the codebase

- the functions folder is where all the firebase function code lives. Don't worry about venv, **pycache**, or .gitignore. The main file you're working on is main.py. The serviceKey.json is used for security certificates & you won't change it.
- the firebase.json and .firebaserc files are just config files, boilerplate that's generated when Kevin ran certain `firebase ...` commands like `firebase init`. You shouldn't have to mess around with these.

# Our tools

1. npm: this is a tool we download from the internet to our mac / windows computers. This allows our terminals / command prompts to download a big world of 3rd party command line tools.
2. firebase: this is an "all in one" platform we use to build commerical level software. It also has a command line tool that we download with npm.
