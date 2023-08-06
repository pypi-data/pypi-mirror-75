**<h2>Scripterminator</h2>** 
**Useful tool to terminate any Python script just using file path and name**

This package provides a small utility function callled `terminate_script(file,delay)`

This function takes two parameters - `file` and `delay` (optional).

file -> file path + file name
delay -> after how much time you want to terminate the process

`terminate_script(file,delay)` returns `True` if the script is in running state and terminated successfully.
Otherwise it returns `False`

Usage:

Suppose your python script name is bar.py and located in `/projects/pythonprojects/bar/` folder -

```python
import scripterminator

file = '/projects/pythonprojects/bar/bar.py'
terminated = scripterminator.terminate_script(file, 3)

if terminated:
    print('script terminated') 
else:
    print('script termination failed') 

```

This project is licensed under the terms of the MIT license.

