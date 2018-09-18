import cairo
import typing as t
import numpy.random as rd
import copy
import math
from pyRavenMatrices.element import (
    Element, BasicElement, ElementModifier, ModifiedElement, CompositeElement
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


class RoutineGenerator(object):
    
    def __init__(
        self,
        routines: dict = None,
        ellipse_params: dict = None, 
        triangle_params: dict = None,
        rectangle_params: dict = None,
        diamond_params: dict = None,
        trapezoid_params: dict = None,
        tee_params: dict = None
    ) -> None:

        if routines == None:
            routines = {
                ellipse: 1 / 6,
                triangle: 1 / 6,
                rectangle: 1 / 6,
                diamond: 1 / 6,
                trapezoid: 1 / 6,
                tee: 1 / 6
            }
        if ellipse_params == None:  
            ellipse_params = {
                'r': {
                    2: 1 / 3,
                    4: 1 / 3,
                    8: 1 / 3
                }
            }
        if triangle_params == None:
            triangle_params = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }
        if rectangle_params == None:
            rectangle_params = {
                'r': {
                    2: 1 / 3,
                    4: 1 / 3,
                    8: 1 / 3,
                }
            }
        if trapezoid_params == None:
            trapezoid_params = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }
        if diamond_params == None:
            diamond_params = {
                'r': {
                    1: 1 / 3,
                    2: 1 / 3,
                    4: 1 / 3,
                }
            }
        if tee_params == None:
            tee_params = {
                'r': {
                    .25: .2,
                    .5: .2,
                    1: .2,
                    2: .2,
                    4: .2
                }
            }

        self.routines: dict = t.cast(dict, routines)
        self.params = {
            ellipse: t.cast(dict, ellipse_params),
            triangle: t.cast(dict, triangle_params),
            rectangle: t.cast(dict, rectangle_params),
            trapezoid: t.cast(dict, trapezoid_params),
            diamond: t.cast(dict, diamond_params),
            tee: t.cast(dict, tee_params)
        }

    def sample(self, size=1, dist=None, replace=True):
        
        if dist == None:
            dist = self.routines

        routine = rd.choice(
            list(dist.keys()), size=size, p=list(dist.values()), replace=replace
        )
        
        return list(routine)

    def sample_params(self, routine=None, size=1, dists=None, replace=True):

        if dists == None:
            dists = self.params[routine]
        
        params = {
            param: rd.choice(
                list(dists[param].keys()),
                size=size,
                p=list(dists[param].values()),
                replace=replace
            ) for param in dists
        }

        params = [
            {param: params[param][i] for param in params} for i in range(size)
        ]

        return params


class DecoratorGenerator(object):
    
    def __init__(
        self,
        decorators: dict = None,
        scale_params: dict = None,
        rotation_params: dict = None,
        shading_params: dict = None,
        numerosity_params: dict = None
    ) -> None:

        if decorators == None:
            decorators = {
                scale: .25,
                rotation: .25,
                shading: .25,
                numerosity: .25
            }        
        if scale_params == None:
            scale_params = {
                'factor': {
                    (3 / 4): 1 / 3,
                    (2 / 4): 1 / 3,
                    (1 / 4): 1 / 3,
                } 
            }        
        if rotation_params == None:
            rotation_params = {
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
        if shading_params == None:
            shading_params = {
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
        if numerosity_params == None:
            numerosity_params = {
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

        self.decorators: dict = t.cast(dict, decorators)
        self.params = {
            scale: t.cast(dict, scale_params),
            rotation: t.cast(dict, rotation_params),
            shading: t.cast(dict, shading_params),
            numerosity: t.cast(dict, numerosity_params)
        }
    
    def sample(self, size=1, dist=None, replace=True):
        
        if dist == None:
            dist = self.decorators

        decorators = rd.choice(
            list(dist.keys()), size=size, p=list(dist.values()), replace=replace
        )
        
        return list(decorators)
        
    def sample_params(self, decorator=None, size=1, dists=None, replace=True):

        if dists == None:
            dists = self.params[decorator]
        
        params = {
            param: rd.choice(
                list(dists[param].keys()),
                size=size,
                p=list(dists[param].values()),
                replace=replace
            ) for param in dists
        }

        params = [
            {param: params[param][i] for param in params} for i in range(size)
        ]

        return params


def is_non_composite(element):
    
    return isinstance(element, (BasicElement, ModifiedElement))


def get_noncomposite_elements(element):
    
    output = [element]
    for sub in output:
        if isinstance(sub, BasicElement) or isinstance(sub, ElementModifier):
            continue
        elif isinstance(sub, ModifiedElement):
            output.append(sub.element)
            for mod in sub.modifiers:
                output.append(mod)
        elif isinstance(sub, CompositeElement):
            for subsub in sub.elements:
                output.append(subsub)
        else:
            raise TypeError('Unexpected type {}'.format(str(type(sub))))
    output = list(filter(is_non_composite, output))    
    return output


def generate_sandia_figure(
    structure_generator: StructureGenerator, 
    routine_generator: RoutineGenerator, 
    decorator_generator: DecoratorGenerator,
) -> Element:
    
    restr_rot_params = {
        'angle': {
            k: v 
            for k, v in decorator_generator.params[rotation]['angle'].items()
            if v < math.pi 
        }
    }
    normalizing_ct = sum(restr_rot_params['angle'].values())
    restr_rot_params['angle'] = {
        k: v / normalizing_ct for k, v in restr_rot_params['angle'].items()
    } 

    element = structure_generator.sample()
    noncomposite_elements = get_noncomposite_elements(element)
    
    for e in noncomposite_elements:
        if isinstance(e, BasicElement):
            e.routine = routine_generator.sample().pop()
            e.params = routine_generator.sample_params(e.routine).pop()
            
    for e in noncomposite_elements:
        if isinstance(e, ModifiedElement):
           
            decorators = decorator_generator.sample(
                size=len(e.modifiers), replace=False
            )  
            # Move numerosity element to the end, if present
            if numerosity in decorators:
                idx = decorators.index(numerosity)
                num = decorators.pop(idx)
                decorators.append(num)

            for modifier, decorator in zip(e.modifiers, decorators):
                modifier.decorator = decorator
                if (
                    e.element in [ellipse, rectangle] and
                    decorator == rotation
                ):
                    modifier.params = decorator_generator.sample_params(
                        dists = restr_rot_params
                    ).pop()
                else:
                    modifier.params = decorator_generator.sample_params(
                        decorator
                    ).pop()

    return element