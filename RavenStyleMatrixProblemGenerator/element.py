'''This module exports classes for representing figures in matrix problems.

Here, matrix figures are conceptualized as structured collections of *elements*, 
where elements are considered to be identifiable/recognizable figural segments. 
Specifically, a matrix figure is considered to be fully specified by the highest 
level element in a given context (i.e., in a given cell).

Elements are recursively defined. An element may have one of three forms: it may 
be

- a basic element (`basic_element` in syntax), which is an unanalyzed visual 
  pattern;
- a modified element (`modified_element` in syntax), which is a base element 
  that has been subject to some sequence of modifications (`modifier_sequence` 
  in syntax); or
- a composite element (`composite_element` in syntax), which is a sequence of 
  overlayed elements.

Element Structure Syntax (BNF)
------------------------------

element ::= basic_element | modified_element | composite_element
modified_element ::= element modifier_sequence
composite_element ::= element element {element}  
modifier_sequence :: element_modifier {element_modifier}
'''


import abc
from typing import Callable, List, Any, Union
import cairo


class ElementNode(abc.ABC):
    '''Represents a generic node in element structure syntax.'''

    def __repr__(self):

        return ''.join(repr(type(self)), '(', repr(vars(self)), ')')

    def __eq__(self, other : Any) -> bool:
        '''Return ``True`` if ``other`` is equal to ``self``.
        
        ``self == other`` iff:

        - ``type(self) == type(other)`` and
        - ``vars(self) == vars(other)`` 
        '''

        return (
            type(self) == type(other) and
            vars(self) == vars(other)
        )


class Element(ElementNode):
    '''Represents an identifiable figure segment.

    ``Element`` is an abstract base class. It cannot be directly instantiated.
    '''

    @abc.abstractmethod
    def draw_in_context(self, ctx : cairo.Context) -> None:
        '''Draw self in the given context.

        :param ctx: The context in which self will be drawn.
        '''
        pass

    
class ElementModifier(ElementNode):
    '''Represents an alteration of the drawing procedure for a given element.
    '''
    
    @abc.abstractmethod
    def __call__(
        self, element : Callable[[cairo.Context], None]
    ) -> Callable[[cairo.Context], None]:
        '''Modify ``element.draw_in_context`` and return result.
        
        Should return a wrapper of ``element.draw_in_context`` implementing the 
        desired modification.

        :param element: An element whose draw routine is to be modified by self.
        '''
        pass


class BasicElement(Element):
    '''An unanalyzed figural unit.
    
    ``BasicElement`` is an abstract base class. It cannot be directly 
    instantiated. 
    '''
    pass


class EmptyElement(BasicElement):
    '''Represents an empty element.
    '''

    def __bool__(self):
        '''Always evaluates to ``False``.'''
        
        return False
    
    def draw_in_context(self, ctx):
        pass
    
    
class ModifiedElement(Element):
    '''Represents an element altered by a sequence of modifiers.
    '''
    
    def __init__(
        self, 
        element : Element, 
        modifier : ElementModifier, 
        *modifiers : ElementModifier
    ) -> None:
        
        self.element = element
        self.modifiers = [modifier]
        self.modifiers.extend(modifiers)
    
    def draw_in_context(self, ctx : cairo.Context):
        
        modified : Callable[[cairo.Context], None] = (
            self.element.draw_in_context
        )
        for modifier in self.modifiers:
            modified = modifier(modified)
        modified(ctx)

    
class CompositeElement(Element):
    '''Represents a sequence of overlayed elements.'''
    
    def __init__(
        self, element_1 : Element, element_2 : Element, *elements : Element
    ) -> None:
        
        self.elements = [element_1, element_2]
        self.elements.extend(elements)
        
    def draw_in_context(self, ctx : cairo.Context) -> None:

        for element in self.elements:
            element.draw_in_context(ctx)