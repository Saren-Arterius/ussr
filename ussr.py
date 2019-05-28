#!/usr/bin/env python3
from subprocess import call, Popen
from os.path import dirname, realpath, join
from time import sleep, time
import pyxhook

TRIGGER_KEY = 'Shift_R' # https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
ESC_KEY = 'Escape'
SAVE_LOCATION = '/tmp' # Video out location
VC = 'hevc_vaapi' # or h264_vaapi
FRAMERATE = 60
QP = 18 # Video quality, lower (=> 0) is better, higher (=> 51) is worse

SCRIPT_PATH = realpath(dirname(__file__))
NOTIFY_SEND_PATH = join(SCRIPT_PATH, './notify-send.py')
hm = pyxhook.HookManager()

points_x = []
points_y = []
left_top = ()
right_bottom = ()
bar = None
process = None
state = 0
out_file = None


def notify(msg):
    call(f'python3 {NOTIFY_SEND_PATH} --replaces-process ussr \'{msg}\' &',
         shell=True)


def kbevent(e):
    global state, left_top, right_bottom, process, out_file, bar
    if e.Key == ESC_KEY:
        if state != -1:
            try:
                process.terminate()
            except:
                pass
            try:
                bar.terminate()
            except:
                pass
            state = -1
            notify(f'Config has been reset. Press {ESC_KEY} again to exit.\rPress {TRIGGER_KEY} to set point 1.')
        else:
            notify(f'USSR exited.')
            exit()
    elif e.Key == TRIGGER_KEY:
        if state in [-1, 0]:
            points_x.clear()
            points_y.clear()
            if hm.mouse_position_x == -1:
                notify(f'Please move the cursor a bit.')
            else:
                points_x.append(hm.mouse_position_x)
                points_y.append(hm.mouse_position_y)
                state = 1
                notify(
                    f'Point 1 set to ({points_x[0]},{points_y[0]}).\rPress {TRIGGER_KEY} to set point 2.')
        elif state == 1:
            points_x.append(hm.mouse_position_x)
            points_y.append(hm.mouse_position_y)
            points_x.sort()
            points_y.sort()
            left_top = points_x[0], points_y[0]
            right_bottom = points_x[1], points_y[1]
            l, t, w, h = left_top[0], left_top[1], (right_bottom[0] -
                                                    left_top[0]) + 1, (right_bottom[1] - left_top[1]) + 1
            try:
                bar = Popen(
                    f'timeout 3 lemonbar -d -n "my_lemonbar" -g {w}x{h}+{l}+{t} -B "#44005588"', shell=True)
            except:
                pass
            notify(
                f'Point 2 set. Rect={left_top} ↘ {right_bottom} [{w}x{h}].\rPress {TRIGGER_KEY} to start recording.')
            state = 2
        elif state == 2:
            try:
                bar.terminate()
            except:
                pass
            l, t, w, h = left_top[0], left_top[1], (right_bottom[0] -
                                                    left_top[0]) + 1, (right_bottom[1] - left_top[1]) + 1
            out_file = join(SAVE_LOCATION, f'{time()}.mp4')
            command = f"""LIBVA_DRIVER_NAME=iHD ffmpeg -y \
        -device /dev/dri/card0 -f kmsgrab -framerate {FRAMERATE} -i - \
        -vaapi_device /dev/dri/renderD128 -vf 'hwmap=derive_device=vaapi,crop={w}:{h}:{l}:{t},scale_vaapi=format=nv12' \
        -c:v {VC} -qp:v {QP} \
        {out_file}"""
            print(command)
            process = Popen(command, shell=True)
            notify(f'Started recording. Press {TRIGGER_KEY} to stop and exit.')
            state = 3
        elif state == 3:
            process.terminate()
            notify(f'Stopped recording and exited USSR. Output file saved to:\r{out_file}')
            call(['xdg-open', SAVE_LOCATION])
            sleep(1)
            exit()


if __name__ == "__main__":
    hm.KeyDown = kbevent
    hm.HookKeyboard()
    hm.HookMouse()
    hm.start()

    notify(f'Press {TRIGGER_KEY} to set point 1.')
