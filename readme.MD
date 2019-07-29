# How To Use
As a user I want to subscribe to a service that I can upload my photo and any company that is part of this service will have their faces blocked.

## Backend (FACE SERVER)
(this is a rough draft from memory)
* Requirements Python 3.6.5
  * install pyenv somehow.
  * pyenv install 3.6.5
  * pyenv init  (put the resulting eval console out in your zshrc or bashprofile)
  * pyenv local 3.6.5 ( i think)
  * pyenv virtualenv python365 (create a virtual env)
  * pyenv activate python365 (activate it) (deactivate it later if you dont needit)
* pip install -r requirements.txt
* set up a config.py and write `YKEY = "<your api key>"`
* ./start.sh (runs the server)
  * Routes will be on the faceserve README. when I have time to write it.
    * The main UI route is /usemetoupload (POST method)

## FrontEnd (YUUBLOCK)
* npm install (8 onwards will work. i'll set up an nvmrc later)
* npm run start (development build)
  * this runs react and the dev server at the same time.
* There's a lot of stuff but the main work will be done in the Components directory in pages. 
* in the root directory create a .env.development file and in it right GATSBY_YKEY which will be the yuuvis api key i'm using. you'll have to refer anything in this as process.env.GATSBY_YKEY. Anything with GATSY_ prefixed will be available client side.

Story so far...
If i have both front end and backend up, FE at 8000 and BE at 5001. I can click an image file wiht my face, submit it and have the backend process it. The processing will censor out my face in any group photo. Backend will save it to the server

to do.
## Present tickets
- [ ] Skip the step where it actually saves it to file, have the server send it to the front end.
- [ ] Have the Group photo be dynamically used.
- [ ] Preview the image after you've selected it.
- [ ] Submit the Group photo and the Censor photo only when both are ready
- [ ] Make the upload button appear only when 2 choices have selected
- [ ] Rewrite The processImage python file to take in Group photo as a param.
- [ ] Finish rewriting the dockerfiles to include in the UNIX way of creating and activating virtual environments for Python.

## stretch goals
- [ ] create a live mode where a local live camera feed will track your face and block it against a group photo you have. (TEST mode)
- [ ] Deploy this app, deploy this server
- [ ] CReate a mobile version of this front end app. (REACT NATIVE)

--- 

CORS, FormDATA, xhr vs fetch vs axios, limitations of python modules


Special thanks to Tim for creating this great Gatsby Material Starter Kit.
Gatsby Material Kit React Starter is the adaptation of [Material Kit React](https://www.creative-tim.com/product/material-kit-react) to [Gatsby](https://www.gatsbyjs.org/)