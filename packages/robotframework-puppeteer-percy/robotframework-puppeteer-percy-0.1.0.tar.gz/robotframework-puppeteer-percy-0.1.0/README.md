# Robotframework-Puppeteer-Percy
[Percy](https://percy.io) visual testing for [Robot Framework Puppeteer](https://github.com/qahive/robotframework-puppeteer).


Keyword documentation
---------------------
See [`keyword documentation`](https://qahive.github.io/robotframework-puppeteer-percy/PuppeteerPercyLibrary.html) for available keywords and more information about the library in general.


Installation
------------
The recommended installation method is using pip:

    pip install --upgrade robotframework-puppeteer-percylibrary
    
Or manually install by running following command
    
    pip install -r requirements.txt
    python setup.py install
    

Usage
------------
Create file name quick-start.robot with following content:

    *** Settings ***
    Library    PuppeteerLibrary
    Library    PuppeteerPercy
    Test Teardown    Close Browser
    
    
    *** Test Cases ***
    Capture home page screenshot
        ${HEADLESS}     Get variable value    ${HEADLESS}    ${False}
        &{options} =    create dictionary   headless=${HEADLESS}
        Open browser    http://example.com  options=${options}
        Maximize Browser Window
        Percy Snapshot    Home page

Need to run robot script with following command:
    
    npx percy exec -- robot quick-start.robot

Limitation
------------
- Not support for web site that restriction for other site resource files. 

FAQ
------------
- Snapshot throw error `ElementHandleError: Evaluation failed: Event`. Your web site not allow to inject 3rd party javascript. Need to ask developer to allow localhost javascript tobe executed.

Development
------------
Generate update keyword documents 

    python -m robot.libdoc -f html PuppeteerPercy docs/PuppeteerPercy.html
