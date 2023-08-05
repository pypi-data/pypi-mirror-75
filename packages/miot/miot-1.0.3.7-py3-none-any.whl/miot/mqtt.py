# MIOT / MQTT MODULE
# (C) Copyright Si Dunford, MAR 2019
# MIT License
#
# VERSION: 0.2.1

# THIRD PARTY MODULES
import paho.mqtt.client as paho_mqtt
from miot import log

# VARIABLES
ERROR_MESSAGES = {
    '0':'Success',
    '1':'Incorrect protocol version',
    '2':'Invalid client identifier',
    '3':'Server unavailable',
    '4':'Bad username or password',
    '5':'Not authorised',
    }

# Default methods
def on_connect( client, userdata, flags, rc ):
    try:
        this = userdata
        if rc==0:    # Connected successfully
            #print("CONNECT : "+str(userdata)+" : "+str(rc))
            this.send( 'connect', { 'id':0, 'message':'Success' } )
            this.isconnected = True
        else:       # Connected with error
            this.send( 'error', { 'id':rc, 'message':'Connection Refused' } )
    except Exception as e:
        print(e)
        log.exception( "Exception", e )
        
def on_disconnect( client, userdata, rc ):
    this = userdata
    this.isconnected = False
    this.send( 'disconnect', { 'id':rc, 'message':'Disconnected' } )

def on_message( client, userdata, msg):
    #print("MESSAGE : "+str(userdata)+" : "+str(msg))
    this = userdata
    payload = str(msg.payload.decode())
    topic = msg.topic           
    this.send( 'message', { 'topic':topic, 'message':payload } )

def on_subscribe( client, userdata, mid, granted_qos ):
    #print("SUBSCRIBE : "+str(userdata)+" : "+str(mid))
    this = userdata
    this.send( 'subscribe', { 'mid':mid } )

def on_unsubscribe( client, userdata, mid, granted_qos ):
    #print("UNSUBSCRIBE : "+str(userdata)+" : "+str(mid))
    this = userdata
    this.send( 'unsubscribe', { 'mid':mid } )

def on_publish( client, userdata, mid ):
    #print("PUBLISH : "+str(userdata)+" : "+str(mid))
    this = userdata
    this.send( 'publish', { 'mid':mid } )
    
# WRAPPER FOR PAHO MQTT
class broker:
    
    def __init__(self, appname='', clean_session=True ):
                    
        self.eventlist = {}
        self.hostname  = '127.0.0.1'
        self.hostport  = 1883
        self.username  = ''
        self.password  = ''
        self.clientid  = ''
        self.root      = 'miot'
        
        try:
            self.client = paho_mqtt.Client( appname, clean_session=clean_session )
        except Exception as e: raise
        
        # Set userdata to self
        self.client.user_data_set( self )
        
        # Connect handlers
        self.client.on_connect     = on_connect
        self.client.on_disconnect  = on_disconnect
        self.client.on_message     = on_message
        self.client.on_publish     = on_publish
        self.client.on_subscribe   = on_subscribe     
        self.client.on_unsubscribe = on_unsubscribe     

    def authenticate( self, username, password ):
        self.username=username
        self.password=password

    # Add event handler
    def on( self, event, handler ):
        #print( "adding '"+event+ "' event handler" )
        event = event.lower()
        if event not in self.eventlist: self.eventlist[event]=[]
        try:  # Check not already in list
            index = self.eventlist[event].index( handler )
        #    print( "- already exists" )
        except ValueError as e:
            # Not in list, so add it.
            self.eventlist[event].append( handler )
        #print( str(self.eventlist[event]) )
        #    print( "- appended" )
        
    # Remove event handler
    def off( self, event, handler ):
        #print( "removing '"+event+ "' event handler" )
        event = event.lower()
        if event in self.eventlist:
            try:
                self.eventlist[event].remove( handler ) 
                #print( "- removed" )
            except ValueError as e:
                #print( "- not in list" )
                pass
        #else:
        #    print( "- handler does not exist" )
    
    # Send a message to event handlers
    def send( self, event, message ):
        if event not in self.eventlist: return
        for handler in self.eventlist[ event ]:
            #print( "- "+event+" handler found" )
            handler( self, message )

    # Convert error numbers into error strings
    def error( self, id ):
        return ERROR_MESSAGES.get( str(id), "Failure" )

    # Connect to the broker
    def connect( self, host='127.0.0.1', port=1883 ):
        print( "--connecting")
        try:
            self.hostname  = host
            self.hostport  = port

            # User authentication
            if self.username != '':
                print( "- MQTT: "+self.username+"@"+self.hostname+":"+str(self.hostport) )    
                self.client.username_pw_set( self.username, self.password )
            else:
                print( "- MQTT: "+self.hostname+":"+str(self.hostport) )    

            # Connect to broker
            self.client.connect( self.hostname, self.hostport , 60 )
        except Exception as e:
            #logging.critical( str(e) )
            print( e )
            return False

    # Are we connected?
    def connected():
        return self.isconnected

    # Gracefully disconnect
    def disconnect( self ):
        self.client.disconnect()

    def publish( self, topic, message ):
        return self.client.publish( topic, message )

    # Subscribe to one or more topics
    # Supported formats:
    #   subscribe( '/my/topic' )    = Always uses QOS=0
    #   subscribe( ('my/topic',0) ) = Second arg in tuple is QOS
    #   subscribe( [('my/topic',0),('your/topic',2)] )
    #
    # Returns tuple (result, mid)
    def subscribe( self, topic ):
        if isinstance( topic, str ):
            topic = ( topic, 0 )    # Convert to tuple
        return self.client.subscribe( topic )
    
    # Subscribe to one or more topics
    def unsubscribe( self, topic ):
        return self.client.unsubscribe( topic )

    # SYNCRONOUS - Wait forever
    def wait( self ):
        self.client.loop_forever()

    # ASYNCHRONOUS - Start thread
    def start( self ):
        self.client.loop_start() 
    
    # ASYNCHRONOUS - Stop thread
    def stop( self ):
        self.client.disconnect()
        self.client.loop_stop()

    # MANUAL - Manual loop
    def dispatch( self ):
        self.client.loop()
        
    # Last will and testament
    # Call this BEFORE connect()
    def lwt( self, topic, message ):
        self.client.will_set( topic, payload=message, qos=0, retain=True )
        
    
