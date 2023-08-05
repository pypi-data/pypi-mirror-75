from rth.virtual_building.utils import *


class RoutingTablesGenerator:

    #
    # DUNDERS
    #
    def __init__(self, network_creator_instance, subnets, routers, links, hops, equitemporality=True):
        self.ncinst = network_creator_instance
        # given basics
        self.subnets = subnets
        self.routers = routers
        self.equitemporality = equitemporality
        self.hops = hops
        self.links = links
        self.master_router = get_master_router(self.routers)

    #
    # Getters
    #
    @staticmethod
    def router_ip(instance_, provided):
        return instance_.routers[provided] if provided in instance_.routers else False

    #
    # Executers
    #
    def build_paths_from_possibilites(self, routers_infos, outer_list, inner_list, return_as_dict=False):
        """

        Args:
            routers_infos: A list with the master router ID in 0 and the current router in 1
            outer_list: The subnetwork(s) to reach from the current router
            inner_list: The subnetwork(s) connected to the current router
            return_as_dict: (boolean) if the results are returned as a dict or only the
                first subnetwork of the smaller path is returned

        Returns:

        """
        paths_ = {} if return_as_dict else []

        for end in outer_list:
            inner_paths = []
            for start in inner_list:
                # we get the previously generated hop
                if start != end:
                    inner_paths.append(self.hops[(start, end)])
                else:
                    inner_paths.append([start])
            # we choose the smaller path out of every path in this list
            if (inner_paths[0] == [routers_infos[1]]) and (routers_infos[0] != routers_infos[1]):
                del inner_paths[0]
            if return_as_dict:
                paths_[end] = smaller_of_list(inner_paths)
            else:
                paths_.append(smaller_of_list(inner_paths))

        if return_as_dict:
            return paths_
        else:
            return smaller_of_list(paths_)[0]

    def try_router_connected_to_subnet(self, subnets, router_uid):
        ip_ = None
        sub = None
        for subnet_ in subnets:
            result = self.router_ip(self.subnets[subnet_]['instance'], router_uid)
            if result is not False:
                ip_ = result
                sub = subnet_
                break
        return ip_, sub

    #
    # Callable
    #
    def get_routing_table(self, router_id):

        routing_table = {}
        subnets_done = []
        subnets_attached = self.links['routers'][router_id]

        # starting off by listing attached subnets and getting their ip for this router
        for subnet in subnets_attached:
            inst_ = self.subnets[subnet]['instance']
            routing_table[inst_.cidr] = {
                'gateway': self.router_ip(inst_, router_id),
                'interface': self.router_ip(inst_, router_id)
            }
            subnets_done.append(subnet)

        # getting master route

        # the subnetwork attached to the master router
        master_attached = self.links['routers'][self.master_router]

        # the subnetwork that leads to the master router
        to_master_uid = self.build_paths_from_possibilites([self.master_router, router_id],
                                                           master_attached, subnets_attached)

        # now retrieving the IP of this router that points to the subnetwork leading to the master router
        to_master_gateway, to_master_uid = self.try_router_connected_to_subnet(subnets_attached, to_master_uid)

        if not to_master_gateway:
            raise Exception("To-master router should have been found in at least one of the subnetworks")

        to_master_interface = self.ncinst.get_ip_of_router_on_subnetwork(to_master_uid, router_id)

        if to_master_interface is None:
            raise Exception(f"Interface to master of router {router_id} should not be None")

        routing_table['0.0.0.0/0'] = {
            "gateway": to_master_gateway,
            "interface": to_master_interface
        }

        # now we get each non-registered-yet subnet left
        subnets_left = [i for i in self.subnets
                        if self.subnets[i]['instance'].uid not in subnets_done]
        paths = self.build_paths_from_possibilites([self.master_router, router_id], subnets_left,
                                                   subnets_attached, return_as_dict=True)

        for subnet in subnets_left:
            router = paths[subnet][0]
            ip, subnet_id = self.try_router_connected_to_subnet(subnets_attached, router)
            if not ip:
                raise Exception(f"Router id {router} should have been found in at least one of the subnetworks")
            interface = self.ncinst.get_ip_of_router_on_subnetwork(subnet_id, router_id)
            if not interface:
                raise Exception(f"Could not find interface of router {router_id} on subnet {subnet_id}, though the "
                                f"router points to a gateway on this subnetwork")
            routing_table[self.subnets[subnet]['instance'].cidr] = {
                "gateway": ip,
                "interface": interface
            }

        return routing_table

    def calculate_better_path_from_delays(self):
        raise NotImplementedError
