from time import sleep
from PIL import Image
import win32con as con
import win32api as api
import win32gui as gui
import win32ui as ui

_message_function = api.PostMessage
_window_offset = [8, 31]


def SetWindowOffset(x, y):
    global _window_offset
    _window_offset = [x, y]


def Windows_by_title(title, strict=False, mustVisible=True, case_sensitive=False, limit=-1):
    def enumHandler(hwnd, lParam):
        if (not mustVisible) or gui.IsWindowVisible(hwnd):
            hwndtitle = gui.GetWindowText(hwnd)
            if not case_sensitive:
                hwndtitle = hwndtitle.lower()
            if title == hwndtitle if strict else title in hwndtitle:
                _hwndList.append(hwnd)
                if 1 <= limit <= len(_hwndList):
                    return False

    if not case_sensitive:
        title = title.lower()

    _hwndsCount = 0
    _hwndList = []

    try:
        gui.EnumWindows(enumHandler, None)
    except:
        pass
    return _hwndList


def _ChangeMessageFunction(new_message_function):
    global _message_function
    if new_message_function == 0:
        _message_function = api.PostMessage
    else:
        _message_function = api.SendMessage


def SetPostMessage():
    _ChangeMessageFunction(0)


def SetSendMessage():
    _ChangeMessageFunction(1)


def Screenshot(hwnd):
    left, top, right, bot = gui.GetClientRect(hwnd)
    width = right - left
    height = bot - top
    wDC = gui.GetWindowDC(hwnd)
    dcObj = ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, _window_offset, con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    gui.ReleaseDC(hwnd, wDC)
    gui.DeleteObject(dataBitMap.GetHandle())
    return im


def KeyPress_Down(hwnd, vk):
    _message_function(hwnd, con.WM_ACTIVATE, con.WA_CLICKACTIVE)
    _message_function(hwnd, con.WM_KEYDOWN, vk)


def KeyPress_Up(hwnd, vk):
    # If this doesn't work use KeyPress_StopAll()
    _message_function(hwnd, con.WM_KEYUP, vk)


def KeyPress_StopAll(hwnd):
    _message_function(hwnd, con.WM_ACTIVATE, con.WA_INACTIVE)
    _message_function(hwnd, con.WM_ACTIVATE, con.WA_CLICKACTIVE)


def GetWindowRect(hwnd):
    x0, y0, x1, y1 = gui.GetWindowRect(hwnd)
    x0 += _window_offset[0]
    x1 += _window_offset[0]
    y0 += _window_offset[1]
    y1 += _window_offset[1]
    return x0, y0, x1, y1


def SetWindowSize(hwnd, x=None, y=None, width=None, height=None):
    x0, y0, x1, y1 = GetWindowRect(hwnd)

    if x is None:
        x = x0
    else:
        x -= _window_offset[0]

    if y is None:
        y = y0
    else:
        y -= _window_offset[1]

    if width is None:
        width = x1 - x0

    if height is None:
        height = y1 - y0

    gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)


def GetMousePosForWindow(hwnd):
    mouse_x, mouse_y = gui.GetCursorPos()
    x0, y0, x1, y1 = GetWindowRect(hwnd)
    return mouse_x - x0, mouse_y - y0


def MousePress_Down(hwnd, x, y, teleport=False, teleportDelay=0.1, press=0):
    # If mouse presses work but it's using the mouse's current position, enable teleport.
    # teleport: Teleports the inputted x and y to the mouse's x and y before pressing. It doesn't focus the window.

    mouse_x, mouse_y = gui.GetCursorPos()
    if teleport:
        SetWindowSize(hwnd, mouse_x - x, mouse_y - y, None, None)
        sleep(teleportDelay)

    pos = api.MAKELONG(x, y)
    _message_function(hwnd, con.WM_MOUSEMOVE, 0000, pos)
    # _message_function(hwnd, con.WM_SETCURSOR, 0x000606FE, pos)
    if press == 0:
        _message_function(hwnd, con.WM_LBUTTONDOWN, con.MK_LBUTTON, pos)
    elif press == 1:
        _message_function(hwnd, con.WM_LBUTTONUP, 0000, pos)


def MousePress_Drag(hwnd, x, y, teleport=False, teleportDelay=0.1):
    MousePress_Down(hwnd, x, y, teleport, teleportDelay, None)


def MousePress_Up(hwnd, x, y, teleport=False, teleportDelay=0.1):
    MousePress_Down(hwnd, x, y, teleport, teleportDelay, 1)
