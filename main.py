import importlib as imp
import os
from modules.ftools import *
import json


#Lets get dat config
configh = open('./config.json', 'r')
config = json.loads(configh.read())
configh.close()

loaded = {}

def load(mod):
    modpath = './modules/'+mod+'.py'
    if os.path.isfile(modpath):
        mod = imp.import_module('modules.'+mod)
        try:
            mod.onLoad()
        except Exception as err:
            error('Failed to load module '+mod.__name__+'\n'+str(err))
            loaded[mod.__name__] = 'failed'
            return false
        loaded[mod.__name__] = [mod, mod.module]
        debug('loaded '+str(loaded[mod.__name__]))
        return mod
    else:
        return false

def loadAll():
    files = os.listdir('./modules')
    debug(files)
    for mod in files:
        if os.path.isfile('./modules/'+mod):
            mod = mod.split('.')[0]
            if mod in config['disabled']:
                loaded['modules.'+mod] = 'unloaded'
                debug(mod+' is disabled in config')
            else:
                debug('loading '+mod)
                load(mod)
        else:
            debug(mod+' is not a file, skipping')


def onShutdown():
    for mod in loaded.keys():
        if loaded[mod] == 'failed' or loaded[mod] == 'unloaded':
            continue
        try:
            loaded[mod][0].onShutdown()
        except Exception as err:
            debug(mod+' did not take onShutdown()\n' + str(err))


def beforeReload():
    for mod in loaded.keys():
        if loaded[mod] == 'failed' or loaded[mod] == 'unloaded':
            continue
        try:
            loaded[mod][0].beforeReload()
        except Exception as err:
            debug(mod+' did not take beforeReload()\n' + str(err))


def reload():
    for mod in loaded.keys():
        if loaded[mod] == 'unloaded':
            continue
        try:
            imp.reload(loaded[mod][0])
        except Exception as err:
            warn(mod+' did not take reload\n' + str(err))


def afterReload():
    for mod in loaded.keys():
        if loaded[mod] == 'failed' or loaded[mod] == 'unloaded':
            continue
        try:
            loaded[mod][0].afterReload()
        except Exception as err:
            debug(mod+' did not take afterReload()\n' + str(err))


def onInput(input):
    for mod in loaded.keys():
        if loaded[mod] == 'failed' or loaded[mod] == 'unloaded':
            continue
        try:
            loaded[mod][0].onInput(input)
        except Exception as err:
            debug(mod+' did not take onInput()\n' + str(err))


def main():
    loadAll()
    while true:
        rawcmd = input('>')
        cmdparts = rawcmd.lower().split(' ')
        cmd = cmdparts[0]
        args = cmdparts[1:]
        argswithquote = []
        for arg in args:
            if '"' in arg:
                argswithquote.append(args.index(arg))
        debug('Command '+cmd+' Args: '+str(args))
        if cmd.lower() == 'shutdown':
            onShutdown()
            break
        elif cmd.lower() == 'reload':
            beforeReload()
            reload()
            afterReload()
        elif cmd.lower() == 'mods':
            loadedlist = []
            for mod in loaded:
                if loaded[mod] == 'failed':
                    loadedlist.append(col(1,style=2)+mod+colend)
                elif loaded[mod] == 'unloaded':
                    loadedlist.append(col(7)+mod+colend)
                else:
                    loadedlist.append(mod)
            print(col(2)+'Mods ('+str(len(loadedlist))+'): '+colend+', '.join(loadedlist))
            debug(loaded)
        else:
            onInput(cmd)


main()
