import pdb

class Grandparent:
    a = 0
    b = 1
    c = 2

class Parent(Grandparent):
    d = 0
    e = 1
    f = 2

class Child(Parent):
    child_member = 1337


