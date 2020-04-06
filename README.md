# Globals
This library allows global access to different python api classes and functions

# Simplest way to use it

## Projects directory
  Put all your git projects you wanna exchange classes between them in a single folder
```
C:\Users\my_user\path\path\path\all_my_git_projects
```
<img align="center" ![Directory with all mai guit projects](https://i.pinimg.com/originals/67/ec/2c/67ec2c13bc7ee72a06eb737eac3dc8bb.png) >


"Globas" project, don't actually needs to be included in this directory. It doesn't even need to be cloned at all.

Unless you wanna use this library the proper way. But it can be done later if it's actually needed.

## Your "main" api
  On the directory you wanna launch the "main api" (the one that will consume other projects classes and funtions), 
you put the PathMannanger.py file following this path tree:
```
C:\Users\my_user\path\path\path\all_my_git_projects\my_launcher_api\api\src\domain\control\PathMannanger.py
```
Don't forget to put your main class in src directory.

<div style="display:block;text-align:center">
  ![PathMannanger.py file](https://i.pinimg.com/originals/d1/a3/3e/d1a33efcc8880eefadec49f503352429.png)
</div>

## On the "main" file of your main api
  Put the following code right on top of the __main__ class of your api.
```
from domain.control import PathMannanger
if __name__ == '__main__' :
    PathMannanger.PathMannanger(mode = 'WRONG_WAY_TO_MAKE_IT_WORKS')
```

<div style="display:block;text-align:center">
  ![Chess api main file](https://i.pinimg.com/originals/71/f1/49/71f149457654ee03091b93e6982429ba.png)
</div>

## Be happy. 
Now, you don'd even need to specify the path of classes you are importing.

Yes, its really that simple. 🌈✨🎇

<div style="display:block;text-align:center">
  ![be hapy](https://i.pinimg.com/originals/9a/73/d0/9a73d02d6552502c748e436edacf1994.png)
</div>

# About the proper way to use this library
I'll be implementing more funcionalities in order to make it extendable and more compatible to python framewors in general.
If you want more information or just want to contribute a litle bit, please hit me up.
