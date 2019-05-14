        
class Item:
    def __init__(self, name, format_string=None, fits_into=None, container=None, install_into=None, is_specified_by=None, parameters={}, **kwargs):
        self.name = name
        self.format_string = format_string if format_string is not None else '{name}'

        self.is_contained_in = None
        self._contains = {}

        self.can_fit_into_slot_type = fits_into
        self._is_installed_in = None
        self._has_slots = {}
        
        self.is_specified_by = is_specified_by
        
        self._install_history = []
        self._location_history = []

        self._parameters = {}
        for k in parameters:
            self._parameters[k] = parameters[k]
        for k in kwargs:
            self._parameters[k] = kwargs[k]

        if container is not None:
            self.change_container(container)

        if install_into is not None:
            self.install_into_slot(install_into)


    def duplicate(self, **kwargs):
        kwargs['name'] = self.name + '.1'
        kwargs['format_string'] = self.format_string
        kwargs['fits_into'] = self.can_fit_into_slot_type
        kwargs['is_specified_by'] = self.is_specified_by
        kwargs['parameters'] = self._parameters

        new_item = Item(**kwargs)

        for sn in self._has_slots:
            slot = self._has_slots[sn]
            new_slot = Slot(new_item, slot.slot_name, slot.slot_type)
        
        return new_item

        
    def install_into_slot(self, slot, date=None):
        if self.can_fit_into_slot_type == slot.slot_type:
            if self._is_installed_in is None:
                if slot.has_installed is None:
                    slot.has_installed = self
                    self._is_installed_in = slot
                    h = Install_history(slot, self, date, 'Install')
                    self.change_container(None)
                else:
                    Install_history(slot, self, date, 'Slot occupied')
            else:
                Install_history(slot, self, date, 'Already installed')
        else:
            Install_history(slot, self, date, 'Does not fit')
    
    def remove_from_slot(self, into_container, date=None):
        if self._is_installed_in is not None:
            slot = self._is_installed_in
            slot.has_installed = None
            self._is_installed_in = None
            Install_history(slot, self, date, 'Remove')
            self.change_container(into_container, date)
        else:
            Install_history(slot, self, date, 'Not in a slot')


    def change_container(self, new_container, date=None):
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
        return self.format_string.format(name=self.name, **self._parameters)

    def dump(self, level=0, indent='|  '):
        print('{}{}'.format(indent*level, self))
        
        for k in sorted(self._parameters):
            print('{}{}={}'.format(indent*(level+1), k, self._parameters[k]))
        if len(self._parameters) > 0 and (len(self._contains) > 0 or len(self._has_slots) > 0):
            print('{}--'.format(indent*(level+1)))

        for item in sorted(self._contains, key=lambda k: k.name):
            item.dump(level+1)
        if len(self._contains) > 0 and len(self._has_slots) > 0:
            print('{}--'.format(indent*(level+1)))

        for k in sorted(self._has_slots):
            self._has_slots[k].dump(level+1, indent)

        if len(self._parameters) > 0 or len(self._contains) > 0 or len(self._has_slots) > 0:
            print('{}+--'.format(indent*(level), self))



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
        self._install_history = []

    def dump(self, level=0, indent='  '):
        print('{}{}'.format(indent*level, self))
        if self.has_installed is not None:
            self.has_installed.dump(level+1, indent)
        else:
            print('{}<empty>'.format(indent*(level+1)))
        print('{}+--'.format(indent*level))


    def __str__(self):
        return '{} ({})'.format(self.slot_name, self.slot_type.name)


class Parameter:
    def __init__(self, item, name, value):
        self.item = item
        self.name = name
        self.value = value
        self.item._parameters[name] = self

    def __str__(self):
        return '{}={}'.format(self.name, self.value)

    def dump(self, level, indent='  '):
        print('{}{}'.format(indent*level, self))


class Install_history:
    def __init__(self, slot, item, date, action):
        self.slot = slot
        self.item = item
        self.date = date
        self.action = action
        
        item._install_history.append(self)
        slot._install_history.append(self)
     
    def __str__(self):
        return '{} {} {} {}'.format(self.date, self.slot, self.item, self.action)


