# Pytonik Bootstrap Flash Message

**Pytonik Bootstrap Flash Message** helps you store messages in session data until they are retrieved. Bootstrap compatibility, sticky messages, and more

## Installation Guide

### Step 1:
You can simply install the module into your pytonik application using any of the methods below.

#### With Pip
~~~bash
  pip install FlashBootstrap
~~~

#### With Git
~~~bash
git clone https://github.com/emmamartins/FlashBootstrap/
~~~

### Step 2:
Import the module using either of the following method

~~~python
from FlashBootstrap.FlashBootstrap import FlashBootstrap
~~~

or

````python
from FlashBootstrap.FlashBootstrap import *
````

### Step 3: Default Parameter 

~~~python
description = ""
title = ""
dismissible = True
key = 'flash' 
~~~

## Basic Usage

~~~python

#Instantiate the class
msg = FlashBootstrap

#Add messages With Bootstrap
msg.info('This is an info message')
msg.success('This is a success message')
msg.warning('This is a warning ')
msg.error('This is an error ')

#Add messages Without Bootstrap
msg.message('This is an info message')


#Wherever you want to display the messages simply call:
msg.display()



#Wherever you want to clear or unset the messages simply call:
msg.clear()


#Wherever you want to redirect to
msg.redirect('/location')

~~~

### Message Types

#### Info
````python
msg.info('This is a info message')
````

![Info Message](https://pytonik.com/public/assets/home/img/info.png)

#### Success
````python
msg.success('This is a success message')
````
![Success Message](https://pytonik.com/public/assets/home/img/success.png)


#### Warning
````python
msg.warning('This is a warning ')
````
![Warning Message](https://pytonik.com/public/assets/home/img/warning.png)

#### Error
````python
msg.error('This is a error')
````
![Error Message](https://pytonik.com/public/assets/home/img/error.png)

### Redirect

It is possible to redirect to a different URL before displaying a message. For example, redirecting from **checklogin** back to a form **login**, (and displaying an error message) so a user can correct an error - **subjected to pytonik developers**.

![Error Message](https://pytonik.com/public/assets/home/img/Flashbootstrap.gif)

````python 
  #Import FlashBootstrap
  from FlashBootstrap.FlashBootstrap import *

  def checklogin():
    FlashBootstrap.error('Cannot login account')
    return FlashBootstrap.redirect('/login', True)
  
````


### Alternative 

````python 
  #Import Pytonik
  from pytonik.Web import app
  #Import FlashBootstrap
  from FlashBootstrap.FlashBootstrap import *

  def checklogin():
    FlashBootstrap.error('Cannot login account')
    return app.redirect('/login', True)
  
````

# Author

👤 **Raphael Essien**

- Github: [Raphael Essien](https://github.com/emmamartins)


## 🤝 Contributing

Contributions, issues and feature requests are welcome!

## Show your support

Give a ⭐️ if you like this project!

