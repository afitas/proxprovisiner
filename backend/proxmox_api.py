from proxmoxer import ProxmoxAPI as PAPI
import os
from dotenv import load_dotenv

load_dotenv()

class ProxmoxAPI:
    def __init__(self):
        self.proxmox = PAPI(
            host=os.getenv('PROXMOX_HOST'),
            user=os.getenv('PROXMOX_USER'),
            password=os.getenv('PROXMOX_PASSWORD'),
            verify_ssl=False
        )

    def create_vm(self, name, cpu_cores, memory, disk_size):
        try:
            # Récupérer le prochain ID VM disponible
            vm_id = self._get_next_vmid()
            
            # Récupérer le premier nœud disponible
            node = self.proxmox.nodes.get()[0]
            
            # Configuration de la VM
            vm_config = {
                'vmid': vm_id,
                'name': name,
                'cores': cpu_cores,
                'memory': memory * 1024,  # Conversion en MB
                'disk': f'local-lvm:{disk_size}G',
                'net0': 'virtio,bridge=vmbr0',
                'ostype': 'l26'  # Linux 2.6+ kernel
            }
            
            # Créer la VM
            node.qemu.create(**vm_config)
            return vm_id
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création de la VM: {str(e)}")

    def _get_next_vmid(self):
        # Récupérer la liste des VMs existantes
        vms = self.proxmox.cluster.resources.get(type='vm')
        existing_ids = {vm['vmid'] for vm in vms}
        
        # Commencer à partir de 100 (pratique courante dans Proxmox)
        next_id = 100
        while next_id in existing_ids:
            next_id += 1
            
        return next_id

    def get_vm_status(self, vm_id):
        try:
            vm = self.proxmox.cluster.resources.get(type='vm', vmid=vm_id)[0]
            return vm['status']
        except Exception:
            return 'unknown'

    def start_vm(self, node_name, vm_id):
        try:
            self.proxmox.nodes(node_name).qemu(vm_id).status.start.post()
            return True
        except Exception as e:
            raise Exception(f"Erreur lors du démarrage de la VM: {str(e)}")

    def stop_vm(self, node_name, vm_id):
        try:
            self.proxmox.nodes(node_name).qemu(vm_id).status.stop.post()
            return True
        except Exception as e:
            raise Exception(f"Erreur lors de l'arrêt de la VM: {str(e)}")

    def delete_vm(self, node_name, vm_id):
        try:
            self.proxmox.nodes(node_name).qemu(vm_id).delete()
            return True
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression de la VM: {str(e)}")
