# easyTui

Very simple TUI module for python

## Capabilities
-Print title
using
```
import easyTui as tui
print(tui.title('Text Sample'))

#Outputs
#=================
#-- Text Sample --
#=================
```
-Print label
using
```
import easyTui as tui
print(tui.label('Text Sample'))

#Outputs
#  Text Sample
#-----------------
```
-Print score
using
```
import easyTui as tui
val = 5
print(tui.score('Text Sample', val))

#Outputs
# Text Sample :  5
# ----------------------
```
-Print updating score
using
```
import easyTui as tui
val = 5
print(tui.updatingScore('Text Sample', val, 1), end='')

#Outputs val, delaied for 1 second and \r
#Text Sample :  5
#----------------------
```
-Print Unordered list
using
```
import easyTui as tui
list = ['Text Sample', '2 Sample', '3 Sample']
print(tui.ul(list))

#Outputs
#  - Text Sample
#  - 2 Sample
#  - 3 Sample
#------------------------
```
-Print Ordered list
using
```
import easyTui as tui
list = ['Text Sample', '2 Sample', '3 Sample']
print(tui.ol(list))

#Outputs
#  [0] Text Sample
#  [1] 2 Sample
#  [2] 3 Sample
#------------------------
```