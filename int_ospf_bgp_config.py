from nornir import InitNornir
from nornir.core import task
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_scrapli.tasks import (
    get_prompt, send_commands, send_command, send_configs)
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_title, print_result

nr = InitNornir(config_file="config.yml")

# loading variable dynamicaly


def load_variable(task):
    input_data = task.run(task=load_yaml, name="Geting info from Variables",
                          file=f'./routers/{task.host}.yaml')
    task.host['conf'] = input_data.result
    int_ospf_bgp_configuration(task)

# sending interface_ospf_bgp_config_to _each_router


def int_ospf_bgp_configuration(task):
    bgp_j2_temp = task.run(
        task=template_file, name="Interface , OSPF and iBGP Configuration", template="int_ospf_bgp_config.j2", path="")
    output_data = bgp_j2_temp.result
    cmd_send = output_data.splitlines()
    task.run(task=netmiko_send_config,
             name="Configuring iBGP", config_commands=cmd_send)


# checking Interface, ospf and bgp status

def show_status_ospf_bgp(task):
    show_cmd = task.run(task=send_commands, commands=[
        "show ip ospf neighbor", "show ip bgp summary"])


print_title('***Interface Ip , OSPF and iBGP configuration***')
result = nr.run(task=load_variable)
print_result(result)

showcmd = nr.run(task=show_status_ospf_bgp)
print_title('OSPF and BGP Neighbor Status')
print_result(showcmd)
