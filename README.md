# surveys
A simple survey made with flask, CSS and HTML

<!-- ABOUT THE PROJECT -->
## About The Project
This is a simple survey built with Flask, HTML and CSS.

**surveys.py**
contains two classes Question and Survey which are used to build a structure of survey instances. 
Two survey instances are included in a surveys dictionary, which has been imported to app.py 

**app.py**

```Python 
from flask import Flask, render_template, redirect, flash, request, session
import surveys
from flask_debugtoolbar import DebugToolbarExtension
```
