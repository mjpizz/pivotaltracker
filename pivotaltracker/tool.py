import os
import sys
import yaml
import pivotaltracker
from pivotaltracker._termcolor import styled
from pivotaltracker._helpers import command, choose_command

__CONFPATH = os.path.join(os.path.expanduser("~"), ".pivotaltracker")

def required_style(msg):
    return styled(" %s " % msg, attrs=["reverse"])

def optional_style(msg):
    return styled(" %s " % msg, attrs=["reverse"])

def result_style(msg):
    return styled(" %s " % msg, attrs=["bgmagenta", "white"])

def _load_config():
    if not os.path.exists(__CONFPATH):
        
        # collect config information
        print required_style("What is your Pivotal Token?")
        token = raw_input("(go to https://www.pivotaltracker.com/profile to generate one): ")
        
        print required_style("What Project do you want to track by default?")
        project_id = raw_input("(visit the project in your browser and the Project ID will be in the URL, e.g. https://www.pivotaltracker.com/projects/<PROJECT-ID>): ")
        
        # print required_style("What is your full name in that project?")
        # username = raw_input("(visit https://www.pivotaltracker.com/projects/%s/overview to see the names): " % project_id)
        
        # dump the config
        data = yaml.dump(dict(token=token, project_id=int(project_id)), default_flow_style=False)
        
        # save the file
        fd = open(__CONFPATH, "w+")
        print "you can update your configuration at any time by editing %s" % __CONFPATH
        fd.write(data);
        fd.close()
        
    # load the config and return the values
    config = yaml.load(open(__CONFPATH, "r").read())
    token = config["token"]
    project_id = config["project_id"]
    return token, project_id

def run(argv=sys.argv):
    """commandline client"""
    
    @command
    def chore(parser):
        """creates a chore in pivotal"""
        
        # get config values
        token, project_id = _load_config()
        
        # get other inputs
        print required_style("chore name")
        name = raw_input("> ")
        
        print optional_style("extra description for the chore")
        description = raw_input("> ")
        
        # create the client
        client = pivotaltracker.Client(token=token)
        response = client.add_story(
            project_id=project_id,
            name=name,
            description=description,
            story_type="chore",
            )
        
        # print the url of the story
        print result_style(response["story"]["url"])

    choose_command(argv=argv)
    