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

Strictly speaking, transformations are not part of the description of a figure, 
thus they are not defined in this module.
'''


import abc
from typing import Callable, List, Any
import cairo


class Element(abc.ABC):
    '''Represents an identifiable figure segment.

    `Element` is an abstract base class. It cannot be directly instantiated.
    '''
    
    @abc.abstractmethod
    def draw_in_context(self, ctx : cairo.Context) -> None:
        '''Draw self in the given context.

        :param ctx: The context in which self will be drawn.
        '''
        pass

    
class ElementModifier(abc.ABC):
    '''Represents an alteration of the drawing procedure for a given element.
    '''
    
    def __eq__(self, other : Any) -> bool:
        '''Return `True` if `other` is equal to `self`.
        
        `self == other` iff:

        - `type(self) == type(other)` and
        - `vars(self) == vars(other)` 
        '''

        return (
            type(self) == type(other) and
            vars(self) == vars(other)
        )

    @abc.abstractmethod
    def __call__(
        self, element : Callable[[cairo.Context], None]
    ) -> Callable[[cairo.Context], None]:
        '''Modify `element.draw_in_context` and return result.
        
        Should return a wrapper of `element.draw_in_context` implementing the 
        desired modification.

        :param element: An element whose draw routine is to be modified by self.
        '''
        pass


class BasicElement(Element):
    '''An unanalyzed figural unit.
    
    `BasicElement` is an abstract base class. It cannot be directly 
    instantiated. 
    '''
    
    def __eq__(self, other : Any) -> bool:
        '''Return `True` if `other` is equal to `self`.
        
        `self == other` iff:

        - `type(self) == type(other)` and
        - `vars(self) == vars(other)` 
        '''

        return (
            type(self) == type(other) and
            vars(self) == vars(other)
        )
    
    
class ModifiedElement(Element):
    '''Represents an element altered by a sequence of modifiers.
    '''
    
    def __init__(
        self, 
        element : Element, 
        modifier : ElementModifier, 
        *modifiers : ElementModifier
    ) -> None:
        
        self._element = element
        self._modifiers = [modifier]
        self._modifiers.extend(modifiers)

    def __eq__(self, other : Any) -> bool:
        '''Return `True` if `other` is equal to `self`.
        
        `self == other` iff:

        - `other` is a `ModifiedElement` instance and
        - `self.element == other.element` and
        - `self.modifiers == other.modifiers` 
        '''

        return (
            isinstance(other, ModifiedElement) and
            self.element == other.element and
            self.modifiers == other.modifiers
        )
    
    def draw_in_context(self, ctx : cairo.Context):
        
        modified : Callable[[cairo.Context], None] = (
            self.element.draw_in_context
        )
        for modifier in self.modifiers:
            modified = modifier(modified)
        modified(ctx)

    @property
    def element(self) -> Element:
        '''The base element of `self`.'''
        return self._element

    @property
    def modifiers(self) -> List[ElementModifier]:
        '''The sequence of modifiers applied to base element of `self`.'''
        return self._modifiers 
        
    
class CompositeElement(Element):
    '''Represents a sequence of overlayed elements.'''
    
    def __init__(
        self, element_1 : Element, element_2 : Element, *elements : Element
    ) -> None:
        
        self._elements = [element_1, element_2]
        self._elements.extend(elements)

    def __eq__(self, other : Any) -> bool:
        '''Return True if other is equal to self.
        
        `self == other` iff:

        - `other` is a `CompositeElement` instance and
        - `self.elements == other.elements`  
        '''

        return (
            isinstance(other, CompositeElement) and 
            self.elements == other.elements
        )
        
    def draw_in_context(self, ctx : cairo.Context) -> None:

        for element in self.elements:
            element.draw_in_context(ctx)

    @property
    def elements(self) -> List[Element]:
        '''Sub-elements of `self`.'''
        return self._elements