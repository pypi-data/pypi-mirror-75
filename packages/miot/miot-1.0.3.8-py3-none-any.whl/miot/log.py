# MIOT / LOG MODULE
# (C) Copyright Si Dunford, JUN 2020
# MIT License
#
__version__ = '1.0.3.8'
#
# Based on code found here:
# https://docs.python.org/2/howto/logging-cookbook.html
#

""" KNOWN ISSUES
* format( SYSLOG )
    - '/dev/log' will only work on Linux
    - OSX should be /var/run/syslog
    - Windows cannot use this format
"""

import logging, logging.handlers, os

# LOG FORMATTING
BASIC  = 0
SYSLOG = 1
DAEMON = 2

# SYSLOG SEVERITY
DEBUG     = 10
INFO      = 20
NOTICE    = 25
WARNING   = 30
ERROR     = 40
CRITICAL  = 50
ALERT     = 60
EMERGENCY = 70

# SYSLOG FACILITIES
LOG_AUTH     = logging.handlers.SysLogHandler.LOG_AUTH
LOG_AUTHPRIV = logging.handlers.SysLogHandler.LOG_AUTHPRIV
LOG_CRON     = logging.handlers.SysLogHandler.LOG_CRON
LOG_DAEMON   = logging.handlers.SysLogHandler.LOG_DAEMON
LOG_FTP      = logging.handlers.SysLogHandler.LOG_FTP
LOG_KERN     = logging.handlers.SysLogHandler.LOG_KERN
LOG_LPR      = logging.handlers.SysLogHandler.LOG_LPR
LOG_MAIL     = logging.handlers.SysLogHandler.LOG_MAIL
LOG_NEWS     = logging.handlers.SysLogHandler.LOG_NEWS
LOG_SYSLOG   = logging.handlers.SysLogHandler.LOG_SYSLOG
LOG_USER     = logging.handlers.SysLogHandler.LOG_USER
LOG_UUCP     = logging.handlers.SysLogHandler.LOG_UUCP
LOG_LOCAL0   = logging.handlers.SysLogHandler.LOG_LOCAL0
LOG_LOCAL1   = logging.handlers.SysLogHandler.LOG_LOCAL1
LOG_LOCAL2   = logging.handlers.SysLogHandler.LOG_LOCAL2
LOG_LOCAL3   = logging.handlers.SysLogHandler.LOG_LOCAL3
LOG_LOCAL4   = logging.handlers.SysLogHandler.LOG_LOCAL4
LOG_LOCAL5   = logging.handlers.SysLogHandler.LOG_LOCAL5
LOG_LOCAL6   = logging.handlers.SysLogHandler.LOG_LOCAL6
LOG_LOCAL7   = logging.handlers.SysLogHandler.LOG_LOCAL7

# CUSTOM ONE-LINE FORMATTER
class One_line_Formatter( logging.Formatter ):
    
    def formatException( self, exc_info ):
        result = super( One_line_Formatter, self ).formatException( exc_info )
        return repr( result ) 
    
    def format( self, record ):
        result = super( One_line_Formatter, self ).format( record )
        if record.exc_text:
            result = result.replace("\\n", ', ')
        return result

# SYSLOG SERVERITY COMPATIBLE LOGGING FUNCTIONS
def emergency( msg ):   logging.log( EMERGENCY, msg ) #0 - Emergency     (70)
def alert( msg ):       logging.log( ALERT, msg )     #1 - Alert         (60)
def critical( msg ):    logging.critical( msg )       #2 - Critical      (50)
def error( msg ):       logging.error( msg )          #3 - Error         (40)
def warning( msg ):     logging.warning( msg )        #4 - Warning       (30)
def notice( msg ):      logging.log( NOTICE, msg )    #5 - Notice        (25)
def info( msg ):        logging.info( msg )           #6 - Informational (20)
def debug( msg ):       logging.debug( msg )          #7 - Debug         (10)

# Exception specific log function
def exception( msg,e ): logging.exception( msg, e )

# LOG CONTROL
def format( logtype=BASIC, level=INFO, facility=LOG_USER ):
    
    if logtype==SYSLOG:
        formatter = One_line_Formatter( logging.BASIC_FORMAT )
        handler   = logging.handlers.SysLogHandler( '/dev/log', facility=facility )
        logger    = logging.getLogger()
        handler.setFormatter( formatter )
        logger.setLevel( level )
        logger.addHandler( handler )
    elif logtype==DAEMON:
        formatter = One_line_Formatter( '%(asctime)s|%(levelname)s|%(message)s|', '%Y-%m-%d %H:%M:%S')
        handler   = logging.StreamHandler()
        logger    = logging.getLogger()
        handler.setFormatter( formatter )
        logger.setLevel( level )
        logger.addHandler( handler )
    else: # BASIC
        logging.basicConfig( level=level )

# DEFINE ADDTIONAL LOG LEVELS
logging.addLevelName( EMERGENCY, "EMERGENCY")
logging.addLevelName( ALERT, "ALERT")
logging.addLevelName( NOTICE, "NOTICE")
