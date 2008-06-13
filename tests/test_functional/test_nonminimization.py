"""Test non-minimization recognition"""

from nose.tools import eq_

from routes.mapper import Mapper


def test_basic():
    m = Mapper()
    m.minimization = False
    m.connect('/:controller/:action/:id')
    m.create_regs(['content'])
    
    # Recognize
    eq_(None, m.match('/content'))
    eq_(None, m.match('/content/index'))
    eq_(None, m.match('/content/index/'))
    eq_({'controller':'content','action':'index','id':'4'}, 
        m.match('/content/index/4'))
    eq_({'controller':'content','action':'view','id':'4.html'},
        m.match('/content/view/4.html'))
    
    # Generate
    eq_(None, m.generate(controller='content'))
    eq_('/content/index/4', m.generate(controller='content', id=4))
    eq_('/content/view/3', m.generate(controller='content', action='view', id=3))

def test_full():
    m = Mapper()
    m.minimization = False
    m.connect('/:controller/:action/', id=None)
    m.connect('/:controller/:action/:id')
    m.create_regs(['content'])
    
    # Recognize
    eq_(None, m.match('/content'))
    eq_(None, m.match('/content/index'))
    eq_({'controller':'content','action':'index','id':None}, 
        m.match('/content/index/'))
    eq_({'controller':'content','action':'index','id':'4'}, 
        m.match('/content/index/4'))
    eq_({'controller':'content','action':'view','id':'4.html'},
        m.match('/content/view/4.html'))
    
    # Generate
    eq_(None, m.generate(controller='content'))
    
    # Looks odd, but only controller/action are set with non-explicit, so we
    # do need the id to match
    eq_('/content/index/', m.generate(controller='content', id=None))
    eq_('/content/index/4', m.generate(controller='content', id=4))
    eq_('/content/view/3', m.generate(controller='content', action='view', id=3))

def test_action_required():
    m = Mapper()
    m.minimization = False
    m.explicit = True
    m.connect('/:controller/index', action='index')
    m.create_regs(['content'])
    
    eq_(None, m.generate(controller='content'))
    eq_(None, m.generate(controller='content', action='fred'))
    eq_('/content/index', m.generate(controller='content', action='index'))

def test_query_params():
    m = Mapper()
    m.minimization = False
    m.explicit = True
    m.connect('/:controller/index', action='index')
    m.create_regs(['content'])
    
    eq_(None, m.generate(controller='content'))
    eq_('/content/index?test=sample', 
        m.generate(controller='content', action='index', test='sample'))
    

def test_syntax():
    m = Mapper()
    m.minimization = False
    m.connect('/{controller}/{action}/{id}')
    m.create_regs(['content'])
    
    # Recognize
    eq_(None, m.match('/content'))
    eq_(None, m.match('/content/index'))
    eq_(None, m.match('/content/index/'))
    eq_({'controller':'content','action':'index','id':'4'}, 
        m.match('/content/index/4'))
    
    # Generate
    eq_(None, m.generate(controller='content'))
    eq_('/content/index/4', m.generate(controller='content', id=4))
    eq_('/content/view/3', m.generate(controller='content', action='view', id=3))

def test_regexp_syntax():
    m = Mapper()
    m.minimization = False
    m.connect('/{controller}/{action}/{id:\d\d}')
    m.create_regs(['content'])
    
    # Recognize
    eq_(None, m.match('/content'))
    eq_(None, m.match('/content/index'))
    eq_(None, m.match('/content/index/'))
    eq_(None, m.match('/content/index/3'))
    eq_({'controller':'content','action':'index','id':'44'}, 
        m.match('/content/index/44'))
    
    # Generate
    eq_(None, m.generate(controller='content'))
    eq_(None, m.generate(controller='content', id=4))
    eq_('/content/index/43', m.generate(controller='content', id=43))
    eq_('/content/view/31', m.generate(controller='content', action='view', id=31))
