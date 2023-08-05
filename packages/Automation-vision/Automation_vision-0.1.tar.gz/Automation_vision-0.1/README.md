# Automation-vision
This package is use for auto clicking and auto writing

## Quickstart
pip install Automation-vision==0.1

## requirements
* Operating System
  * Windows
* Programming Language
  * python 3.7

## Usage
* First open this link [link ](https://clickdimensions.com/form/default.html) make sure it remain open
* then

```python
from Auto import Automation

app='Sample Web Form - ClickDimensions - Google Chrome'
dictionary_data=Automation.Get_RT_app_elements('Vision-179',app)
action='write'
Automation.add_action(action,dictionary_data,app,label_='*First name:',enter_text='test1')
Automation.add_action(action,dictionary_data,app,label_='*Last name:',enter_text='test')
Automation.add_action(action,dictionary_data,app,label_='*Email:',enter_text='test@gmail.com')
Automation.add_action(action,dictionary_data,app,label_='*Company:',enter_text='Expert')
Automation.add_action(action,dictionary_data,app,label_='City:',enter_text='islamabad')
Automation.add_action('click',dictionary_data,app,label_='*Country:',enter_text='test')
Automation.add_action('click',dictionary_data,app,label_='*Country:')
Automation.add_action(action,dictionary_data,app,label_='Phone:',enter_text='00000000')
Automation.add_action('click',dictionary_data,app,label_='Sign-up to receive our monthly newsletter?')
```
