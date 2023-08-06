from sample.animal import Animal


class Pet(Animal):
    def __init__(self, name, *args):
        '''
        @apiParam {String} [name]
        @apiParam {String} [args]
        '''
        Animal.__init__(self, *args)
        self._name = name

    def get_name(self):
        '''
        The below declaration make sure that the function return match the value return. This only allow when the class has the init function
        @apiReturn {String}
        '''
        return self._name

    @staticmethod
    def lower(s):
        '''
        @apiParam {String} [s]
        @apiReturn {String}
        '''
        return s.lower()

    def __str__(self):
        return '%s is a %s aged %d' % (

            self.get_name(),

            Pet.lower(self.get_species()), self.get_age()

        )


class Dog(Pet):
    pass
