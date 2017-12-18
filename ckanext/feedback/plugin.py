# -*- coding: utf-8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation


class FeedbackPlugin(plugins.SingletonPlugin, DefaultTranslation):

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.ITranslation)

  def update_config(self,config):
    toolkit.add_template_directory(config, 'templates')

  def before_map(self, m):
    m.connect('feedback', '/feedback', controller='ckanext.feedback.controller:FeedbackController', action='feedback')
    m.connect('feedbackProv', '/feedbackProv', controller='ckanext.feedback.controller:FeedbackController', action='feedbackProv')

    return m
