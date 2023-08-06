from sample.pet import Pet as AnimalPet, Dog
from sample.pet import Pet
from sample.animal import Animal


def create_pet(name, species, age=0):
    '''
    @apiParam {String} [name]
    @apiParam {String} [species]
    @apiParam {Number=random_int} [age]
    @apiReturn {Object} [Pet(apiParam.name,apiParam.species)]
    '''
    return Pet(name, species).get_name()


def create_pet_with_empty_return_object(name, species, age=0):
    '''
    @apiParam {String} [name]
    @apiParam {String} [species]
    @apiParam {Number=random_int} [age]
    @apiReturn {Object}

    '''
    return Pet(name, species)


def create_pet_return_true(name, species, age=0):
    '''
    @apiParam {String} [name]
    @apiParam {String} [species]
    @apiParam {Number=random_int} [age]
    @apiReturn {String}
    '''
    return Pet(name, species).get_name()


def create_animal(species):
    '''
    @apiParam {String} [species]
    @apiReturn {Object}
    '''
    return Animal(species)


def create_pet_return_false(name, species, age=0):
    '''
    @apiParam {String} [name]
    @apiParam {String} [species]
    @apiParam {Number=random_int} [age]
    @apiReturn {Boolean} [False]
    '''
    Pet(name, species)
    return False


def create_pet_return_none(name, species, age=0):
    '''
    @apiParam {String} [name]
    @apiParam {String} [species]
    @apiParam {Number} [age]
    @apiReturn {Boolean} [False]    
    '''
    Pet(name, species)


if __name__ == '__main__':
    print(Pet('Polly', 'Parrot'))
    print(create_pet('Clifford', 'Dog', 32))
