import winreg as wr

def toReg(str):
    if(str == "String"):
        return wr.REG_SZ
    if(str == "Binary"):
        return wr.REG_BINARY
    if(str == "DWORD"):
        return wr.REG_DWORD
    if(str == "QWORD"):
        return wr.REG_QWORD
    if(str == "Multi-String"):
        return wr.REG_MULTI_SZ
    if(str == "Expandable String"):
        return wr.REG_EXPAND_SZ
    return wr.REG_SZ

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
        dataType = toReg(dataType)
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
        dataType = toReg(dataType)
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