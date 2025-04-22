import logging
import json
from processor.base import ResourceProcessor

class MDBMySQLProcessor(ResourceProcessor):
    """Processor for MDB MySQL Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_mysql_cluster"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        disk_size = resource_values["resources"][0].get("disk_size", 0)
        disk_type = resource_values["resources"][0].get("disk_type_id", "network-hdd")
        preset_id = resource_values["resources"][0].get("resource_preset_id", [])
        instances = resource_values.get("host", [])

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('mysql', preset_id)
        except ValueError as e:
            logging.error(e)
            return 1

        instance_num = len(instances)
        public_ip_num = sum(1 for instance in instances if instance.get("assign_public_ip") is True)

        if platform_id == "standard-v3":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn2mfa1c935rjc6t4eek", cores * instance_num, resource_name, resource_type) # MySQL. Intel Ice Lake. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn2lo0l3birckqii0kpd", cores * instance_num, resource_name, resource_type) # MySQL. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2nhjlpvll7kron0lv0", memory * instance_num, resource_name, resource_type) # MySQL. Intel Ice Lake. RAM [gbyte*hour]

        elif platform_id == "highfreq-v3":
            # cpu
            usage_collector.add_usage("dn26hjuqup86h8g2dc4o", cores * instance_num, resource_name, resource_type) # MySQL. Intel Ice Lake (Compute Optimised). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2afr14vhrtu5rgvtvj", memory * instance_num, resource_name, resource_type) # MySQL. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]
        
        elif platform_id == "standard-v2":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn2ekqj88rk6cj186bgv", cores * instance_num, resource_name, resource_type) # MySQL. Intel Cascade Lake. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn23em5ur8pmc5oe1ugg", cores * instance_num, resource_name, resource_type) # MySQL. Intel Cascade Lake. 50% vCPU [core*hour]
            if core_fraction == 20:
                usage_collector.add_usage("dn29qcell9096oecia43", cores * instance_num, resource_name, resource_type) # MySQL. Intel Cascade Lake. 20% vCPU [core*hour]
            if core_fraction == 5:
                usage_collector.add_usage("dn2ikmrgbcfqnq0e89rh", cores * instance_num, resource_name, resource_type) # MySQL. Intel Cascade Lake. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2q9cgq04cl6ju1j2k7", memory * instance_num, resource_name, resource_type) # MySQL. Intel Cascade Lake. RAM [gbyte*hour]
        
        elif platform_id == "standard-v1":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn2hi38l2amv53lnkudh", cores * instance_num, resource_name, resource_type) # MySQL. Intel Broadwell. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn234519saji1v5gtbk7", cores * instance_num, resource_name, resource_type) # MySQL. Intel Broadwell. 50% vCPU [core*hour]
            if core_fraction == 20:
                usage_collector.add_usage("dn24fhsc8h68f51o549s", cores * instance_num, resource_name, resource_type) # MySQL. Intel Broadwell. 20% vCPU [core*hour]
            if core_fraction == 5:
                usage_collector.add_usage("dn2manmpat7cv2ge9kbm", cores * instance_num, resource_name, resource_type) # MySQL. Intel Broadwell. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2s8tj0qdakj5c49e5o", memory * instance_num, resource_name, resource_type) # MySQL. Intel Broadwell. RAM [gbyte*hour]

        if public_ip_num > 0:
            usage_collector.add_usage("dn2non93sh0grnlrjb7m", public_ip_num, resource_name, resource_type) # Public IP address - MySQL [fip*hour]

        if disk_type == "network-ssd":
            usage_collector.add_usage("dn2j7e6hs2j2ugni50lq", disk_size * instance_num, resource_name, resource_type) # Fast network storage \u2014 MySQL [gbyte*hour]
        elif disk_type == "network-hdd":
            usage_collector.add_usage("dn2thbds4400ckbijvch", disk_size * instance_num, resource_name, resource_type) # Standard network storage \u2014 MySQL [gbyte*hour]
        elif disk_type == "network-ssd-nonreplicated":
            usage_collector.add_usage("dn286bla0e9c7d2fnqst", disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 MySQL [gbyte*hour]
        elif disk_type == "network-ssd-io-m3":
            usage_collector.add_usage("dn2po189eb088u6kpa9o", disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 MySQL [gbyte*hour]
        elif disk_type == "local-ssd":
            usage_collector.add_usage("dn28goa6h2rkk2skokee", disk_size * instance_num, resource_name, resource_type) # Fast local storage \u2014 MySQL [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBPostgreProcessor(ResourceProcessor):
    """Processor for MDB PostgreSQL Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_postgresql_cluster"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        disk_size = resource_values["config"][0]["resources"][0].get("disk_size", 0)
        disk_type = resource_values["config"][0]["resources"][0].get("disk_type_id", "network-hdd")
        preset_id = resource_values["config"][0]["resources"][0].get("resource_preset_id", [])
        instances = resource_values.get("host", [])

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('postgresql', preset_id)
        except ValueError as e:
            logging.error(e)
            return 1

        instance_num = len(instances)
        public_ip_num = sum(1 for instance in instances if instance.get("assign_public_ip") is True)

        # Process based on platform_id
        if platform_id == "standard-v3":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn232gunmdllqdl5cicd", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Ice Lake. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn20phj76ak2oh3m4sgn", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2snd5f5rifj49dhovh", memory * instance_num, resource_name, resource_type) # PostgreSQL. Intel Ice Lake. RAM [gbyte*hour]
        
        elif platform_id == "highfreq-v3":
            # cpu
            usage_collector.add_usage("dn2878t3j92nm7ht5tlq", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Ice Lake (Compute Optimised). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2dflbiele6g9he24ee", memory * instance_num, resource_name, resource_type) # PostgreSQL. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]
        
        elif platform_id == "standard-v2":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn2foiqm6aoaghmjcr38", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Cascade Lake. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn2ac5geuj2i95lkh5te", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Cascade Lake. 50% vCPU [core*hour]
            if core_fraction == 20:
                usage_collector.add_usage("dn2k4nll5o0unlnnn0hf", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Cascade Lake. 20% vCPU [core*hour]
            if core_fraction == 5:
                usage_collector.add_usage("dn217kngosua0ige7glr", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Cascade Lake. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2b1ve4tifofkbpqtlo", memory * instance_num, resource_name, resource_type) # PostgreSQL. Intel Cascade Lake. RAM [gbyte*hour]
        
        elif platform_id == "standard-v1":
            # cpu
            if core_fraction == 100:
                usage_collector.add_usage("dn2n5qctucuvrif2l6v2", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Broadwell. 100% vCPU [core*hour]
            if core_fraction == 50:
                usage_collector.add_usage("dn24saqltp4lsu0kgc6a", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Broadwell. 50% vCPU [core*hour]
            if core_fraction == 20:
                usage_collector.add_usage("dn24heoov30dnk16kvqi", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Broadwell. 20% vCPU [core*hour]
            if core_fraction == 5:
                usage_collector.add_usage("dn26tqk6cr5ocu7v3j5i", cores * instance_num, resource_name, resource_type) # PostgreSQL. Intel Broadwell. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2i2qka7e75bh6ok7he", memory * instance_num, resource_name, resource_type) # PostgreSQL. Intel Broadwell. RAM [gbyte*hour]

        if public_ip_num > 0:
            usage_collector.add_usage("dn2cc943s27vr5gviq0k", public_ip_num, resource_name, resource_type) # Public IP address - PostgreSQL [fip*hour]

        # Process disk
        if disk_type == "network-ssd":
            usage_collector.add_usage("dn2euvjs01kht9oftfji", disk_size * instance_num, resource_name, resource_type) # Fast network storage \u2014 PostgreSQL [gbyte*hour]
        elif disk_type == "network-hdd":
            usage_collector.add_usage("dn2l0lh2aon42b2d7jb9", disk_size * instance_num, resource_name, resource_type) # Standard network storage \u2014 PostgreSQL [gbyte*hour]
        elif disk_type == "network-ssd-nonreplicated":
            usage_collector.add_usage("dn2t1rhogdm8t0gtao1s", disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 PostgreSQL [gbyte*hour]
        elif disk_type == "network-ssd-io-m3":
            usage_collector.add_usage("dn2vi9oeraem9ptu27ad", disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 PostgreSQL [gbyte*hour]
        elif disk_type == "local-ssd":
            usage_collector.add_usage("dn2nr78ch39birtq8cud", disk_size * instance_num, resource_name, resource_type) # Fast local storage \u2014 PostgreSQL [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBClickhouseProcessor(ResourceProcessor):
    """Processor for MDB Clickhouse Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_clickhouse_cluster"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        disk_size_ch = resource_values["clickhouse"][0]["resources"][0].get("disk_size", 0)
        disk_type_ch = resource_values["clickhouse"][0]["resources"][0].get("disk_type_id", "network-hdd")
        preset_id_ch = resource_values["clickhouse"][0]["resources"][0].get("resource_preset_id", [])

        disk_size_zk = resource_values["zookeeper"][0]["resources"][0].get("disk_size", 0)
        disk_type_zk = resource_values["zookeeper"][0]["resources"][0].get("disk_type_id", "network-hdd")
        preset_id_zk = resource_values["zookeeper"][0]["resources"][0].get("resource_preset_id", [])
        
        instances = resource_values.get("host", [])

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('clickhouse', preset_id_ch)
        except ValueError as e:
            logging.error(e)
            return 1

        try:
            cores_zk, core_fraction_zk, memory_zk, platform_id_zk = self.resource_spec_service.get_mdb_preset('clickhouse', preset_id_zk)
        except ValueError as e:
            logging.error(e)
            return 1

        instances_num_ch = sum(1 for instance in instances if instance['type'] == 'CLICKHOUSE')
        instances_num_zk = sum(1 for instance in instances if instance['type'] == 'ZOOKEEPER')
        public_ip_num_ch = sum(1 for instance in instances if (instance.get("assign_public_ip") is True and instance['type'] == 'CLICKHOUSE'))

        if(platform_id == "standard-v3"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn2h2fne3qa9bjv2mm0b", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Ice Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn2slkf8qnvg3lohvlnk", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2cvuiesm49elnni1a5", memory * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Ice Lake. RAM [gbyte*hour]
        
        if(platform_id == "highfreq-v3"): #! нет в биллинге
            #! ClickHouse. Intel Ice Lake (Compute Optimized). Software accelerated network
            # cpu
            usage_collector.add_usage("dn277ac8ru4ub394msu1", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Ice Lake (Compute Optimised). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2co8sk8cldl5on3ckf", memory * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

        if(platform_id == "standard-v2"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn2bo4tud2qeo60gr008", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Cascade Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn2qjtq7ee80fj9c2ot0", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Cascade Lake. 50% vCPU [core*hour]
            if(core_fraction == 20):
                usage_collector.add_usage("dn24kods372d64lhijmn", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Cascade Lake. 20% vCPU [core*hour]
            if(core_fraction == 5):
                usage_collector.add_usage("dn2ro2rucgm410h34tiu", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Cascade Lake. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2fol5odat55iak187k", memory * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Cascade Lake. RAM [gbyte*hour]
        
        if(platform_id == "standard-v1"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn23nulcgejjcs3a5k6c", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Broadwell. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn27d2sdttppcok68ikt", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Broadwell. 50% vCPU [core*hour]
            if(core_fraction == 20):
                usage_collector.add_usage("dn20nfs6nvqmsnvjdd5r", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Broadwell. 20% vCPU [core*hour]
            if(core_fraction == 5):
                usage_collector.add_usage("dn2bl87f2dv7shnmistk", cores * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Broadwell. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2ci1m71mcpuans0njt", memory * instances_num_ch, resource_name, resource_type) # ClickHouse. Intel Broadwell. RAM [gbyte*hour]

        # Zookeeper
        if(platform_id_zk == "standard-v3"):
            if(core_fraction_zk == 100):
                usage_collector.add_usage("dn270b41ltvr4qs6fdu0", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Ice Lake. 100% vCPU [core*hour]
            if(core_fraction_zk == 50):
                usage_collector.add_usage("dn28oel39sj8kmfr78lk", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2tg9g6pi4k18isqcq7", memory_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Ice Lake. RAM [gbyte*hour]

        if(platform_id_zk == "highfreq-v3"):
            #! ZooKeeper for ClickHouse. Intel Ice Lake (Compute Optimized). Software accelerated network
            usage_collector.add_usage("dn29tpsi73qabnq4m9kb", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper for ClickHouse. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2i1lhi7dqj2nah4i2n", memory_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper for ClickHouse. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

        if(platform_id_zk == "standard-v2"):
            if(core_fraction_zk == 100):
                usage_collector.add_usage("dn2g6deavckbovip5uu5", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Cascade Lake. 100% vCPU [core*hour]
            if(core_fraction_zk == 50):
                usage_collector.add_usage("dn2b40gt80iuh70kfpqc", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Cascade Lake. 50% vCPU [core*hour]
            if(core_fraction_zk == 20):
                usage_collector.add_usage("dn2iv9kja0ntvt3uocjm", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Cascade Lake. 20% vCPU [core*hour]
            if(core_fraction_zk == 5):
                usage_collector.add_usage("dn2ud13pi583kt52h4jv", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Cascade Lake. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2hhsaqch2o4tkn1qnk", memory_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Cascade Lake. RAM [gbyte*hour]
        
        if(platform_id_zk == "standard-v1"):
            if(core_fraction_zk == 100):
                usage_collector.add_usage("dn2a5pb4kkrvk6ra5vhk", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Broadwell. 100% vCPU [core*hour]
            if(core_fraction_zk == 50):
                usage_collector.add_usage("dn29aeejuka6vtvul02s", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Broadwell. 50% vCPU [core*hour]
            if(core_fraction_zk == 20):
                usage_collector.add_usage("dn2m7d3nj7qtfhi14gjv", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Broadwell. 20% vCPU [core*hour]
            if(core_fraction_zk == 5):
                usage_collector.add_usage("dn2vh46ucftq2ponpe4c", cores_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Broadwell. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2fg67mc3h26dqfs2s9", memory_zk * instances_num_zk, resource_name, resource_type) # ZooKeeper. Intel Broadwell. RAM [gbyte*hour]

        if(public_ip_num_ch > 0):
            usage_collector.add_usage("dn2riv150c97qbgpik5k", public_ip_num_ch, resource_name, resource_type) # Public IP address - ClickHouse [fip*hour]

        # Clickhouse
        if(disk_type_ch == "network-ssd"):
            usage_collector.add_usage("dn2mvvhqdpp24tm36ks4", disk_size_ch * instances_num_ch, resource_name, resource_type) # Fast network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_ch == "network-hdd"):
            usage_collector.add_usage("dn2utn4rqnas617dfa2q", disk_size_ch * instances_num_ch, resource_name, resource_type) # Standard network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_ch == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn2e0j7ko5l58njegum8", disk_size_ch * instances_num_ch, resource_name, resource_type) # Non-replicated fast network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_ch == "network-ssd-io-m3"):
            usage_collector.add_usage("dn2lou40il2st50oh4pd", disk_size_ch * instances_num_ch, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 ClickHouse [gbyte*hour]
        if(disk_type_ch == "local-ssd"):
            usage_collector.add_usage("dn222q64f5mcjm36ed4q", disk_size_ch * instances_num_ch, resource_name, resource_type) # Fast local storage \u2014 ClickHouse [gbyte*hour]

        # Zookeeper
        if(disk_type_zk == "network-ssd"):
            usage_collector.add_usage("dn2mvvhqdpp24tm36ks4", disk_size_zk * instances_num_zk, resource_name, resource_type) # Fast network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_zk == "network-hdd"):
            usage_collector.add_usage("dn2utn4rqnas617dfa2q", disk_size_zk * instances_num_zk, resource_name, resource_type) # Standard network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_zk == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn2e0j7ko5l58njegum8", disk_size_zk * instances_num_zk, resource_name, resource_type) # Non-replicated fast network storage \u2014 ClickHouse [gbyte*hour]
        if(disk_type_zk == "network-ssd-io-m3"):
            usage_collector.add_usage("dn2lou40il2st50oh4pd", disk_size_zk * instances_num_zk, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 ClickHouse [gbyte*hour]
        if(disk_type_zk == "local-ssd"):
            usage_collector.add_usage("dn222q64f5mcjm36ed4q", disk_size_zk * instances_num_zk, resource_name, resource_type) # Fast local storage \u2014 ClickHouse [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBGreenplumProcessor(ResourceProcessor):
    """Processor for MDB Greenplum Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_greenplum_cluster"
    
    def process(self, resource, usage_collector):
        resource_type       = resource["type"]
        resource_name       = resource["name"]
        resource_values     = resource["values"]
        
        master              = resource_values["master_subcluster"][0]
        segment             = resource_values["segment_subcluster"][0]

        disk_size_master           = master["resources"][0].get("disk_size", 0)
        disk_type_master           = master["resources"][0].get("disk_type_id", "network-hdd")
        preset_id_master           = master["resources"][0].get("resource_preset_id", [])
        
        disk_size_segment          = segment["resources"][0].get("disk_size", 0)
        disk_type_segment          = segment["resources"][0].get("disk_type_id", "network-hdd")
        preset_id_segment          = segment["resources"][0].get("resource_preset_id", [])

        try:
            cores_master, core_fraction_master, memory_master, platform_id_master = self.resource_spec_service.get_mdb_preset('greenplum', preset_id_master)
        except ValueError as e:
            logging.error(e)
            return 1
        
        try:
            cores_segment, core_fraction_segment, memory_segment, platform_id_segment = self.resource_spec_service.get_mdb_preset('greenplum', preset_id_segment)
        except ValueError as e:
            logging.error(e)
            return 1

        master_num          = resource_values.get("master_host_count", 0)
        segment_num         = resource_values.get("segment_host_count", 0)
        public_ip_num       = master_num if resource_values.get("assign_public_ip", False) else 0

        # GreenPlum Masters
        if(platform_id_master == "standard-v3"):
            # cpu
            usage_collector.add_usage("dn22vrmol6tmlqmnflh0", cores_master * master_num, resource_name, resource_type) # Greenplum. Intel Ice Lake. 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2fkkqvmd2dhlo7b07m", memory_master * master_num, resource_name, resource_type) # Greenplum. Intel Ice Lake. RAM [gbyte*hour]

        #! добавить highfreq платформу
        if(platform_id_master == "highfreq-v3"):
            # cpu
            usage_collector.add_usage("dn21dgdltqrgdsodkm4i", cores_master * master_num, resource_name, resource_type) # Greenplum. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2hom6ljm6s2js93o40", memory_master * master_num, resource_name, resource_type) # Greenplum. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]
        
        if(platform_id_master == "standard-v2"):
            # cpu
            usage_collector.add_usage("dn27vfbvh9mtobabcvd3", cores_master * master_num, resource_name, resource_type) # Greenplum. Intel Cascade Lake. 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2gbhl2hc3aun6t7dgm", memory_master * master_num, resource_name, resource_type) # Greenplum. Intel Cascade Lake. RAM [gbyte*hour]
        
        if(public_ip_num > 0):
            usage_collector.add_usage("dn2gikj1nkrl5epq2ivi", public_ip_num, resource_name, resource_type) # Public IP address - Greenplum [fip*hour]

        if(disk_type_master == "network-ssd"):
            usage_collector.add_usage("dn24ljti6nor6rm64n98", disk_size_master * master_num, resource_name, resource_type) # Fast network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_master == "network-hdd"):
            usage_collector.add_usage("dn2amtenb2bmhm5r3t26", disk_size_master * master_num, resource_name, resource_type) # Standard network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_master == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn281sknb94nk6dhg5f1", disk_size_master * master_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_master == "network-ssd-io-m3"):
            usage_collector.add_usage("dn2q30eprodapfghra4q", disk_size_master * master_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 Greenplum [gbyte*hour]
        if(disk_type_master == "local-ssd"):
            usage_collector.add_usage("dn23vk0nguhc9qe9v30c", disk_size_master * master_num, resource_name, resource_type) # Fast local storage \u2014 Greenplum [gbyte*hour]
        
        # GreenPlum Segments
        if(platform_id_segment == "standard-v3"):
            # cpu
            usage_collector.add_usage("dn22vrmol6tmlqmnflh0", cores_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Ice Lake. 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2fkkqvmd2dhlo7b07m", memory_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Ice Lake. RAM [gbyte*hour]

        #! добавить highfreq платформу
        if(platform_id_segment == "highfreq-v3"):
            # cpu
            usage_collector.add_usage("dn21dgdltqrgdsodkm4i", cores_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2hom6ljm6s2js93o40", memory_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

        if(platform_id_segment == "standard-v2"):
            # cpu
            usage_collector.add_usage("dn27vfbvh9mtobabcvd3", cores_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Cascade Lake. 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2gbhl2hc3aun6t7dgm", memory_segment * segment_num, resource_name, resource_type) # Greenplum. Intel Cascade Lake. RAM [gbyte*hour]

        if(disk_type_segment == "network-ssd"):
            usage_collector.add_usage("dn24ljti6nor6rm64n98", disk_size_segment * segment_num, resource_name, resource_type) # Fast network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_segment == "network-hdd"):
            usage_collector.add_usage("dn2amtenb2bmhm5r3t26", disk_size_segment * segment_num, resource_name, resource_type) # Standard network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_segment == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn281sknb94nk6dhg5f1", disk_size_segment * segment_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 Greenplum [gbyte*hour]
        if(disk_type_segment == "network-ssd-io-m3"):
            usage_collector.add_usage("dn2q30eprodapfghra4q", disk_size_segment * segment_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 Greenplum [gbyte*hour]
        if(disk_type_segment == "local-ssd"):
            usage_collector.add_usage("dn23vk0nguhc9qe9v30c", disk_size_segment * segment_num, resource_name, resource_type) # Fast local storage \u2014 Greenplum [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBKafkaProcessor(ResourceProcessor):
    """Processor for MDB Kafka Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_kafka_cluster"
    
    def process(self, resource, usage_collector):
        resource_type           = resource["type"]
        resource_name           = resource["name"]
        resource_values         = resource["values"]

        disk_size               = resource_values["config"][0]["kafka"][0]["resources"][0].get("disk_size", 0)
        disk_type               = resource_values["config"][0]["kafka"][0]["resources"][0].get("disk_type_id", "network-hdd")
        preset_id               = resource_values["config"][0]["kafka"][0]["resources"][0].get("resource_preset_id", [])

        if resource_values["config"][0].get("zookeeper"):
            disk_size_zk            = resource_values["config"][0]["zookeeper"][0]["resources"][0].get("disk_size", 0)
            disk_type_zk            = resource_values["config"][0]["zookeeper"][0]["resources"][0].get("disk_type_id", "network-hdd")
            preset_id_zk            = resource_values["config"][0]["zookeeper"][0]["resources"][0].get("resource_preset_id", [])

            try:
                cores_zk, core_fraction_zk, memory_zk, platform_id_zk = self.resource_spec_service.get_mdb_preset('kafka', preset_id_zk)
            except ValueError as e:
                logging.error(e)
                return 1

            if(platform_id_zk == "standard-v3"):
                # cpu
                if(core_fraction_zk == 100):
                    usage_collector.add_usage("dn2nhhb7jic2747airrn", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake. 100% vCPU [core*hour]
                if(core_fraction_zk == 50):
                    usage_collector.add_usage("dn2gsmai0ju430119mqj", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake. 50% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2r01fpbih17tae9m00", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake. RAM [gbyte*hour]

            #! добавить highfreq платформу
            if(platform_id_zk == "highfreq-v3"):
                # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). Software accelerated network
                # cpu
                usage_collector.add_usage("dn2prkfjerh1oh1km220", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2un2g6tou5jrg18j3d", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

            if(platform_id_zk == "standard-v2"):
                # cpu
                if(core_fraction_zk == 100):
                    usage_collector.add_usage("dn2rqdpeh829k7prtfng", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Cascade Lake. 100% vCPU [core*hour]
                if(core_fraction_zk == 50):
                    usage_collector.add_usage("dn2oobqd83ld4uucdr5g", cores_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Cascade Lake. 50% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2kd8egpcfqmm4b9f1m", memory_zk * 3, resource_name, resource_type) # ZooKeeper for Apache Kafka\u00ae. Intel Cascade Lake. RAM [gbyte*hour]

            if(disk_type_zk == "network-ssd"):
                usage_collector.add_usage("dn2du1uuuvjdqdpmsmsd", disk_size_zk * 3, resource_name, resource_type) # Fast network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
            if(disk_type_zk == "network-hdd"):
                usage_collector.add_usage("dn28vvrfmvdd2a9vhfus", disk_size_zk * 3, resource_name, resource_type) # Standard network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
            if(disk_type_zk == "network-ssd-nonreplicated"):
                usage_collector.add_usage("dn278mhc61kqavrjh26u", disk_size_zk * 3, resource_name, resource_type) # Non-replicated fast network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
            if(disk_type_zk == "network-ssd-io-m3"):
                usage_collector.add_usage("dn25ksor7p112bvs2qts", disk_size_zk * 3, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 Apache Kafka\u00ae [gbyte*hour]
            if(disk_type_zk == "local-ssd"):
                usage_collector.add_usage("dn26m07r3n3lfhu0sshg", disk_size_zk * 3, resource_name, resource_type) # Fast local storage \u2014 Apache Kafka\u00ae [gbyte*hour]
            
        instance_num            = resource_values["config"][0].get("brokers_count", 1)
        public_ip_num           = instance_num if resource_values["config"][0].get("assign_public_ip", False) else 0

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('kafka', preset_id)
        except ValueError as e:
            logging.error(e)
            return 1

        if(platform_id == "standard-v3"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn24mf6m837qdtfaus9o", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Ice Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn2j1e6ag4ebi1lqhpb5", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2ftqohv8psorjabi12", memory * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Ice Lake. RAM [gbyte*hour]

        #! добавить highfreq платформу
        if(platform_id == "highfreq-v3"):
            # Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). Software accelerated network
            # cpu
            usage_collector.add_usage("dn2u61ode72vg51luvm5", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2u83rsns5m0bdk8pra", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

        if(platform_id == "standard-v2"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn20mtnp2jnjj4km7u5g", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Cascade Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn25ij9c6ncskqe2v804", cores * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Cascade Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn29ei2iq0joi59033pb", memory * instance_num, resource_name, resource_type) # Apache Kafka\u00ae. Intel Cascade Lake. RAM [gbyte*hour]

        if(public_ip_num > 0):
            usage_collector.add_usage("dn2kol05hvp3tj76pqep", public_ip_num, resource_name, resource_type) # Public IP address - Apache Kafka\u00ae [fip*hour]

        if(disk_type == "network-ssd"):
            usage_collector.add_usage("dn2du1uuuvjdqdpmsmsd", disk_size * instance_num, resource_name, resource_type) # Fast network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
        if(disk_type == "network-hdd"):
            usage_collector.add_usage("dn28vvrfmvdd2a9vhfus", disk_size * instance_num, resource_name, resource_type) # Standard network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
        if(disk_type == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn278mhc61kqavrjh26u", disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 Apache Kafka\u00ae [gbyte*hour]
        if(disk_type == "network-ssd-io-m3"):
            usage_collector.add_usage("dn25ksor7p112bvs2qts", disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 Apache Kafka\u00ae [gbyte*hour]
        if(disk_type == "local-ssd"):
            usage_collector.add_usage("dn26m07r3n3lfhu0sshg", disk_size * instance_num, resource_name, resource_type) # Fast local storage \u2014 Apache Kafka\u00ae [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBRedisProcessor(ResourceProcessor):
    """Processor for MDB Redis Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_redis_cluster"
    
    def process(self, resource, usage_collector):
        resource_type       = resource["type"]
        resource_name       = resource["name"]
        resource_values     = resource["values"]

        disk_size           = resource_values["resources"][0].get("disk_size", 0)
        disk_type           = resource_values["resources"][0].get("disk_type_id", "network-ssd")
        preset_id           = resource_values["resources"][0].get("resource_preset_id", [])
        instances           = resource_values.get("host", [])

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('redis', preset_id)
        except ValueError as e:
            logging.error(e)
            return 1

        instance_num        = len(instances)
        public_ip_num       = sum(1 for instance in instances if instance.get("assign_public_ip") is True)

        if(platform_id == "standard-v3"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn2qrqp6uho94a80hgr3", cores * instance_num, resource_name, resource_type) # Redis. Intel Ice Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn2olfc9i989aj43sdh9xx", cores * instance_num, resource_name, resource_type) # Redis. Intel Ice Lake. 50% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2i5hfnisk3mg4rkl0v", memory * instance_num, resource_name, resource_type) # Redis. Intel Ice Lake. RAM [gbyte*hour]

        #! добавить highfreq платформу
        if(platform_id == "highfreq-v3"):
            #! Redis. Intel Ice Lake (Compute Optimized). Software accelerated network
            # cpu
            usage_collector.add_usage("dn2p5vd4ccc8i53ia6bi", cores * instance_num, resource_name, resource_type) # Redis. Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2sf9026ldfpoaflvju", memory * instance_num, resource_name, resource_type) # Redis. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

        if(platform_id == "standard-v2"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn266b8r1i07682ojiiq", cores * instance_num, resource_name, resource_type) # Redis. Intel Cascade Lake. 100% vCPU [core*hour]
            if(core_fraction == 50):
                usage_collector.add_usage("dn26opl99hcbjqvo87gf", cores * instance_num, resource_name, resource_type) # Redis. Intel Cascade Lake. 50% vCPU [core*hour]
            if(core_fraction == 5):
                usage_collector.add_usage("dn2qgqnuuucr2uat9be2", cores * instance_num, resource_name, resource_type) # Redis. Intel Cascade Lake. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn2gac3fpk1bsurdkf0h", memory * instance_num, resource_name, resource_type) # Redis. Intel Cascade Lake. RAM [gbyte*hour]
        
        if(platform_id == "standard-v1"):
            # cpu
            if(core_fraction == 100):
                usage_collector.add_usage("dn2ta4lgerp02btumaic", cores * instance_num, resource_name, resource_type) # Redis. Intel Broadwell. 100% vCPU [core*hour]
            if(core_fraction == 20):
                usage_collector.add_usage("dn29cjcghhc5ihatrc35", cores * instance_num, resource_name, resource_type) # Redis. Intel Broadwell. 20% vCPU [core*hour]
            if(core_fraction == 5):
                usage_collector.add_usage("dn2gvhqj7nimn9jaofi0", cores * instance_num, resource_name, resource_type) # Redis. Intel Broadwell. 5% vCPU [core*hour]
            # ram
            usage_collector.add_usage("dn24sref9ucjdo6ut46k", memory * instance_num, resource_name, resource_type) # Redis. Intel Broadwell. RAM [gbyte*hour]

        if(public_ip_num > 0):
            usage_collector.add_usage("dn21adn8pgvr7hr9jhh3", public_ip_num, resource_name, resource_type) # Public IP address - Redis [fip*hour]

        if(disk_type == "network-ssd"):
            usage_collector.add_usage("dn2brvmhtb2i0o7gchn6", disk_size * instance_num, resource_name, resource_type) # Fast network storage \u2014 Redis [gbyte*hour]
        if(disk_type == "network-ssd-nonreplicated"):
            usage_collector.add_usage("dn265o7f5n5dh8pcdes5", disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage \u2014  [gbyte*hour]
        if(disk_type == "network-ssd-io-m3"):
            usage_collector.add_usage("dn2jbe8pp30806tb8dev", disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014  [gbyte*hour]
        if(disk_type == "local-ssd"):
            usage_collector.add_usage("dn2b2d8c9e60npmqq41k", disk_size * instance_num, resource_name, resource_type) # Fast local storage \u2014 Redis [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBOpensearchProcessor(ResourceProcessor):
    """Processor for MDB Opensearch Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_mdb_opensearch_cluster"
    
    def process(self, resource, usage_collector):
        resource_type       = resource["type"]
        resource_name       = resource["name"]
        resource_values     = resource["values"]

        node_groups         = resource_values["config"]["opensearch"].get("node_groups", [])
        dashboards          = resource_values["config"]["dashboards"].get("node_groups", [])

        for node_group in node_groups + dashboards:
            BYTES_IN_GIGABYTE = 1024 * 1024 * 1024

            instance_num = node_group.get("hosts_count", 1)
            public_ip_num = instance_num if node_group.get("assign_public_ip") else 0

            disk_size           = round(node_group["resources"].get("disk_size", 0) / BYTES_IN_GIGABYTE) #! why it has to be in bytes?
            disk_type           = node_group["resources"].get("disk_type_id", "network-hdd")
            preset_id           = node_group["resources"].get("resource_preset_id", [])

            try:
                cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('opensearch', preset_id)
            except ValueError as e:
                logging.error(e)

            if(platform_id == "standard-v3"):
                # cpu
                if(core_fraction == 100):
                    usage_collector.add_usage("dn2rf1bupkvgk646cpqo", cores * instance_num, resource_name, resource_type) # OpenSearch. Intel Ice Lake. 100% vCPU [core*hour]
                if(core_fraction == 50):
                    usage_collector.add_usage("dn2jeuof2ujtjeadau6i", cores * instance_num, resource_name, resource_type) # OpenSearch. Intel Ice Lake. 50% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn22dhakdgfrijul4v1f", memory * instance_num, resource_name, resource_type) # OpenSearch. Intel Ice Lake. RAM [gbyte*hour]

            if(platform_id == "highfreq-v3"):
                # OpenSearch. Intel Ice Lake (Compute Optimized). Software accelerated network
                # cpu
                usage_collector.add_usage("dn2p79o9d7r4tdm1s1jr", cores * instance_num, resource_name, resource_type) # OpenSearch. Intel Ice Lake (Compute Optimised). 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2ko90o5lnvcgc0u6km", memory * instance_num, resource_name, resource_type) # OpenSearch. Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]

            if(platform_id == "standard-v2"):
                # cpu
                if(core_fraction == 100):
                    usage_collector.add_usage("dn211hvm5bgm4dl0gblv", cores * instance_num, resource_name, resource_type) # OpenSearch. Intel Cascade Lake. 100% vCPU [core*hour]
                if(core_fraction == 50):
                    usage_collector.add_usage("dn2l6h3sovqem675uih2", cores * instance_num, resource_name, resource_type) # OpenSearch. Intel Cascade Lake. 50% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2uga61a66rcda0igtk", memory * instance_num, resource_name, resource_type) # OpenSearch. Intel Cascade Lake. RAM [gbyte*hour]

            if(public_ip_num > 0):
                usage_collector.add_usage("dn2mqb0g06ogqnsinbt2", public_ip_num, resource_name, resource_type) # Public IP address - OpenSearch [fip*hour]

            if(disk_type == "network-ssd"):
                usage_collector.add_usage("dn28u08us0otvnpd7tiu", disk_size * instance_num, resource_name, resource_type) # Fast network storage \u2014 OpenSearch [gbyte*hour]
            if(disk_type == "network-hdd"):
                usage_collector.add_usage("dn217fio8e4jq2bb93va", disk_size * instance_num, resource_name, resource_type) # Standard network storage \u2014 OpenSearch [gbyte*hour]
            if(disk_type == "network-ssd-nonreplicated"):
                usage_collector.add_usage("dn2gt4e75hm80bpgk8i7", disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage \u2014 OpenSearch [gbyte*hour]
            if(disk_type == "network-ssd-io-m3"):
                usage_collector.add_usage("dn2690d7uj1the1vaggf", disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) \u2014 OpenSearch [gbyte*hour]
            if(disk_type == "local-ssd"):
                usage_collector.add_usage("dn2dnba7orfgdag64gmh", disk_size * instance_num, resource_name, resource_type) # Fast local storage \u2014 OpenSearch [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class MDBYDBProcessor(ResourceProcessor):
    """Processor for MDB YDB Database resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_ydb_database_dedicated"
    
    def process(self, resource, usage_collector):
        resource_type       = resource["type"]
        resource_name       = resource["name"]
        resource_values     = resource["values"]

        disk_size           = resource_values["storage_config"][0].get("group_count", 0) * 100
        preset_id           = resource_values.get("resource_preset_id", [])

        try:
            cores, core_fraction, memory, platform_id = self.resource_spec_service.get_mdb_preset('ydb', preset_id)
        except ValueError as e:
            logging.error(e)
            return 1

        instance_num        = resource_values["scale_policy"][0]["fixed_scale"][0].get("size", 1)

        # cpu
        usage_collector.add_usage("dn2uh84ab9ga5954i807", cores * instance_num, resource_name, resource_type) # YDB. Intel Cascade Lake. 100% vCPU [core*hour]
        # ram
        usage_collector.add_usage("dn24ok7m82d8uhe9g725", memory * instance_num, resource_name, resource_type) # YDB. Intel Cascade Lake. RAM [gbyte*hour]
        # disk
        usage_collector.add_usage("dn26b206u8r13m8go6d2", disk_size * instance_num, resource_name, resource_type) # YDB. Fast storage [gbyte*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0
