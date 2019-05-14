from inventory import *

def test_all():
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

def test_spec():
    st_usba = Slot_type('USB-A')
    st_uSD = Slot_type('uSD')
    st_uSIM = Slot_type('uSIM')

    ms1 = Item_spec('Huawei modem', fits_into=st_usba, manufacturer='Huawei', model='e3131 3G modem')
    ms1ss1 = Slot_spec(ms1, 'SIM', st_uSIM)
    ms1ss2 = Slot_spec(ms1, 'SD', st_uSD)

    root = Item('My stuff')
    m1 = ms1.new_item(container=root, IMEI='12355')
    m2 = ms1.new_item(container=root, IMEI='QWERT')
    
    root.dump()

if __name__ == '__main__':
    test_all()
    test_spec()
