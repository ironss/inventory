


class Item:
    def __init__(self, common_name, notes=None, container=None):
        self.notes = notes
        self.common_name = common_name
        self.container = None
        self.installed_in_slot = None
        self.inventory = {}
        self.slots = {}
        self.change_container(container)
        
    def change_container(self, new_container):
        old_container = self.container
        if old_container is not None:
            try:
                del(old_container.inventory[self])  # Remove from old_container.inventory
            except KeyError:        # If not in this container
                pass

        if new_container is not None:
            new_container.inventory[self] = 1   # Add to new container
        self.container = new_container
        self.installed_in_slot = None
        

    def __str__(self):
        return self.common_name


        
class Item:
    def __init__(self, manufacturer='<none>', model_number='<none>', serial_number='<none>', common_name='', description='', location=None, container=None, fits_into=None, install_into=None, is_specified_by=None, ):
        self.manufacturer = manufacturer
        self.model_number = model_number
        self.serial_number = serial_number
        self.common_name = common_name
        self.description = description

        self.has_location = location
        
        self.is_contained_in = None
        self._contains = {}

        self.can_fit_into_slot_type = fits_into
        self._is_installed_in = None
        self._has_slots = {}
        
        self.is_specified_by = is_specified_by

        if container is not None:
            self.change_container(container)

        if install_into is not None:
            self.install_into_slot(install_into)
        
        
    def install_into_slot(self, slot):
        if self.can_fit_into_slot_type == slot.slot_type:
            if slot.has_installed == None:
                self._is_installed_in = slot
                slot.has_installed = self
                self.is_contained_in = None
            else:
                print('Remove', slot.device_installed.common_name)
        else:
            print('Cannot install {} into {} because {} does not fit into {}'.format(self.common_name, slot.slot_name, self.can_fit_into_slot_type, slot.slot_type))
    
    def remove_from_slot(self, into_container):
        self._is_installed_in.has_installed = None
        self._is_installed_in = None
        self.change_container(into_container)


    def change_container(self, new_container):
        old_container = self.is_contained_in
        if old_container is not None:
            try:
                del(old_container._contains[self])  # Remove from old_container contents list
            except KeyError:                        # If not in this container
                pass

        if new_container is not None:
            new_container._contains[self] = 1   # Add to new container
        self.is_contained_in = new_container
        self.installed_in_slot = None

        
    def __str__(self):
        return '{name} ({manufacturer} {model} sn:{serial})'.format(manufacturer=self.manufacturer, model=self.model_number, serial=self.serial_number, name=self.common_name)


    def dump(self, level=0, indent='   '):
        print('{} {}'.format(indent*level, self))
        for item in sorted(self._contains.keys()):
            item.dump(level+1)
        for k in sorted(self._has_slots.keys()):
            self._has_slots[k].dump(level+1, indent)


class Slot_type:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Slot:
    def __init__(self, item, name, slot_type):
        self.item = item
        self.slot_name = name
        self.slot_type = slot_type
        self.item._has_slots[name] = self
        self.has_installed = None

    def dump(self, level=0, indent='  '):
        print('{} {}'.format(indent*level, self))
        if self.has_installed is not None:
            self.has_installed.dump(level+1, indent)
        else:
            print('{} <empty>'.format(indent*(level+1)))


    def __str__(self):
        return '{} ({})'.format(self.slot_name, self.slot_type.name)






if __name__ == '__main__':
    st_usba = Slot_type('USB-A')
    st_sata = Slot_type('SATA')
    st_mPCIe = Slot_type('mPCIe')
    
    root = Item(common_name='My stuff')

    m1 = Item(common_name='Moveable', container=root)

    h1 = Item(common_name='9 Liverton Crescent', container=root)
    h2 = Item(common_name='Study', container=h1)
    h3 = Item(common_name='Family room', container=h1)
    cab1 = Item(common_name='4 drawer cabinet', container=h3)

    o1 = Item(common_name='EPIC Centre', container=root)
    o2 = Item(common_name='Office', container=o1)
    o3 = Item(common_name='Store room', container=o1)

    laptop1 = Item('HP', 'Envy 15', '111XX', "Stephen's laptop", container=m1)
    lu1 = Slot(laptop1, 'usb1', st_usba)
    lu2 = Slot(laptop1, 'usb2', st_usba)
    lu3 = Slot(laptop1, 'usb3', st_usba)
    lu4 = Slot(laptop1, 'usb4', st_usba)
    ls1 = Slot(laptop1, 'sata1', st_sata)
    
    hdd1 = Item('WD', 'WSFDS', '222YY', "250GB SSD", fits_into=st_sata, install_into=ls1)
    flash8g = Item('Generic', '8GB flash', '<unknown>', "Red 8G flash drive", fits_into=st_usba, install_into=lu1)
    seckey = Item('Yubico', 'Yubikey 5', '<unknown>', "Security key #1", fits_into=st_usba, install_into=lu2)

    usbh1 = Item('Generic', '4-port USB hub', '<unknown>', 'Black USB hub', fits_into=st_usba, install_into=lu3)
    usbh1p1 = Slot(usbh1, 'usb1', st_usba)
    usbh1p2 = Slot(usbh1, 'usb2', st_usba)
    usbh1p3 = Slot(usbh1, 'usb3', st_usba)
    usbh1p4 = Slot(usbh1, 'usb4', st_usba)
    
    laptop2 = Item('Lenovo', 'WQ123', '3333AAA', "Cathy's laptop", container=h2)
    mon1 = Item('AOC', 'IW2269', '555XY', "Work monitor", container=o2)
    mon2 = Item('AOC', 'IW2269', '8XYZ987', "Home monitor", container=h2)

    ub1 = Item(common_name='Ubuntu 18.10 LTS', container=hdd1)
    lic1 = Item(common_name='Expensive licence file', container=hdd1)
    word = Item(common_name='MS Word', container=hdd1)
    ooorg = Item(common_name='LibreOffice', container=hdd1)

    toolbox1 = Item(common_name='Big toolbox', container=m1)
    toolbox2 = Item(common_name='Small toolbox', container=m1)
    hammer = Item(common_name='Hammer', container=toolbox1)
    flatspanners = Item(common_name='Flat spanner set', container=toolbox1)
    fs1 = Item(common_name='6-7 flat', container=flatspanners)
    fs2 = Item(common_name='8-9 flat', container=flatspanners)
    fs3 = Item(common_name='10-11 flat', container=flatspanners)
    fs4 = Item(common_name='12-13 flat', container=flatspanners)

    root.dump()

    seckey.remove_from_slot(into_container=cab1)
    hdd1.remove_from_slot(into_container=cab1)
    seckey.install_into_slot(ls1)
    
    root.dump()

