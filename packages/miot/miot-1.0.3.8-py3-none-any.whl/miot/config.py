# MIOT / CONFIG MODULE
# (C) Copyright Si Dunford, JUN 2020
# MIT License
#
__version__ = '1.0.3.8'

# THIRD PARTY MODULES
import json,os

# VARIABLES
CONFIG_FILE = os.path.expanduser( "~/.config/miot.cfg" )
__data = {}

def default():
    global __data
    #print( "* loading default values" )
    __data = {
        'mqtt':{
            'default':{'host':'127.0.0.1','port':1883,'root':'home'}
            },
        'system':{
            'root':'home'
            }
        }

# Walk the dictionary until we identify the requested key.
def __getkey( keys, config, alt ):
    if len(keys)==0: return alt
    #print( "* finding "+keys[0]+" in "+str(config) )
    # Check for key
    if keys[0] in config:
        #print( "found "+keys[0]+" in "+str(config) )
        #print( keys[1:] )
        if len(keys)==1: return config[keys[0]]
        return __getkey( keys[1:], config[ keys[0]], alt )
    
    # Check for 'default'
    #print( "Checking for default value" )
    if 'default' in config:
        return __getkey( keys, config['default'], alt )
    
    #print( "failed to find "+keys[0]+" in "+str(config) )
    # Failed to find key
    return alt

def __setkey( keys, config, value ):
    if len(keys)==0: return

    #print( "* finding "+keys[0]+" in "+str(config) )
    # Check for key
    if keys[0] in config:
        #print( "found "+keys[0]+" in "+str(config) )
        #print( keys[1:] )
        if len(keys)==1:
            #print( "THIS IS IT" )
            config[keys[0]]=value
            return
        __setkey( keys[1:], config[keys[0]], value )
        return

    # Check for 'default'
    #print( "Checking for default value" )
    if 'default' in config:
        #print( "Default found" )
        __setkey( keys, config['default'], value )
        return

    # Failed to find key
    #print( "failed to find "+keys[0]+" in "+str(config) )
    if len(keys)==1:
        config[keys[0]]=value
        return
    config[keys[0]]={}
    __setkey( keys[1:], config[keys[0]], value )

def __walk( config, keys, allow_default=True ):
    if len(keys)==0: return 

    if keys[0] in config:
        if len(keys)==1:
            return (true)
        return __walk( keys[1:], config[keys[0]], allow_default )

    if allow_default and 'default' in config:
        return __walk( keys, config['default'], allow_default )
    
    if len(keys)==1:
        return (false)
    
    return __walk( keys[1:], config[keys[0]], allow_default )
    
def get( key, alt='' ):
    global __data
    #print( "Searching for '"+key+"' ['"+alt+"']" )
    keys = key.split(".")
    #print( keys )
    return __getkey( keys, __data, alt )

def set( key, value ):
    global __data
    #print("")
    #print( "Setting '"+key+"' to '"+str(value)+"'" )
    #print(__data)
    keys = key.split(".")
    #print( keys )
    __setkey( keys, __data, value )
    #print( "-RESULT")
    #print( json.dumps( __data ) )

def exist( key, allow_default=False ):
    global __data
    return __walk( __data, key.split("."), allow_default )

def exists( key, allow_default=False ):
    global __data
    return __walk( __data, key.split("."), allow_default )
    
def load():
    global __data
    #print( "LOADING" )
    try:
        with open( CONFIG_FILE, 'r') as cfg:
            __data = json.load(cfg)
    except:
        #print( "Failed to load config" )
        #default()
        pass
    if __data == {}:
        default()
        
def save():
    global __data
    #__data={}
    #print( "SAVING" )
    #print( json.dumps( __data ) )
    with open( CONFIG_FILE, 'w' ) as cfg:
        json.dump( __data, cfg, indent=4, sort_keys=True )

def wipe():
    global __data
    __data={}
    save()
    
def tostring( indent=4, sort=True ):
    return json.dumps( __data, indent=indent, sort_keys=sort )
    
""" INITIALISE MODULE """

#print( "config.init()" )
load()
#print( json.dumps( __data ) )

