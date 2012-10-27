from koala import application

class Logger(object):
    def process_request(self, request):        
        """
        This is where we can have all the auth check. redirect to login if no authentication info
        #TBD: for now we just get the user_id from session        
        """        
        application.getContext(request)
    def process_response(self, request, response):
        #TBD close connection        
        application.clearContext()
        return response
     