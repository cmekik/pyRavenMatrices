#############
### SETUP ###
#############


import math
import cairo
import os
import RavenStyleMatrixProblems.matrix as mat
import RavenStyleMatrixProblems.element as elt


##############
### SHAPES ###
##############


def oval(ctx, cell_structure, tallness = 2, slack=.9):
    
    if not 1 < tallness:        
        raise ValueError()
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(width / (2 * tallness), height / 2.)
    ctx.new_sub_path()
    ctx.arc(0., 0., 1., 0., 2 * math.pi)
    ctx.restore()


def triangle(ctx, cell_structure, wideness=1, tallness=1, slack=.9):
    
    if not (wideness >= 1 and tallness >= 1):        
        raise ValueError()
        
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    div = max(tallness, wideness)
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(wideness / div,tallness / div)
    ctx.new_sub_path()
    ctx.move_to(- width / 2., height / 2.)
    ctx.line_to(width / 2., height / 2.)
    ctx.line_to(0, - height / 2.)
    ctx.line_to(- width / 2., height / 2.)
    ctx.restore()


def rectangle(ctx, cell_structure, tallness = 2, slack=.9):
    
    if not tallness > 1:
        raise ValueError()
    
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(1/tallness, 1)
    ctx.new_sub_path()
    ctx.move_to(- width / 2., height / 2.)
    ctx.line_to(width / 2., height / 2.)
    ctx.line_to(width / 2., - height / 2.)
    ctx.line_to(- width / 2., - height / 2.)
    ctx.line_to(- width / 2., height / 2.)
    ctx.restore()


def trapezoid(ctx, cell_structure, wideness=2, tallness=1, slack=.9):
    
    if not (1 <= tallness and 1 <= wideness):        
        raise ValueError()
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    div = max(tallness, wideness)
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(wideness / div, tallness / div)
    ctx.new_sub_path()
    ctx.move_to(- width / 2., height / 2.)
    ctx.line_to(width / 2., height / 2.)
    ctx.line_to(width / 4., - height / 2.)
    ctx.line_to(- width / 4., - height / 2.)
    ctx.line_to(- width / 2., height / 2.)
    ctx.restore()


def diamond(ctx, cell_structure, tallness=1, slack=.9):
    
    if not 1 <= tallness:        
        raise ValueError()
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(1 / tallness, 1)
    ctx.new_sub_path()
    ctx.move_to(0, height / 2.)
    ctx.line_to(width / 2., - height / 4.)
    ctx.line_to(0, - height / 2.)
    ctx.line_to(- width / 2., - height / 4.)
    ctx.line_to(0, height / 2.)
    ctx.restore()


def tee(ctx, cell_structure, wideness=1, tallness=1, slack=.9):
    
    if not (1 <= tallness and 1 <= wideness):        
        raise ValueError()
    width = cell_structure.width * slack
    height = cell_structure.height * slack
    
    div = max(tallness, wideness)
    
    ctx.save()
    ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
    ctx.scale(wideness / div, tallness / div)
    ctx.new_sub_path()
    ctx.move_to(- width / 6., height / 2.)
    ctx.line_to(width / 6., height / 2.)
    ctx.line_to(width / 6., - height / 4.)
    ctx.line_to(width / 2., - height / 4.)
    ctx.line_to(width / 2., - height / 2.)
    ctx.line_to(- width / 2., - height / 2.)
    ctx.line_to(- width / 2., - height / 4.)
    ctx.line_to(- width / 6., - height / 4.)
    ctx.line_to(- width / 6., height / 2.)
    ctx.restore()


#################
### MODIFIERS ###
#################


def scale(element, factor=.5):

    def wrapped(ctx, cell_structure, *args, **kwargs):

        ctx.save()
        ctx.scale(factor, factor)
        ctx.translate(cell_structure.width/2., cell_structure.height/2.)
        element(ctx, cell_structure, *args, **kwargs)
        ctx.restore()

    return wrapped


def rotation(element, angle=math.pi/2.):

    def wrapped(ctx, cell_structure, *args, **kwargs):

        ctx.save()
        ctx.translate(cell_structure.width / 2., cell_structure.height / 2.)
        ctx.rotate(angle)
        ctx.translate(-cell_structure.width / 2., -cell_structure.height / 2.)
        element(ctx, cell_structure)
        ctx.restore()
        
    return wrapped


def shading(element, lightness=.5):
    
    def wrapped(ctx, cell_structure, *args, **kwargs):

        element(ctx, cell_structure, *args, **kwargs)
        ctx.save()
        ctx.set_source_rgb(lightness, lightness, lightness)
        ctx.fill_preserve()
        ctx.restore()
    
    return wrapped


def numerosity(element, number=5):
    
    def wrapped(ctx, cell_structure, *args, **kwargs):

        for i in range(number):
            
            x = (i % 3) * (cell_structure.width / 3.)
            y = (i // 3) * (cell_structure.height / 3.)
            
            ctx.save()
            ctx.translate(x, y)
            ctx.scale(1 / 3, 1 / 3)
            element(ctx, cell_structure, *args, **kwargs)
            ctx.restore()
    
    return wrapped
