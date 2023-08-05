A library used to control programs(mainly games) without focusing them.  
This isn't guaranteed to work and will sometimes require to be very creative with how you perform actions.  
Example:
```
hwnd = Windows_by_title('GamesTitle', strict=True)[0]

# Open up menu(It doesn't close it)
KeyPress_Down(hwnd, VK_ESCAPE)
KeyPress_Up(hwnd, VK_ESCAPE)

# Press the right key
KeyPress_Down(hwnd, VK_RIGHT)
KeyPress_StopAll(hwnd) # KeyPress_Up() won't work. Why? I don't know, for every program it's different.
```

Module's functions are easy to understand.