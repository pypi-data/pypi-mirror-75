username = None


def name():
    '''
    @apiReturn {String} [Evarist]
    '''
    return "Evarist"


def set_username(name):
    '''
    @apiParam {String} [name]
    @apiReturn {Boolean} [True]
    '''
    global username
    username = name
    return True


def get_username():
    global username
    return username


def test_boolean_true(first_name):
    '''
    @apiParam {String} first_name
    @apiReturn {Boolean} [True]
    '''
    if isinstance(first_name, str):
        return True
    return None


def test_boolean_false(first_name):
    '''
    @apiParam {String} first_name
    @apiReturn {Boolean} [False]    
    '''
    if not isinstance(first_name, str):
        return False
