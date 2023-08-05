import asyncio
import requests
from robot.api.deco import keyword, not_keyword
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.1.0'


class PuppeteerPercy:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LISTENER_API_VERSION = 3

    AGENT_URL = 'http://localhost:5338'

    loop = asyncio.get_event_loop()
    percyIsRunning = True

    def __init__(self):
        self.percyIsRunning = True

    @keyword
    def percy_snapshot(self, name, **kwargs):
        self.loop.run_until_complete(self.percy_snapshot_async(name))

    @not_keyword
    async def percy_snapshot_async(self, name, **kwargs):
        puppeteerLibrary = BuiltIn().get_library_instance('PuppeteerLibrary')
        page = puppeteerLibrary.get_current_page()

        # Exit if we have failed to connect to the percy-agent server
        if self.percyIsRunning == False:
            return
        agent_js = self.get_agent_js()

        # Exit if we fail to grab the JS that serializes the DOM
        if agent_js == False:
            return

        # await page.addScriptTag({'url': self.AGENT_URL + '/percy-agent.js'})
        await page.addScriptTag({'content': agent_js})

        domSnapshot = await page.evaluate(
            'var agent = new PercyAgent({ handleAgentCommunication: false }); agent.snapshot("name");')
        postData = {
            'name': name,
            'url': page.url,
            'widths': kwargs.get('widths') or [],
            'percyCSS': kwargs.get('percyCSS') or '',
            'minHeight': kwargs.get('minHeight') or '',
            'enableJavaScript': kwargs.get('enableJavaScript') or False,
            'domSnapshot': domSnapshot,
            'clientInfo': 'percy-selenium-python/',
            'environmentInfo': self.env_info()
        }
        self.post_snapshot(postData)

    @not_keyword
    def post_snapshot(self, postData):
        try:
            requests.post(self.AGENT_URL + '/percy/snapshot', json=postData)
        except requests.exceptions.RequestException as e:
            print('[percy] failed to POST snapshot to percy-agent:' + postData.get('name'))
            return

    @not_keyword
    def env_info(self, capabilities=None):
        return 'robotframework-puppeteer-percy: 1.0.0'

    @not_keyword
    def get_agent_js(self):
        try:
            agentJS = requests.get(self.AGENT_URL + '/percy-agent.js')
            return agentJS.text
        except requests.exceptions.RequestException as e:
            if self.percyIsRunning == True:
                self.percyIsRunning = False
            BuiltIn().log('[Percy] failed to fetch percy-agent.js, disabling Percy', level='WARN')
            return self.percyIsRunning
