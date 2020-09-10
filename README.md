# Ultra Simple Screen Recorder
This program is for recording screen on Linux. This program utilizes ffmpeg's kmsgrab capture and vaapi encoding to achieve highest possible performance at least on ~~our~~ my laptop. 

Currently only Arch Linux, X11 (and maybe intel iGPUs) is supported. Wayland is supported, but keyboard capture only work with a Xwayland window (firefox etc) in focus.

# Install
Ensure `community/intel-media-driver`, `aur/ffmpeg-vaapi-crop`, `aur/lemonbar-xft-git` and is installed.

DE/WM with `notify-send` support is also required.

1. `# setcap cap_sys_admin+ep /usr/bin/ffmpeg`
2. `$ git clone https://github.com/Saren-Arterius/ussr.git && cd ussr`
3. `# pip install -r requirements.txt`

# Config
Open `ussr.py`, the variables and comments are self-explanatory.

# Usage

1. `$ python3 ussr.py`
2. Move the cursor to the left top desired record area, then press right Shift.
3. Move the cursor to the right bottom desired record area, then press right Shift. You should see a blue box indicating the record area.
4. Press right Shift again to start record.
5. When finished, press right Shift again to stop record. The save location will be automatically opened in your file manager.
6. If you need to change record area, press Esc and go to 2.
7. To exit, press Esc again after Esc is pressed. In other words, press Esc twice.

# Library used
1. https://github.com/phuhl/notify-send.py
2. https://github.com/JeffHoogland/pyxhook/
