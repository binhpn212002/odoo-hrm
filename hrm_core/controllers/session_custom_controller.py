# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import operator

from werkzeug.urls import url_encode

import odoo
import odoo.modules.registry
from odoo import http
from odoo.modules import module
