import cairo
import numpy.random as rd
import math
from pyRavenMatrices.element import (
    BasicElement, ElementModifier, ModifiedElement, CompositeElement
) 
from pyRavenMatrices.lib.sandia.definitions import (
    ellipse, rectangle, diamond, triangle, trapezoid, tee,
    scale, rotation, shading, numerosity
)

class StructureGenerator(object):
    
    def __init__(
        self, 
        branch: dict = None, 
        composite_num: dict = None, 
        modifier_num: dict = None
    ) -> None:

        if branch == None:
            branch = {
                'basic': 1 / 3,
                'composite': 1 / 3,
                'modified': 1 / 3
            }
        if composite_num == None:
            composite_num = {
                2: .5,
                3: .5
            }
        if modifier_num == None:
            modifier_num = {
                1: 1 / 3,
                2: 1 / 3,
                3: 1 / 3
            }

        self.branch = branch
        self.composite_num = composite_num
        self.modifier_num = modifier_num

    def sample(self):

        branch = rd.choice(
            list(self.branch.keys()), p=list(self.branch.values())
        )
        composite_num = rd.choice(
            list(self.composite_num.keys()), p=list(self.composite_num.values())
        )
        modifier_num = rd.choice(
            list(self.modifier_num.keys()), p=list(self.modifier_num.values())
        )

        if branch == 'basic':
            element = BasicElement()
        elif branch == 'composite':
            element = CompositeElement(
                *[BasicElement() for i in range(composite_num)]
            )
        else: # branch == 'modified'
            element = ModifiedElement(
                BasicElement(), 
                *[ElementModifier() for i in range(modifier_num)]
            )
        return element


class ShapeGenerator(object):
    
    def __init__(
        self,
        shapes: dict = None,
        ellipse: dict = None, 
        triangle: dict = None,
        rectangle: dict = None,
        diamond: dict = None,
        trapezoid: dict = None,
        tee: dict = None
    ) -> None:

        if shapes == None:
            shapes = {
                'ellipse': 1 / 6,
                'triangle': 1 / 6,
                'rectangle': 1 / 6,
                'diamond': 1 / 6,
                'trapezoid': 1 / 6,
                'tee': 1 / 6
            }
        if ellipse == None:  
            ellipse = {
                'r': {
                    2: 1 / 3,
                    4: 1 / 3,
                    8: 1 / 3
                }
            }
        if triangle == None:
            triangle = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }
        if rectangle == None:
            rectangle = {
                'r': {
                    2: 1 / 3,
                    4: 1 / 3,
                    8: 1 / 3,
                }
            }
        if trapezoid == None:
            trapezoid = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }
        if diamond == None:
            diamond = {
                'r': {
                    1: 1 / 3,
                    2: 1 / 3,
                    4: 1 / 3,
                }
            }
        if tee == None:
            tee = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }

        self.shapes = shapes
        self.ellipse = ellipse
        self.triangle = triangle
        self.rectangle = rectangle
        self.trapezoid = trapezoid
        self.diamond = diamond
        self.tee = tee

    def sample(self):
        
        shape = rd.choice(list(self.shapes.keys()), p=list(self.shapes.values()))
        
        if shape == 'ellipse':
            routine, params = ellipse, self.sample_params(self.ellipse)
        elif shape == 'triangle':
            routine, params = triangle, self.sample_params(self.triangle)
        elif shape == 'rectangle':
            routine, params = rectangle, self.sample_params(self.rectangle)
        elif shape == 'diamond':
            routine, params = diamond, self.sample_params(self.diamond)
        elif shape == 'trapezoid':
            routine, params = trapezoid, self.sample_params(self.trapezoid)
        else: # shape == 'tee'
            routine, params = tee, self.sample_params(self.tee)
        return routine, params
        
    @staticmethod
    def sample_params(dists):
        
        params = {
            param: rd.choice(
                list(dists[param].keys()), 
                p=list(dists[param].values())
            )
            
            for param in dists
        }
        return params


class DecoratorGenerator(object):
    
    def __init__(
        self,
        decorators: dict = None,
        scale: dict = None,
        rotation: dict = None,
        shading: dict = None,
        numerosity: dict = None
    ) -> None:

        if decorators == None:
            decorators = {
                'scale': .25,
                'rotation': .25,
                'shading': .25,
                'numerosity': .25
            }        
        if scale == None:
            scale = {
                'factor': {
                    (7 / 8): 1 / 7,
                    (6 / 8): 1 / 7,
                    (5 / 8): 1 / 7,
                    (4 / 8): 1 / 7,
                    (3 / 8): 1 / 7,
                    (2 / 8): 1 / 7,
                    (1 / 8): 1 / 7
                } 
            }        
        if rotation == None:
            rotation = {
                'angle': {
                    (1 / 8) * 2 * math.pi: 1 / 7,
                    (2 / 8) * 2 * math.pi: 1 / 7,
                    (3 / 8) * 2 * math.pi: 1 / 7,
                    (4 / 8) * 2 * math.pi: 1 / 7,
                    (5 / 8) * 2 * math.pi: 1 / 7,
                    (6 / 8) * 2 * math.pi: 1 / 7,
                    (7 / 8) * 2 * math.pi: 1 / 7
                }
            }        
        if shading == None:
            shading = {
                'lightness': {
                    (7 / 8): 1 / 7,
                    (6 / 8): 1 / 7,
                    (5 / 8): 1 / 7,
                    (4 / 8): 1 / 7,
                    (3 / 8): 1 / 7,
                    (2 / 8): 1 / 7,
                    (1 / 8): 1 / 7            
                }
            }        
        if numerosity == None:
            numerosity = {
                'number': {
                    2: 1 / 7,
                    3: 1 / 7,
                    4: 1 / 7,
                    5: 1 / 7,
                    6: 1 / 7,
                    7: 1 / 7,
                    8: 1 / 7
                }
            }

        self.decorators = decorators
        self.scale = scale
        self.rotation = rotation
        self.shading = shading
        self.numerosity = numerosity
    
    def sample(self):
        
        decorator = rd.choice(
            list(self.decorators.keys()), p=list(self.decorators.values())
        )
        
        if decorator == 'scale':
            decorator, params = scale, self.sample_params(self.scale)
        elif decorator == 'rotation':
            decorator, params = rotation, self.sample_params(self.rotation)
        elif decorator == 'shading':
            decorator, params = shading, self.sample_params(self.shading)
        else: # decorator == 'numerosity'
            decorator, params = numerosity, self.sample_params(self.numerosity)
        
        return decorator, params
        
    @staticmethod
    def sample_params(dists):
        
        params = {
            param: rd.choice(
                list(dists[param].keys()), 
                p=list(dists[param].values())
            )
            
            for param in dists
        }
        return params