import logging
import json
from processor.base import ResourceProcessor

class KubernetesClusterProcessor(ResourceProcessor):
    """Processor for Kubernetes Cluster resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_kubernetes_cluster"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        for master in resource_values.get("master", []):
            if "zonal" in master:
                usage_collector.add_usage("dn2tdli7u18tvvc28ov8", 1, resource_name, resource_type) # Managed Kubernetes. Zonal Master - small (hour)
            elif "regional" in master:
                usage_collector.add_usage("dn2j2khrfcdc4p1aki30", 1, resource_name, resource_type) # Managed Kubernetes. Regional Master - small (hour)

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0


class KubernetesNodeGroupProcessor(ResourceProcessor):
    """Processor for Kubernetes Node Group resources"""
    
    def can_process(self, resource_type):
        return resource_type == "yandex_kubernetes_node_group"
    
    def process(self, resource, usage_collector):
        resource_type = resource["type"]
        resource_name = resource["name"]
        resource_values = resource["values"]

        auto_scale = resource_values["scale_policy"][0].get("auto_scale", [])
        fixed_scale = resource_values["scale_policy"][0].get("fixed_scale", [])
        boot_disk_size = resource_values["instance_template"][0]["boot_disk"][0].get("size", 0)
        boot_disk_type = resource_values["instance_template"][0]["boot_disk"][0].get("type", "network-hdd")
        network_nat = resource_values["instance_template"][0]["network_interface"][0].get("nat", False)
        platform_id = resource_values["instance_template"][0]["platform_id"]
        resources_cores = resource_values["instance_template"][0]["resources"][0]["cores"]
        resources_fraction = resource_values["instance_template"][0]["resources"][0].get("core_fraction", 100)
        resources_memory = resource_values["instance_template"][0]["resources"][0]["memory"]
        resources_gpus = resource_values["instance_template"][0]["resources"][0]["gpus"]
        scheduling_policy = resource_values["instance_template"][0].get("scheduling_policy", [{}])
        preemptible = scheduling_policy[0].get("preemptible", False)

        if auto_scale:
            instance_num = auto_scale[0]["initial"]
            if instance_num == 0:
                instance_num = 1
        elif fixed_scale:
            instance_num = fixed_scale[0]["size"]
        else:
            instance_num = 1

        if platform_id == "standard-v3":
            # preemptible
            if preemptible:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn2e2fphfupugm21k4hv", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 100% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 50:
                    usage_collector.add_usage("dn2333h2iv190t06bon8", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 50% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn2pdedm5fon78kbl0fh", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 20% vCPU \u2014 preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn26ur5frjbgdek2a0g5", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake. RAM \u2014 preemptible instances [gbyte*hour]
            # non preemptible
            else:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn2k3vqlk9snp1jv351u", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 100% vCPU [core*hour]
                if resources_fraction == 50:
                    usage_collector.add_usage("dn2f0q0d6gtpcom4b1p6", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 50% vCPU [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn2r8aklo79bmpkd87l3", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake. 20% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2ilq72mjc3bej6j74p", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake. RAM [gbyte*hour]
        
        elif platform_id == "standard-v2":
            # preemptible
            if preemptible:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn2ipnaa10sls6i7osfv", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 100% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 50:
                    usage_collector.add_usage("dn20jng1b3a6ggtn52bo", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 50% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn2krclp8uj3432vmpre", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 20% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 5:
                    usage_collector.add_usage("dn292ebti5dcjio7vh2s", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 5% vCPU \u2014 preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn26ur5frjbgdek2a0g5", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake. RAM \u2014 preemptible instances [gbyte*hour]
            # non preemptible
            else:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn218a07u143r9v1r5ms", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 100% vCPU [core*hour]
                if resources_fraction == 50:
                    usage_collector.add_usage("dn2qbqi1am9oq6oc9s05", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 50% vCPU [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn26skitjdon841jqit7", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 20% vCPU [core*hour]
                if resources_fraction == 5:
                    usage_collector.add_usage("dn2l09d8brnv9s8m5p2r", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake. 5% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2fhtcoocq50j1uj4tg", resources_memory * instance_num, resource_name, resource_type) # Intel Cascade Lake. RAM [gbyte*hour]
        
        elif platform_id == "standard-v1":
            # preemptible
            if preemptible:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn247qigcq66fq6t3tk5", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 100% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn24sf8vh5cvj53voa7k", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 20% vCPU \u2014 preemptible instances [core*hour]
                if resources_fraction == 5:
                    usage_collector.add_usage("dn2g5qo1211n5k8i1s3v", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 5% vCPU \u2014 preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2u497ok1kl70on0ta2", resources_memory * instance_num, resource_name, resource_type) # Intel Broadwell. RAM \u2014 preemptible instances [gbyte*hour]
            # non preemptible
            else:
                # cpu
                if resources_fraction == 100:
                    usage_collector.add_usage("dn299ll54t5jt2gojh7e", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 100% vCPU [core*hour]
                if resources_fraction == 20:
                    usage_collector.add_usage("dn2vmq6na03r9vlds7j8", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 20% vCPU [core*hour]
                if resources_fraction == 5:
                    usage_collector.add_usage("dn2pm2gap1cc09a33s06", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell. 5% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2dka206olokggsieuu", resources_memory * instance_num, resource_name, resource_type) # Intel Broadwell. RAM [gbyte*hour]
        
        elif platform_id == "highfreq-v3":
            # cpu
            usage_collector.add_usage("no_sku_id", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake (Compute Optimized). 100% vCPU [core*hour]
            # ram
            usage_collector.add_usage("no_sku_id", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake (Compute Optimized). RAM [gbyte*hour]
        
        elif platform_id == "standard-v3-t4":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2lsfskfirek2985fnd", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. 100% vCPU \u2014 preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2im0g43iedeohe4sac", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. RAM - preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2cpk4mc82b1vib72e5", resources_gpus * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn24b7m6qol7tb7tukga", resources_cores * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2lg2hrvbn5b8lm7em4", resources_memory * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn20ml8ifdps6m7048an", resources_gpus * instance_num, resource_name, resource_type) # Intel Ice Lake with Nvidia T4. GPU [gpus*hour]
        
        elif platform_id == "standard-v3-t4i":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2960mi7268n67o8iae", resources_cores * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. 100% vCPU - preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn25rffeums4j1ku5649", resources_memory * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. RAM - preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2qlml2u48bng4jgilh", resources_gpus * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn242l2ivnhdd5so2oga", resources_cores * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn290pbmohupnus9ajb7", resources_memory * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2hql9evci880d8jq7i", resources_gpus * instance_num, resource_name, resource_type) # Intel Ice lake with t4i. GPU" [gpus*hour]
        
        elif platform_id == "gpu-standard-v3":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2tvs05nnrib706hgnt", resources_cores * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. 100% vCPU - preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2m4gusa7m7t4hl6vo2", resources_memory * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. RAM \u2014 preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn211dses9ju3abvq0bs", resources_gpus * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn28c1erut6m9f9uem08", resources_cores * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn21jcm82510bfa6is22", resources_memory * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2395q10bihjmm2b0v6", resources_gpus * instance_num, resource_name, resource_type) # AMD Epyc with Nvidia A100. GPU [gpus*hour]
        
        elif platform_id == "gpu-standard-v3i":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2o9fiqemifmch1dq7c", resources_cores * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. 100% vCPU - preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2mgiub24223fh5mvgv", resources_memory * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. RAM - preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2qvcfe8i5vqlrvterc", resources_gpus * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn2fd3g50rub98vfprlt", resources_cores * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2h5gi2u2l3bdclrput", resources_memory * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2jfrjoic5h3nh7e6jh", resources_gpus * instance_num, resource_name, resource_type) # AMD Epyc 9474F with Gen2. GPU [gpus*hour]
        
        elif platform_id == "gpu-standard-v2":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2h4u30djq3jhh8dqh8", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. 100% vCPU - preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2hotj7skno0turhbq1", resources_memory * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. RAM \u2014 preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn23ppvthcls7rjt5pol", resources_gpus * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn2udmu2aa9jm5a8f4ug", resources_cores * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2qtp90p3r8l8vakmm6", resources_memory * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2dlvuk2ecf6hu0kjtl", resources_gpus * instance_num, resource_name, resource_type) # Intel Cascade Lake with Nvidia Tesla v100. GPU [gpus*hour]
        
        elif platform_id == "gpu-standard-v1":
            # preemptible
            if preemptible:
                # cpu
                usage_collector.add_usage("dn2t7aa68lehsmvo5mss", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. 100% vCPU - preemptible instances [core*hour]
                # ram
                usage_collector.add_usage("dn2k0omvmglh857u60vu", resources_memory * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. RAM - preemptible instances [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2lov15qqamcimfv84q", resources_gpus * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. GPU - preemptible instances [gpus*hour]
            # non preemptible
            else:
                # cpu
                usage_collector.add_usage("dn2sfcnkn3jlhmq568ac", resources_cores * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. 100% vCPU [core*hour]
                # ram
                usage_collector.add_usage("dn2nccae8nra81iqphdn", resources_memory * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. RAM [gbyte*hour]
                # gpu
                usage_collector.add_usage("dn2oroscvvtb6sqtt83i", resources_gpus * instance_num, resource_name, resource_type) # Intel Broadwell with Nvidia Tesla v100. GPU [gpus*hour]
        
        # Process boot disk
        if boot_disk_size > 0:
            if boot_disk_type == "network-ssd":
                usage_collector.add_usage("dn27ajm6m8mnfcshbi61", boot_disk_size * instance_num, resource_name, resource_type) # Fast network storage (SSD) [gbyte*hour]
            elif boot_disk_type == "network-hdd":
                usage_collector.add_usage("dn2al287u6jr3a710u8g", boot_disk_size * instance_num, resource_name, resource_type) # Standard network storage (HDD) [gbyte*hour]
            elif boot_disk_type == "network-ssd-nonreplicated":
                usage_collector.add_usage("dn24kdllggk8ahsol15g", boot_disk_size * instance_num, resource_name, resource_type) # Non-replicated fast network storage (SSD) [gbyte*hour]
            elif boot_disk_type == "network-ssd-io-m3":
                usage_collector.add_usage("dn25ksor7p112bvs2qts", boot_disk_size * instance_num, resource_name, resource_type) # Ultra fast network storage with 3 replicas (SSD) [gbyte*hour]

        # Process network NAT
        if network_nat:
            usage_collector.add_usage("dn229q5mnmp58t58tfel", 1 * instance_num, resource_name, resource_type) # Public IP address [fip*hour]

        logging.debug(json.dumps(resource_values, indent=4).replace('\n', '\r'))
        return 0
