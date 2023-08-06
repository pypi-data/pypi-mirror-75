# PyWebCamWebMonitor
 
This is an app made in Flask and Vue that can help you control your webcams from a web panel, you can see the webcams installed, view them live, setting video resolution, record videos either encoded or unencoded and stream the video( see the video and recording the video in the same time),
download recording and view recordings of encoded videos.


## Requirments


- A Linux Distribution
- FFmpeg program installed( it's available in most distros, example Ubuntu `apt-get install ffmpeg`)
- Some python packages
- python > 3.6

If you install this app using pip the python packages should be installed automatically.

These packages are included in the requirements.txt of the git repo
#
## Installing the app
 
**Method 1 using pip**

run either 

`pip3 install pyWebCamWebServerMonitor`

**Method 2 using git clone**

`git clone https://gitlab.flashsoft.eu/python/flask-pyWebCamWebMonitor`

then you can install using the setup.py:

`cd flask-pyWebCamWebMonitor`

`python3 setup install`

or 

`pip3 -r requirements.txt`

**Installing notes**

The app should work both under a normal Linux user or root, if you want to install it under root you should use `sudo` on the install commands( `pip3 install` or `python3 setup install`)

If you install under normal user be sure that the python bin files are in your environment path, this can be done by adding this in your `.profile` file:

```
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```
## Using the App

After installing it, if you installed using pip or setup.py you can use the command `pyWebCamMonitorCtl` provided by the package to either start/stop the app by using `pyWebCamMonitorCtl start` - `pyWebCamMonitorCtl stop` or you can use `pyWebCamMonitorCtl install-service`(with admin rights) to install the app as a service. 

Using the `pyWebCamMonitorCtl` with no command will print the help of the tool with all possible configurations. 

By default the app will be listening on **http://0.0.0.0:6345**, you can change the port and the listening IP ( either 127.0.0.1 or 0.0.0.0 ) by using `pyWebCamMonitorCtl` 

The web login user and password are **admin:admin** you can change them after you logged in. Settings and the admin user are stored in an SQLite database, in case of database corruption, the database will be recreated using the default user and settings, if admin user has the default password, a notification will be shown at the login screen, to let you know you should change the password. 


If you installed using the git command you can run the `cmds.py` file which is the file that implements the `pyWebCamMonitorCtl` so you can control the app as with `pyWebCamMonitorCtl` the `cmds.py` is located outside of the main python package, in the root of the git repo.

## Important Notes
This app was designed in mind to work on small Linux devices that don't have much CPU power, so you can use an orange pi, or Raspberry pi or any low-end Linux device as a controller for your webcam.

That's why it is recommended to record only in unencoded mode with a small frame rate ( 10-20 ) to require the least possible CPU power. 

On small devices having the CPU at 100% for a long period can freeze your OS due to temperature safety measures. 

Also, unencoded videos aren't yet supported by web browsers but they can be seen in programs like VLC and you can use VLC to encode them, using this app to encode a video will also use a lot of CPU if your device is the low end/embedded. 

If your device is mid-end it should support all functions without consuming much CPU. 

## Some Screenshots

![Screenshot 1](https://lh3.googleusercontent.com/pw/ACtC-3dMyWamZv6nvlVtUmQ5jC1vXCWRCPdWX1Qrp23n-Fg9PLNQSDZB4rZIUuQPtuiSAvj8xulvgzhVKpbwHXaumP3UOCMTJMy8eY56xnER-9yZN5dBxMH_lIokyv3QFS7FSnXqy8PI4uHNAdbjWCkICFer=w634-h322-no)

[Full Image Screenshot 1 Link](https://lh3.googleusercontent.com/pw/ACtC-3dMyWamZv6nvlVtUmQ5jC1vXCWRCPdWX1Qrp23n-Fg9PLNQSDZB4rZIUuQPtuiSAvj8xulvgzhVKpbwHXaumP3UOCMTJMy8eY56xnER-9yZN5dBxMH_lIokyv3QFS7FSnXqy8PI4uHNAdbjWCkICFer)

![Screenshot 3](https://lh3.googleusercontent.com/pw/ACtC-3emaVRk4J4xlAn1rg-adUt-i6nXHbHKlNWwaGWJHiwr2oEpCLVPSBCWOdfU83EvTKE552QqB13rNIgX1SQodN6QP_gBS3uv_2CqZEM0Q0GRFc2a3TkwIRHARTJ3jdGlSn5gFgT3AcPka5V8nbagYkmL=w634-h318-no)

[Full Image Screenshot 2 Link](https://lh3.googleusercontent.com/pw/ACtC-3emaVRk4J4xlAn1rg-adUt-i6nXHbHKlNWwaGWJHiwr2oEpCLVPSBCWOdfU83EvTKE552QqB13rNIgX1SQodN6QP_gBS3uv_2CqZEM0Q0GRFc2a3TkwIRHARTJ3jdGlSn5gFgT3AcPka5V8nbagYkmL)

![Screenshot 3](https://lh3.googleusercontent.com/pw/ACtC-3c2f6JHiXf3xFDrL3rPV0BtCIw98Wd8nf_oxo-JBWZ3l7jw8R-8t5dbEujiDHD_eqx60uPEnoyC_rbn9zRU4VazTh5r3XdjyjX7KFxdTBrLpmGw3qNlFpQMwpyL2nVet3TFd86W37FUZwnHjAh3D5BT=w634-h315-no)

[Full Image Screenshot 3 Link](https://lh3.googleusercontent.com/pw/ACtC-3c2f6JHiXf3xFDrL3rPV0BtCIw98Wd8nf_oxo-JBWZ3l7jw8R-8t5dbEujiDHD_eqx60uPEnoyC_rbn9zRU4VazTh5r3XdjyjX7KFxdTBrLpmGw3qNlFpQMwpyL2nVet3TFd86W37FUZwnHjAh3D5BT)