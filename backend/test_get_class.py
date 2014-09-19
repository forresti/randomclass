from pprint import pprint
import get_class

def test_get_class_simple():
    for i in xrange(0, 10):
        print get_class.getSampleClass()

def test_get_class():
    for i in xrange(0, 10):
        pprint(get_class.getRandomClass_berkeley())

#test_get_class_simple()
test_get_class()

