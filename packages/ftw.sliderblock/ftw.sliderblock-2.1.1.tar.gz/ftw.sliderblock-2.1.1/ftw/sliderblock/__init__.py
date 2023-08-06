from Products.CMFPlone.utils import getFSVersionTuple
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('ftw.sliderblock')


if getFSVersionTuple() > (5, ):
    IS_PLONE_5 = True
else:
    IS_PLONE_5 = False
