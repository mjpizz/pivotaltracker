import optparse
from pivotaltracker._termcolor import styled

_COMMANDS = {}
_ORDERED_COMMANDS = []

def command(method=None):
    
    def decorate(method):

        name = method.__name__.replace("_", "-")
        doc = method.__doc__ or "(no documentation)"
        description = "\n".join(["  %s" % line.strip() for line in doc.split("\n")])
        
        parser = optparse.OptionParser(usage="usage: %(name)s [options]\n\n%(description)s" % dict(name=name, description=description))
        
        def wrapper():
            try:
                # call the command
                method(parser)

            except Exception, e:
                print
                print styled("*** error: %s" % str(e), attrs=["red"])
                raise
        
        # add to command registry
        _ORDERED_COMMANDS.append(name)
        _COMMANDS[name] = (description, wrapper)
        
        return wrapper
        
    if method == None:
        def subdecorator(method):
            return decorate(method)
        return subdecorator
    else:
        return decorate(method)

def choose_command(argv):
    """chooses a command to run based on the given argv, defaulting to 'help'"""
    
    @command
    def help(parser=None):
        """shows help for all available commands"""
        print "available commands:"
        print
        format_string = "    %%(name)-%ds" % maxlen(_COMMANDS.keys())
        def print_command(name, description):
            print styled(format_string % dict(name=name), attrs=["bold"]), description
        for name in _ORDERED_COMMANDS:
            description, callback = _COMMANDS[name]
            print_command(name, description)
        if _COMMANDS:
            print
    
    # force help to be the first option
    _ORDERED_COMMANDS.insert(0, _ORDERED_COMMANDS.pop())
    
    if len(argv) > 1:
        # run command
        name = argv[1]
        description, callback = _COMMANDS[name]
        callback()
        
    else:
        # list all commands
        _COMMANDS["help"][1]()

def maxlen(stringlist):
    """returns the length of the longest string in the string list"""
    maxlen = 0
    for x in stringlist:
        if len(x) > maxlen:
            maxlen = len(x)
    return maxlen