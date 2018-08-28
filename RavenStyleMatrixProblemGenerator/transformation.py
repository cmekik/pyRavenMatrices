import copy
from element import (
    ElementModifier, 
    BasicElement, 
    EmptyElement, 
    ModifiedElement, 
    CompositeElement
)


class Transformation(object):
    '''Represents a Raven-style figure transformation.'''
    
    def __init__(self, *args):
        '''
        Initialize transformation instance
        
        Every arg is assumed to have the form:

        ``(condition, action)``
        
        ``condition`` is an element and ``action`` is a tuple
        to of the form ``(op, loc, *args, **kwarg)``, where ``op`` is the
        desired operation ``loc`` points to the location in an element at 
        which the operation should be executed and ``*args``` are a list of 
        arguments to be given that operation.        
        '''
        
        self.pairs = args
        
    def __call__(self, element):
        '''Transform ``element``.'''
        
        output = copy.deepcopy(element)
        for condition, action in self.args:
            if condition in get_subtrees(element):
                output = transform(output, *action)
        return output


def transform(element, op, loc, *args, **kwargs):
    '''
    Apply ``op`` to every occurrence of ``loc`` in ``element``.

    :param ``element``: Target element for transformation.
    :param ``op``: Operation for altering ``element``.
    :param ``loc``: Subelement of ``element`` to be modified.
    :param ``*args``: Args to be passed on to ``op``.
    :param ``**kwargs``: Kwargs to be passed on to ``op``.
    '''
    
    # Implemented using recursion.

    if element == loc: # apply op; return result.
    
        return op(element, *args, **kwargs)
    
    else: # propagate to subelements (if any) and return result
        
        if isinstance(element, (BasicElement, ElementModifier)):
            return element
        
        elif isinstance(element, ModifiedElement):
            new_subelt = transform(op, element.element, loc, *args, **kwargs)
            new_mods = [
                tfd for tfd in (
                    transform(op, mod, loc, *args, **kwargs) for mod in 
                    element.modifiers
                ) if tfd
            ]
            if new_subelt and new_mods:
                return ModifiedElement(new_subelt, *new_mods)
            elif new_subelt and not new_mods:
                return new_subelt
            else:
                return EmptyElement()
            
        elif isinstance(element, CompositeElement):
            new_elts = [
                elt for elt in (
                    transform(op, elt, loc, *args, **kwargs) for elt in 
                    element.elements
                ) if elt
            ]
            if len(new_elts) > 1:
                return CompositeElement(*new_elts)
            elif len(new_elts) == 1:
                return new_elts.pop()
            else:
                return EmptyElement()
            
            
def add(element, addition):
    '''Add ``addition`` to ``element`` and return result.'''

    # Should add addition to element and return result
    
    # **Deepcopy** for safe in-place ops
    output = copy.deepcopy(element)
    
    if (
        isinstance(output, (BasicElement, ModifiedElement)) and 
        isinstance(addition, Element)
    ):
        output = CompositeElement(output, addition)
    elif (
        isinstance(output, (BasicElement, CompositeElement)) and 
        isinstance(addition, ElementModifier)
    ):
        output = ModifiedElement(output, addition)
    elif (
        isinstance(output, CompositeElement) and 
        isinstance(addition, Element)
    ):
        output.elements.append(addition)
    elif (
        isinstance(output, ModifiedElement) and 
        isinstance(addition, ElementModifier)
    ):
        output.modifiers.append(addition)
    
    return output


def remove(element):
    '''Remove ``element``.'''
    
    return EmptyElement()


def replace(element, replacement):
    '''Replace ``element`` with ``replacement``.'''
    
    if (
        isinstance(element, Element) and 
        not isinstance(replacement, Element)
    ): 
        raise TypeError(
            'Expected Element, got {}'.format(
                type(replacement).__name__
            )
        )        
    elif (
        isinstance(element, ElementModifier) and
        not isinstance(replacement, ElementModifier)
    ):
        raise TypeError(
            'Expected ElementModifier, got {}'.format(
                type(replacement).__name__
            )
        )
    
    return replacement