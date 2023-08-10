import winreg as wr

# class regEditor:
#     def __init__(self):
#         self.location = wr.HKEY_CURRENT_USER
#         self.location = wr.OpenKey(self.location, "Software", 0, wr.KEY_ALL_ACCESS)
    
#     def set_location(self, location):
#         self.location = location
    
#     def get_location(self):
#         print(wr.QueryInfoKey(self.location))
    
#     def make_dir(self, key):
#         wr.CreateKey(self.location, key)
    
#     def move_to(self, key):
#         self.location = wr.OpenKey(self.location, key, 0, wr.KEY_ALL_ACCESS)
        
#     def list_key(self):
#         key_list = []
#         for i in range(wr.QueryInfoKey(self.location)[0]):
#             key_list.append(wr.EnumKey(self.location, i))
#         return key_list

#     def list_value(self):
#         value_list = []
#         for i in range(wr.QueryInfoKey(self.location)[1]):
#             value_list.append(wr.EnumValue(self.location, i))
#         return value_list

#     def get_value(self, value):
#         return wr.QueryValueEx(self.location, value)[0]
    
#     def set_value(self, value, data):
#         wr.SetValueEx(self.location, value, 0, wr.REG_SZ, data)
    
#     def delete_value(self, value):
#         wr.DeleteValue(self.location, value)
    
#     def delete_key(self, key):
#         wr.DeleteKey(self.location, key)
    
#     def close(self):
#         wr.CloseKey(self.location)

def getValue(path, value_name):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        value = wr.QueryValueEx(key, value_name)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return value
    except:
        return False
    
def setValue(path, value_name, dataType, data):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.SetValueEx(key, value_name, 0, dataType, data)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
    
def createValue(path, value_name, dataType, data):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.SetValueEx(key, value_name, 0, dataType, data)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
    
def deleteValue(path, value_name):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.DeleteValue(key, value_name)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False

def createKey(path, newkey):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.CreateKey(key, newkey)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
  
def deleteKey(path, delKey):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.DeleteKey(key, delKey)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
