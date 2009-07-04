import urllib
import urllib2
from xml.dom import minidom


class Client(object):
    """Client wrapper for PivotalTracker API"""
    
    
    def __init__(self, token, secure=True, parse_xml=True):
        """instantiates a PivotalTracker API client.  By default,
        all requests are made securely (via HTTPS) and all returned
        XML is parsed into a Python dictionary.  You can override
        these options by setting 'secure' or 'parse_xml' to False"""
        self.__token = token
        protocol = "https" if secure else "http"
        self.__base_url = "%(protocol)s://www.pivotaltracker.com/services/v2/" % dict(protocol=protocol)
        self.__parse_xml = parse_xml
        
    def get_project(self, project_id):
        """gets a project from the tracker"""
        return self.__remote_http_get("projects/%s" % project_id)
        
    def get_all_projects(self):
        """gets all projects for this user"""
        return self.__remote_http_get("projects")
    
    def get_story(self, project_id, story_id):
        """gets an individual story"""
        return self.__remote_http_get("projects/%s/stories/%s" % (project_id, story_id))
    
    def get_stories(self, project_id, query=None, limit=None, offset=None):
        """gets stories from a project.  These stories can be filtered via 'query', and
        paginated via 'limit' and 'offset'"""
        params = {}
        if query:
            params["filter"] = query
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if params:
            # we have parameters to send
            encoded_params = urllib.urlencode(params)
            return self.__remote_http_get("projects/%s/stories?%s" % (project_id, encoded_params))
        else:
            # no arguments, get all stories
            return self.__remote_http_get("projects/%s/stories" % project_id)
        
    def get_iterations(self, project_id, limit=None, offset=None):
        """gets iterations from a project.  These iterations can be paginated via 'limit' and 'offset'"""
        return self.__iterations_request_helper(sub_url="iterations", project_id=project_id, limit=limit, offset=offset)
        
    def get_done_iterations(self, project_id, limit=None, offset=None):
        """gets all done iterations from a project.  These iterations can be paginated via 'limit' and 'offset'"""
        if offset is not None:
            offset = -1*offset
        return self.__iterations_request_helper(sub_url="iterations/done", project_id=project_id, limit=limit, offset=offset)
        
    def get_current_iterations(self, project_id, limit=None, offset=None):
        """gets current iteration from a project.  These iterations can be paginated via 'limit' and 'offset'"""
        return self.__iterations_request_helper(sub_url="iterations/current", project_id=project_id, limit=limit, offset=offset)
        
    def get_backlog_iterations(self, project_id, limit=None, offset=None):
        """gets backlog from a project.  These iterations can be paginated via 'limit' and 'offset'"""
        return self.__iterations_request_helper(sub_url="iterations/backlog", project_id=project_id, limit=limit, offset=offset)
    
    def add_story(self, project_id, name, description, story_type, requested_by=None, estimate=None, current_state=None, labels=None):
        """adds a story to a project"""
        xml = self.__get_story_xml(project_id, name, description, requested_by, story_type, estimate, current_state, labels)
        data = xml.toxml()
        return self.__remote_http_post("projects/%s/stories" % project_id, data=data)
    
    def update_story(self, project_id, story_id, name=None, description=None, requested_by=None, story_type=None, estimate=None, current_state=None, labels=None):
        """updates a story in a project"""
        xml = self.__get_story_xml(project_id, name, description, requested_by, story_type, estimate, current_state, labels)
        data = xml.toxml()
        return self.__remote_http_put("projects/%s/stories/%s" % (project_id, story_id), data=data)
    
    def delete_story(self, project_id, story_id):
        """deletes a story in a project"""
        return self.__remote_http_delete("projects/%s/stories/%s" % (project_id, story_id))
    
    def add_comment(self, project_id, story_id, text, author=None):
        """adds a comment to a story in a project"""
        # build XML elements
        elements = []
        if text is not None:
            elements.append("<text>%s</text>" % text)
        if author is not None:
            elements.append("<author>%s</author>" % author)
        
        # build XML
        xml_string = "<note>%s</note>" % "".join(elements)
        xml = minidom.parseString(xml_string.strip())
        data = xml.toxml()
        return self.__remote_http_post("projects/%s/stories/%s/notes" % (project_id, story_id), data=data)
    
    def deliver_all_finished_stories(self, project_id):
        """delivers all finished stories in a project.  This is perfect for automated
        deployments to a staging server, indicating that the code has been deployed
        for live testing."""
        return self.__remote_http_put("projects/%s/stories/deliver_all_finished" % project_id)
    
    def __get_story_xml(self, project_id, name, description, requested_by, story_type, estimate, current_state, labels):
        
        # build XML elements
        elements = []
        if name is not None:
            elements.append("<name>%s</name>" % name)
        if description is not None:
            elements.append("<description>%s</description>" % description)
        if requested_by is not None:
            elements.append("<requested_by>%s</requested_by>" % requested_by)
        if story_type is not None:
            elements.append("<story_type>%s</story_type>" % story_type)
        if estimate is not None:
            elements.append("<estimate type=\"integer\">%s</estimate>" % estimate)
        if current_state is not None:
            elements.append("<current_state>%s</current_state>" % current_state)
        if labels is not None:
            if len(labels) > 0:
                # set labels
                elements.append("<labels>%s</labels>" % ",".join(labels))
            else:
                # clear labels (to empty list)
                elements.append("<labels>,</labels>")
        
        # build XML
        xml_string = "<story>%s</story>" % "".join(elements)
        xml = minidom.parseString(xml_string.strip())
        return xml
    
    def __iterations_request_helper(self, sub_url, project_id, limit, offset):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if params:
            # we have parameters to send
            encoded_params = urllib.urlencode(params)
            return self.__remote_http_get("projects/%s/%s?%s" % (project_id, sub_url, encoded_params))
        else:
            # no arguments, get all iterations
            return self.__remote_http_get("projects/%s/%s" % (project_id, sub_url))

    def __xml_to_dictionary(self, dom):
        
        xml_as_dict = {}
        
        def parse_by_type(node):
            
            # determine type
            if node.attributes:
                obj_type = node.attributes["type"].value
            elif node.nodeName in ["stories", "notes"]:
                obj_type = "array"
            elif node.nodeName in ["labels"]:
                obj_type = "commalist"
            elif len(node.childNodes) == 1:
                obj_type = "string"
            elif node.nodeName in ["description"] and len(node.childNodes) == 0:
                # FIXME: this is a hack to make sure that empty descriptions no NOT become dictionaries
                return ""
            else:
                obj_type = "dictionary"
            
            # parse differently depending on type
            if obj_type == "array":
                # list node
                return parse_to_list(node)
            
            elif obj_type == "integer":
                # integer node
                value = node.childNodes[0].wholeText.strip()
                return int(value)
            
            elif obj_type == "datetime":
                # datetime node
                value = node.childNodes[0].wholeText.strip()
                return value # FIXME: parse the datetime
            
            elif obj_type == "string":
                # text node
                value = node.childNodes[0].wholeText.strip()
                return value
            
            elif obj_type == "commalist":
                value = node.childNodes[0].wholeText.strip()
                return value.split(",")

            elif obj_type == "dictionary":
                # dictionary node
                return parse_to_dict(node)
                
            else:
                # default to dictionary node
                return parse_to_dict(node)

        def parse_to_list(parent_node):
            new_list = []
            for child_node in parent_node.childNodes:
                if child_node.nodeName != "#text":
                    value = parse_by_type(child_node)
                    new_list.append(value)
            return new_list
            
        def parse_to_dict(parent_node):
            new_dict = {}
            for child_node in parent_node.childNodes:
                if child_node.nodeName != "#text":
                    value = parse_by_type(child_node)
                    new_dict[child_node.nodeName] = value
            return new_dict

        return parse_to_dict(dom)
    
    def __perform_request(self, req):
        try:
            response = urllib2.urlopen(req)
            dom = minidom.parseString(response.read())
            if self.__parse_xml:
                return self.__xml_to_dictionary(dom)
            else:
                return dom
        except urllib2.HTTPError, e:
            if e.code == 422:
                dom = minidom.parseString(e.read())
                return self.__xml_to_dictionary(dom)
            else:
                raise

    def __remote_http_get(self, path):
        url = self.__base_url + path
        req = urllib2.Request(url, None, {'X-TrackerToken': self.__token})
        return self.__perform_request(req)

    def __remote_http_post(self, path, data):
        url = self.__base_url + path
        req = urllib2.Request(url, data, {'X-TrackerToken': self.__token, 'Content-type': 'application/xml'})
        return self.__perform_request(req)
    
    def __remote_http_put(self, path, data):
        url = self.__base_url + path
        req = urllib2.Request(url, data, {'X-TrackerToken': self.__token, 'Content-type': 'application/xml'})
        req.get_method = lambda: 'PUT'
        return self.__perform_request(req)
    
    def __remote_http_delete(self, path):
        url = self.__base_url + path
        req = urllib2.Request(url, None, {'X-TrackerToken': self.__token})
        req.get_method = lambda: 'DELETE'
        return self.__perform_request(req)
