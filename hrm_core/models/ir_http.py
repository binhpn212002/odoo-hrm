from odoo import models
class IrHttp(models.AbstractModel):
  _inherit = "ir.http"

  @classmethod
  def _auth_method_my_api_key(cls):
    pass