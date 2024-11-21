for vm in $(virsh list --all --name); do
    virsh undefine "$vm"
done
