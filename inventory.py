"""
This file implements the classes for a simple inventory management system.

The idea is that the system keeps a record of 'things'. A thing can be stored in 
another thing (eg. a cupboard) and that thing can be stored in another thing, and so
on (eg. a device in a tray in a rack-of-trays on a shelf in a cupboard in a room of
and office in a building).

From another viewpoint, a thing has slots that other things can plug into to make
a composite thing. In this case, the composite thing can be stored in a cupboard,
but the component parts do not their own location; they are part of the composite.

A third viewpoint is a system, where parts of a system are distributed geographically.
This is not supported.

This system keeps a record of when things change: when an Item is plugged into or removed
from a slot, when an Item is stored in a container, etc.
"""
        
class Item:
    """
    An Item is a thing to be kept in the inventory system. It keeps a record of three types 
    of things:

    * a set of Items that it 'contains'

    * a set of slots that can each be empty or have one Item installed into it, 
      provided that the Item-installed is of the same Slot_type as the slot

    * set set of key-value parameters, gathered from the extra keyword arguments 
      provided to the __init__ function. These are useful for location address, manufacturer,
      model, serial numbers, etc.
    
    Each item can be either stored in a container or plugged into a slot, not both. The
    thinking is that an Item in a slot has no location of its own: it is located in the 
    same place as the Item whose Slot it is installed in.
    
    Installing and removing from slots is managed well; changing containers needs work.
    """
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
        if self.can_fit_into_slot_type != slot.slot_type:
            Install_history(slot, self, date, 'Does not fit')
            return
                        
        if self._is_installed_in is not None:
            Install_history(slot, self, date, 'Already installed')
            return
        
        if slot.has_installed is not None:
            Install_history(slot, self, date, 'Slot occupied')
            return
           
        slot.has_installed = self
        self._is_installed_in = slot
        h = Install_history(slot, self, date, 'Install')
        self.change_container(None)
    
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
    """
    This could just as well be a string type. But having a class of its own means we
    things about it properly.
    """
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


