class Person:
    name = []

    def set_name(self, user_name):
        '''
        @apiParam {String} [user_name]
        @apiReturn {apiParam.user_name} [self.get_name(0)]
        '''
        self.name.append(user_name)
        return len(self.name) - 1

    def get_name(self, user_id):
        '''
        @apiParam {Number} [user_id=1]
        @apiReturn {String} [There is no such user]
        '''
        if user_id >= len(self.name):
            return 'There is no such user'
        else:
            return self.name[user_id]
