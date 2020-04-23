    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/27
# @Author  : Kun Guo
# @Version : 1.0
from statistics.intersect.guest import IntersectGuest
from statistics.intersect.host import IntersectHost

class Intersect(object):
    '''
    A class for privacy preserving entity match. Algorithm is designed according to paper
    "G. Liang and S. S. Chawathe, “Privacy-Preserving Inter-database Operations,” in Lecture Notes in Computer Science
     (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics), vol. 3073, 2004,
      pp. 66–82."
    '''
    def run(self, dataset_host, dataset_guest):
        '''
        :param dataset_host: user id list from host
        :param dataset_guest: user id list from guest
        :return: intersection of their idx
        '''
        host = IntersectHost()
        guest = IntersectGuest(host.get_rsa_public_key())
        guest_idx = guest.send_guest_idx(dataset_guest)
        guest_idx_host = host.process_guest_idx(guest_idx)
        host_idx = host.send_host_idx(dataset_host)
        (intersect_idx_enc, intersect_idx_raw_guest) = guest.process_host_guest_idx(host_idx, guest_idx_host)
        intersect_idx_raw_host = host.process_intersect_idx(intersect_idx_enc)
        assert(intersect_idx_raw_host == intersect_idx_raw_guest) #execute when false
        return intersect_idx_raw_host