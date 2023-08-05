A library used to control programs(mainly games) without focusing them.  
This isn't guaranteed to work and will sometimes require to be very creative with how you perform actions.  
Example:
```python
import DistanceControl as dc

hwnd = dc.Windows_by_title('GamesTitle', strict=True, limit=1)[0]

# Open up menu(It doesn't close it)
dc.KeyPress_Down(hwnd, dc.con.VK_ESCAPE)
dc.KeyPress_Up(hwnd, dc.con.VK_ESCAPE)

# Press the right key
dc.KeyPress_Down(hwnd, dc.con.VK_RIGHT)
dc.KeyPress_StopAll(hwnd) # KeyPress_Up() won't work. Why? I don't know, for every program it's different!
```

Module's functions are easy to understand.


## Changelog

DistanceControl 0.0.2.5:  
- Made usage much cleaner.
- Fixed a few tiny bugs.

DistanceControl 0.0.2:  
- Fixed unable to download package.

DistanceControl 0.0.1:  
- Initial release.
