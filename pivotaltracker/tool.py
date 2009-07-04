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

def header(msg, attrs):
    attrs += ["bold"]
    padding = styled(" "*8 + " "*len(msg), attrs=attrs)
    padded_message = styled(" "*4 + msg + " "*4, attrs=attrs)
    return "%s\n%s\n%s" % (padding, padded_message, padding)

def run(argv=sys.argv):
    """commandline client"""
    
    @command
    def chore(parser):
        """creates a chore in pivotal"""

        print header("CHORE", attrs=["bgblue", "white"])
        print
        
        # get config values
        token, project_id = _load_config()
        
        # get other inputs
        print required_style("chore name")
        name = raw_input("> ")
        
        print optional_style("extra description for the chore"), "(optional)"
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
    
    @command
    def bug(parser):
        """creates a bug in pivotal"""

        print header("BUG", attrs=["bgred", "white"])
        print
        
        # get config values
        token, project_id = _load_config()
        
        # get other inputs
        print required_style("bug name")
        name = raw_input("> ")
        
        # input the steps
        step_idx = 1
        keep_going = True
        description = ""
        while keep_going:
            print optional_style("step %s" % step_idx), "(just leave a blank entry to stop giving steps)"
            new_step = raw_input("> ")
            if new_step.strip():
                description += "%s. %s\n" % (step_idx, new_step)
                keep_going = True
                step_idx += 1
            else:
                keep_going = False
        
        # get any extra description
        print optional_style("extra description for the bug %s" % step_idx), "(optional)"
        extra_description = raw_input("> ")
        description += extra_description
        
        # create the client
        client = pivotaltracker.Client(token=token)
        response = client.add_story(
            project_id=project_id,
            name=name,
            description=description,
            story_type="bug",
            )
        
        # print the url of the story
        print result_style(response["story"]["url"])

    choose_command(argv=argv)
    