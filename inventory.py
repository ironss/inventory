


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

    indent='  '
    def dump(self, level=0):
        print('{} {}'.format(self.indent*level, self))
        for item in sorted(self.inventory.keys()):
            item.dump(level+1)
        for k in sorted(self.slots.keys()):
            self.slots[k].dump(level+1)

class Room(Item):
    def __init__(self, address, location=None, common_name=None, notes=None, container=None):
        self.address = address
        self.location = location
        Item.__init__(self, common_name, notes, container)

    def __str__(self):
        return self.address
        
class Cabinet(Item):
    def __init__(self, physical_description, relative_location, common_name=None, notes=None, container=None):
        self.physical_description = physical_description
        self.relative_location = relative_location
        Item.__init__(self, common_name, notes, container)
        
    def __str__(self):
        return self.physical_description


        
class Device(Item):
    def __init__(self, manufacturer, model_number, serial_number, common_name=None, notes=None, container=None, fits_into=None, install_into=None):
        self.manufacturer = manufacturer
        self.model_number = model_number
        self.serial_number = serial_number
        self.fits_into_slot_type = fits_into
        
        Item.__init__(self, common_name, notes, container)
        
        if install_into is not None:
            self.install_into_slot(install_into)

    def __str__(self):
        return '{name} ({manufacturer} {model} {serial})'.format(manufacturer=self.manufacturer, model=self.model_number, serial=self.serial_number, name=self.common_name)

    def install_into_slot(self, slot):
        if self.fits_into_slot_type == slot.slot_type:
            if slot.device_installed == None:
                self.installed_in_slot = slot
                slot.device_installed = self
                self.container = None
            else:
                print('Remove', slot.device_installed.common_name)
        else:
            print('{} does not fit into {}'.format(self.fits_into_slot_type, slot.slot_type))
    
    def remove_from_slot(self, into_container=None):
        self.installed_in_slot.device_installed = None
        self.installed_in_slot = None
        if into_container is not None:
            new_container = into_container
        else:
            new_container = self.installed_in_slot.device.container
        self.change_container(new_container)


class Slot_type:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Slot:
    def __init__(self, device, name, slot_type):
        self.device = device
        self.name = name
        self.slot_type = slot_type
        self.device.slots[name] = self
        self.device_installed = None

    indent='  '
    def dump(self, level=0):
        print('{} {}'.format(self.indent*level, self))
        if self.device_installed is not None:
            self.device_installed.dump(level+1)
        else:
            print('{} <empty>'.format(self.indent*(level+1)))

    def __str__(self):
        return '{} ({})'.format(self.name, self.slot_type.name)






if __name__ == '__main__':
    st_usba = Slot_type('USB-A')
    st_sata = Slot_type('SATA')
    st_mPCIe = Slot_type('mPCIe')
    
    root = Item('My stuff')

    m1 = Item('Moveable', container=root)

    h1 = Room('9 Liverton Crescent', container=root)
    h2 = Room('Study', container=h1)
    h3 = Room('Family room', container=h1)
    cab1 = Cabinet('4 drawer cabinet', 'In the corner', "The grey one", container=h3)

    o1 = Room('EPIC Centre', container=root)
    o2 = Room('Office', container=o1)
    o3 = Room('Store room', container=o1)

    laptop1 = Device('HP', 'Envy 15', 'SN1234', "Stephen's laptop", container=m1)
    lu1 = Slot(laptop1, 'usb1', st_usba)
    lu2 = Slot(laptop1, 'usb2', st_usba)
    lu3 = Slot(laptop1, 'usb3', st_usba)
    lu4 = Slot(laptop1, 'usb4', st_usba)
    ls1 = Slot(laptop1, 'sata1', st_sata)
    
    hdd1 = Device('WD', 'WSFDS', 'SN1234', "250GB SSD", fits_into=st_sata, install_into=ls1)
    flash8g = Device('Generic', '8GB flash', 'unknown', "Red 8G flash drive", fits_into=st_usba, install_into=lu1)
    seckey = Device('Yubico', 'Yubikey 5', 'unknown', "Security key #1", fits_into=st_usba, install_into=lu2)

    usbh1 = Device('Generic', '4-port USB hub', 'none', 'Black USB hub', fits_into=st_usba, install_into=lu3)
    usbh1p1 = Slot(usbh1, 'usb1', st_usba)
    usbh1p2 = Slot(usbh1, 'usb2', st_usba)
    usbh1p3 = Slot(usbh1, 'usb3', st_usba)
    usbh1p4 = Slot(usbh1, 'usb4', st_usba)
    
    laptop2 = Device('Lenovo', 'WQ123', 'SN2211', "Cathy's laptop", container=h2)
    mon1 = Device('AOC', 'IW2269', 'SN5555', "Work monitor", container=o2)
    mon2 = Device('AOC', 'IW2269', 'SN8888', "Home monitor", container=h2)

    ub1 = Item('Ubuntu 18.10 LTS', container=hdd1)
    lic1 = Item('Expensive licence file', container=hdd1)
    word = Item('MS Word', container=hdd1)
    ooorg = Item('LibreOffice', container=hdd1)

    toolbox1 = Item('Big toolbox', container=m1)
    toolbox2 = Item('Small toolbox', container=m1)
    flatspanners = Item('Flat spanner set', container=toolbox1)
    fs1 = Item('6-7 flat', container=flatspanners)
    fs2 = Item('8-9 flat', container=flatspanners)
    fs3 = Item('10-11 flat', container=flatspanners)
    fs4 = Item('12-13 flat', container=flatspanners)

    root.dump()


    seckey.remove_from_slot(into_container=cab1)
    hdd1.remove_from_slot(into_container=cab1)
    seckey.install_into_slot(ls1)
    
    root.dump()

