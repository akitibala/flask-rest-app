
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

import csv
import json
import os

from flask.json import jsonify 
from flask import make_response

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, rectangle:list,points:list):
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
      
        
        return handler

    @abstractmethod
    def handle(self, rectangle:list,points:list):
        if self._next_handler:
            return self._next_handler.handle(rectangle=rectangle,points=points)
        return True


    def point_in_rectangle(self,rectangle:list,point:tuple) -> bool:
        A = rectangle[0]
        B = rectangle[1]
        C = rectangle[2]
    
        BA = self._vector(B,A)
        BC = self._vector(B,C)
        BM = self._vector(B,point)
        dotBABA = self._dot(BA,BA)
        dotBCBC = self._dot(BC,BC)
        dotBMBC = self._dot(BM,BC)
        dotBMBA = self._dot(BM,BA)

        return 0 <= dotBMBA and dotBMBA <= dotBABA and 0 <= dotBMBC and dotBMBC <= dotBCBC

    def _vector(self,X:tuple,Y:tuple):

        x1,y1=X
        x2,y2=Y
        return y1-x1,y2-x2
        # return t

    def _dot(self,U:tuple,V:tuple):
        return U[0]*V[0] + U[1]*V[1]


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""

@singleton
class TopLeftHandler(AbstractHandler):
    def handle(self, rectangle:list,points:list):
        
    
        if self.point_in_rectangle(rectangle,points[0]):
        
             return super().handle(rectangle,points)
        return False

       

@singleton
class BottomLeftHandler(AbstractHandler):
    def handle(self, rectangle:list,points:list):
    
        if self.point_in_rectangle(rectangle,points[1]):
             return super().handle(rectangle,points)
        return False

@singleton
class BottomRightHandler(AbstractHandler):

    def handle(self, rectangle:list,points:list):
        
        if self.point_in_rectangle(rectangle,points[2]):
             return super().handle(rectangle,points)
        return False

@singleton
class TopRightHandler(AbstractHandler):

    def handle(self, rectangle:list,points:list):
        
        if self.point_in_rectangle(rectangle,points[3]):
            return super().handle(rectangle,points)
        return False




def is_valid(handler:Handler,rectangle=[],points=[]):

    res = handler.handle(rectangle=rectangle,points=points)

    if res:
        return True
    return False





def generate_rectangle_points(points=[]):
    A = (points[0],points[1])
    B = (points[0],points[3])
    C = (points[2],points[3])
    temp=[]
    temp.append(A)
    temp.append(B)
    temp.append(C)
    return temp
def generate_4_rectangle_points(points=[]):
    temp=[]

    D = (points[2],points[1])
    ABC = generate_rectangle_points(points=points)
    temp.extend(ABC)
    temp.append(D)
    
    return temp

def sort_and_extract_text(points=[]):
    sorted_list = sorted(points, key=lambda x: (x[1],x[0]))
    return " ".join(list(map(lambda x:x[4],sorted_list)))


def process_csv(filename=None,points=[]):
    text=''
    try:
        file=os.path.join(os.path.dirname(__file__),"csvs",filename)
        rectangle=generate_rectangle_points(points=points)

        with open(file) as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')
            wanted_points=[]
            top_left = TopLeftHandler()
            bottom_left = BottomLeftHandler()
            bootom_right = BottomRightHandler()
            top_right = TopRightHandler()
            top_left.set_next(bottom_left).set_next(bootom_right).set_next(top_right)
            line_count=0
            for row in csv_file:
                row_with_text=row[4]
                if line_count == 0:
                    line_count += 1
                else:

                    row = row[:4]
                    text_points=list(map(int,row))
            
                    p=generate_4_rectangle_points(points=text_points)
                    if is_valid(top_left,rectangle=rectangle,points=p):
                    
                        temp = []
                        temp.extend(text_points)
                        temp.append(row_with_text)
                    
                        wanted_points.append(temp)
        
            text = sort_and_extract_text(points=wanted_points)
    except FileNotFoundError as e:
        raise FileNotFoundError("File Not Found") from None


    
    return text


