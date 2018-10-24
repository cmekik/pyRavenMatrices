'''
This module provides tools for implementing figure transformations.

Transformations vs. Modifiers
-----------------------------

There are, so to speak, two levels at which we can talk about *figure 
transformations* and it is worth explicitly disambiguating them. 
*Transformations* as understood in the Raven's Matrices specification, are 
patterns that define how figures differ between matrix rows and columns. 
*Modifiers* (`element_modifier` in syntax) are specific to the representational 
scheme used in this package and serve to define one figural element in terms of 
other more basic elements.

The key difference between transformations and modifiers is that 
**transformations alter the structure of elements**, whereas **modifiers alter 
the way an element is drawn**. Thus, transformations are a higher level concept 
in this scheme than modifiers: transformations may add modifiers to or remove 
modifiers from figures in addition to having other effects such as addition of 
elements to or removal of elements from figures.
'''


import copy
from typing import Callable, Any, List, cast


class Target(object):
    
    def __init__(
        self, 
        attribute: str = None, 
        index: int = None, 
        parent: 'Target' = None, 
        type: type = None
    ) -> None:
        
        self.attribute = attribute
        self.index = index
        self.parent = parent
        self.type = type
        
    def __repr__(self):
        
        details = self._repr()
        if self.type is not None:
            type_annotation = ', type={}'.format(self.type.__name__)
        else:
            type_annotation = ''
        return 'Target({}{})'.format(details, type_annotation)
    
    def __eq__(self, other):
        
        return (
            self.attribute == other.attribute,
            self.index == other.index,
            self.parent == other.parent,
            self.type == other.type
        )

    def __call__(self, element):
        
        target = element
        if self.parent is not None:
            target = parent(element)
        if self.attribute is not None:
            target = getattr(target, self.attribute)
        if self.index is not None:
            target = target[self.index]
        return target
    
    def _repr(self):
        
        if self.parent is not None:
            parent = self.parent._repr()
        else:
            parent = 'root'
            
        if self.attribute is not None:
            attribute = '.' + self.attribute
        else:
            attribute = ''
            
        if self.index is not None:
            index = str(self.index).join(['[',']'])
        else:
            index = ''
            
        return ''.join([parent, attribute, index])


class Transformation(object):
    
    def __init__(self, *triples):
        
        self.triples = list(triples)
        
    def __call__(self, element):
        
        output = copy.deepcopy(element)
        for target, pattern, value in self.triples:
            if target(element) == pattern:
                if issubclass(target.type, elt.BasicElement):
                    target(output).routine = value['routine']
                else:
                    target(output).decorator = value['decorator']
                target(output).params = value['params']
        return output


def get_targets(element_structure, parent=None):
    
    if isinstance(element_structure, (elt.BasicElement, elt.ElementModifier)):
        if parent:
            return [parent]
        else:
            return [Target(type=type(element_structure))]
    elif isinstance(element_structure, elt.ModifiedElement):
        sub_element = element_structure.element
        ret = get_targets(
            sub_element, 
            parent = Target(
                'element', 
                parent = parent, 
                type = type(sub_element)
            )
        )
        for i, modifier in enumerate(element_structure.modifiers):
            ret += get_targets(
                modifier, 
                Target('modifiers', index=i, parent=parent, type=type(modifier))
            )
    elif isinstance(element_structure, elt.CompositeElement):
        ret = []
        for i, sub_element in enumerate(element_structure.elements):
            ret += get_targets(
                sub_element, 
                Target(
                    'elements', index=i, parent=parent, type=type(sub_element)
                )
            )
    return ret
