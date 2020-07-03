# Globals
This library allows global access to different python projects classes and functions.

Put all your git projects you wanna exchange classes between them in a single folder

Let's say "projects"

```
C:\Users\my_user\path\path\path\path\path\path\path\path\projects
```

## Put this code in your root file (the one that starts up everithing)

```
from globals import Globals
Globals(__file__, globalsEverything = True)
```

## Be happy

Now, you don'd even need to specify the path of classes you are importing.

Yes, its really that simple. 🌈✨🎇