if __name__ == '__main__':
    detailed_format_string='{name} ({manufacturer} {model} {serial})'
    
    st_usba = Slot_type('USB-A')
    st_sata = Slot_type('SATA')
    st_mPCIe = Slot_type('mPCIe')
    st_uSD = Slot_type('uSD')
    st_SIM = Slot_type('SIM')
    st_mSIM = Slot_type('miniSIM')
    st_uSIM = Slot_type('uSIM')
    st_nSIM = Slot_type('nanoSIM')
    
    root = Item('My stuff')

    m1 = Item('Moveable', container=root)

    h1 = Item('Home', container=root, address='9 Liverton Crescent')
    h2 = Item('Study', container=h1)
    h3 = Item('Family room', container=h1)
    cab1 = Item('4 drawer cabinet', container=h3)

    o1 = Item('Brush office', container=root, address='EPIC Centre, 106 Manchester Street')
    o2 = Item('Office', container=o1)
    o3 = Item('Store room', container=o1)

    laptop1 = Item("Stephen's laptop", container=m1, manufacturer='HP', model='Envy 15', serial='QWOP541234', format_string=detailed_format_string)
    lu1 = Slot(laptop1, 'usb1', st_usba)
    lu2 = Slot(laptop1, 'usb2', st_usba)
    lu3 = Slot(laptop1, 'usb3', st_usba)
    lu4 = Slot(laptop1, 'usb4', st_usba)
    ls1 = Slot(laptop1, 'sata1', st_sata)
    
    hdd1 = Item('256G SSD', fits_into=st_sata, install_into=ls1, manufacturer='WD', model='WSFDS', serial='222YY', format_string=detailed_format_string)
    flash8g = Item('Red 8G flash', fits_into=st_usba, install_into=lu1)
    seckey = Item('Yubikey_1', fits_into=st_usba, install_into=lu2, manufacturer='Yubico', model='Yubikey 5', serial='<unknown>', format_string=detailed_format_string)

    usbh1 = Item('Black USB hub', fits_into=st_usba, install_into=lu3)
    usbh1p1 = Slot(usbh1, 'usb1', st_usba)
    usbh1p2 = Slot(usbh1, 'usb2', st_usba)
    usbh1p3 = Slot(usbh1, 'usb3', st_usba)
    usbh1p4 = Slot(usbh1, 'usb4', st_usba)
    
    laptop2 = Item("Cathy's laptop", container=h2)
    mon1 = Item("Work monitor", container=o2, manufacturer='AOC', model='IW2269', serial='555XY')
    mon2 = Item("Home monitor", container=h2, manufacturer='AOC', model='IW2269', serial='8XYZ987')

    ub1 = Item('Ubuntu 18.10 LTS', container=hdd1, cost='$0.00', value='$1000.00')
    lic1 = Item('Expensive licence file', container=hdd1, cost='$10000.00', value='$10000.00')
    word = Item('MS Word', container=hdd1, cost='$100.00', value='$1.00')
    ooorg = Item('LibreOffice', container=hdd1, cost='$0.00', value='($10.00)')

    toolbox1 = Item('Big toolbox', container=m1)
    toolbox2 = Item('Small toolbox', container=m1)
    hammer = Item('Hammer', container=toolbox1)
    flatspanners = Item('Flat spanner set', container=toolbox1)
    fs1 = Item('6-7 flat', container=flatspanners)
    fs2 = Item('8-9 flat', container=flatspanners)
    fs3 = Item('10-11 flat', container=flatspanners)
    fs4 = Item('12-13 flat', container=flatspanners)

    m1 = Item('Huawei modem', fits_into=st_usba, install_into=lu4, IMEI='543213564')
    m1s1 = Slot(m1, 'SIM', st_uSIM)
    m1s2 = Slot(m1, 'SD', st_uSD)
    sim1 = Item('2degrees SIM', fits_into=st_uSIM, install_into=m1s1, Number='0211425358')

    root.dump()

    seckey.install_into_slot(lu1, date='00:01')
    seckey.remove_from_slot(into_container=cab1, date='00:02')
    seckey.install_into_slot(ls1, date='00:03')
    seckey.install_into_slot(lu1, date='00:04')
    seckey.install_into_slot(usbh1p3, date='00:05')
    hdd1.remove_from_slot(into_container=cab1, date='00:06')
    
    root.dump()

    for item in seckey._install_history:
        print(item)

    m2 = m1.duplicate(IMEI='NEW')
    laptop3 = laptop1.duplicate(serial='Another')

    m1.dump()
    m2.dump()
    laptop3.dump()

