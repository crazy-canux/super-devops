import unittest
from enum import Enum, EnumMeta


class Persona(Enum):
# class Persona(int, Enum):
    UNKNOWN = -1
    IT_ADMIN = 0
    DATA_ADMIN = 1
    SECURITY_ADMIN = 2
    CONSUMER = 3

# class Role(Enum):
class Role(str, Enum):
    UNKNOWN = 'unknown'
    IT_ADMIN = 'itadmin'
    DATA_ADMIN = 'dataadmin'
    SECURITY_ADMIN = 'secadmin'
    CONSUMER = 'consumer'

class TestEnum(unittest.TestCase):
    def test_persona(self):
        print Persona.CONSUMER
        print Persona.CONSUMER.name
        print Persona.CONSUMER.value
        print 'Persona(0): ', Persona(0)
        print '3 == Persona.CONSUMER: ', 3 == Persona.CONSUMER
        print '3 in Persona.CONSUMER: ', 3 in [Persona.CONSUMER]

    def test_role(self):
        print Role.CONSUMER
        print Role.CONSUMER.name
        print Role.CONSUMER.value
        print 'Role(dataadmin): ', Role('dataadmin')
        print 'consumer == Role.CONSUMER: ', 'consumer' == Role.CONSUMER
        print 'consumer in [Role.CONSUMER]', 'consumer' in [Role.CONSUMER]
        print 'Role.CONSUMER.lower()', Role.CONSUMER.lower()

if __name__ == "__main__":
    unittest.main()
