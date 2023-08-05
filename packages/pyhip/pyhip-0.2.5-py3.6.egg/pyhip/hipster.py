"""hipster fallback for pyhip"""
import os
import subprocess
import platform
import pkg_resources
#pylint: disable=import-error,no-name-in-module
# from hip_wrapper import hip_cmd


HIP_CMD = pkg_resources.resource_filename("pyhip", "hip_%s.exe" % platform.system())

__all__ = ["pyhip_cmd"]

def pyhip_cmd(command, fallback=True):
    """Fallback function for pyhip when hip process fails"""
    # if not fallback:
    #     status, msg = hip_cmd(command)
    #     if status != 0:
    #         raise RuntimeError(msg)

    #     if msg is not None:
    #         print(msg)
    #         if command == "list periodic":
    #             return msg, [command]
    #         return [command]
    #     return [command]

    #fallback
    hip_file = os.path.abspath(f"{os.getpid()}_hip.in")

    with open(hip_file, 'a') as fout:
        fout.write(command + '\n')

    if command == "exit":
        status, log = run_command(hip_file)

        if status > 0:
            log_err = f"HIP process failed with exit code {status}.\n\n"
            log_err += "HIP commands :\n  "
            with open(hip_file, 'r') as fin:
                log_err += "  ".join(fin.readlines())
            os.remove(hip_file)
            log_err += "\nHIP error :\n  "
            with open('hip-fatal.log', 'r') as fin:
                log_err += "  ".join(fin.readlines())

            raise RuntimeError(log_err)

        os.remove(hip_file)
        return log, ['exit']
    return [command]

def run_command(hip_file):
    """ Run command """
    import shlex
    process = subprocess.Popen(
        shlex.split(f'{HIP_CMD} {hip_file}'),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=os.path.dirname(hip_file),
    )
    log = []
    while process.poll() is None:
        stdout = process.stdout.readline()
        if stdout:
            log.append(stdout.decode('utf-8').rstrip())
            print(log[-1])
            
    return process.poll(), log
