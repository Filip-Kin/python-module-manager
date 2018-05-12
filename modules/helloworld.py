from modules.ftools import *

module = {
    'name': 'Hello World',
    'version': '0.1',
    'author': 'Filip9696',
    'description': 'Example mod',
    'functions': {
        'helloWorld': {
            'args': {
                'required': [
                    {
                        'name': 'variable',
                        'type': 'bool'
                    }
                ],
                'optional': []
            },
            'desc': 'Prints "Hello World!" if given true'
        }
    }
}


def helloWorld(variable):
    if variable:
        print('Hello World!')


def onLoad():
    print('Hello World Loaded')
    helloWorld(true)
    return true


def onShutdown():
    print('Hello World shutting down')


def beforeReload():
    print('Hello World Reloading')


def afterReload():
    print('Hello World Reloaded')

def onInput(input):
    print('Hello World got: '+input)


print('This should print out whenever the module reloads')
