# todo: copy templates to material_admin

settings = """
INSTALLED_APPS = [x for x in INSTALLED_APPS if x != 'django.contrib.admin']
INSTALLED_APPS = ['material.admin', 'material.admin.default'] + INSTALLED_APPS
MATERIAL_ADMIN_SITE = {
    # 'HEADER': _(COMPANY_BRAND_NAME),  # Admin site header
    # 'FAVICON': 'favicon.ico',  # 'flagstar.ico'
    # 'MAIN_BG_COLOR': '#007399',  # 'firebrick',  # Admin site main color, css color should be specified
    # 'MAIN_HOVER_COLOR': 'black',  # Admin site main hover color, css color should be specified
    # 'PROFILE_PICTURE': None,  # 'material/admin/images/login-logo-red.jpg',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG': 'material/admin/images/login-bg-default.jpg',  # Admin site profile background (path to static should be specified)
    # 'PROFILE_BG': 'grouppic.JPG',  # Admin site profile background (path to static should be specified)
    # 'LOGIN_LOGO': 'favicon.ico',  # Admin site logo on login page (path to static should be specified)
    # 'LOGOUT_BG': 'blurrybar.JPG',  # Admin site background on login/logout pages (path to static should be specified)
    # 'SHOW_COUNTS': True,
}
TEMPLATES[0]["DIRS"] = [
    os.path.join(BASE_DIR, "templates", "material_admin")
] + TEMPLATES[0]["DIRS"]
"""
