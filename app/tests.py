from django.test import TestCase


# Create your tests here.

class A:
      a=10
      def m1(self):
            print("A class")

class B(A):
      def m1(self):
            print("B class")

class C(B):
      def m1(self):
            print("C class")

class D(C):
      def m1(self):
            super(B,self).m1()
            print(super(B,self).a)

d = D()
d.m1()


