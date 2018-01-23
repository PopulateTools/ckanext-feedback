# -*- coding: utf-8 -*-

import smtplib
import os
import logging
import socket

import ckan.plugins as p
import ckan.plugins.toolkit as t

import pylons.config as config

from ckan.common import request
from ckan.common import c
from ckan.lib.base import BaseController
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


class FeedbackController(BaseController):

    def feedback(self):
        return p.toolkit.render('feedbackForm.html')

    def feedbackProv(self):
        current_user = t.get_action('user_show')({}, { 'id': c.user })
        request_sender_name = current_user['display_name']

        try:
            receiver_user = t.get_action('user_show')({},{ 'id': 'ecoembes' })
            receiver_email = receiver_user['email']
        except t.ObjectNotFound:
            receiver_email = config.get('ckan.feedback.receiver_email')

        sender_email   = config.get('ckan.feedback.sender_email', 'notifications@ckan.dev')

        # build message

        msg = MIMEMultipart()
        msg['From']    = sender_email
        msg['To']      = receiver_email
        msg['Date']    = formatdate(localtime=True)
        msg['Subject'] = 'Nueva petición de datos recibida'

        email_body = ('Nombre de usuario: ' + request_sender_name.encode('utf-8') + "\nPetición: ".decode('utf-8') + request.params['data_request_description']).encode('utf-8')

        msg.attach(MIMEText(email_body))

        # send email
        try:
            smtp_address = config.get('ckan.feedback.smtp_address')
            smtp_port = t.asint(config.get('ckan.feedback.smtp_port', 25))
            smtp_server = smtplib.SMTP(smtp_address, smtp_port)
            smtp_server.sendmail(sender_email, receiver_email, msg.as_string() )
            smtp_server.close()
        except socket.error:
            logging.error('Error establishing SMTP connection to server: ' + smtp_address + ' port ' + str(smtp_port))
            raise

        return p.toolkit.render('feedbackProv.html')
