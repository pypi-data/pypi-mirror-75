#!python
#!/usr/bin/python3

# Modular Internet of Things
# Command line utility / REPL
# (c) Copyright Si Dunford, Mar 2019
#
# STATE: Pre-Alpha

import sys
from miot import config,mqtt

VERSION = '1.0.3.6'

brokers = {}
interactive = False

## SUPPORT FUNCTIONS

def die( message, subtext='', pointer=0 ):
    print( COLOR(YELLOW)+message )
    if subtext!='': print( "  "+subtext )
    if pointer>0:
        print( " "*(pointer+1)+"^" )
    if interactive: return
    sys.exit(1)

def repl():
    #print( "Welcome to Modular IoT" )
    print( "REPL: "+str(VERSION) )
    print( "" )
    print( "Type 'quit' to exit, or 'help' for assistance." )
    print( "" )
    running = True
    try:
        while running:
            value = input( COLOR(WHITE)+":" )
            if value!='':
                cmd = value.split(" ")
                if cmd[0]=='quit': 
                    running = False
                else:
                    func = CMDswitcher.get( cmd[0], unknown )
                    func( cmd )
    except KeyboardInterrupt:
        print( COLOR(WHITE)+"" )
        print( "- Bye!" )
        sys.exit()
    except Exception as e:
        print( COLOR(YELLOW)+e )

## ANSI COLOUR SUPPORT

BLACK=0
RED=1
GREEN=2
YELLOW=3
BLUE=4
PURPLE=5
CYAN=6
WHITE=7

def COLOR( fg ):
    return "\033[{}m".format( fg+30 )

## MQTT SUPPORT

def on_error( broker, error ):
    try:
        #print( "Error" )
        err = str(error['id'])
        print( COLOR(YELLOW)+"!ERROR: {} | ({}) {} | {}".format( broker.hostname, err, error['message'], broker.error( err ) ))
    except Exception as e:
        print( COLOR(YELLOW)+e )
        
def on_connect( broker, msg ):
    #print("Connected")
    print( COLOR(GREEN)+"!CONNECTED: {}".format( broker.hostname ) )

def on_message( broker, msg ):
    #print( "Message" )
    print( COLOR(CYAN)+"!MESSAGE: {} | {} | {}".format( broker.hostname, msg['topic'], msg['message'] ))

def connect( host='default' ):
    try:
        global brokers
        brokerkey = host
        if brokerkey=='': brokerkey='default'
        if brokerkey in brokers:
            #print( "- Using saved host" )
            return brokers[brokerkey]
        #
        if( host=='' ):
            hostip   = config.get( "mqtt.host" )
            port     = config.get( "mqtt.port" )
            username = config.get( "mqtt.username" )
            userpass = config.get( "mqtt.password" )
        else:
            hostip   = config.get( "mqtt.{}.host".format( host ) )
            port     = config.get( "mqtt.{}.port".format( host ) )
            username = config.get( "mqtt.{}.username".format( host ) )
            userpass = config.get( "mqtt.{}.password".format( host ) )
        #
        #print( "  HOST:     "+host )
        #print( "  BROKER:   {}:{}".format(hostip,port) )
        #print( "  USERNAME: "+username )
        
        broker = mqtt.broker()
        broker.authenticate( username, userpass )
        broker.on( 'error',   on_error )
        broker.on( 'connect', on_connect )
        broker.on( 'message', on_message )
        broker.connect( hostip, port )
        #
        broker.start()  # Start ASYNC MODE
        #
        brokers[brokerkey]=broker
        return broker
    except Exception as e:
        print( COLOR(YELLOW)+e )

def disconnect( brokerkey ):
    global brokers
    if brokerkey=='': brokerkey='default'
    if brokerkey in brokers:
        brokers[brokerkey].stop()
        del brokers[brokerkey]

def disconnectall():
    global brokers
    for key,value in list(brokers.items()):
        disconnect( key )
        
## COMMANDS

"""
def exist( args ):
    if len(args)<1:
        die( COLOR(YELLOW)+"Missing parameter:", "exist <key>", 7 )
    key = args[0]
    default = False
    print( len(args))
    if len(args)==2:
        print( "has default flag" )
        temp = args[2][0]
        print(temp)
        default = True if args[2][0].lower()==true else False
    result = config.exist( key, default )
    print( COLOR(WHITE)+str(result) )
"""

def get( args ):
    cmd = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', cmd+' <key>', len(cmd)+2)
        return
    key = args.pop(0)
    if len(args)>0:
        unexpected = " ".join(args)
        die( COLOR(YELLOW)+'Unexpected argument:', cmd+' '+key+' '+unexpected, len(cmd)+3+len(key)  )
        return
    print( COLOR(WHITE)+key+" = '"+str(config.get( key ))+"'" )
        
def help( args ):
    print( COLOR(WHITE)+"""
  get <key>              Displays a configuration key
  set <key> <value>      Sets a configuration key
  subscribe <topic>      Subscribes to a topic (Shows messages)
  publish <topic> <msg>  Publishes a message on a topic
  version                Shows the current version
  
  Alias:
  show <key>    Same as "get <key>"
  listen <topic>  Same as "subscribe <topic>"
  """)

"""
def list( args ):
    print( COLOR(WHITE)+"LIST" )

    # READ CONFIG.INI FOR INSTALLED COMPONENTS
    # READ MODULES.DAT FOR AVAILABLE COMPONENTS
    # SHOW LIST
"""

def publish( args ):

    cmd = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', 'publish <topic> <Message>', 9 )
        return
        
    topic = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', 'publish '+topic+' <Message>', 10+len(topic) )
        return
       
    message  = " ".join(args)
        
    broker = connect()
    broker.publish( topic, message )
    print( COLOR(GREEN)+"- Published to {}.".format( topic ) )
 
def set( args ):
    cmd = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', 'set <key> <value>', 5)
        return
    key = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', 'set '+key+' <value>', 6+len(key))
        return
    value = " ".join(args)
    config.set( key, value )
    config.save()
    print( COLOR(WHITE)+key+" = '"+str(value)+"'" )

def subscribe( args ):
    cmd = args.pop(0)
    if len(args)<1:
        die( COLOR(YELLOW)+'Missing parameter:', cmd+' <topic>', len(cmd)+2)
        return
    topic = args.pop(0)
    if len(args)>0:
        unexpected = " ".join(args)
        die( COLOR(YELLOW)+'Unexpected argument:', cmd+' '+topic+' '+unexpected, len(cmd)+3+len(topic)  )
        return
        
    broker = connect()
    broker.subscribe( topic )
   
#def unsubscribe( args ):
#    pass

def unknown( args ):
    die( COLOR(YELLOW)+"- Unknown command: {}".format(args[0]) )
     
#def update( args ):
#    print( COLOR(WHITE)+"UPDATE")

def version( args ):
    print( COLOR(WHITE)+"Version: "+VERSION )

# COMMAND SWITCHER
CMDswitcher = { 
    "--help":help,
    "get":get,
    "help":help,
    "listen":subscribe,
    "publish":publish,
    "set":set,
    "show":get,
    "subscribe":subscribe,
    "version":version 
}
# "list":list,
# "update":update, 

if __name__=="__main__":

    # PROCESS ARGUMENTS
    if len(sys.argv) <= 1:
        interactive = True
        repl()
        sys.exit(0)

    func = CMDswitcher.get( sys.argv[1], unknown )
    func( sys.argv[1:] )




