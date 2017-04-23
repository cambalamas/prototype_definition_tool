# Dependencies. (Mac)

`brew install gtk+3`
`brew install pygobject3 --with-python3`

```
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
```
