class LoginManager():
    def __init__(self):
        pass

    def set_anonymous(self, request):
        # will be called with before_request
        request.session['email'] = 'visitor@unknown.com'
        request.session['role'] = 'public'
        request.session['login'] = False

    def set_user(self, identity, request):
        # must set session['login']
        request.session['email'] = identity['email']
        request.session['role'] = identity['role']
        request.session['login'] = identity['email'].endswith('@school.pyc.edu.hk')

    def anonymous_setter(self, func):
        # update set_anonymous function, use as decorator
        self.set_anonymous = func

    def user_setter(self, func):
        # update set_user function, use as decorator
        self.set_user = func


login_manager = LoginManager()
