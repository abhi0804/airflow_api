import importlib
import pkgutil
import plugins.custom_operators  # Assume this is the package name for your custom plugins

# Function to dynamically import all operators in the plugins folder

# for loader, module_name, is_pkg in pkgutil.iter_modules(plugins.custom_operators.__path__):
#     try:
#         module = importlib.import_module(f"plugins.custom_operators.{module_name}")
#         print(f"from custom_operators.{module_name} import *")
#     except ImportError as e:
#         print(f"Error importing module {module_name}: {e}")


from jinja2 import Template

# template = """hostname {{ hostname }}

# no ip domain lookup
# ip domain name local.lab
#     ip name-server {{ name_server_pri }}
#     ip name-server {{ name_server_sec }}

# ntp server {{ ntp_server_pri }} prefer
# ntp server {{ ntp_server_sec }}"""

# data = {
#     "hostname": "core-sw-waw-01",
#     "name_server_pri": "1.1.1.1",
#     "name_server_sec": "8.8.8.8",
#     "ntp_server_pri": "0.pool.ntp.org",
#     "ntp_server_sec": "1.pool.ntp.org",
# }

data = {

    "jobs" : [
        {"name" : "first"},
        {"name" : "second"},
        {"name" : "third"}
    ]
}

template = """

{% for job in jobs %}
    i = []
    
    job count : {{job.name.upper()}}
{% endfor %}

"""


j2_template = Template(template)

print(j2_template.render(data))
