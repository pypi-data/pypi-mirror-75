from .server import Server


class AnchorPeer:

    def __init__(self, name, org_name=None):

        self.name = name
        self.org_name = org_name
        self.server = Server()

    def dump(self):
        if self.org_name.lower() not in self.server.host:
            self.server.host = "{}.{}".format(
                self.org_name.lower(), self.server.host)

        return "\n\n\n\t\t\t- Host: {}.{}\n\t\t\t  Port: {}".format(self.name, self.server.host, self.server.port)

    def test_unit_that_return_dict(self):
        '''
         @apiReturn {Number} [{"name":4}]
        '''
        print("hi there ")
        return

    def test_unit_that_return_dict_with_a_dictionary_type(self):
        '''
         @apiReturn {Dict} [{"name":4}]
        '''
        print("hi there ")
        return

    def test_unit_with_email(self, test1):
        '''
         @apiParam {String=Email} [test1]

         @apiReturn {Boolean} [True]
        '''
        pass

    def test_unit_with_default_test2_value_and_string(self, test1, test2):
        '''
         @apiParam {String=first_Name} [test1]

         @apiParam {String} test2="Fangnikoue Evarist"

         @apiReturn {Boolean} [True]
        '''
        pass

    def test_unit_with_number_and_string(self, test1, test2):
        '''
         @apiParam {String=first_Name} [test1]

         @apiParam {Number} test2

         @apiReturn {Boolean} [True]
        '''
        pass

    def test_unit_with_address(self, address):
        '''
         @apiParam {String=street_address} [address]

         @apiReturn {Boolean} [True]
        '''
        pass

    def test_unit_with_boolean_and_string(self, test1, test2):
        '''
         @apiParam {String} [test1]

         @apiParam {Boolean} [test2]

         @apiReturn {Boolean} [True]
        '''
        pass

    def test_unit_that_return_a_list(self, test1, test2):
        '''
         @apiReturn {Number} [1,2,3,4]
        '''
        pass

    def test_unit_that_return_a_list_with_a_list_type(self, test1, test2):
        '''
         @apiReturn {List} [1,2,3,4]
        '''
        pass

    def test_unit_3(self, test1, test2):
        '''


        '''
        pass

    def test_unit_4(self, test1, test2):
        pass
