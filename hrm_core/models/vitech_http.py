from odoo import http

# Save the original method
_old_get_session_and_dbname = http.Request._get_session_and_dbname

# Define the new method
def _new_get_session_and_dbname(self):
    session, dbname = _old_get_session_and_dbname(self)
    # If no dbname is found, use the value from the 'x-db' header
    if not dbname:
        dbname = self.httprequest.headers.get('x-db')
    return session, dbname

# Override the original method with the new one
http.Request._get_session_and_dbname = _new_get_session_and_dbname
