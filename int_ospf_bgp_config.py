
from nornir import InitNornir
from nornir_scrapli.tasks import send_commands, send_configs
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_title, print_result

nr = InitNornir(config_file="config.yml")

# Loading variable dynamicaly #
def load_variable(task):
    input_data = task.run(task=load_yaml, name="Geting info from Variables",
                          file=f'./routers/{task.host}.yaml')
    task.host['conf'] = input_data.result
    int_ospf_bgp_configuration(task)

# Sending interface_IP_ospf_iBGP _config_to _RR-1,RR-2,R1,R2,R3,R4#
def int_ospf_bgp_configuration(task):
    int_ospf_bgp_j2_temp = task.run(
        task=template_file, name="Interface , OSPF and iBGP Configuration", template="int_ospf_bgp_config.j2", path="")
    output_data = int_ospf_bgp_j2_temp.result
    cmd_send = output_data.splitlines()
    task.run(task=send_configs,
             name="Configuring Int_OSPF_iBGP", configs=cmd_send)

# Checking Interface, ospf and bgp neighbor status#
def show_status_ospf_bgp(task):
    show_cmd = task.run(task=send_commands, commands=[
        "show ip ospf neighbor", "show ip bgp summary"])


# Checking IGP and iBGP nrighbor status #
print_title('***Interface Ip , OSPF and iBGP configuration***')
result = nr.run(task=load_variable)
print_result(result)

showcmd = nr.run(task=show_status_ospf_bgp)
print_title('OSPF and BGP Neighbor Status')
print_result(showcmd)

