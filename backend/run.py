from core.app import app, HOST, PORT
from core.controllers.brands import bp as bp_brands
from core.controllers.categories import bp as bp_categories
from core.controllers.distributors import bp as bp_distributors
from core.controllers.users import bp as bp_users
from core.controllers.groups import bp as bp_groups
from core.controllers.permissions import bp as bp_permissions
from core.controllers.modules import bp as bp_modules
from core.controllers.equipments import bp as bp_equipments
from core.controllers.parts import bp as bp_parts
from core.controllers.installations import bp as bp_installations
from core.controllers.manuals import bp as bp_manuals
from core.controllers.warranties import bp as bp_warranties


app.register_blueprint(bp_brands, url_prefix='/api/brands')
app.register_blueprint(bp_categories, url_prefix='/api/categories')
app.register_blueprint(bp_distributors, url_prefix='/api/distributors')
app.register_blueprint(bp_users, url_prefix='/api/users')
app.register_blueprint(bp_groups, url_prefix='/api/groups')
app.register_blueprint(bp_modules, url_prefix='/api/modules')
app.register_blueprint(bp_permissions, url_prefix='/api/permissions')
app.register_blueprint(bp_equipments, url_prefix='/api/equipments')
app.register_blueprint(bp_parts, url_prefix='/api/parts')
app.register_blueprint(bp_installations, url_prefix='/api/installations')
app.register_blueprint(bp_manuals, url_prefix='/api/manuals')
app.register_blueprint(bp_warranties, url_prefix='/api/warranties')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
